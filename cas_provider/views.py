import logging
logger = logging.getLogger('cas_provider.views')

try:
    from urllib.error import HTTPError, URLError
    from urllib.parse import parse_qsl, urlencode, urlparse, urlsplit, urlunsplit
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode
    from urllib2 import HTTPError, URLError, urlopen
    from urlparse import parse_qsl, urlparse, urlsplit, urlunsplit
from functools import wraps

from django.utils.decorators import available_attrs
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import cache_control
from django.utils.cache import patch_cache_control
from django.views.decorators.csrf import csrf_protect

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import get_callable
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from lxml import etree
from cas_provider.attribute_formatters import NSMAP, CAS
from cas_provider.models import ProxyGrantingTicket, ProxyTicket
from cas_provider.models import ServiceTicket

from cas_provider.forms import LoginForm, MergeLoginForm

from . import signals

__all__ = ['login', 'validate', 'logout', 'service_validate']

INVALID_TICKET = 'INVALID_TICKET'
INVALID_SERVICE = 'INVALID_SERVICE'
INVALID_REQUEST = 'INVALID_REQUEST'
INTERNAL_ERROR = 'INTERNAL_ERROR'

ERROR_MESSAGES = (
    (INVALID_TICKET, u'The provided ticket is invalid.'),
    (INVALID_SERVICE, u'Service is invalid'),
    (INVALID_REQUEST, u'Not all required parameters were sent.'),
    (INTERNAL_ERROR, u'An internal error occurred during ticket validation'),
    )


logger = logging.getLogger(__name__)


_never_cache = cache_control(no_cache=True, must_revalidate=True)


def never_cache(view_func):
    """
    Decorator that adds headers to a response so that it will
    never be cached.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        patch_cache_control(response, no_cache=True,
                            must_revalidate=True, proxy_revalidate=True)
        response['Pragma'] = 'no-cache'
        return response
    return _wrapped_view_func


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='cas/login.html',
          success_redirect=settings.LOGIN_REDIRECT_URL,
          warn_template_name='cas/warn.html', **kwargs):
    merge = kwargs.get('merge', False)
    logging.debug('CAS Provider Login view. Method is %s, merge is %s, template is %s.',
                  request.method, merge, template_name)

    service = request.GET.get('service', None)
    if service is not None:
        # Save the service on the session, for later use if we end up
        # in one of the more complicated workflows.
        request.session['service'] = service

    user = request.user

    errors = []

    if request.method == 'POST':
        if merge:
            form = MergeLoginForm(request.POST, request=request)
        else:
            form = LoginForm(request.POST, request=request)

        if form.is_valid():
            service = form.cleaned_data.get('service', None)
            try:
                auth_args = dict(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
                if merge:
                    # We only want to send the merge argument if it's
                    # True. If it it's False, we want it to propagate
                    # through the auth backends properly.
                    auth_args['merge'] = merge
                user = authenticate(**auth_args)
            except:
                # Need to merge the accounts?
                if merge:
                    # We shouldn't get here...
                    raise
                else:
                    base_url = reverse('cas_provider_merge')
                    args = dict(
                        success_redirect=success_redirect,
                        username=form.cleaned_data['username'],
                        )
                    if service is not None:
                        args['service'] = service
                    args = urlencode(args)

                    url = '%s?%s' % (base_url, args)
                    logging.debug('Redirecting to %s', url)
                    return HttpResponseRedirect(url)

            if user is None:
                errors.append(_('Incorrect username and/or password.'))
            else:
                if user.is_active:
                    auth_login(request, user)

    else:  # Not a POST...
        if merge:
            form = MergeLoginForm(initial={'service': service, 'username': request.GET.get('username')})
        else:
            form = LoginForm(initial={'service': service})

    if user is not None and user.is_authenticated():
        # We have an authenticated user.
        if not user.is_active:
            errors.append(_('This account is disabled. Please contact us if you feel it should be enabled again.'))
        else:
            # Send the on_cas_login signal. If we get an HttpResponse, return that.
            for receiver, response in signals.on_cas_login.send(sender=login, request=request, **kwargs):
                if isinstance(response, HttpResponse):
                    return response

            if service is None:
                # Try and pull the service off the session
                service = request.session.pop('service', service)

            signals.on_cas_login_success.send(sender=login, request=request,
                                              service=service, **kwargs)

            if service is None:
                # Normal internal success redirection.
                logging.debug('Redirecting to %s', success_redirect)
                return HttpResponseRedirect(success_redirect)
            else:
                if request.GET.get('warn', False):
                    return render_to_response(warn_template_name, {
                        'service': service,
                        'warn': False
                    }, context_instance=RequestContext(request))

                # Create a service ticket and redirect to the service.
                ticket = ServiceTicket.objects.create(service=service, user=user)
                if 'service' in request.session:
                    # Don't need this any more.
                    del request.session['service']

                url = ticket.get_redirect_url()
                logging.debug('Redirecting to %s', url)
                return HttpResponseRedirect(url)

    logging.debug('Rendering response on %s, merge is %s', template_name, merge)
    return render_to_response(template_name, {'form': form, 'errors': errors}, context_instance=RequestContext(request))


@never_cache
def validate(request):
    """Validate ticket via CAS v.1 protocol
    """
    service = request.GET.get('service', None)
    ticket_string = request.GET.get('ticket', None)
    logger.info('Validating ticket %s for %s', ticket_string, service)
    if service is not None and ticket_string is not None:
        #renew = request.GET.get('renew', True)
        #if not renew:
        # TODO: check user SSO session
        try:
            ticket = ServiceTicket.objects.get(ticket=ticket_string)
            assert ticket.service == service
        except ServiceTicket.DoesNotExist:
            logger.exception("Tried to validate with an invalid ticket %s for %s", ticket_string, service)
        except Exception as e:
            logger.exception('Got an exception: %s', e)
        else:
            username = ticket.user.username
            ticket.delete()

            results = signals.on_cas_collect_histories.send(sender=validate, for_user=ticket.user)
            histories = '\n'.join('\n'.join(rs) for rc, rs in results)
            logger.info('Validated %s %s', username, "(also %s)" % histories if histories else '')
            return HttpResponse("yes\n%s\n%s" % (username, histories))

    logger.info('Validation failed.')
    return HttpResponse("no\n\n")


@never_cache
def logout(request, template_name='cas/logout.html',
           auto_redirect=settings.CAS_AUTO_REDIRECT_AFTER_LOGOUT):
    url = request.GET.get('url', None)
    if request.user.is_authenticated():
        for ticket in ServiceTicket.objects.filter(user=request.user):
            ticket.delete()
        auth_logout(request)
        if url and auto_redirect:
            return HttpResponseRedirect(url)
    return render_to_response(template_name, {'url': url},
        context_instance=RequestContext(request))


@never_cache
def proxy(request):
    targetService = request.GET['targetService']
    pgt_id = request.GET['pgt']

    try:
        proxyGrantingTicket = ProxyGrantingTicket.objects.get(ticket=pgt_id)
    except ProxyGrantingTicket.DoesNotExist:
        return _cas2_error_response(INVALID_TICKET)

    pt = ProxyTicket.objects.create(proxyGrantingTicket=proxyGrantingTicket,
        user=proxyGrantingTicket.user,
        service=targetService)
    return _cas2_proxy_success(pt.ticket)


def ticket_validate(service, ticket_string, pgtUrl):
    if service is None or ticket_string is None:
        return _cas2_error_response(INVALID_REQUEST)

    try:
        if ticket_string.startswith('ST'):
            ticket = ServiceTicket.objects.get(ticket=ticket_string)
        elif ticket_string.startswith('PT'):
            ticket = ProxyTicket.objects.get(ticket=ticket_string)
        else:
            return _cas2_error_response(INVALID_TICKET,
                '%(ticket)s is neither Service (ST-...) nor Proxy Ticket (PT-...)' % {
                    'ticket': ticket_string})
    except ServiceTicket.DoesNotExist:
        return _cas2_error_response(INVALID_TICKET)

    ticketUrl = urlparse(ticket.service)
    serviceUrl = urlparse(service)

    if not(ticketUrl.hostname == serviceUrl.hostname and ticketUrl.path == serviceUrl.path and ticketUrl.port == serviceUrl.port):
        return _cas2_error_response(INVALID_SERVICE)

    pgtIouId = None
    proxies = ()
    if pgtUrl is not None:
        pgt = generate_proxy_granting_ticket(pgtUrl, ticket)
        if pgt:
            pgtIouId = pgt.pgtiou

    if hasattr(ticket, 'proxyticket'):
        pgt = ticket.proxyticket.proxyGrantingTicket
        # I am issued by this proxy granting ticket
        while pgt.pgt is not None:
            proxies += (pgt.service,)
            pgt = pgt.pgt

    user = ticket.user
    ticket.delete()
    return _cas2_sucess_response(user, pgtIouId, proxies)


@never_cache
def service_validate(request):
    """Validate ticket via CAS v.2 protocol"""
    service = request.GET.get('service', None)
    ticket_string = request.GET.get('ticket', None)
    pgtUrl = request.GET.get('pgtUrl', None)
    if ticket_string.startswith('PT-'):
        return _cas2_error_response(INVALID_TICKET, "serviceValidate cannot verify proxy tickets")
    else:
        return ticket_validate(service, ticket_string, pgtUrl)


@never_cache
def proxy_validate(request):
    """Validate ticket via CAS v.2 protocol"""
    service = request.GET.get('service', None)
    ticket_string = request.GET.get('ticket', None)
    pgtUrl = request.GET.get('pgtUrl', None)
    return ticket_validate(service, ticket_string, pgtUrl)


def generate_proxy_granting_ticket(pgt_url, ticket):
    proxy_callback_good_status = (200, 202, 301, 302, 304)
    uri = list(urlsplit(pgt_url))

    pgt = ProxyGrantingTicket()
    pgt.user = ticket.user
    pgt.service = ticket.service
    # Remember if it's a chained PGT.
    pgt.pgt = getattr(ticket, 'proxyGrantingTicket', None)

    params = {'pgtId': pgt.ticket, 'pgtIou': pgt.pgtiou}

    query = dict(parse_qsl(uri[4]))
    query.update(params)

    uri[3] = urlencode(query)

    try:
        urlopen(urlunsplit(uri))
    except HTTPError as e:
        if not e.code in proxy_callback_good_status:
            logger.debug('Checking Proxy Callback URL {} returned {}. Not issuing PGT.'.format(uri, e.code))
            return
    except URLError as e:
        logger.debug('Checking Proxy Callback URL {} raised URLError. Not issuing PGT.'.format(uri))
        return

    pgt.save()
    return pgt


def _cas2_proxy_success(pt):
    return HttpResponse(proxy_success(pt))


def _cas2_sucess_response(user, pgt=None, proxies=None):
    return HttpResponse(auth_success_response(user, pgt, proxies), content_type='text/xml')


def _cas2_error_response(code, message=None):
    return HttpResponse(u'''<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
            <cas:authenticationFailure code="%(code)s">
                %(message)s
            </cas:authenticationFailure>
        </cas:serviceResponse>''' % {
        'code': code,
        'message': message if message else dict(ERROR_MESSAGES).get(code)
    }, content_type='text/xml')


def proxy_success(pt):
    response = etree.Element(CAS + 'serviceResponse', nsmap=NSMAP)
    proxySuccess = etree.SubElement(response, CAS + 'proxySuccess')
    proxyTicket = etree.SubElement(proxySuccess, CAS + 'proxyTicket')
    proxyTicket.text = pt
    return etree.tostring(response, encoding='unicode')


def auth_success_response(user, pgt, proxies):
    response = etree.Element(CAS + 'serviceResponse', nsmap=NSMAP)
    auth_success = etree.SubElement(response, CAS + 'authenticationSuccess')
    username = etree.SubElement(auth_success, CAS + 'user')
    username.text = user.username

    attrs = {}
    for receiver, custom in signals.cas_collect_custom_attributes.send(sender=auth_success_response, user=user):
        if custom:
            attrs.update(custom)

    identifiers = [i for sr, rr in signals.on_cas_collect_histories.send(sender=validate, for_user=user)
                   for i in rr]

    if identifiers:
        # Singular `identifier`, as that is the name of the element tag(s).
        attrs['identifier'] = identifiers

    if attrs:
        formatter = get_callable(settings.CAS_CUSTOM_ATTRIBUTES_FORMATER)
        formatter(auth_success, attrs)

    if pgt:
        pgtElement = etree.SubElement(auth_success, CAS + 'proxyGrantingTicket')
        pgtElement.text = pgt

    if proxies:
        proxiesElement = etree.SubElement(auth_success, CAS + "proxies")
        for proxy in proxies:
            proxyElement = etree.SubElement(proxiesElement, CAS + "proxy")
            proxyElement.text = proxy

    return etree.tostring(response, encoding='unicode')

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from random import Random
import string
try:
    from urllib.parse import urlencode, urlparse, parse_qs, ParseResult
except ImportError:
    from urllib import urlencode
    from urlparse import urlparse, ParseResult
    from urlparse import parse_qs

__all__ = ['ServiceTicket', 'LoginTicket', 'ProxyGrantingTicket', 'ProxyTicket', 'ProxyGrantingTicketIOU']

class BaseTicket(models.Model):
    ticket = models.CharField(_('ticket'), max_length=32)
    created = models.DateTimeField(_('created'), auto_now=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        if 'ticket' not in kwargs:
            kwargs['ticket'] = self._generate_ticket()
        super(BaseTicket, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.ticket

    def _generate_ticket(self, length=ticket.max_length, chars=string.ascii_letters + string.digits):
        """ Generates a random string of the requested length. Used for creation of tickets. """
        return "%s-%s" % (self.prefix, ''.join(Random().sample(chars, length - (len(self.prefix) + 1))))


class ServiceTicket(BaseTicket):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    service = models.URLField(_('service'), max_length=2048)

    prefix = 'ST'

    class Meta:
        verbose_name = _('Service Ticket')
        verbose_name_plural = _('Service Tickets')

    def get_redirect_url(self):
        parsed = urlparse(self.service)
        query = parse_qs(parsed.query)
        query['ticket'] = [self.ticket]
        query = [((k, v) if len(v) > 1 else (k, v[0])) for k, v in query.items()]
        parsed = ParseResult(parsed.scheme, parsed.netloc,
                                      parsed.path, parsed.params,
                                      urlencode(query), parsed.fragment)
        return parsed.geturl()


class LoginTicket(BaseTicket):
    prefix = 'LT'

    class Meta:
        verbose_name = _('Login Ticket')
        verbose_name_plural = _('Login Tickets')


class ProxyGrantingTicket(BaseTicket):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE)
    service = models.URLField(_('service'), null=True)
    pgt = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    pgtiou = models.CharField(max_length=256, verbose_name=_('PGTiou'))
    prefix = 'PGT'

    def __init__(self, *args, **kwargs):
        if 'pgtiou' not in kwargs:
            kwargs['pgtiou'] = "PGTIOU-%s" % (''.join(Random().sample(string.ascii_letters + string.digits, 50)))
        super(ProxyGrantingTicket, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _('Proxy Granting Ticket')
        verbose_name_plural = _('Proxy Granting Tickets')


class ProxyTicket(ServiceTicket):
    proxyGrantingTicket = models.ForeignKey(ProxyGrantingTicket, verbose_name=_('Proxy Granting Ticket'), on_delete=models.CASCADE)

    prefix = 'PT'

    class Meta:
        verbose_name = _('Proxy Ticket')
        verbose_name_plural = _('Proxy Tickets')


class ProxyGrantingTicketIOU(BaseTicket):
    proxyGrantingTicket = models.ForeignKey(ProxyGrantingTicket, verbose_name=_('Proxy Granting Ticket'), on_delete=models.CASCADE)

    prefix = 'PGTIOU'

    class Meta:
        verbose_name = _('Proxy Granting Ticket IOU')
        verbose_name_plural = _('Proxy Granting Tickets IOU')


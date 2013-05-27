from django.conf.urls import patterns, url


urlpatterns = patterns('cas_provider.views',
    url(r'^login/merge/', 'login', {'merge': True, 'template_name': 'cas/merge.html'}),
    url(r'^login/?$', 'login', name='cas_login'),
    url(r'^socialauth-login/$', 'login', name='cas_socialauth_login'),
    url(r'^validate/?$', 'validate', name='cas_validate'),
    url(r'^proxy/?$', 'proxy', name='proxy'),
    url(r'^serviceValidate/?$', 'service_validate', name='cas_service_validate'),
    url(r'^proxyValidate/?$', 'proxy_validate', name='cas_proxy_validate'),
    url(r'^logout/?$', 'logout', name='cas_logout'),
)

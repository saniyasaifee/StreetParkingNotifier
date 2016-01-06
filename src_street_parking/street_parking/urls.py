from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#from signups import regbackend
from registration.views import *
from registration.backends.default.views import RegistrationView
#from signups.forms import UserRegForm
#from registration.views import register


from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'signups.views.home', name='home'),
    #url(r'^auth/$', 'signups.views.auth_view'),
    url(r'^maps/$', 'showmaps.views.maps', name='maps'),
    url(r'^whereiam/$', 'locations.views.whereiam', name='whereiam'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^blog/', include('blog.urls')),url(r'^maps/$', 'showmaps.views.maps', name='maps'),
    #url(r'^tools/$', 'tools.views.homepage', name='homepage'),
    #url(r'^register/$', RegistrationView.as_view(form_class=UserRegForm)),
    url(r'^accounts/profile/', include('userprofile.urls')),
    url(r'^emailAlert$','signups.views.email_alert',name="sendEmail"),
    url(r'^settings/$', 'tools.views.settings', name='settings'),
    url(r'^editinfo/$', 'tools.views.editinfo', name='editinfo'),
    url(r'^bugs/$', 'settings.views.bugs', name='bugs'),
    url(r'^contactus/$', 'settings.views.contactus', name='contactus'),
    url(r'^features/$', 'settings.views.features', name='features'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',
        {}, name='password_change'),
    url(r'^password_change_done/$', 'django.contrib.auth.views.password_change_done',
        {}, name='password_change_done'),

    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {}, 'password_reset'),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done',
        {}, 'password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>.+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {}, 'password_reset_confirm'),
    url(r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete',
        {}, 'password_reset_complete'),
    #url(r'^whereiam/reverseGeocode/$', 'locations.views.doReverseGeocode', name = 'doReverseGeocode' ),
    url(r'^select_parking_sign/$', 'locations.views.select_parking_sign', name = 'select_parking_sign' ),
    #url(r'^accounts/register/$', register, {'backend': 'registration.backends.default.DefaultBackend','form_class': UserRegForm}, name='registration_register'),
) 

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


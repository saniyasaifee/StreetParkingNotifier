'''
Local file for the links to the user profile.
This is called int he main urls file of the project.
'''
from django.conf.urls import patterns, url

from userprofile import views

urlpatterns = patterns(
    '',
    url(r'^edit/$',
        views.update_profile,
        name='userprofile_edit_profile'),
    url(r'^$',
        views.detail_profile,
        name='userprofile_detail_profile'),
)

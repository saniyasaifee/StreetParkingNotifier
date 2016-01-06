from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from userprofile import utils
from userprofile.models import UserProfile
from userprofile.forms import FormUserProfileUpdate, FormUserUpdate

# Create your views here.

'''this view is to edit the user profile'''
@login_required
def update_profile(request,
                   success_url=None,
                   template_name='profiles/edit_profile.html',
                   extra_context=None):
    try:
        profile_obj = request.user
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('userprofile_detail_profile'))

    if success_url is None:
        success_url = reverse('userprofile_detail_profile')
    if request.method == 'POST':
        formuser = FormUserUpdate(data=request.POST, instance=request.user)
        instance = UserProfile.objects.get(user=profile_obj)
        formuserprofile = FormUserProfileUpdate(data=request.POST, instance=instance)
        if formuser.is_valid() and formuserprofile.is_valid():
            formuser.save()
            formuserprofile.save()
            return HttpResponseRedirect(reverse('userprofile_detail_profile'))
    else:
        formuser = FormUserUpdate(instance=profile_obj)
        instance = UserProfile.objects.get(user=profile_obj)
        formuserprofile = FormUserProfileUpdate(instance=instance)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': formuser,
                               'formuser': formuserprofile,
                               'profile': profile_obj},
                              context_instance=context)

'''this method is used to view the profile'''
@login_required
def detail_profile(request,
                   public_profile_field=None,
                   template_name='profiles/detail_profile.html',
                   extra_context=None):
    user = request.user
    try:
        profile_obj = UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile_obj = utils.create_profile(user=user)

    if public_profile_field is not None and \
    not getattr(profile_obj, public_profile_field):
        profile_obj = None

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'profile': profile_obj},
                              context_instance=context)

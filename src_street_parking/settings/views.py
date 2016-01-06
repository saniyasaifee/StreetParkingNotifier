from models import Bug,BugForm
from django.shortcuts import render,render_to_response,RequestContext
from django.template import loader, Context
from django.contrib.auth.models import User

def bugs(request):
    form = BugForm(request.POST, instance=Bug(reporter=request.user))
    if form.is_valid():
        form.save()
    return render_to_response("bug.html",locals(),context_instance=RequestContext(request))

def contactus(request):
    return render(request, "contactus.html",)

def features(request):
    return render(request, "slide.html",) 

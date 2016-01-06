from models import AddPreferences,AddPreferencesForm
from django.shortcuts import render,render_to_response,RequestContext
from django.http import Http404
#from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

def editinfo(request):
    logged_in=True
    UserFormset=modelformset_factory(User,max_num=1,fields=("username","first_name","last_name","email","password",))
    if request.method == "POST":
       formset = UserFormset(request.POST,request.FILES)
       if formset.is_valid():
        formset.save()
        return render(request, "editprofile.html",{"formset":formset})
       else:
        print (formset.errors())
    else:
        if User.objects.all().filter(id=request.user.id).count() > 0:
            formset = UserFormset(queryset=User.objects.all().filter(id=request.user.id).order_by('-id')[:1])
            context = {"formset":formset,'logged_in': logged_in}
            return render(request, "editprofile.html",context)
        else:
            logged_in=False
            context = {'logged_in': logged_in }
            return render(request, "editprofile.html",context)
        
def settings(request):
    form = AddPreferencesForm(request.POST, instance=AddPreferences(user_prefer=request.user))
    if form.is_valid():
        form.save()
    return render_to_response("settings.html",locals(),context_instance=RequestContext(request))
      
 

 

    
    
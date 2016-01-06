from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import EmailAlertForm
from django.core.mail import BadHeaderError

# Create your views here.

'''this is the view for the home page'''
def home(request):
    error = False
    if 'username' in request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('whereiam'))
        else:
            error = True
            return render(request, 'registration/login.html', {'error': error})
    else:
        return render(request, 'registration/login.html', {'error': error})

'''this is the view to send an email notificiation'''
@login_required
def email_alert(request):
    if request.method == 'POST':
        form = EmailAlertForm(request.POST)
        #print form.errors
        if form.is_valid():
            subject = "This is a REMINDER!!"
            from_email = "streetnotifier@gmail.com"
            message = request.POST.get('message', '')
            email = request.POST.get('email', '')
            try:
                send_mail(subject, message, from_email, [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(reverse('whereiam'))
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    else:
        form = EmailAlertForm()
    ctx = {'form': form}
    return render_to_response('EmailAlert.html',
                              ctx,
                              context_instance=RequestContext(request),)
    
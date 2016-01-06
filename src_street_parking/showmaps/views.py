from django.shortcuts import render, render_to_response, RequestContext
from .forms import ShowMapForm

# Create your views here.

def maps(request):
    form =ShowMapForm(request.POST or None)
    '''
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
    '''
    return render_to_response("showmap.html",
                              locals(), context_instance=RequestContext(request))
    


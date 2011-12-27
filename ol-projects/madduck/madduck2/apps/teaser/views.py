#from django
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

#from teaser
from teaser.models import Subscribe, SubscribeForm

def index(request):
    """ returns teaser page """
    
#    if request.user.is_authenticated():
#          return render_to_response('homepage.html', {
#              }, context_instance=RequestContext(request))
#        
    if request.method == 'POST':
       subscribe_form = SubscribeForm(request.POST)
       if subscribe_form.is_valid():
          new_subscribe = subscribe_form.save(commit=False)
          new_subscribe.save()
          return HttpResponseRedirect(reverse('teaser.views.thankyou'))
          
    #GET Request
    else:
        subscribe_form = SubscribeForm()
        
    return render_to_response('teaser/index.html', {
                'subscribe_form' : subscribe_form,
            }, context_instance=RequestContext(request))

def thankyou(request):
    """ returns successful completion page. """
    
    return render_to_response('teaser/thankyou.html', {
         }, context_instance=RequestContext(request))


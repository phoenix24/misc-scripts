from django.template import RequestContext
from django.shortcuts import render_to_response
from decorators import anonymous_required

@anonymous_required(viewname='home.views.index')
def welcome(request):
  """ returns the home-page. """
  return render_to_response("static_pages/welcome.html", {
    }, context_instance=RequestContext(request))

def aboutus(request):
    """ returns a static aboutus page. """
    return render_to_response("static_pages/aboutus.html", {
         }, context_instance=RequestContext(request))
    
def contactus(request):
    """ returns a static contactus page. """
    return render_to_response("static_pages/contactus.html", {
         }, context_instance=RequestContext(request))
    
def termsofservice(request):
    """ returns a static terms-of-service page. """
    return render_to_response("static_pages/termsofservice.html", {
         }, context_instance=RequestContext(request))
    
def privacypolicy(request):
    """ returns a static privacy policy page. """
    return render_to_response("static_pages/privacypolicy.html", {
         }, context_instance=RequestContext(request))
    
def pricing(request):
    """ returns a static page on pricing information. """
    return render_to_response("static_pages/pricing.html", {
         }, context_instance=RequestContext(request))
    
def features(request):
    """ returns a static page on application features. """
    return render_to_response("static_pages/features.html", {
         }, context_instance=RequestContext(request))
    
def tour(request):
    """ returns a static page for the application tour """
    return render_to_response("static_pages/tour.html", {
         }, context_instance=RequestContext(request))

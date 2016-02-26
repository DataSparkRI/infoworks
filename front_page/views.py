from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from data.models import School, District
# Create your views here.

def search(request):
    context = {}
    return render_to_response('front_page/base.html', context, context_instance=RequestContext(request))
    
def school(request, slug):
    school = School.objects.get(slug=slug)
    context = {"school": school}
    return render_to_response('front_page/school_report.html', context, context_instance=RequestContext(request))
    
def district(request, slug):
    district = District.objects.get(slug=slug)
    context = {"district": district}
    return render_to_response('front_page/district_report.html', context, context_instance=RequestContext(request))


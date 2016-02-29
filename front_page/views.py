from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from data.models import School, District

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def landing_page(request):
    
    district = District.objects.filter(activate=True).order_by('district_name')
    paginator = Paginator(district, 10) # Show 25 contacts per page
    
    page = request.GET.get('page')
    
    try:
        district = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        district = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        district = paginator.page(paginator.num_pages)
    
    
    context = {"district": district}
    return render_to_response('front_page/landing_page.html', context, context_instance=RequestContext(request))
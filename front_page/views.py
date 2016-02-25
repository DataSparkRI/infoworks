from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from data.models import School, District
# Create your views here.

def search(request):
    context = {}
    return render_to_response('front_page/base.html', context, context_instance=RequestContext(request))
    
def report(request, report_type, code):
    if report_type == "school":
        school = School.objects.get(school_code=code)
        context = {"school": school}
        return render_to_response('front_page/school_report.html', context, context_instance=RequestContext(request))
    elif report_type == "district":
        district = District.objects.get(district_code=code)
        context = {"district": district}
        return render_to_response('front_page/district_report.html', context, context_instance=RequestContext(request))
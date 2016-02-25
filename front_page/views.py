from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from data.models import School, SchoolIndicatorSet, SchoolIndicator, SchoolIndicatorDataSet
# Create your views here.

def search(request):
    context = {}
    return render_to_response('front_page/base.html', context, context_instance=RequestContext(request))
    
def report(request, report_type, code):
    if report_type == "school":
        school = School.objects.get(school_code=code)
        school_indicator_set = SchoolIndicatorSet.objects.filter(school = school).order_by("order")

        context = {"school": school,
                   "school_indicator_set": school_indicator_set}
    return render_to_response('front_page/report.html', context, context_instance=RequestContext(request))
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from data.models import School, District, State, \
SchoolIndicator, DistrictIndicator, StateIndicator, \
DistrictDisplayDataYDetailSet, DistrictDisplayDataYDetail, DistrictIndicatorSet, DistrictIndicatorDataSet,\
SchoolYear
from models import Dictionary, Category

from django.core import exceptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def search(request):
    context = {}
    return render_to_response('front_page/base.html', context, context_instance=RequestContext(request))
    
def school(request, slug):
    try:
        school = School.objects.get(slug=slug.lower(), activate=True)
    except exceptions.ObjectDoesNotExist:
        reg = '^('
        for i in slug.split("-"):
            reg = reg + i + '?|'
        reg = reg +') +'
        objects = School.objects.filter(school_name__iregex=reg, activate=True)
        context = {"message": "Oops! The Page you requested was not found!",
                   "objects": objects}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    
    context = {"school": school}
    return render_to_response('front_page/school_report.html', context, context_instance=RequestContext(request))
    
def district(request, slug):
    try:
        district = District.objects.get(slug=slug.lower(), activate=True)
    except exceptions.ObjectDoesNotExist:
        reg = '^('
        for i in slug.split("-"):
            reg = reg + i + '?|'
        reg = reg +') +'
        objects = District.objects.filter(district_name__iregex=reg, activate=True)
        context = {"message": "Oops! The Page you requested was not found!",
                   "objects":objects}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    
    context = {"district": district}
    return render_to_response('front_page/district_report.html', context, context_instance=RequestContext(request))

def district_detail(request, slug, indicator_id, school_year, detail_slug):
    
    
    indicator = DistrictIndicator.objects.get(id=indicator_id)
    school_year = SchoolYear.objects.get(school_year=school_year)
    indicator_set = DistrictIndicatorDataSet.objects.get(district_indicator=indicator, school_year = school_year)
    detail = DistrictDisplayDataYDetail.objects.get(slug=detail_slug)
    context = {"detail": detail,
               "school_year": school_year,
               "indicator": indicator,
               }

    #table = [{"dimension_y":"", "names":[], "data":[]}]
    table = {}
    
    
    display_detail_set = [{"set_name":"", "data": table}]
    
    for detail_set in detail.detail_set:

        for data in detail_set.detail_data:
            try:
                print data.new_dimension_y_name
                table[data.new_dimension_y_name]
            except KeyError, e:
                table[data.new_dimension_y_name] = {"names":[], "data":[]}
            
            table[data.new_dimension_y_name]['names'].append(data.new_dimension_x_name)
            table[data.new_dimension_y_name]['data'].append(indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
            '''
            table.append({"dimension_y":data.new_dimension_y_name, 
                        "dimension_x": data.new_dimension_x_name, 
                        "object": indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name)
                        })
            names_x.append(data.new_dimension_x_name)
            data_y.append(indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
            #print data.dimension_x_name,'-', data.dimension_y_name
            #print indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name)
            '''
        print table
        print "-"*4
        
        display_detail_set.append({"set_name":detail_set.title, "data": table})
        

    
    
    
    return render_to_response('front_page/district_detail.html', context, context_instance=RequestContext(request))

def state(request):
    try:
        state = State.objects.filter(default_state=True)[0]
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Please contacts administrator to select default state."}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"state": state}
    return render_to_response('front_page/state_report.html', context, context_instance=RequestContext(request))

def states(request, slug):
    try:
        state = State.objects.get(slug=slug)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"state": state}
    return render_to_response('front_page/state_report.html', context, context_instance=RequestContext(request))

def landing_page(request):
    
    district = District.objects.filter(activate=True).order_by('district_name')
    paginator = Paginator(district, 10) # Show 10 contacts per page
    
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
    
def dictionary(request):
    category = Category.objects.all()
    context = {"category":category}
    return render_to_response('front_page/dictionary.html', context, context_instance=RequestContext(request))

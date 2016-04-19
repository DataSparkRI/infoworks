from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from data.models import School, District, State, \
SchoolIndicator, DistrictIndicator, StateIndicator, \
DistrictDisplayDataYDetailSet, DistrictDisplayDataYDetail, DistrictIndicatorSet, DistrictIndicatorDataSet,\
SchoolDisplayDataYDetailSet, SchoolDisplayDataYDetail, SchoolIndicatorSet, SchoolIndicatorDataSet,\
StateIndicatorDataSet, StateDisplayDataYDetail, StateDisplayDataY, \
SchoolYear, DistrictIndicatorDetailDataSet, SchoolIndicatorDetailDataSet, StateIndicatorDetailDataSet
from models import Dictionary, Category
import collections
from django.core import exceptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    context = {}
    return render_to_response('front_page/home.html', context, context_instance=RequestContext(request))

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
    
def schools_history(request, slug):
    try:
        school = School.objects.get(slug=slug)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"school": school}
    return render_to_response('front_page/school_history.html', context, context_instance=RequestContext(request))

def schools_history_detail(request, slug, school_year):
    
    try:
        school = School.objects.get(slug=slug)
        category = request.GET.get("category")
        indicator = SchoolIndicator.objects.get(school_indicator_set__school = school, title__title=category)
        indicator_dataset = SchoolIndicatorDataSet.objects.get(school_indicator=indicator, school_year__school_year=school_year)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"school": school,
               "indicator":indicator,
               "indicator_dataset":indicator_dataset}
    return render_to_response('front_page/school_history_detail.html', context, context_instance=RequestContext(request))
    
def school_detail(request, slug, indicator_id, school_year, detail_slug):
    
    indicator = SchoolIndicator.objects.get(id=indicator_id)
    school_year = SchoolYear.objects.get(school_year=school_year)
    school_indicator_set = SchoolIndicatorDataSet.objects.get(school_indicator=indicator, school_year = school_year)
    try:
        district_indicator_set = DistrictIndicatorDataSet.objects.get(district_indicator__title = indicator.title, district_indicator__district_indicator_set__district=indicator.school_indicator_set.school.district, school_year = school_year)
    except:
        district_indicator_set = None
    try:
        state_indicator_set = StateIndicatorDataSet.objects.get(state_indicator__title = indicator.title, state_indicator__state_indicator_set__state=indicator.school_indicator_set.school.district.us_state, school_year = school_year)    
    except:
        state_indicator_set = None
    detail = SchoolDisplayDataYDetail.objects.get(slug=detail_slug)


    display_detail_set = []
    
    for detail_set in detail.detail_set:
        table = collections.OrderedDict()
        for data in detail_set.detail_data:
            try:
                table[data.new_dimension_y_name.name]
            except KeyError, e:
                table[data.new_dimension_y_name.name] = {"dimension_y":data.new_dimension_y_name, "names":[], "data":[]}
            
            table[data.new_dimension_y_name.name]['names'].append(data.new_dimension_x_name)
            
            if data.dimension_x_name.name == "This District":
                if district_indicator_set != None:
                    table[data.new_dimension_y_name.name]['data'].append(district_indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
                else:
                    table[data.new_dimension_y_name.name]['data'].append(None)
            elif data.dimension_x_name.name == "Statewide":
                if state_indicator_set != None:
                    table[data.new_dimension_y_name.name]['data'].append(state_indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
                else:
                    table[data.new_dimension_y_name.name]['data'].append(None)
            else:
                table[data.new_dimension_y_name.name]['data'].append(school_indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))

        display_detail_set.append({"set_name":detail_set, "data": table})

    context = {"detail": detail,
               "school_year": school_year,
               "indicator": indicator,
               "detail_set": display_detail_set,
               }
               
    return render_to_response('front_page/school_detail.html', context, context_instance=RequestContext(request))

def school_overtime(request, slug):
    
    try:
        category = request.GET.get("category")
        indicator = SchoolIndicator.objects.get(school_indicator_set__school__slug=slug,title__title=category)
    except:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"indicator":indicator}
    return render_to_response('front_page/school_overtime.html', context, context_instance=RequestContext(request))

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

def districts_history(request, slug):
    try:
        district = District.objects.get(slug=slug)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"district": district}
    return render_to_response('front_page/district_history.html', context, context_instance=RequestContext(request))

def districts_history_detail(request, slug, school_year):
    
    try:
        district = District.objects.get(slug=slug)
        category = request.GET.get("category")
        indicator = DistrictIndicator.objects.get(district_indicator_set__district = district, title__title=category)
        indicator_dataset = DistrictIndicatorDataSet.objects.get(district_indicator=indicator, school_year__school_year=school_year)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"district": district,
               "indicator":indicator,
               "indicator_dataset":indicator_dataset}
    return render_to_response('front_page/district_history_detail.html', context, context_instance=RequestContext(request))

def district_detail(request, slug, indicator_id, school_year, detail_slug):
    from data.models import DistrictDisplayDataY
    indicator = DistrictIndicator.objects.get(id=indicator_id)
    school_year = SchoolYear.objects.get(school_year=school_year)
    district_indicator_set = DistrictIndicatorDataSet.objects.get(district_indicator=indicator, school_year = school_year)
    state_indicator_set = StateIndicatorDataSet.objects.get(state_indicator__title =indicator.title, state_indicator__state_indicator_set__state=indicator.district_indicator_set.district.us_state, school_year = school_year)
    detail = DistrictDisplayDataYDetail.objects.get(slug=detail_slug)

    if detail.district_display_type == 'SCHOOL':
        district = indicator.district_indicator_set.district
        district_display_data_y = DistrictDisplayDataY.objects.filter(district_indicator=indicator,detail=detail)
        context = {"type":detail.district_display_type,
                   "y":district_display_data_y,
                   "indicator_set":district_indicator_set,
                   "district":district,
                   "detail": detail,
                   "school_year": school_year,
                   "indicator": indicator}
        return render_to_response('front_page/district_summary.html', context, context_instance=RequestContext(request))
    else:

        display_detail_set = []
        
        for detail_set in detail.detail_set:
            table = collections.OrderedDict()
            for data in detail_set.detail_data:
                try:
                    table[data.new_dimension_y_name.name]
                except KeyError, e:
                    table[data.new_dimension_y_name.name] = {"dimension_y":data.new_dimension_y_name, "names":[], "data":[]}
                
                table[data.new_dimension_y_name.name]['names'].append(data.new_dimension_x_name)
                
                if data.dimension_x_name.name == "Statewide":
                    table[data.new_dimension_y_name.name]['data'].append(state_indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
                else:
                    table[data.new_dimension_y_name.name]['data'].append(district_indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
    
            display_detail_set.append({"set_name":detail_set, "data": table})
    
        context = {"detail": detail,
                   "school_year": school_year,
                   "indicator": indicator,
                   "detail_set": display_detail_set,
                   }
        return render_to_response('front_page/district_detail.html', context, context_instance=RequestContext(request))

def district_overtime(request, slug):
    
    try:
        category = request.GET.get("category")
        indicator = DistrictIndicator.objects.get(district_indicator_set__district__slug=slug,title__title=category)
    except:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"indicator":indicator}
    return render_to_response('front_page/district_overtime.html', context, context_instance=RequestContext(request))

def states(request, slug):
    try:
        state = State.objects.get(slug=slug)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"state": state}
    return render_to_response('front_page/state_report.html', context, context_instance=RequestContext(request))

def states_history(request, slug):
    try:
        state = State.objects.get(slug=slug)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"state": state}
    return render_to_response('front_page/state_history.html', context, context_instance=RequestContext(request))

def states_history_detail(request, slug, school_year):
    
    try:
        state = State.objects.get(slug=slug)
        category = request.GET.get("category")
        indicator = StateIndicator.objects.get(state_indicator_set__state = state, title__title=category)
        indicator_dataset = StateIndicatorDataSet.objects.get(state_indicator=indicator, school_year__school_year=school_year)
    except exceptions.ObjectDoesNotExist:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"state": state,
               "indicator":indicator,
               "indicator_dataset":indicator_dataset}
    return render_to_response('front_page/state_history_detail.html', context, context_instance=RequestContext(request))


def state_detail(request, slug, indicator_id, school_year, detail_slug):
    indicator = StateIndicator.objects.get(id=indicator_id)
    school_year = SchoolYear.objects.get(school_year=school_year)
    indicator_set = StateIndicatorDataSet.objects.get(state_indicator=indicator, school_year = school_year)
    detail = StateDisplayDataYDetail.objects.get(slug=detail_slug)
    
    if detail.state_display_type == 'SCHOOL' or detail.state_display_type == 'DISTRICT':
        state = indicator.state_indicator_set.state
        state_display_data_y = StateDisplayDataY.objects.filter(state_indicator=indicator,detail=detail)
        context = {"type":detail.state_display_type,
                   "y":state_display_data_y,
                   "indicator_set":indicator_set,
                   "state":state,
                   "detail": detail,
                   "school_year": school_year,
                   "indicator": indicator}
        return render_to_response('front_page/state_summary.html', context, context_instance=RequestContext(request))
    else:
        display_detail_set = []
        for detail_set in detail.detail_set:
            table = collections.OrderedDict()
            for data in detail_set.detail_data:
                try:
                    table[data.new_dimension_y_name.name]
                except KeyError, e:
                    table[data.new_dimension_y_name.name] = {"dimension_y":data.new_dimension_y_name, "names":[], "data":[]}
                table[data.new_dimension_y_name.name]['names'].append(data.new_dimension_x_name)
                table[data.new_dimension_y_name.name]['data'].append(indicator_set.get_objects(data.dimension_x_name, data.dimension_y_name))
            display_detail_set.append({"set_name":detail_set, "data": table})
        context = {"detail": detail,
                   "school_year": school_year,
                   "indicator": indicator,
                   "detail_set": display_detail_set,
                   }
        return render_to_response('front_page/state_detail.html', context, context_instance=RequestContext(request))

def state_overtime(request, slug):
    
    try:
        category = request.GET.get("category")
        indicator = StateIndicator.objects.get(state_indicator_set__state__slug=slug,title__title=category)
    except:
        context = {"message": "Oops! The Page you requested was not found!"}
        return render_to_response('404.html', context, context_instance=RequestContext(request))
    context = {"indicator":indicator}
    return render_to_response('front_page/state_overtime.html', context, context_instance=RequestContext(request))

def state(request):
    try:
        state = State.objects.filter(default_state=True)[0]
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
#    if request.method == 'POST':
#        search_result = Dictionary.objects.filter(content__contains='school')
#        category = Category.objects.filter(category=search_result.category)
#        context = {"category":category}
#        return redirect('/')
#        return HttpResponse(request.POST['search_term'])

    if 'search_term' in request.GET and request.GET['search_term']:
        terms = Dictionary.objects.filter(content__contains=request.GET['search_term'])
    else:
        terms = Dictionary.objects.all()
        
    category = []
    for d in terms:
        if d.category.category not in category:
            category.append(d.category.category)
    context = {"category":category,"terms":terms}
        
    return render_to_response('front_page/dictionary.html', context, context_instance=RequestContext(request))

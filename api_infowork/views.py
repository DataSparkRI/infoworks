from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from django.http import JsonResponse
from data.models import StateIndicator, DistrictIndicator, DistrictIndicatorData, SchoolIndicator, SchoolIndicatorData, SchoolYear, IndicatorTitle
from data.models import State, District, School
from data.models import StateDisplayDataYDetailSet, DistrictDisplayDataYDetailSet, SchoolDisplayDataYDetailSet
from data.models import SchoolYear, SchoolIndicatorSet, SchoolIndicatorDataSet, DistrictIndicatorSet, DistrictIndicatorDataSet
# Create your views here.
import json
from django.core import serializers
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from front_page.models import Config

from django.http import HttpResponse
from django.template import loader

'''
https://infoworks-yangxu.c9users.io/api/?indicator_type=school&indicator_id=2&school_year=2015-2016
https://infoworks-yangxu.c9users.io/api/?indicator_type=school&school_code=1104&indicator_title=SAT Exams (High School)&school_year=2014-2015

{"indicator_type":"District",
"district_code":"1",
"district_name":"Barrington",
"indicator_name":"SAT Exams (High School)",
"school_year":"2014-2015",
"indicator_data":[{
        "dimension_y": "Reading Average (out of 800)",
        "data":[
                {"dimension_x":"This District", "value":"432"},
                {"dimension_x":"Statewide", "value":"653"},
                ... ...
                {"dimension_x":"Nationwide", "value":"653"}
                ]
        },
        {"dimension_y": "Writing Average (out of 800)",
        "data":[
                {"dimension_x":"This District", "value":"432"},
                {"dimension_x":"Statewide", "value":"653"},
                ... ...
                {"dimension_x":"Nationwide", "value":"653"}
                ]
        }]
}
'''

@staff_member_required
def clean_memcached(request):
    from django.core.cache import cache
    cache.clear()
    return redirect(request.META["HTTP_REFERER"])

def highchart_js(request, type, indicator_id, school_year, detail_slug, detail_id):
    name = request.GET.get('name', 'highchart')
    if type=='state':
        indicator = StateIndicator.objects.get(id=indicator_id)
        school_year = SchoolYear.objects.get(school_year=school_year)
        detail = StateDisplayDataYDetailSet.objects.get(id=detail_id)
    elif type=='district':
        indicator = DistrictIndicator.objects.get(id=indicator_id)
        school_year = SchoolYear.objects.get(school_year=school_year)
        detail = DistrictDisplayDataYDetailSet.objects.get(id=detail_id)
    elif type=='school':
        indicator = SchoolIndicator.objects.get(id=indicator_id)
        school_year = SchoolYear.objects.get(school_year=school_year)
        detail = SchoolDisplayDataYDetailSet.objects.get(id=detail_id)
    
    if detail.display_type == 'PIE-CHART':
        t = loader.get_template('charts/highchart_pie_chart.js')
        series = {}
        for row in detail.detail_data:
            try:
                series[row.new_dimension_x_name]['data'].append({"name": row.new_dimension_y_name.name,
                                                               "y":{"x":row.dimension_x_name.name,"y":row.dimension_y_name.name}
                                                               })
            except:
                series.update({row.new_dimension_x_name:{"name":row.new_dimension_x_name.name,
                                                          "colorByPoint":"true",
                                                          "data":[{"name": row.new_dimension_y_name.name,
                                                                   "y":{"x":row.dimension_x_name.name,"y":row.dimension_y_name.name}
                                                                }]
                                                        }
                            })
        context={"name":name,
                "type":type,
                "series":series,
                "detail":detail,
                "indicator":indicator,
                "school_year":school_year}
        return HttpResponse(t.render(context, request), content_type='text/javascript')


def api(request):
        if request.method == 'GET':
                indicator_type = request.GET.get("indicator_type")
                indicator_id = request.GET.get("indicator_id")
                school_year = request.GET.get("school_year")
                school_code = request.GET.get("school_code")
                district_code = request.GET.get("district_code")
                indicator_title = request.GET.get("indicator_title")
                
                if indicator_id != None and indicator_type =="school":
                        try:
                                indicator = SchoolIndicator.objects.get(id = indicator_id)
                        except:
                                return JsonResponse({"messages":"indicator does not exist"})
                elif school_code != None and indicator_title!=None and indicator_type =="school":
                        try:
                                indicator = SchoolIndicator.objects.get(school_indicator_set__school__school_code = school_code, title__title=indicator_title)
                        except:
                                return JsonResponse({"messages":"indicator does not exist"})
                elif indicator_id != None and indicator_type =="district":
                        try:
                                indicator = DistrictIndicator.objects.get(id = indicator_id)
                        except:
                                return JsonResponse({"messages":"indicator does not exist"})
                elif district_code != None and indicator_title!=None and indicator_type =="district":
                        try:
                                indicator = DistrictIndicator.objects.get(district_indicator_set__district__district_code = district_code, title__title=indicator_title)
                        except:
                                return JsonResponse({"messages":"indicator does not exist"})
                else:
                        return JsonResponse({"messages":"indicator does not exist"})
                
                if indicator_type == "school":
                        
                        data = {"indicator_type":"School",
                                "district_code":indicator.school_indicator_set.school.school_code,
                                "district_name":indicator.school_indicator_set.school.school_name,
                                "indicator_name":indicator.title.title,
                                "school_year":school_year,
                                "indicator_data":[]}
                        indicator_data = []
                        if school_year != None:
                                school_indicator_data = SchoolIndicatorData.objects.filter(school_indicator_dataset__school_indicator=indicator,school_indicator_dataset__school_year__school_year=school_year)
                        else:
                                school_indicator_data = SchoolIndicatorData.objects.filter(school_indicator_dataset__school_indicator=indicator)
                        index = school_indicator_data.values("dimension_y").annotate(Count("dimension_y"))
                        for i in index:
                                dimension_data = []
                                data_rows = school_indicator_data.filter(dimension_y=i["dimension_y"])
                                for j in data_rows:
                                        dimension_data.append({"dimension_x":j.dimension_x,"value":j.key_value, "data_type":j.data_type})
                                indicator_data.append({"dimension_y":i["dimension_y"], "data":dimension_data})
                        data["indicator_data"] = indicator_data
                        return JsonResponse(data, safe=False)
                        
                elif indicator_type == "district":
                        data = {"indicator_type":"District",
                                "district_code":indicator.district_indicator_set.district.district_code,
                                "district_name":indicator.district_indicator_set.district.district_name,
                                "indicator_name":indicator.title.title,
                                "school_year":school_year,
                                "indicator_data":[]}
                        indicator_data = []
                        if school_year != None:
                                school_indicator_data = DistrictIndicatorData.objects.filter(district_indicator_dataset__district_indicator__id=indicator_id,school_indicator_dataset__school_year__school_year=school_year)
                        else:
                                school_indicator_data = DistrictIndicatorData.objects.filter(district_indicator_dataset__district_indicator__id=indicator_id)
                        index = district_indicator_data.values("dimension_y").annotate(Count("dimension_y"))
                        for i in index:
                                dimension_data = []
                                data_rows = district_indicator_data.filter(dimension_y=i["dimension_y"])
                                for j in data_rows:
                                        dimension_data.append({"dimension_x":j.dimension_x,"value":j.key_value, "data_type":j.data_type})
                                indicator_data.append({"dimension_y":i["dimension_y"], "data":dimension_data})
                        data["indicator_data"] = indicator_data
                        return JsonResponse(data, safe=False)
                else:
                        return JsonResponse({"messages":"indicator does not exist"})
                
                return JsonResponse()
        elif request.method == 'POST':
                return JsonResponse({"messages":"indicator does not exist"})

def overtime(request):
    result = {}
    import ast
    try:
        order_by = Config.objects.get(name = "over-time-school-year-order").value
    except:
        order_by = '-school_year__school_year'
    if request.method == 'POST':
        type = request.POST.get("type")
        slug = request.POST.get("slug")
        indicator_title = request.POST.get("category")
        school_year = request.POST.get("school_year")
        dataset = ast.literal_eval(request.POST.get("dataset"))
        
        if type == "school":
            indicator = SchoolIndicator.objects.get(title__title=indicator_title, school_indicator_set__school__slug=slug)            
            if school_year == None:
                school_year = [i.school_year.school_year for i in indicator.dataset.order_by(order_by)]
                result.update({"school_year":school_year})
                result.update({"school_name":indicator.school_indicator_set.school.school_name})
                data = []
                for i in dataset:
                    current = {"name":i,"row":[]}
                    for j in indicator.dataset.order_by(order_by):
                        value = j.get_objects("This School",i)
                        if value ==None:
                            current["row"].append(None)
                        else:
                            current["row"].append(j.get_objects("This School", i).key_value)
                    data.append(current)
                result.update({"data":data})
            return JsonResponse(result)
        elif type == "district":
            indicator = DistrictIndicator.objects.get(title__title=indicator_title, district_indicator_set__district__slug=slug)            
            if school_year == None:
                school_year = [i.school_year.school_year for i in indicator.dataset.order_by(order_by) ]
                result.update({"school_year":school_year})
                result.update({"district_name":indicator.district_indicator_set.district.district_name})
                data = []
                for i in dataset:
                    current = {"name":i,"row":[]}
                    for j in indicator.dataset.order_by(order_by):
                        value = j.get_objects("This District",i)
                        if value ==None:
                            current["row"].append(None)
                        else:
                            current["row"].append(j.get_objects("This District", i).key_value)
                    data.append(current)
                result.update({"data":data})
            return JsonResponse(result)
        elif type == "state":
            indicator = StateIndicator.objects.get(title__title=indicator_title, state_indicator_set__state__slug=slug)            
            if school_year == None:
                school_year = [i.school_year.school_year for i in indicator.dataset.order_by(order_by) ]
                result.update({"school_year":school_year})
                result.update({"state_name":indicator.state_indicator_set.state.state_name})
                data = []
                for i in dataset:
                    current = {"name":i,"row":[]}
                    for j in indicator.dataset.order_by(order_by):
                        value = j.get_objects("Statewide",i)
                        if value ==None:
                            current["row"].append(None)
                        else:
                            current["row"].append(j.get_objects("Statewide", i).key_value)
                    data.append(current)
                result.update({"data":data})
            return JsonResponse(result)
        
    return JsonResponse({"messages":"indicator does not exist"})
    

def data(request):
    state = None
    district = None
    school = None
    dimension_y = [school.school_year for school in SchoolYear.objects.all().order_by("school_year")]
    table = cache.get(request.get_full_path())
    if not table:
        pass
    else:
        return JsonResponse(table, safe=False)
    table = {"dimension_x": ["Topic","Category"] + dimension_y, "data":[]}
    
    def getData(obj):
        result = []
        for indicator_set in obj.indicatorset:
            data = []
            for indicator in indicator_set.indicators:
                data = [indicator_set.title]
                data.append(indicator.title.title)
                for school_year in dimension_y:
                    try:
                        indicator.dataset.get(school_year__school_year=school_year)
                        data.append(True)
                    except:
                        data.append(None)
                result.append(data)
        return result
    
    def returnDefaultState():
        state = State.objects.get(default_state=True)
        table["name"] = state.state_name
        table["description"] = state.description
        return getData(state)
    
    if request.method == 'GET':
        type = request.GET.get("type")
        get = request.GET.get("get")
        if type == "state":
            try:
                state = State.objects.get(slug=get)
                table["name"] = state.state_name
                table["description"] = state.description
                table["data"] = getData(state)
            except:
                table["data"] = returnDefaultState()
        elif type == "district":
            try:
                district = District.objects.get(slug=get)
                table["name"] = district.district_name
                table["description"] = district.description
                table["data"] = getData(district)
            except:
                table["data"] = returnDefaultState()
        elif type == "school":
            try:
                school = School.objects.get(slug=get)
                table["name"] = school.school_name
                table["description"] = school.description
                table["data"] = getData(school)
            except:
                table["data"] = returnDefaultState()
        else:
            table["data"] = returnDefaultState()
    cache.set(request.get_full_path(), table)
    return JsonResponse(table, safe=False)


def school(request):
    type = request.GET.get("type")
    school_code = request.GET.get("school_code")
    district_code = request.GET.get("district_code")
    if school_code == None:
        if type == "E":
           school = School.objects.filter(activate = True, elementary_school=True).order_by('school_name')
        elif type == "M":
            school = School.objects.filter(activate = True, middle_school = True).order_by('school_name')
        elif type == "H":
            school = School.objects.filter(activate = True, high_school = True).order_by('school_name')
        else:
            school = School.objects.filter(activate = True).order_by('school_name')
        if district_code != None:
            district = District.objects.get(district_code=district_code)
            school = school.filter(district=district).order_by('school_name')
        return JsonResponse(dict(genres=list(school.values('id', 'district__district_code', 'school_code', 'short_name', 'school_name'))))
    else:
        school = School.objects.get(school_code=school_code)
        indicator_set = SchoolIndicatorSet.objects.filter(school=school)
        indicators = SchoolIndicator.objects.filter(school_indicator_set__in=indicator_set).order_by("title__title")
        return JsonResponse(dict(genres=list(indicators.values('id', 'school_indicator_set__title', 'title__title',))))

def district(request):
    district_code = request.GET.get("district_code")
    if district_code == None:
       districts = District.objects.filter(activate=True).order_by('district_name')
       return JsonResponse(dict(genres=list(districts.values('id', 'us_state__state_code', 'district_code', 'district_name',))))
    else:
        district = District.objects.get(district_code=district_code)
        indicator_set = DistrictIndicatorSet.objects.filter(district=district)
        indicators = DistrictIndicator.objects.filter(district_indicator_set__in=indicator_set).order_by("title__title")
        return JsonResponse(dict(genres=list(indicators.values('id', 'district_indicator_set__title', 'title__title',))))

def district_indicator(request):
    indicator_id = request.GET.get("indicator_id")
    districtdataset_id = request.GET.get("districtdataset_id")
    
    if indicator_id != None:
        indicator = DistrictIndicator.objects.get(id=indicator_id)
        school_year = indicator.dataset
        return JsonResponse(dict(genres=list(school_year.values('id','school_year__school_year'))))
    elif districtdataset_id != None:
        dataset = DistrictIndicatorDataSet.objects.get(id=districtdataset_id)
        data = DistrictIndicatorData.objects.filter(district_indicator_dataset=dataset).exclude(key_value='--').order_by('dimension_y')
        return JsonResponse(dict(genres=list(data.values('id','district_indicator_dataset__school_year__school_year','dimension_x','dimension_y','key_value','data_type'))))
    else:
        return JsonResponse(dict(genres=[]))

def school_indicator(request):
    indicator_id = request.GET.get("indicator_id")
    schooldataset_id = request.GET.get("schooldataset_id")
    
    if indicator_id != None:
        indicator = SchoolIndicator.objects.get(id=indicator_id)
        school_year = indicator.dataset
        return JsonResponse(dict(genres=list(school_year.values('id','school_year__school_year'))))
    elif schooldataset_id != None:
        dataset = SchoolIndicatorDataSet.objects.get(id=schooldataset_id)
        data = SchoolIndicatorData.objects.filter(school_indicator_dataset=dataset).exclude(key_value='--').order_by('dimension_y')
        return JsonResponse(dict(genres=list(data.values('id','school_indicator_dataset__school_year__school_year','dimension_x','dimension_y','key_value','data_type'))))
    else:
        return JsonResponse(dict(genres=[]))

def school_tabledata(request):
    indicatordata_ids = request.GET.get("indicatordata_ids")
    compare = request.GET.get("compare") # school or school_year
    type = request.GET.get("type")
    ids = indicatordata_ids.split(',')

    result = []
    if type == "school":
        data = SchoolIndicatorData.objects.filter(id__in=ids)
    elif type == "district":
        data = DistrictIndicatorData.objects.filter(id__in=ids)
        
    if type == "school" and compare == "school_year":
        fields = [{"name":"dimension_y","type":'string'}]
        columns = [{'text' : 'Dimension Y','flex' : 1, 'sortable' : True,'dataIndex': 'dimension_y'}]

        if data.count() > 0:
            indicator = data[0].school_indicator_dataset.school_indicator
            school_years = indicator.dataset.values("school_year__school_year").order_by('school_year__school_year')
            for school_year in school_years:
                fields.append({"name":school_year['school_year__school_year'],"type":'string'})
                columns.append({'text' : school_year['school_year__school_year'],'width' : "10%", 'sortable' : True,'dataIndex': school_year['school_year__school_year']})
            for i in data:
                row = [i.dimension_y]
                for dataset in indicator.dataset.order_by('school_year__school_year'):
                    
                    try:
                        key_value = SchoolIndicatorData.objects.filter(school_indicator_dataset=dataset,
                                               dimension_y=i.dimension_y,
                                               dimension_x=i.dimension_x,
                                               data_type=i.data_type).first().key_value
                        row.append(key_value)
                    except:
                        row.append(None)
                result.append(row)
            return JsonResponse(dict(fields=fields, data=result, columns=columns))
    
        else:
            return JsonResponse(dict(fields=[], data=[], columns=[]))
    elif type == "school" and compare == "school_or_district":
        fields = [{"name":"school_name","type":'string'},{"name":"school_year","type":'string'}]
        columns = [{'text' : 'School Name', 'flex' : 1, 'sortable' : True,'dataIndex': 'school_name'},
                   {'text' : 'School Year', 'width' : "15%", 'sortable' : True,'dataIndex': 'school_year'}]

        if data.count() > 0:
            indicator = data[0].school_indicator_dataset.school_indicator
            school_year = data[0].school_indicator_dataset.school_year
            indicator_set = SchoolIndicatorSet.objects.filter(title = indicator.school_indicator_set.title)
            indicators = SchoolIndicator.objects.filter(title=indicator.title, school_indicator_set__in=indicator_set).order_by('school_indicator_set__school__school_name')
            for i in data:
                fields.append({"name":i.dimension_y, "type":'string'})
                columns.append({'text' : i.dimension_y,'width' : "10%", 'sortable' : True,'dataIndex': i.dimension_y})

            for i in indicators:
                row = [i.school_indicator_set.school.school_name, school_year.school_year]
                for j in data:
                    try:
                        dataset = SchoolIndicatorDataSet.objects.get(school_year=school_year, school_indicator=i)

                        key_value = SchoolIndicatorData.objects.filter(school_indicator_dataset=dataset,
                                                                       dimension_y=j.dimension_y,
                                                                       dimension_x=j.dimension_x,
                                                                       data_type=j.data_type).first().key_value
                        row.append(key_value)
                    except:
                        row.append(None)
                result.append(row)
            return JsonResponse(dict(fields=fields, data=result, columns=columns))
        else:
            return JsonResponse(dict(fields=[], data=[], columns=[]))
    elif type == "district" and compare == "school_year":
        fields = [{"name":"dimension_y","type":'string'}]
        columns = [{'text' : 'Dimension Y','flex' : 1, 'sortable' : True,'dataIndex': 'dimension_y'}]

        if data.count() > 0:
            indicator = data[0].district_indicator_dataset.district_indicator
            school_years = indicator.dataset.values("school_year__school_year").order_by('school_year__school_year')
            for school_year in school_years:
                fields.append({"name":school_year['school_year__school_year'],"type":'string'})
                columns.append({'text' : school_year['school_year__school_year'],'width' : "10%", 'sortable' : True,'dataIndex': school_year['school_year__school_year']})
            for i in data:
                row = [i.dimension_y]
                for dataset in indicator.dataset.order_by('school_year__school_year'):
                    
                    try:
                        key_value = DistrictIndicatorData.objects.filter(district_indicator_dataset=dataset,
                                               dimension_y=i.dimension_y,
                                               dimension_x=i.dimension_x,
                                               data_type=i.data_type).first().key_value
                        row.append(key_value)
                    except:
                        row.append(None)
                result.append(row)
            return JsonResponse(dict(fields=fields, data=result, columns=columns))
    
        else:
            return JsonResponse(dict(fields=[], data=[], columns=[]))
    elif type == "district" and compare == "school_or_district":
        fields = [{"name":"district_name","type":'string'},{"name":"school_year","type":'string'}]
        columns = [{'text' : 'District Name', 'flex' : 1, 'sortable' : True,'dataIndex': 'district_name'},
                   {'text' : 'School Year', 'width' : "15%", 'sortable' : True,'dataIndex': 'school_year'}]

        if data.count() > 0:
            indicator = data[0].district_indicator_dataset.district_indicator
            school_year = data[0].district_indicator_dataset.school_year
            indicator_set = DistrictIndicatorSet.objects.filter(title = indicator.district_indicator_set.title)
            indicators = DistrictIndicator.objects.filter(title=indicator.title, district_indicator_set__in=indicator_set).order_by('district_indicator_set__district__district_name')
            for i in data:
                fields.append({"name":i.dimension_y, "type":'string'})
                columns.append({'text' : i.dimension_y,'width' : "10%", 'sortable' : True,'dataIndex': i.dimension_y})

            for i in indicators:
                row = [i.district_indicator_set.district.district_name, school_year.school_year]
                for j in data:
                    try:
                        dataset = DistrictIndicatorDataSet.objects.get(school_year=school_year, district_indicator=i)

                        key_value = DistrictIndicatorData.objects.filter(district_indicator_dataset=dataset,
                                                                       dimension_y=j.dimension_y,
                                                                       dimension_x=j.dimension_x,
                                                                       data_type=j.data_type).first().key_value
                        row.append(key_value)
                    except:
                        row.append(None)
                result.append(row)
            return JsonResponse(dict(fields=fields, data=result, columns=columns))
        else:
            return JsonResponse(dict(fields=[], data=[], columns=[]))
    return JsonResponse(dict(fields=[], data=[], columns=[]))
    

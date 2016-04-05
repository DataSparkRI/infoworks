from django.shortcuts import render
from django.http import JsonResponse
from data.models import DistrictIndicator, DistrictIndicatorData, SchoolIndicator, SchoolIndicatorData, SchoolYear, IndicatorTitle
from data.models import State, District, School
from data.models import SchoolYear
# Create your views here.
import json
from django.core import serializers
from django.db.models import Count

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
    if request.method == 'POST':
        type = request.POST.get("type")
        slug = request.POST.get("slug")
        indicator_title = request.POST.get("category")
        school_year = request.POST.get("school_year")
        dataset = ast.literal_eval(request.POST.get("dataset"))

        
        if type == "school":
            indicator = SchoolIndicator.objects.get(title__title=indicator_title, school_indicator_set__school__slug=slug)            
            if school_year == None:
                school_year = [i.school_year.school_year for i in indicator.dataset ]
                result.update({"school_year":school_year})
                result.update({"school_name":indicator.school_indicator_set.school.school_name})
                data = []
                for i in dataset:
                    current = {"name":i,"row":[]}
                    for j in indicator.dataset:
                        value = j.get_objects("This School",i)
                        if value ==None:
                            current["row"].append(None)
                        else:
                            current["row"].append(j.get_objects("This School", i).key_value)
                    data.append(current)
                result.update({"data":data})
            return JsonResponse(result)
        
    return JsonResponse({"messages":"indicator does not exist"})
    



def data(request):
    state = None
    district = None
    school = None
    dimension_y = [school.school_year for school in SchoolYear.objects.all().order_by("school_year")]
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
    return JsonResponse(table, safe=False)


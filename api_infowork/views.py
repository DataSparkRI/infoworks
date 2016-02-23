from django.shortcuts import render
from django.http import JsonResponse
from data.models import DistrictIndicator, DistrictIndicatorData, SchoolIndicator, SchoolIndicatorData, SchoolYear, IndicatorTitle
# Create your views here.
import json
from django.core import serializers
from django.db.models import Count

'''
indicator_type=school&indicator_id=2&school_year=2014-2015
indicator_type=school&school_code=1104&indicator_title=SAT Exams (High School)&school_year=2014-2015

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


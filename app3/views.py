from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.http import HttpResponse,HttpResponseRedirect
from .models import Person,Task,GPSData,DataStorage,ClueMedia,WaypointsData,GPShistoricalData,ExperimentDataStorage,ParticipantStatusModel,QuestionnaireModel,DemographicsModel,PostExpSurveyModel,WebapplicationModel
from .models import QuestionnaireModel3D,PostExpSurveyModel3D,PostTrainingModel3D,DemographicsModel3D
import json
from .forms import DemoForm,TaskAssignmentForm,QuestionnaireForm,ConsentForm,DemographicsForm,PostExpSurveyForm,WebapplicationForm
from .forms import DemographicsForm3D,QuestionnaireForm3D,PostExpSurveyForm3D,PostTrainingForm3D

from django.urls import reverse
from django.template import loader
from django.core import serializers
from rest_framework import viewsets
from .serializers import GPSDataSerializer,ClueMediaSerializer,WaypointsDataSerializer, GPShistoricalDataSerializer
import time
from rest_framework import permissions

from .py.watershed import AreaSegment
from .py.contourmapanalysis import SegmentWeight
from .py.pathPlanGrid import GetPathFromCell3D,UpdateHeight

import csv
from django.http import StreamingHttpResponse

# Create your views here.
class IndexView(ListView):
    template_name='app3/MemberManagement.html'

    def get_queryset(self):
        return Person.objects.all()

class TaskGenerationView(TemplateView):
    template_name='app3/Taskgeneration.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #tasks_all=Task.objects.only('taskid').distinct('taskid')
        tasks_all=list(Task.objects.exclude(taskid=None).values_list('taskid', flat=True).distinct())
        #print(tasks_all)
        context['task_all']=tasks_all
        last_n_deviceid=GPSData.objects.values().order_by('-updated_at')[:5]
        context['gpsdevice']=last_n_deviceid

        pathid = WaypointsData.objects.values().order_by('-updated_at')[:5]
        context['dronepath']=pathid

        historicalpathid = GPShistoricalData.objects.values().order_by('-updated_at')[:5]
        context['dronehistoricalpath']=historicalpathid

        return context

    def get_values(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = DemoForm(request.POST)
            #print(form)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                # form.save_to_db()
                return render(request, 'app3/demo.html', {'form': form})#HttpResponseRedirect('sketch')

        # if a GET (or any other method) we'll create a blank form
            else:
                form = DemoForm()
            return render(request, 'app3/demo.html', {'form': form})

    def tasksave(request):
        if request.method == 'POST':
            #for item in request.POST:
            #print(request.POST['Taskarea'])
            #res=TestingSlideAdd(request.POST['Duress1'],request.POST['Duress2'],request.POST['Duress3'],request.POST['Duress4'])
            task_instance = Task.objects.create(notes=request.POST['task_notes'],taskid=request.POST['task_id'],taskpolygon=request.POST['task_polygon'])

            context={'title':"This is the result of tasksave",
            'Taskarea':"here in py",
            'flag':'success'}
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def gpsupdate(request):
        if request.method == 'POST':
            gpsdata_id = request.POST['id_device_id']
            gpsitem = GPSData.objects.get(deviceid=gpsdata_id)
            context={'gpsdata':getattr(gpsitem, 'gpsdata'),'flag':'success'}
            #print(context)
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def pathplanningupdate(request):
        if request.method == 'POST':
            pathdata_id = request.POST['id_device_id']
            pathitem = WaypointsData.objects.get(deviceid=pathdata_id)
            #tobj={'data':getattr(pathitem, 'waypointsdata')}
            #context={'waypointsdata':tobj,'flag':'success'}
            context={'waypointsdata':getattr(pathitem, 'waypointsdata'),'flag':'success'}
            #print(context)
            return HttpResponse(json.dumps(context)) # if everything is OK
        return HttpResponse('FAIL!!!!!')

    def gpshistoricaldataupdate(request):
        if request.method == 'POST':
            pathdata_id = request.POST['id_device_id']
            pathitem = GPShistoricalData.objects.get(deviceid=pathdata_id)
            context={'gpshistoricaldata':getattr(pathitem, 'gpshistoricaldata'),'flag':'success'}
            return HttpResponse(json.dumps(context)) # if everything is OK
        return HttpResponse('FAIL!!!!!')

    def gpsdatastorage(request):
        if request.method == 'POST':
            t_datastorage=DataStorage()
            t_datastorage.taskid = request.POST['task_notes']
            t_datastorage.subtaskid = request.POST['id_device_id']+"_"+request.POST['rand_gpsdevicename']

            all_gpsdata=request.POST.get('all_gpsdata')
            #print(all_gpsdata)

            t_datastorage.data = {'device_id':request.POST['device_id'],'gps':all_gpsdata}
            t_datastorage.save()
            context={'gpsdata':all_gpsdata,'flag':'success'}

            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def getwatershed(request):
        if request.method == 'POST':
            elevation_arr = request.POST.get('elevation_arr')
            img_w=request.POST['width']
            img_h=request.POST['height']

            #image processing watershed opencv pyhon
            tjson=json.loads(elevation_arr)
            #print(tjson)
            res=AreaSegment.GetWatershedPolygon_contours(tjson,int(img_w),int(img_h),1)
            #res=AreaSegment.GetWatershedPolygon_vironoi(tjson,int(img_w),int(img_h),1)
            #res=AreaSegment.GetAdaptiveThresholdingPolygon(tjson,int(img_w),int(img_h),1)

            context={'watershedpolygon':res,'flag':'success'}
            #print(context)

            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('Getwatershed failed!')

    def getClueMedia(request):
        if request.method == 'POST':
            clue_id = request.POST['photoid']
            clueitem = ClueMedia.objects.get(id=int(clue_id))

            context={'cluephotoid':str(clueitem.id),
                    'name':str(clueitem.name),
                    'lon':str(clueitem.longitude),
                    'lat':str(clueitem.latitude),
                    'url':str(clueitem.photo.url),
                    'detail':str(clueitem.description),
                    'flag':'success'}
            #print(context)
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def getSegmentVal(request):
        if request.method == 'POST':
            print("getSegmentVal")
            contourarr = request.POST.get('contourarr')
            voronoiarr = request.POST.get('voronoiarr')
            spatialReference = request.POST.get('spatialReference')
            #image processing segment opencv pyhon
            contourjson=json.loads(contourarr)
            voronoijson=json.loads(voronoiarr)
            #print(tjson)
            res,arr_vor=SegmentWeight(contourjson,voronoijson,spatialReference)

            context={'segmentval':res,'updatevoronoi':arr_vor,'flag':'success'}
            #print(context)

            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('Getwatershed failed!')


class TaskassignmentExperimentView(TaskGenerationView):
    template_name='app3/Taskgeneration_exp_v5.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pid = kwargs.get('participantid', None)
        if pid != None:
            context["participantid"] = kwargs['participantid']

        pindex = kwargs.get('participantindex', None)
        if pindex != None:
            context["participantindex"] = kwargs['participantindex']

        #save to ParticipantStatusModel
        pname=""
        res=ParticipantStatusModel(participantid=pid,participantname=pname,participantindex=pindex,status=True,taskstatus={"startat":int(time.time()*1000)})
        res.save()

        return context

    def updateExperimentData(request):
        if request.method == 'POST':
            #print("update experiment data")
            resarr = request.POST.get('resarr')
            details=json.loads(resarr)

            t_datastorage=ExperimentDataStorage()
            t_datastorage.details = resarr
            t_datastorage.save()

            context={'flag':'success'}

            return HttpResponse(json.dumps(context))
        return HttpResponse('Getexperimentdatastorage failed!')

class TaskIndexView(TemplateView):
    template_name="app3/index.html"
    #def get_queryset(self):
    def get(self, request, *args, **kwargs):
        img=ClueMedia.objects.all()
        context ={'message': img}
        return render(request, 'app3/index.html',context=context)
    def get_context_data(self, *args, **kwargs):
        context = super(Home. self).get_context_data(*args, **kwargs)
        context['message'] = 'Hello World!'
        return context
        #return  render_to_response("app3/index.html", {"img": img})

class TaskGenerationFormView(TemplateView):
    template_name="app3/taskgenerationform.html"
    #polygongs=Task.objects.get(id=14)
    #number of areas,

    #{'0':{'form':{'task_instructions':'[][][][]','task_complete':'yes'} ,'buttonmuber':20 },'1':{} }
    context={"form":{"task_instractions":"polygongs"}}#{'task_instructions': "[[1,1],[2,2]]"}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #polygons=Task.objects.get(taskid=kwargs['task_id'])
        polygons=Task.objects.filter(taskid=kwargs['task_id']).latest('id')
        if (polygons is not None):
            context["task_id"] = kwargs['task_id']
            if(len(polygons.taskpolygon)>10):
                taskpolygon_json=json.loads(polygons.taskpolygon)
                subtaskpolygon=taskpolygon_json[kwargs['subtask_id']]
                plytsr=str(subtaskpolygon).replace('[','').replace('],',';\r').replace(']','').replace(' ','')
                context["form"] = {"task_instractions":plytsr,"task_number":kwargs['task_id']}#self.context["form"]
                context["subtask_id"] = int(kwargs['subtask_id'])
                context["subtask_sum"] = range(len(taskpolygon_json))
            else:
                context["form"] = {"task_instractions":"Please generate searching areas for the task in the previous page!","task_number":kwargs['task_id']}
                context["subtask_id"] = 1
                context["subtask_sum"] = [1]
        return context

    def FormToDB(request):
        form=TaskAssignmentForm(request.POST or None)
        #print(request.POST)
        if form.is_valid():
            form.save()
        context={'form': form}
        #print(form)
        return render(request,'app3/demo.html',context)

class WaypointsDataViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = WaypointsData.objects.all()
    serializer_class = WaypointsDataSerializer

'''
class ExperimentDataStorage(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ExperimentDataStorage.objects.all()
    serializer_class = ExperimentDataStorageSerializer
'''

class GPShistoricalDataViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = GPShistoricalData.objects.all()
    serializer_class = GPShistoricalDataSerializer

class GPSDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.

    import requests
    r = requests.get('http://127.0.0.1:8000/gpsdatas/')
    r = requests.patch('http://127.0.0.1:8000/app3/gpsdatas/max_testing/', auth=('username','password'), data = {'deviceid':'max_testing', 'taskid':'sar_put2','gpsdata':'{"gps":["stamp":004,"lat":-80,"log":38]}'})
    r = requests.post('http://127.0.0.1:8000/app3/gpsdatas/', auth=('username','password'),data = {'deviceid':'max_test_100', 'taskid':'sar_put2','gpsdata':'{"gps":["stamp":004,"lat":-80,"log":38]}'})
    r.text

    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = GPSData.objects.all()
    serializer_class = GPSDataSerializer

class ClueMediaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.

    import base64
    import requests

    # filnename is the location of where the image are sent from
    filename="D:/Projects/SARWeb/static/img/cluesamples/thermal_sample.png"

    # url are the target IP address and port + "/cluemedia/", for example, http://172.29.20.199:8000/cluemedia/
    url = "http://127.0.0.1:8000/cluemedia/"

    # the format of uploading files
    # files = {'photo': open(filename, 'rb')}

    # requests.get is to view the existing data
    r = requests.get(url)

    # requests.post is to create a new item in the database
    r = requests.post(url,
        auth=(username,password),
        data = {'id':'2', 'name':'Drone2','longitude':'-80.543407', 'latitude':'37.196209', 'description':'Thermal camera top view'},
        files={'photo':open(filename, 'rb')}
        )
    # requests.patch is to update an existing item in the database, the url need to add a index
    r=requests.patch('http://127.0.0.1:8000/cluemedia/2/',
        auth=(username,password),
        data = {'id':'2', 'name':'Drone2','longitude':'-80.543407', 'latitude':'37.196209', 'description':'Thermal camera top view'},
        files={'photo':open(filename, 'rb')}
        )
    print (r.text)
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = ClueMedia.objects.all()
    serializer_class = ClueMediaSerializer

class TaskassignmentFullView(TaskassignmentExperimentView):
    template_name='app3/Taskgeneration_full.html'

class ConsentFormView(TemplateView):
    template_name="app3/exp_survey_consentform.html"
    context={"participantid":0,"participantindex":0}
    def FormToDB(request):
        pflag=request.POST.get("check1")
        pid=request.POST.get("participantid")
        pname=request.POST.get("participantname")
        pindex=0

        queryset = ParticipantStatusModel.objects.exclude(participantindex=None).values().order_by('-participantindex')
        if not queryset:
            pindex=0
        else:
            pindex = queryset[0]['participantindex']+1
        res=ParticipantStatusModel(participantid=pid,participantname=pname,participantindex=pindex)
        res.save()

        pindex = pindex % 55

        #context={"participantid":pid,"participantindex":pindex}

        return redirect(reverse('demos',kwargs={"participantid":pid,"participantindex":str(pindex)}))
        #return render(request,'app3/exp_survey_demographics.html',context)

class DemogrphicsView(TemplateView):
    template_name="app3/exp_survey_demographics.html"
    context={"participantid":0,"participantindex":0}
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        #context["participantid"] = kwargs['participantid']
        #context["participantindex"] = kwargs['participantindex']
        #print(context)
        return context
    def FormToDB(request):
        pid=request.POST.get("participantid")
        pindex=request.POST.get("participantindex")
        form=DemographicsForm(request.POST or None)
        if form.is_valid():
            form.save()
        return redirect(reverse('experiment',kwargs={"participantid":pid,"participantindex":pindex}))


class SurveyPostEFormView(TemplateView):
    template_name="app3/exp_survey_postexp.html"
    context={"form":{"participantid":"0"}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        '''
        context["participant_id"] = kwargs['participant_id']
        '''
        return context

    def FormToDB(request):

        form=PostExpSurveyForm(request.POST or None)

        if form.is_valid():
            form.save()

        #context={'form': form,"flag":"success"}

        return redirect('exp_thanks')
        #return render(request,'app3/exp_thanks.html')

class QuestionnaireFormView(TemplateView):
    template_name="app3/questionnaire_task.html"
    context={"form":{"participantid":"0"}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["participant_id"] = kwargs['participant_id']
        context["task_id"] = kwargs['task_id']
        context["scene_id"] = kwargs['scene_id']
        context["title"] = int(context["scene_id"])
        #context["measurements"]=["trust","transparency","workload"]
        #print(context)
        context["measurement_left"]=[
            {"name":"transparency","question":"Model transparency: Do you know in general how the model works?","left":"Very little","right":"very much"},
            {"name":"trans1","question":"I understand what the model shows by this visualization.","left":"Not agree","right":"Agree"},
            {"name":"trans2","question":"It is easy to notice the distribution of the lost person in the area by this visualization.","left":"Not agree","right":"Agree"},
            {"name":"trans3","question":"I understand why the model looks like this.","left":"Not agree","right":"Agree"},
            {"name":"trans4","question":"I’m confident my choice is the best under the circumstances.","left":"Not agree","right":"Agree"},
            {"name":"trans5","question":"I understand how the system will assist me with decisions I have to make.","left":"Not agree","right":"Agree"},
            {"name":"trust","question":"I trust the system.","left":"Not agree","right":"Agree"},
            {"name":"trust1","question":"To what extent does the model predict lost person location properly?","left":"Not at all","right":"Very high"},
            {"name":"trust2","question":"To what extent can the model’s behavior be predicted from moment to moment?","left":"Not at all","right":"Very high"},
            {"name":"trust3","question":"To what extent can you count on the model to do its job?","left":"Not at all","right":"Very high"},
            {"name":"trust4","question":"Your degree of trust in the model?","left":"Not at all","right":"Very high"},
            {"name":"trust5","question":"I can rely on the system to function properly","left":"not at all","right":"Very high"}

            ]
        context["measurement_right"]=[
            {"name":"workload","question":"Please select your workload level.","left":"Very low","right":"Very high"},
            {"name":"NASATLX1_mental","question":"How mentally demanding was the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX2_physical","question":"How physically demanding was the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX3_temporal","question":"How hurried or rushed was the pace of the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX4_performance","question":"How successful were you in accomplishing what you were asked to do?","left":"Very low","right":"Very high"},
            {"name":"NASATLX5_effort","question":"How hard did you have to work to accomplish your level of performance?","left":"Very low","right":"Very high"},
            {"name":"NASATLX6_frustration","question":"How insecure, discouraged, irritated, stressed, and annoyed were you?","left":"Very low","right":"Very high"},
            {"name":"q4","question":"This visualization is helpful for decision making that SAR professionals and volunteers perform to conduct searches.","left":"Disagree","right":"Agree"},
            {"name":"q5","question":"This visualization captures most likely location(s)/area(s) for finding the lost person at different time of the SAR mission.","left":"Disagree","right":"Agree"},
            {"name":"q7","question":"This visualization captures representative travel speed or mobility of the lost person.","left":"Strongly Disagree","right":"Agree"},
            {"name":"q9","question":"This visualization captures representative directions of travel of the lost person, given the landscape and initial planning point.","left":"Disagree","right":"Agree"},
            {"name":"q11","question":"This visualization captures most likely travel route(s) of the lost person.","left":"Disagree","right":"Agree"}
            ]
        return context

    def FormToDB(request):
        form=QuestionnaireForm(request.POST or None)
        #print(form)
        #print(form.errors)
        if form.is_valid():
            #print(form)
            form.save()
        sid=request.POST.get("sceneid")
        sid=sid.rstrip('/')
        if int(sid)>=8:
            pid=request.POST.get("participantid")
            #context={"participantid":pid}
            #return render(request,'app3/exp_survey_postexp.html',context)

            #return redirect(reverse('survey_postexperiment',kwargs={"participantid":pid}))
            return redirect(reverse('survey_postexp_webapp',kwargs={"participantid":pid}))

        context={'form': form,"flag":"success"}
        return  HttpResponse('''
   <script type="text/javascript">
      window.close();
      top.close();
   </script>''')

class WebapplicationFormView(TemplateView):
    template_name="app3/exp_survey_postexp_rating.html"
    context={"form":{"participantid":"0"}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["participantid"] = kwargs['participantid']
        context["measurement_left"]=[
            {"name":"q1","question":"The web application is useful for SAR professionals and volunteers in conducting their missions.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q2","question":"The map division function provides effective search areas for tasking.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q3","question":"The map division function could save time for task assignment.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q4","question":"The map division function is flexible for customizing search areas for tasking.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q5","question":"The map division function is easy and intuitive to use for creating search areas.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q6","question":"The task assigning function based on search areas produces useful options for assigning search teams.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q7","question":"The task assigning function based on search areas could save time for producing task assignments.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q8","question":"The task assigning function is flexible for customizing task assignments.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q9","question":"The task assigning function is easy and intuitive to use for producing task assignments.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q10","question":"This web application complements existing SAR tools.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q11","question":"This web application is easy to learn.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q12","question":"This web application is easy to use.","left":"Strongly Disagree","right":"Strongly Agree"},
            {"name":"q13","question":"I would recommend this web application to my SAR colleagues.","left":"Strongly Disagree","right":"Strongly Agree"}
            ]
        context["measurement_right"]=[

            ]
        return context

    def FormToDB(request):
        form=WebapplicationForm(request.POST or None)
        #print(form)
        #print(form.errors)
        if form.is_valid():
            #print(form)
            form.save()
        #print(reverse('survey_postexperiment',kwargs={"participantid":pid}))
        pid=request.POST.get("participantid")
        return redirect(reverse('survey_postexperiment',kwargs={"participantid":pid}))

class DownloadDataView(TemplateView):
    template_name="app3/downloaddata.html"
    context={}

    def questionnairedata(request):
        """A view that streams a large CSV file."""
        all_set=QuestionnaireModel.objects.all().values_list()
        rows = list(all_set)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        columrow=['id','participantid','taskid','trust','transparency','workload',
        'trans1','trans2','trans3','trans4','trans5',
        'trust1','trust2','trust3','trust4','trust5',
        'NASATLX1_mental','NASATLX2_physical','NASATLX3_temporal','NASATLX4_performance','NASATLX5_effort','NASATLX6_frustration',
        'created_at','updated_at']
        rows.insert(0,columrow)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows),content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="questionnairedata.csv"'
        return response

    def questionnaireview(request):
        context={}
        columrow=['id','participantid','taskid','trust','transparency','workload',
        'trans1','trans2','trans3','trans4','trans5',
        'trust1','trust2','trust3','trust4','trust5',
        'NASATLX1_mental','NASATLX2_physical','NASATLX3_temporal','NASATLX4_performance','NASATLX5_effort','NASATLX6_frustration',
        'created_at','updated_at']
        #context["query_results"]= list(QuestionnaireModel.objects.all())
        context["query_results"]=QuestionnaireModel.objects.values().order_by('-updated_at')[:5]
        context["columname"]= columrow
        return render(request,'app3/downloaddata.html',context)

    def questionnaireviewall(request):
        context={}
        columrow=['id','participantid','taskid','trust','transparency','workload',
        'trans1','trans2','trans3','trans4','trans5',
        'trust1','trust2','trust3','trust4','trust5',
        'NASATLX1_mental','NASATLX2_physical','NASATLX3_temporal','NASATLX4_performance','NASATLX5_effort','NASATLX6_frustration',
        'created_at','updated_at']
        #context["query_results"]= list(QuestionnaireModel.objects.all())
        context["query_results"]=QuestionnaireModel.objects.values().order_by('-updated_at')
        context["columname"]= columrow
        return render(request,'app3/downloaddata_details.html',context)

    def expdata(request):
        """A view that streams a large CSV file."""
        all_set=ExperimentDataStorage.objects.all().values_list()
        rows = list(all_set)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        columrow=['id','details','created_at']
        rows.insert(0,columrow)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows),content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="expdata.csv"'
        return response

    def expview(request):
        context={}
        context["query_results"]=ExperimentDataStorage.objects.values('id','created_at').order_by('-created_at')[:5]
        context["columname"]= ['id','created_at']
        return render(request,'app3/downloaddata.html',context)
    def expviewall(request):
        context={}
        context["query_results"]=ExperimentDataStorage.objects.values('id','created_at').order_by('-created_at')
        context["columname"]= ['id','created_at']
        return render(request,'app3/downloaddata_details.html',context)

    def participantdata(request):
        """A view that streams a large CSV file."""
        all_set=ParticipantStatusModel.objects.all().values_list()
        rows = list(all_set)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        columrow=['id','participantid','participantindex','participantname','status','taskstatus','created_at','updated_at']
        rows.insert(0,columrow)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows),content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="participantdata.csv"'
        return response

    def participantview(request):
        context={}
        context["query_results"]=ParticipantStatusModel.objects.values().order_by('-created_at')[:5]
        context["columname"]= ['id','participantid','participantindex','participantname','status','taskstatus','created_at','updated_at']
        return render(request,'app3/downloaddata.html',context)
    def participantviewall(request):
        context={}
        context["query_results"]=ParticipantStatusModel.objects.values().order_by('-created_at')
        context["columname"]= ['id','participantid','participantindex','participantname','status','taskstatus','created_at','updated_at']
        return render(request,'app3/downloaddata_details.html',context)
class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class TaskGenerationView3D(TemplateView):
    template_name='app3/Taskgeneration3D.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #tasks_all=Task.objects.only('taskid').distinct('taskid')
        tasks_all=list(Task.objects.exclude(taskid=None).values_list('taskid', flat=True).distinct())
        #print(tasks_all)
        context['task_all']=tasks_all
        last_n_deviceid=GPSData.objects.values().order_by('-updated_at')[:5]
        context['gpsdevice']=last_n_deviceid

        pathid = WaypointsData.objects.values().order_by('-updated_at')[:5]
        context['dronepath']=pathid

        historicalpathid = GPShistoricalData.objects.values().order_by('-updated_at')[:5]
        context['dronehistoricalpath']=pathid

        return context

    def get_values(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = DemoForm(request.POST)
            #print(form)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                # form.save_to_db()
                return render(request, 'app3/demo.html', {'form': form})#HttpResponseRedirect('sketch')

        # if a GET (or any other method) we'll create a blank form
            else:
                form = DemoForm()
            return render(request, 'app3/demo.html', {'form': form})

    def tasksave(request):
        if request.method == 'POST':
            #for item in request.POST:
            #print(request.POST['Taskarea'])
            #res=TestingSlideAdd(request.POST['Duress1'],request.POST['Duress2'],request.POST['Duress3'],request.POST['Duress4'])
            task_instance = Task.objects.create(notes=request.POST['task_notes'],taskid=request.POST['task_id'],taskpolygon=request.POST['task_polygon'])

            context={'title':"This is the result of tasksave",
            'Taskarea':"here in py",
            'flag':'success'}
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def gpsupdate(request):
        if request.method == 'POST':
            gpsdata_id = request.POST['id_device_id']
            gpsitem = GPSData.objects.get(deviceid=gpsdata_id)
            context={'gpsdata':getattr(gpsitem, 'gpsdata'),'flag':'success'}
            #print(context)
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def pathplanningupdate(request):
        if request.method == 'POST':
            pathdata_id = request.POST['id_device_id']
            pathitem = WaypointsData.objects.get(deviceid=pathdata_id)
            #tobj={'data':getattr(pathitem, 'waypointsdata')}
            #context={'waypointsdata':tobj,'flag':'success'}
            context={'waypointsdata':getattr(pathitem, 'waypointsdata'),'flag':'success'}
            #print(context)
            return HttpResponse(json.dumps(context)) # if everything is OK
        return HttpResponse('FAIL!!!!!')

    def gpshistoricaldataupdate(request):
        if request.method == 'POST':
            pathdata_id = request.POST['id_device_id']
            pathitem = GPShistoricalData.objects.get(deviceid=pathdata_id)
            context={'gpshistoricaldata':getattr(pathitem, 'gpshistoricaldata'),'flag':'success'}
            return HttpResponse(json.dumps(context)) # if everything is OK
        return HttpResponse('FAIL!!!!!')

    def gpsdatastorage(request):
        if request.method == 'POST':
            t_datastorage=DataStorage()
            t_datastorage.taskid = request.POST['task_notes']
            t_datastorage.subtaskid = request.POST['id_device_id']+"_"+request.POST['rand_gpsdevicename']

            all_gpsdata=request.POST.get('all_gpsdata')
            #print(all_gpsdata)

            t_datastorage.data = {'device_id':request.POST['device_id'],'gps':all_gpsdata}
            t_datastorage.save()
            context={'gpsdata':all_gpsdata,'flag':'success'}

            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def getClueMedia(request):
        if request.method == 'POST':
            clue_id = request.POST['photoid']
            clueitem = ClueMedia.objects.get(id=int(clue_id))

            context={'cluephotoid':str(clueitem.id),
                    'name':str(clueitem.name),
                    'lon':str(clueitem.longitude),
                    'lat':str(clueitem.latitude),
                    'url':str(clueitem.photo.url),
                    'detail':str(clueitem.description),
                    'flag':'success'}
            #print(context)
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('FAIL!!!!!')

    def getSegmentVal(request):
        if request.method == 'POST':
            print("getSegmentVal")
            contourarr = request.POST.get('contourarr')
            voronoiarr = request.POST.get('voronoiarr')
            spatialReference = request.POST.get('spatialReference')
            #image processing segment opencv pyhon
            contourjson=json.loads(contourarr)
            voronoijson=json.loads(voronoiarr)
            #print(tjson)
            res,arr_vor=SegmentWeight(contourjson,voronoijson,spatialReference)

            context={'segmentval':res,'updatevoronoi':arr_vor,'flag':'success'}
            #print(context)

            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('Getwatershed failed!')
    def getPathFromArea(request):
        if request.method == 'POST':
            #print("getPathFromArea")
            contourarr = request.POST.get('contourarr')
            terrainobj = request.POST.get('terrainobj')
            extentarr = request.POST.get('extentarr')
            voronoiarr = request.POST.get('voronoiarr')
            indexarr = request.POST.get('indexarr')
            resolution = request.POST.get('resolution')
            baseline = request.POST.get('baseline')
            spatialReference = request.POST.get('spatialReference')
            maptype = request.POST.get('maptype')
            #print(maptype)

            #image processing segment opencv pyhon
            contourjson=json.loads(contourarr)
            terrainjson=json.loads(terrainobj)
            extentarrjson=json.loads(extentarr)
            voronoijson=json.loads(voronoiarr)
            indexjson=json.loads(indexarr)
            maptypejson=int(maptype)
            arr_resolution=[0.0006,0.001,0.0016]#[0.0003,0.00055,0.0008]
            arr_baseheight=[0,0,0]
            baseHeight=40

            res_arrH,colorH=GetPathFromCell3D(contourjson, terrainjson, extentarrjson, voronoijson, indexjson,arr_baseheight[2], arr_resolution[2],spatialReference,maptypejson)
            res_arrM,colorM=GetPathFromCell3D(contourjson, terrainjson, extentarrjson, voronoijson, indexjson,arr_baseheight[1], arr_resolution[1],spatialReference,maptypejson)
            res_arrL,colorL=GetPathFromCell3D(contourjson, terrainjson, extentarrjson, voronoijson, indexjson,arr_baseheight[0], arr_resolution[0],spatialReference,maptypejson)

            res_arrH=UpdateHeight(res_arrH,200,400)
            res_arrM=UpdateHeight(res_arrM,100,300)
            res_arrL=UpdateHeight(res_arrL,50,200)

            #print(colorH);

            context={'path3DH':res_arrH,'coloH':colorH,'path3DM':res_arrM,'coloM':colorM,'path3DL':res_arrL,'coloL':colorL,'flag':'success'}
            print("backend finished")
            return HttpResponse(json.dumps(context)) # if everything is OK
        # nothing went well
        return HttpResponse('Getwatershed failed!')

class ConsentFormView3D(TemplateView):
    template_name="app3/exp_survey_consentform_3D.html"
    context={"participantid":0,"participantindex":0}
    def FormToDB(request):
        pflag=request.POST.get("check1")
        pid=request.POST.get("participantid")
        pname=request.POST.get("participantname")
        pindex=0

        queryset = ParticipantStatusModel.objects.exclude(participantindex=None).values().order_by('-participantindex')
        if not queryset:
            pindex=0
        else:
            pindex = queryset[0]['participantindex']+1
        res=ParticipantStatusModel(participantid=pid,participantname=pname,participantindex=pindex)
        res.save()
        #print("829")
        pindex = pindex % 55
        return redirect(reverse('demos3D',kwargs={"participantid":pid,"participantindex":str(pindex)}))

class ConsentFormView3D_ISE3614(TemplateView):
    template_name="app3/exp_survey_consentform_3D_ISE3614.html"
    context={"participantid":0,"participantindex":0}
    def FormToDB(request):
        pflag=request.POST.get("check1")
        pid=request.POST.get("participantid")
        pname=request.POST.get("participantname")
        pindex=0

        queryset = ParticipantStatusModel.objects.exclude(participantindex=None).values().order_by('-participantindex')
        if not queryset:
            pindex=0
        else:
            pindex = queryset[0]['participantindex']+1
        res=ParticipantStatusModel(participantid=pid,participantname=pname,participantindex=pindex)
        res.save()
        #print("829")
        pindex = pindex % 55
        return redirect(reverse('demos3D',kwargs={"participantid":pid,"participantindex":str(pindex)}))

class DemogrphicsView3D(TemplateView):
    template_name="app3/exp_survey_demographics_3D.html"
    context={"participantid":0,"participantindex":0}
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
    def FormToDB(request):
        pid=request.POST.get("participantid")
        pindex=request.POST.get("participantindex")
        form=DemographicsForm3D(request.POST or None)
        #print("form")
        if form.is_valid():
            form.save()

        return redirect(reverse('experiment3D',kwargs={"participantid":pid,"participantindex":pindex}))

class SurveyPostEFormView3D(TemplateView):
    template_name="app3/exp_survey_postexp_3D.html"
    context={"form":{"participantid":"0"}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def FormToDB(request):
        form=PostExpSurveyForm3D(request.POST or None)
        if form.is_valid():
            form.save()
        return redirect('exp_thanks')

class QuestionnaireFormView3D(TemplateView):
    template_name="app3/exp_survey_midexp_3D.html"
    context={"form":{"participantid":"0"}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["participant_id"] = kwargs['participant_id']
        context["task_id"] = kwargs['task_id']
        context["scene_id"] = kwargs['scene_id']
        context["title"] = int(context["scene_id"])
        #context["measurements"]=["trust","transparency","workload"]
        #print(context)
        context["measurement_left"]=[
            {"name":"trust1","question":"Please select your trust in the system.","left":"Not trust","right":"Trust"},
            {"name":"trust2","question":"To what extent do you rely on the autonomous system for decision making?","left":"Not at all","right":"Totally"},
            {"name":"trust3","question":"To what extent does the UAV survey the area properly?","left":"Not at all","right":"Totally"},
            {"name":"trust4","question":"To what extent does the searching process is proper for achieving the goal?","left":"Not at all","right":"Totally"},
            {"name":"trust5","question":"To what extent do you think the autonomous system helps you achieve the goal under uncertainty and vulnerability?","left":"Not at all","right":"Totally"},
            {"name":"trust6","question":"To what extent do you think the autonomous system is hindering disturbing your decision-making?","left":"Not at all","right":"Totally"},
            {"name":"trust7","question":"To what extent are you confident on whether your choice is the best given the circumstances/scenarios?","left":"Not at all","right":"Totally"},

            {"name":"trans1","question":"To what extent do you understand how the system works?","left":"Not at all","right":"Totally"},
            {"name":"trans2","question":"To what extend do you think the responsibility of the autonomous system is clear or easily understandable to you?","left":"Not at all","right":"Totally"},
            {"name":"trans3","question":"To what extend do you think the capabilities of the autonomous system is clear or easily understandable to you?","left":"Not at all","right":"Totally"},
            {"name":"trans4","question":"To what extend do you think the activities of the autonomous system is clear or easily understandable to you?","left":"not at all","right":"Totally"}
        ]
        context["measurement_right"]=[
            {"name":"trans5","question":"To what extend do you think the mechanism of the autonomous system is clear or easily understandable to you?","left":"Not at all","right":"Totally"},
            {"name":"trans6","question":"To what extent does the system provide with you get appropriate information to make any decisions?","left":"Not at all","right":"Totally"},
            {"name":"trans7","question":"To what extend do you understand why the result looks like this?","left":"Not at all","right":"Totally"},

            {"name":"workload","question":"Please select your workload level.","left":"Very low","right":"Very high"},
            {"name":"NASATLX1_mental","question":"How mentally demanding was the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX2_physical","question":"How physically demanding was the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX3_temporal","question":"How hurried or rushed was the pace of the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX4_performance","question":"How successful were you in accomplishing what you were asked to do?","left":"Very low","right":"Very high"},
            {"name":"NASATLX5_effort","question":"How hard did you have to work to accomplish your level of performance?","left":"Very low","right":"Very high"},
            {"name":"NASATLX6_frustration","question":"How insecure, discouraged, irritated, stressed, and annoyed were you?","left":"Very low","right":"Very high"}

        ]
        return context

    def FormToDB(request):
        form=QuestionnaireForm3D(request.POST or None)
        if form.is_valid():
            form.save()
        sid=request.POST.get("sceneid")
        print("sceneid:",sid)
        sid=sid.rstrip('/')
        if int(sid)>=4:
            pid=request.POST.get("participantid")
            return redirect(reverse('survey_postexperiment3D',kwargs={"participantid":pid}))

        context={'form': form,"flag":"success"}

        #print("894")
        return HttpResponse('''
   <script type="text/javascript">
      window.close();
      top.close();
   </script>''')

class TaskassignmentExperimentView3D(TaskGenerationView):
    template_name='app3/Taskgeneration3D_exp.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pid = kwargs.get('participantid', None)
        if pid != None:
            context["participantid"] = kwargs['participantid']

        pindex = kwargs.get('participantindex', None)
        if pindex != None:
            context["participantindex"] = kwargs['participantindex']

        #save to ParticipantStatusModel
        pname=""
        res=ParticipantStatusModel(participantid=pid,participantname=pname,participantindex=pindex,status=True,taskstatus={"startat":int(time.time()*1000)})
        res.save()
        print(context)
        return context

    def updateExperimentData(request):
        if request.method == 'POST':
            #print("update experiment data")
            resarr = request.POST.get('resarr')
            details=json.loads(resarr)

            t_datastorage=ExperimentDataStorage()
            t_datastorage.details = resarr
            t_datastorage.save()

            context={'flag':'success'}

            return HttpResponse(json.dumps(context))
        return HttpResponse('Getexperimentdatastorage failed!')

    def SaveExperimentdatatoDBDataStorage(request):
        if request.method == 'POST':
            resarr = request.POST.get('resarr')
            details=json.loads(resarr)

            t_datastorage=DataStorage()
            t_datastorage.taskid = request.POST['participantIndex']
            t_datastorage.subtaskid = request.POST['taskIndex']
            t_datastorage.data= resarr
            t_datastorage.save()

            context={'flag':'success'}
            return HttpResponse(json.dumps(context))
        return HttpResponse('SaveExperimentdatatoDBDataStorage failed!')

class PostTrainingFormView3D(TemplateView):
    template_name="app3/exp_survey_midexp_3D.html"
    context={"form":{"participantid":"0"}}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["participant_id"] = kwargs['participant_id']
        context["task_id"] = kwargs['task_id']
        context["scene_id"] = kwargs['scene_id']
        context["title"] = int(context["scene_id"])
        context["measurement_left"]=[
            {"name":"trust1","question":"Please select your trust in the system.","left":"Not trust","right":"Trust"},
            {"name":"trust2","question":"To what extent do you rely on the autonomous system for decision making?","left":"Not at all","right":"Totally"},
            {"name":"trust3","question":"To what extent does the UAV survey the area properly?","left":"Not at all","right":"Totally"},
            {"name":"trust4","question":"To what extent does the searching process is proper for achieving the goal?","left":"Not at all","right":"Totally"},
            {"name":"trust5","question":"To what extent do you think the autonomous system helps you achieve the goal under uncertainty and vulnerability?","left":"Not at all","right":"Totally"},
            {"name":"trust6","question":"To what extent do you think the autonomous system is hindering disturbing your decision-making?","left":"Not at all","right":"Totally"},
            {"name":"trust7","question":"To what extent are you confident on whether your choice is the best given the circumstances/scenarios?","left":"Not at all","right":"Totally"},

            {"name":"trans1","question":"To what extent do you understand how the system works?","left":"Not at all","right":"Totally"},
            {"name":"trans2","question":"To what extend do you think the responsibility of the autonomous system is clear or easily understandable to you?","left":"Not at all","right":"Totally"},
            {"name":"trans3","question":"To what extend do you think the capabilities of the autonomous system is clear or easily understandable to you?","left":"Not at all","right":"Totally"},
            {"name":"trans4","question":"To what extend do you think the activities of the autonomous system is clear or easily understandable to you?","left":"not at all","right":"Totally"}
        ]
        context["measurement_right"]=[
            {"name":"trans5","question":"To what extend do you think the mechanism of the autonomous system is clear or easily understandable to you?","left":"Not at all","right":"Totally"},
            {"name":"trans6","question":"To what extent does the system provide with you get appropriate information to make any decisions?","left":"Not at all","right":"Totally"},
            {"name":"trans7","question":"To what extend do you understand why the result looks like this?","left":"Not at all","right":"Totally"},

            {"name":"workload","question":"Please select your workload level.","left":"Very low","right":"Very high"},
            {"name":"NASATLX1_mental","question":"How mentally demanding was the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX2_physical","question":"How physically demanding was the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX3_temporal","question":"How hurried or rushed was the pace of the task?","left":"Very low","right":"Very high"},
            {"name":"NASATLX4_performance","question":"How successful were you in accomplishing what you were asked to do?","left":"Very low","right":"Very high"},
            {"name":"NASATLX5_effort","question":"How hard did you have to work to accomplish your level of performance?","left":"Very low","right":"Very high"},
            {"name":"NASATLX6_frustration","question":"How insecure, discouraged, irritated, stressed, and annoyed were you?","left":"Very low","right":"Very high"}
        ]
        return context

    def FormToDB(request):
        form=PostTrainingForm3D(request.POST or None)
        if form.is_valid():
            form.save()
        sid=request.POST.get("sceneid")
        sid=sid.rstrip('/')
        context={'form': form,"flag":"success"}

        return  HttpResponse('''
   <script type="text/javascript">
      opener.dismissAddAnotherPopup(window);
   </script>''')


class TaskGenerationView3DDemo(TaskGenerationView3D):
    template_name='app3/Taskgeneration3D_demo.html'

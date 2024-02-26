from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from app3.views import IndexView,TaskGenerationView,TaskGenerationView3D,TaskGenerationFormView,TaskassignmentExperimentView,TaskassignmentFullView,TaskIndexView,QuestionnaireFormView,ConsentFormView,SurveyPostEFormView,DemogrphicsView, WebapplicationFormView
from app3.views import ConsentFormView3D,DemogrphicsView3D,SurveyPostEFormView3D,QuestionnaireFormView3D,TaskassignmentExperimentView3D,PostTrainingFormView3D,ConsentFormView3D_ISE3614
from app3.views import DownloadDataView, TaskGenerationView3DDemo
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gpsdatas', views.GPSDataViewSet,basename="gpsdatas")
router.register(r'cluemedia', views.ClueMediaViewSet,basename="cluemedia")
router.register(r'waypointsdata', views.WaypointsDataViewSet,basename="waypointsdata")
router.register(r'gpshistoricaldata', views.GPShistoricalDataViewSet,basename="gpshistoricaldata")

urlpatterns = [
    #path('', TaskGenerationView.as_view(),name='sarwebinit'),
    path('',TemplateView.as_view(template_name="demo.html")),
    path('sarwebinit', TaskGenerationView.as_view(),name='sarwebinit'),

    path('sarweb3D', TaskGenerationView3D.as_view(),name='sarweb3D'),
    path('sarweb3DDemo', TaskGenerationView3DDemo.as_view(),name='sarweb3DDemo'),

    re_path(r'^experiment/task/$', TaskassignmentExperimentView.as_view(),name='experiment'),
    re_path(r'^experiment/task/(?P<participantid>\w+)/$',TaskassignmentExperimentView.as_view(),name="experiment"),
    re_path(r'^experiment/task/(?P<participantid>\w+)/(?P<participantindex>\w+)/$',TaskassignmentExperimentView.as_view(),name="experiment"),

    path('experiment/consentform',ConsentFormView.as_view(),name='consentform'),
    path('experiment/consentform_action', ConsentFormView.FormToDB),

    path('experiment/demos',DemogrphicsView.as_view(),name="demos"),
    re_path(r'^experiment/demos/(?P<participantid>\w+)/(?P<participantindex>\w+)/$',DemogrphicsView.as_view(),name="demos"),
    re_path(r'^experiment/demos/\w+/\w+/action$', DemogrphicsView.FormToDB,name="demos"),

    path('experiment/survey_postexperiment',SurveyPostEFormView.as_view(),name="survey_postexperiment"),
    re_path(r'^experiment/survey_postexperiment/\w+/action$', SurveyPostEFormView.FormToDB,name="survey_postexperiment"),
    re_path(r'^experiment/survey_postexperiment/(?P<participantid>\w+)/$',SurveyPostEFormView.as_view(),name="survey_postexperiment"),

    path('experiment/survey_postexp_webapp',WebapplicationFormView.as_view(),name="survey_postexp_webapp"),
    re_path(r'^experiment/survey_postexp_webapp/(?P<participantid>\w+)/$',WebapplicationFormView.as_view(),name="survey_postexp_webapp"),
    re_path(r'^experiment/survey_postexp_webapp/\w+/action$', WebapplicationFormView.FormToDB,name="survey_postexp_webapp"),
    path('rating_action', WebapplicationFormView.FormToDB),
    re_path(r'^experiment/survey_postexp_webapp/\w+/rating_action$',WebapplicationFormView.FormToDB,name="rating_action"),

    path('experiment/exp_thanks',TemplateView.as_view(template_name="app3/exp_thanks.html"),name="exp_thanks"),

    path('experiment/consentform3D',ConsentFormView3D.as_view(),name='consentform3D'),
    path('experiment/consentform3D_ISE3614',ConsentFormView3D_ISE3614.as_view(),name='consentform3D_ISE3614'),
    path('experiment/consentform3D_action', ConsentFormView3D.FormToDB),

    path('experiment/demos3D',ConsentFormView3D.as_view(),name="demos3D"),
    re_path(r'^experiment/demos3D/(?P<participantid>\w+)/(?P<participantindex>\w+)/$',DemogrphicsView3D.as_view(),name="demos3D"),
    re_path(r'^experiment/demos3D/\w+/\w+/action$', DemogrphicsView3D.FormToDB,name="demos3D"),
    path('experiment/survey_postexperiment3D',SurveyPostEFormView3D.as_view(),name="survey_postexperiment3D"),
    re_path(r'^experiment/survey_postexperiment3D/\w+/action$', SurveyPostEFormView3D.FormToDB,name="survey_postexperiment3D"),
    re_path(r'^experiment/survey_postexperiment3D/(?P<participantid>\w+)/$',SurveyPostEFormView3D.as_view(),name="survey_postexperiment3D"),

    path('questionnaireform3D',QuestionnaireFormView3D.as_view(),name="questionnaireform3D"),
    re_path(r'^questionnaireform3D/(?P<participant_id>\w+)/(?P<task_id>\w+)/(?P<scene_id>\w+)/$',QuestionnaireFormView3D.as_view(),name="questionnaireform3D"),
    path('questionnaire_action3D', QuestionnaireFormView3D.FormToDB),
    re_path(r'^questionnaireform3D/\w+/\w+/\w+/questionnaire_action3D$',QuestionnaireFormView3D.FormToDB,name="questionnaire_action3D"),

    path('posttrainingform3D',PostTrainingFormView3D.as_view(),name="posttrainingform3D"),
    re_path(r'^posttrainingform3D/(?P<participant_id>\w+)/(?P<task_id>\w+)/(?P<scene_id>\w+)/$',PostTrainingFormView3D.as_view(),name="posttrainingform3D"),
    path('posttraining_action3D', PostTrainingFormView3D.FormToDB),
    re_path(r'^posttrainingform3D/\w+/\w+/\w+/posttraining_action3D$',PostTrainingFormView3D.FormToDB,name="posttraining_action3D"),
    path('takeabreak/',TemplateView.as_view(template_name="app3/takeabreak.html")),

    re_path(r'^experiment/task3D/$', TaskassignmentExperimentView3D.as_view(),name='experiment3D'),
    re_path(r'^experiment/task3D/(?P<participantid>\w+)/$',TaskassignmentExperimentView3D.as_view(),name="experiment3D"),
    re_path(r'^experiment/task3D/(?P<participantid>\w+)/(?P<participantindex>\w+)/$',TaskassignmentExperimentView3D.as_view(),name="experiment3D"),
    re_path(r'^updateexperimentdata3D$', TaskassignmentExperimentView3D.updateExperimentData,name='updateexperimentdata3D'),
    re_path(r'^SaveExperimentdatatoDBDataStorage$', TaskassignmentExperimentView3D.SaveExperimentdatatoDBDataStorage,name='SaveExperimentdatatoDBDataStorage'),

    path('downloaddata', DownloadDataView.as_view(),name='downloaddata'),
    path('downloaddatadetails',TemplateView.as_view(template_name="app3/downloaddata_details.html"),name='downloaddata'),

    re_path(r'^qndata/$',DownloadDataView.questionnairedata,name="qndata"),
    re_path(r'^viewqndata/$',DownloadDataView.questionnaireview,name="viewqndata"),
    re_path(r'^viewqnall/$',DownloadDataView.questionnaireviewall,name="viewqnall"),

    re_path(r'^expdata/$',DownloadDataView.expdata,name="expdata"),
    re_path(r'^viewexpdata/$',DownloadDataView.expview,name="viewexpdata"),
    re_path(r'^viewexpdataall/$',DownloadDataView.expviewall,name="viewexpdataall"),

    re_path(r'^ptdata/$',DownloadDataView.participantdata,name="ptdata"),
    re_path(r'^viewptdata/$',DownloadDataView.participantview,name="viewptdata"),
    re_path(r'^viewptdataall/$',DownloadDataView.participantviewall,name="viewptdataall"),

    re_path(r'^updateexperimentdata$', TaskassignmentExperimentView.updateExperimentData,name='updateexperimentdata'),
    path('full', TaskassignmentFullView.as_view(),name='full'),
    path('members', IndexView.as_view()),
    path('edit',TemplateView.as_view(template_name="app3/edit.html"),name='edit'),
    path('sketch',TemplateView.as_view(template_name="app3/sketch.html")),
    path('formdemo',TemplateView.as_view(template_name="app3/FormDemo.html")),

    path('taskgenerationform',TaskGenerationFormView.as_view(),name="taskgenerationform"),
    re_path(r'^taskgenerationform/(?P<task_id>\w+)_(?P<subtask_id>\d+)/$',TaskGenerationFormView.as_view(),name="taskgenerationform"),
    path('action_page', TaskGenerationFormView.FormToDB),#.get_values
    re_path(r'^taskgenerationform/\w+/action_page$',TaskGenerationFormView.FormToDB,name="action_page"),

    path('questionnaireform',QuestionnaireFormView.as_view(),name="questionnaireform"),
    re_path(r'^questionnaireform/(?P<participant_id>\w+)/(?P<task_id>\w+)/(?P<scene_id>\w+)/$',QuestionnaireFormView.as_view(),name="questionnaireform"),
    path('questionnaire_action', QuestionnaireFormView.FormToDB),
    re_path(r'^questionnaireform/\w+/\w+/\w+/questionnaire_action$',QuestionnaireFormView.FormToDB,name="questionnaire_action"),

    path('offlinemapdemo',TemplateView.as_view(template_name="app3/offlinemapdemo.html")),
    re_path(r'^tasksave$',TaskGenerationView.tasksave,name='tasksave'),
    re_path(r'^gpsupdate$',TaskGenerationView.gpsupdate,name='gpsupdate'),
    re_path(r'^pathplanningupdate$',TaskGenerationView.pathplanningupdate,name='pathplanningupdate'),
    re_path(r'^gpshistoricaldataupdate$',TaskGenerationView.gpshistoricaldataupdate,name='gpshistoricaldataupdate'),
    re_path(r'^getwatershed$',TaskGenerationView.getwatershed,name='getwatershed'),
    re_path(r'^getsegmentVal$',TaskGenerationView.getSegmentVal,name='getsegmentVal'),
    re_path(r'^gpsdatastorage$',TaskGenerationView.gpsdatastorage,name='gpsdatastorage'),
    re_path(r'^demo$',TemplateView.as_view(template_name="app3/demo.html"), name="demo"),
    re_path(r'^openstreatmap$',TemplateView.as_view(template_name="app3/openstreatmap.html"), name="openstreatmap"),
    re_path(r'^taskgenerationform/(?P<task_id>\w+)_(?P<subtask_id>\d+)/$',TaskGenerationFormView.as_view(),name="taskgenerationform"),
    re_path(r'^readfile$',TemplateView.as_view(template_name="app3/readfile.html"), name="readfile"),
    path('api-auth/', include('rest_framework.urls')),
    path('layerquerytest',TemplateView.as_view(template_name="app3/layerquerytest.html")),

    re_path(r'^watershed/$',TemplateView.as_view(template_name="app3/watershed_segmentation.html"),name="watershed"),
    re_path(r'^watershed/(?P<bobid>\w+)/$',TemplateView.as_view(template_name="app3/watershed_getlinearfeature.html"),name="watershed"),
    path('heatmapringdownload',TemplateView.as_view(template_name="app3/Taskgeneration_download.html")),
    path('videostream',TemplateView.as_view(template_name="app3/UAVVideostream.html")),
    path('index',TaskIndexView.as_view(),name='index'),
    re_path(r'^getcluemedia$', TaskGenerationView.getClueMedia,name='getcluemedia'),
    path('translateshapefiletogeojson',TemplateView.as_view(template_name="app3/Translate_shapefile_to_geojson.html")),
    path('realdatalocation',TemplateView.as_view(template_name="app3/realdatalocation.html")),
    path('realdatalocationfiltered',TemplateView.as_view(template_name="app3/realdatalocation_filtered.html")),
    path('SARAWSMT',TemplateView.as_view(template_name="app3/SAR_AWSMechTurk_Test.html")),
    #path('index',TaskIndexView.asView()),

    re_path(r'^getPathFromArea$',TaskGenerationView3D.getPathFromArea,name='getPathFromArea'),
]

urlpatterns += router.urls
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#print(urlpatterns)

from django.contrib import admin
from .models import ClueMedia
from .models import GPSData,DataStorage,WaypointsData,GPShistoricalData,ExperimentDataStorage,QuestionnaireModel,ParticipantStatusModel,DemographicsModel,PostExpSurveyModel,WebapplicationModel,TaskAssignment,QuestionnaireModel3D,PostExpSurveyModel3D,PostTrainingModel3D,DemographicsModel3D
import csv
from django.http import HttpResponse
# Register your models here.
class ClueMediaAdmin(admin.ModelAdmin):
    def photo_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.photo.url,
            width=obj.photo.width,
            height=obj.photo.height,
            )
    )
    pass
admin.site.register(ClueMedia, ClueMediaAdmin)

class GPSDataAdmin(admin.ModelAdmin):
    list_display = ['deviceid','taskid','gpsdata','created_at','updated_at']
    pass
admin.site.register(GPSData, GPSDataAdmin)
#admin.site.register(ClueMedia)

class DataStorageAdmin(admin.ModelAdmin):
    list_display = ['id','taskid','subtaskid','data','created_at','updated_at']
    pass
admin.site.register(DataStorage, DataStorageAdmin)

class WaypointsDataAdmin(admin.ModelAdmin):
    list_display = ['deviceid','taskid','waypointsdata','created_at','updated_at']
    pass
admin.site.register(WaypointsData, WaypointsDataAdmin)

class GPShistoricalDataAdmin(admin.ModelAdmin):
    list_display = ['deviceid','taskid','gpshistoricaldata','created_at','updated_at']
    pass
admin.site.register(GPShistoricalData, GPShistoricalDataAdmin)

class ExperimentDataStorageAdmin(admin.ModelAdmin):
    list_per_page = 200
    actions = ['download_csv']
    list_display = ['id','created_at','details']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = "Download CSV file for selected stats."
admin.site.register(ExperimentDataStorage, ExperimentDataStorageAdmin)

class QuestionnaireModelAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','taskid','sceneid','trust','transparency','workload',
    'trans1','trans2','trans3','trans4','trans5',
    'trust1','trust2','trust3','trust4','trust5',
    'NASATLX1_mental','NASATLX2_physical','NASATLX3_temporal','NASATLX4_performance','NASATLX5_effort','NASATLX6_frustration',
    'q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12',
    'created_at']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = "Download CSV file for selected stats."

admin.site.register(QuestionnaireModel, QuestionnaireModelAdmin)

class ParticipantStatusModelAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','participantindex','participantname','status','taskstatus','created_at']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(ParticipantStatusModel, ParticipantStatusModelAdmin)

class DemographicsModelAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','participantindex','age','gender','education','sart','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','created_at']

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(DemographicsModel, DemographicsModelAdmin)


class PostExpSurveyModelAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20','created_at']

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(PostExpSurveyModel, PostExpSurveyModelAdmin)

class WebapplicationModelAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','q11','q12','q13','created_at']

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(WebapplicationModel, WebapplicationModelAdmin)


class TaskAssignmentAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','resourcetype','planningno','priority','task_complete','task_partially_finished','urgent_follow_up','task_number','team_identifier','resource_type','task_map','branch','division_group','incident_name','task_instructions','previous_search','transportation','equipment_requirements','expected_time_frame','expected_time_frame_input','target_pod_subject','target_pod_subject_input','target_pod_clues','target_pod_clues_input','team_nearby','team_nearby_input','applicable_clues','terrain_hazrds','weather_safety_issues','press_family_plans','subject_information','rescue_find_plans','others','others_input','team_call_sign','freq_team','base_call_sign','freq_base','pertinent_phone_no','base','check_in_feq','check_in_hour','tactical_1_function','tactical_1_freq','tactical_1_comments','tactical_2_function','tactical_2_freq','tactical_2_comments','tactical_3_function','tactical_3_freq','tactical_3_comments','tactical_4_function','tactical_4_freq','tactical_4_comments','note_safety_message','prepared_by','briefed_by','time_out','created_at']

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(TaskAssignment, TaskAssignmentAdmin)

class DemographicsModel3DAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','participantindex','age','gender','education','sart','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','created_at']

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(DemographicsModel3D, DemographicsModel3DAdmin)

class QuestionnaireModel3DAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','taskid','sceneid',
    'trust1','trust2','trust3','trust4','trust5','trust6','trust7',
    'trans1','trans2','trans3','trans4','trans5','trans6','trans7',
    'workload','NASATLX1_mental','NASATLX2_physical','NASATLX3_temporal','NASATLX4_performance','NASATLX5_effort','NASATLX6_frustration',
    'created_at']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = "Download CSV file for selected stats."

admin.site.register(QuestionnaireModel3D, QuestionnaireModel3DAdmin)

class PostExpSurveyModel3DAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','q1','q2','q3','q4','q5','q6','q7','created_at']

    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download CSV file for selected stats."
    pass
admin.site.register(PostExpSurveyModel3D, PostExpSurveyModel3DAdmin)

class PostTrainingModel3DAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display =['id','participantid','taskid','sceneid',
    'trust1','trust2','trust3','trust4','trust5','trust6','trust7',
    'trans1','trans2','trans3','trans4','trans5','trans6','trans7',
    'workload','NASATLX1_mental','NASATLX2_physical','NASATLX3_temporal','NASATLX4_performance','NASATLX5_effort','NASATLX6_frustration',
    'created_at']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = "Download CSV file for selected stats."

admin.site.register(PostTrainingModel3D, PostTrainingModel3DAdmin)

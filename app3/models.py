from django.db import models
from django.utils.text import slugify
# Create your models here.
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __str__(self):
        return self.first_name

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    taskpolygon = models.TextField(blank=True,null=True)
    notes = models.CharField(max_length=30)
    taskid = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.notes

class GPSData(models.Model):
    #id = models.AutoField(primary_key=True)
    deviceid = models.CharField(max_length=20,primary_key=True)
    taskid = models.CharField(max_length=100,blank=True,null=True)
    gpsdata = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return self.gpsdata

class WaypointsData(models.Model):
    #id = models.AutoField(primary_key=True)
    deviceid = models.CharField(max_length=20,primary_key=True)
    taskid = models.CharField(max_length=100,blank=True,null=True)
    waypointsdata = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return self.waypointsdata

class GPShistoricalData(models.Model):
    #id = models.AutoField(primary_key=True)
    deviceid = models.CharField(max_length=20,primary_key=True)
    taskid = models.CharField(max_length=100,blank=True,null=True)
    gpshistoricaldata = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return self.gpshistoricaldata

class DataStorage(models.Model):
    id = models.AutoField(primary_key=True)
    taskid = models.CharField(max_length=100,blank=True,null=True)
    subtaskid = models.CharField(max_length=100,blank=True,null=True)
    data = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return self.data


class TaskAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    resourcetype=models.CharField(max_length=100, blank=True, null=True)
    planningno=models.CharField(max_length=100, blank=True,null=True)
    priority=models.CharField(max_length=100, blank=True,null=True)

    task_complete=models.BooleanField(default=True)
    task_partially_finished=models.BooleanField(default=True)
    urgent_follow_up=models.BooleanField(default=True)

    task_number=models.CharField(max_length=100,blank=True,  default="0000")
    team_identifier=models.CharField(max_length=100, blank=True,null=True)
    resource_type=models.CharField(max_length=100, blank=True,null=True)
    task_map=models.CharField(max_length=100, blank=True,null=True)

    branch=models.CharField(max_length=100, blank=True,null=True)
    division_group=models.CharField(max_length=100, blank=True,null=True)
    incident_name=models.CharField(max_length=100, blank=True,null=True)

    task_instructions=models.TextField( blank=True,null=True)
    previous_search=models.CharField(max_length=1000, blank=True,null=True)
    transportation=models.CharField(max_length=1000, blank=True,null=True)
    equipment_requirements=models.CharField(max_length=1000, blank=True,null=True)

    expected_time_frame=models.BooleanField(default=True)
    expected_time_frame_input=models.CharField(max_length=100, blank=True,null=True)
    target_pod_subject=models.BooleanField(default=True)
    target_pod_subject_input=models.CharField(max_length=100, blank=True,null=True)

    target_pod_clues=models.BooleanField(default=True)
    target_pod_clues_input=models.CharField(max_length=100, blank=True,null=True)
    team_nearby=models.BooleanField(default=True)
    team_nearby_input=models.CharField(max_length=100, blank=True,null=True)

    applicable_clues=models.BooleanField(default=True)
    terrain_hazrds=models.BooleanField(default=True)
    weather_safety_issues=models.BooleanField(default=True)
    press_family_plans=models.BooleanField(default=True)
    subject_information=models.BooleanField(default=True)
    rescue_find_plans=models.BooleanField(default=True)
    others=models.BooleanField(default=True)
    others_input=models.TextField(blank=True,null=True)

    team_call_sign=models.CharField(max_length=100, blank=True,null=True)
    freq_team=models.CharField(max_length=100, blank=True,null=True)
    base_call_sign=models.CharField(max_length=100, blank=True,null=True)
    freq_base=models.CharField(max_length=100, blank=True,null=True)
    pertinent_phone_no=models.CharField(max_length=100, blank=True,null=True)
    base=models.CharField(max_length=100, blank=True,null=True)
    check_in_feq=models.CharField(max_length=100, blank=True,null=True)
    check_in_hour=models.CharField(max_length=100, blank=True,null=True)

    tactical_1_function=models.CharField(max_length=100, blank=True,null=True)
    tactical_1_freq=models.CharField(max_length=100, blank=True,null=True)
    tactical_1_comments=models.CharField(max_length=100, blank=True,null=True)

    tactical_2_function=models.CharField(max_length=100, blank=True,null=True)
    tactical_2_freq=models.CharField(max_length=100, blank=True,null=True)
    tactical_2_comments=models.CharField(max_length=100, blank=True,null=True)

    tactical_3_function=models.CharField(max_length=100, blank=True,null=True)
    tactical_3_freq=models.CharField(max_length=100, blank=True,null=True)
    tactical_3_comments=models.CharField(max_length=100, blank=True,null=True)

    tactical_4_function=models.CharField(max_length=100, blank=True,null=True)
    tactical_4_freq=models.CharField(max_length=100, blank=True,null=True)
    tactical_4_comments=models.CharField(max_length=100, blank=True,null=True)

    note_safety_message=models.TextField( blank=True,null=True)
    prepared_by=models.CharField(max_length=100, blank=True,null=True)
    briefed_by=models.CharField(max_length=100, blank=True,null=True)
    time_out=models.CharField(max_length=100, blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return self.resourcetype


class ClueMedia(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True,null=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True,null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True,null=True)
    photo = models.ImageField(upload_to='uploads/', default='No-img.png', blank=True,null=True)
    description = models.CharField(max_length=100, blank=True,null=True)


    def __str__(self):
        return str(self.id)

class ExperimentDataStorage(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    details = models.TextField( blank=True,null=True)

    def __str__(self):
        return str(self.id)


class QuestionnaireModel(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True)
    taskid=models.CharField(max_length=100, blank=True, null=True)
    sceneid=models.CharField(max_length=100, blank=True, null=True)
    trust=models.IntegerField(blank=True,null=True)
    transparency=models.IntegerField(blank=True,null=True)
    workload=models.IntegerField(blank=True,null=True)

    trans1=models.IntegerField(blank=True,null=True)
    trans2=models.IntegerField(blank=True,null=True)
    trans3=models.IntegerField(blank=True,null=True)
    trans4=models.IntegerField(blank=True,null=True)
    trans5=models.IntegerField(blank=True,null=True)

    trust1=models.IntegerField(blank=True,null=True)
    trust2=models.IntegerField(blank=True,null=True)
    trust3=models.IntegerField(blank=True,null=True)
    trust4=models.IntegerField(blank=True,null=True)
    trust5=models.IntegerField(blank=True,null=True)

    NASATLX1_mental=models.IntegerField(blank=True,null=True)
    NASATLX2_physical=models.IntegerField(blank=True,null=True)
    NASATLX3_temporal=models.IntegerField(blank=True,null=True)
    NASATLX4_performance=models.IntegerField(blank=True,null=True)
    NASATLX5_effort=models.IntegerField(blank=True,null=True)
    NASATLX6_frustration=models.IntegerField(blank=True,null=True)

    q1=models.IntegerField(blank=True,null=True)
    q2=models.IntegerField(blank=True,null=True)
    q3=models.IntegerField(blank=True,null=True)
    q4=models.IntegerField(blank=True,null=True)

    q5=models.IntegerField(blank=True,null=True)
    q6=models.IntegerField(blank=True,null=True)
    q7=models.IntegerField(blank=True,null=True)
    q8=models.IntegerField(blank=True,null=True)

    q9=models.IntegerField(blank=True,null=True)
    q10=models.IntegerField(blank=True,null=True)
    q11=models.IntegerField(blank=True,null=True)
    q12=models.IntegerField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return str(self.id)

class WebapplicationModel(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True)

    q1=models.IntegerField(blank=True,null=True)
    q2=models.IntegerField(blank=True,null=True)
    q3=models.IntegerField(blank=True,null=True)

    q4=models.IntegerField(blank=True,null=True)
    q5=models.IntegerField(blank=True,null=True)
    q6=models.IntegerField(blank=True,null=True)
    q7=models.IntegerField(blank=True,null=True)
    q8=models.IntegerField(blank=True,null=True)

    q9=models.IntegerField(blank=True,null=True)
    q10=models.IntegerField(blank=True,null=True)
    q11=models.IntegerField(blank=True,null=True)
    q12=models.IntegerField(blank=True,null=True)
    q13=models.IntegerField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return str(self.id)

class ParticipantStatusModel(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True) # a unix time
    participantindex=models.IntegerField(blank=True, null=True) # a number between 1-122
    participantname=models.CharField(max_length=100, blank=True, null=True)

    status=models.BooleanField(default=False) # participant id has finished the whole task
    taskstatus=models.TextField( blank=True,null=True) # json text {'task1':{'status':0,'experimentsetup':54,'duration':0},}

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    #updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return str(self.id)


class DemographicsModel(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True) # a unix time
    participantindex=models.IntegerField(blank=True, null=True)

    age=models.IntegerField(blank=True,null=True)
    gender=models.IntegerField(blank=True,null=True)
    education=models.IntegerField(blank=True,null=True)
    sart=models.IntegerField(blank=True,null=True)

    q1=models.IntegerField(blank=True,null=True)
    q2=models.CharField(max_length=100, blank=True, null=True)
    q3=models.CharField(max_length=100, blank=True, null=True)
    q4=models.TextField( blank=True,null=True)
    q5=models.TextField( blank=True,null=True)

    q6=models.TextField( blank=True,null=True)
    q7=models.TextField( blank=True,null=True)
    q8=models.TextField( blank=True,null=True)
    q9=models.TextField( blank=True,null=True)
    q10=models.TextField( blank=True,null=True)


    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return str(self.id)


class PostExpSurveyModel(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True) # a unix time

    q1=models.TextField(blank=True,null=True)
    q2=models.TextField(blank=True, null=True)
    q3=models.TextField(blank=True, null=True)
    q4=models.TextField( blank=True,null=True)
    q5=models.TextField( blank=True,null=True)

    q6=models.TextField( blank=True,null=True)
    q7=models.TextField( blank=True,null=True)
    q8=models.TextField( blank=True,null=True)
    q9=models.TextField( blank=True,null=True)
    q10=models.TextField( blank=True,null=True)

    q11=models.TextField( blank=True,null=True)
    q12=models.TextField( blank=True,null=True)
    q13=models.TextField( blank=True,null=True)
    q14=models.TextField( blank=True,null=True)
    q15=models.TextField( blank=True,null=True)

    q16=models.TextField( blank=True,null=True)
    q17=models.TextField( blank=True,null=True)
    q18=models.TextField( blank=True,null=True)
    q19=models.TextField( blank=True,null=True)
    q20=models.TextField( blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return str(self.id)

class DemographicsModel3D(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True) # a unix time
    participantindex=models.IntegerField(blank=True, null=True)

    age=models.IntegerField(blank=True,null=True)
    gender=models.IntegerField(blank=True,null=True)
    education=models.IntegerField(blank=True,null=True)
    sart=models.IntegerField(blank=True,null=True)

    q1=models.IntegerField(blank=True,null=True)
    q2=models.CharField(max_length=100, blank=True, null=True)
    q3=models.CharField(max_length=100, blank=True, null=True)
    q4=models.TextField( blank=True,null=True)
    q5=models.TextField( blank=True,null=True)

    q6=models.TextField( blank=True,null=True)
    q7=models.TextField( blank=True,null=True)
    q8=models.TextField( blank=True,null=True)
    q9=models.TextField( blank=True,null=True)
    q10=models.TextField( blank=True,null=True)


    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return str(self.id)

class QuestionnaireModel3D(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True)
    taskid=models.CharField(max_length=100, blank=True, null=True)
    sceneid=models.CharField(max_length=100, blank=True, null=True)

    trust1=models.IntegerField(blank=True,null=True)
    trust2=models.IntegerField(blank=True,null=True)
    trust3=models.IntegerField(blank=True,null=True)
    trust4=models.IntegerField(blank=True,null=True)
    trust5=models.IntegerField(blank=True,null=True)
    trust6=models.IntegerField(blank=True,null=True)
    trust7=models.IntegerField(blank=True,null=True)

    trans1=models.IntegerField(blank=True,null=True)
    trans2=models.IntegerField(blank=True,null=True)
    trans3=models.IntegerField(blank=True,null=True)
    trans4=models.IntegerField(blank=True,null=True)
    trans5=models.IntegerField(blank=True,null=True)
    trans6=models.IntegerField(blank=True,null=True)
    trans7=models.IntegerField(blank=True,null=True)

    workload=models.IntegerField(blank=True,null=True)

    NASATLX1_mental=models.IntegerField(blank=True,null=True)
    NASATLX2_physical=models.IntegerField(blank=True,null=True)
    NASATLX3_temporal=models.IntegerField(blank=True,null=True)
    NASATLX4_performance=models.IntegerField(blank=True,null=True)
    NASATLX5_effort=models.IntegerField(blank=True,null=True)
    NASATLX6_frustration=models.IntegerField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return str(self.id)

class PostExpSurveyModel3D(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True) # a unix time

    q1=models.TextField(blank=True,null=True)
    q2=models.TextField(blank=True, null=True)
    q3=models.TextField(blank=True, null=True)
    q4=models.TextField(blank=True,null=True)
    q5=models.TextField(blank=True,null=True)
    q6=models.TextField(blank=True,null=True)
    q7=models.TextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    #updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return str(self.id)

class PostTrainingModel3D(models.Model):
    id = models.AutoField(primary_key=True)
    participantid=models.CharField(max_length=100, blank=True, null=True)
    taskid=models.CharField(max_length=100, blank=True, null=True)
    sceneid=models.CharField(max_length=100, blank=True, null=True)

    trust1=models.IntegerField(blank=True,null=True)
    trust2=models.IntegerField(blank=True,null=True)
    trust3=models.IntegerField(blank=True,null=True)
    trust4=models.IntegerField(blank=True,null=True)
    trust5=models.IntegerField(blank=True,null=True)
    trust6=models.IntegerField(blank=True,null=True)
    trust7=models.IntegerField(blank=True,null=True)

    trans1=models.IntegerField(blank=True,null=True)
    trans2=models.IntegerField(blank=True,null=True)
    trans3=models.IntegerField(blank=True,null=True)
    trans4=models.IntegerField(blank=True,null=True)
    trans5=models.IntegerField(blank=True,null=True)
    trans6=models.IntegerField(blank=True,null=True)
    trans7=models.IntegerField(blank=True,null=True)

    workload=models.IntegerField(blank=True,null=True)

    NASATLX1_mental=models.IntegerField(blank=True,null=True)
    NASATLX2_physical=models.IntegerField(blank=True,null=True)
    NASATLX3_temporal=models.IntegerField(blank=True,null=True)
    NASATLX4_performance=models.IntegerField(blank=True,null=True)
    NASATLX5_effort=models.IntegerField(blank=True,null=True)
    NASATLX6_frustration=models.IntegerField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return str(self.id)

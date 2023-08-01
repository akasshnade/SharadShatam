
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .managers import CustomUserManager
from datetime import datetime, date
from django.conf import settings
# import signals
# from month.models import MonthField
# from django.db import models

from django.contrib.auth.models import Group

class MyModel(models.Model):
    field = models.ForeignKey(Group,on_delete=models.CASCADE,null=True,blank=True)

# Create your models here.
class district(models.Model):

    districtName = models.CharField(max_length=300,blank=True,null=True)
    def __unicode__(self):
        return self.id

class taluka(models.Model):

    talukaName = models.CharField(max_length=300,blank=True,null=True)

    dist = models.ForeignKey(district,related_name="dist",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id

class districtHospital(models.Model):

    hospitalName = models.CharField(max_length=300,blank=True,null=True)
    category = models.CharField(max_length=700,blank=True,null=True)
    concernedPerson = models.ForeignKey('CustomUser',related_name="districtHospital_concernedPerson",on_delete=models.CASCADE,null=True,blank=True)
    hospitaldistrict = models.ForeignKey(district,related_name="hospitaldistrict",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id

class primaryHealthCenter(models.Model):

    phcName = models.CharField(max_length=300,blank=True,null=True)

    taluka = models.ForeignKey(taluka,related_name="taluka",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id


class subCenter(models.Model):

    scName = models.CharField(max_length=300,blank=True,null=True)

    Phc = models.ForeignKey(primaryHealthCenter,related_name="Phc",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id

class village(models.Model):

    villageName = models.CharField(max_length=300,blank=True,null=True)

    Sc = models.ForeignKey(subCenter,related_name="Sc",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id


class municipalCorporation(models.Model):

    mcName = models.CharField(max_length=300,blank=True,null=True)

    dist = models.ForeignKey(district,related_name="mcdist",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id


class mcWard(models.Model):

    ward = models.CharField(max_length=100,blank=True,null=True)

    mcrop= models.ForeignKey(municipalCorporation,related_name="mcrop",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id



class municipalCouncil(models.Model):

    councilName = models.CharField(max_length=300,blank=True,null=True)

    dist = models.ForeignKey(district,related_name="councildist",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id


class cantonmentBoard(models.Model):

    canttName = models.CharField(max_length=300,blank=True,null=True)

    dist = models.ForeignKey(district,related_name="canttdist",on_delete=models.CASCADE,null=True,blank=True)
    def __unicode__(self):
        return self.id

# Create your models here.
class CustomUser(AbstractUser):


    unique_id = models.CharField(max_length=200,blank=True,null=True) 
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.CharField(max_length=200,blank=True,null=True)
    username = models.CharField(max_length=200,blank=True,null=True,unique=True)
    idProof = models.CharField(max_length=100,blank=True,null=True)
    idProofno = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=20,blank=True)
    confirm_password = models.CharField(max_length=50)
    doctorSpeciality = models.CharField(max_length=200,default="")
    hospitalName = models.CharField(max_length=500,default="")
    district = models.CharField(max_length=100,blank=True,null=True)
    region_type = models.CharField(max_length=50,blank=True,null=True)
    municipal_corporation = models.CharField(max_length=100,default="",blank=True,null=True)
    ward = models.CharField(max_length=200,default="",blank=True,null=True)
    municipal_council = models.CharField(max_length=100,default="",blank=True,null=True)
    taluka = models.CharField(max_length=100,default="",blank=True,null=True)
    phc = models.CharField(max_length=100,default="",blank=True,null=True)
    pathlab = models.ForeignKey('CustomUser',related_name='CustomUserpathlab',on_delete=models.CASCADE,blank=True,null=True)
    masterSupervisor = models.ForeignKey('CustomUser',related_name='supervisor',on_delete=models.CASCADE,blank=True,null=True)
    # Surveyour_Dob = models.DateTimeField(blank=True,null=True)

    signup_date = models.DateTimeField(auto_now_add=True)
    login_date_time = models.DateTimeField(blank=True,null=True)
    otp = models.CharField(max_length=6,blank=True,null=True)
    otp_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    expirey_date = models.DateTimeField(blank=True,null=True)
    otp_attempts = models.CharField(max_length=6,blank=True,null=True)
    is_delete = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __unicode__(self):
        return self.id

class SurveyourAddress(models.Model):
    district = models.CharField(max_length=100,blank=True,null=True)
    region_type = models.CharField(max_length=50,blank=True,null=True)
    municipal_corporation = models.CharField(max_length=100,default="",blank=True,null=True)
    ward = models.CharField(max_length=200,default="",blank=True,null=True)
    municipal_council = models.CharField(max_length=100,default="",blank=True,null=True)
    taluka = models.CharField(max_length=100,default="",blank=True,null=True)
    phc = models.CharField(max_length=100,default="",blank=True,null=True)
    addressOfSurveyor = models.ForeignKey('CustomUser',related_name='SurveyourAddress_surveyor',on_delete=models.CASCADE,blank=True,null=True)

class sendRegisterOtp(models.Model):
    phone = models.CharField(max_length=20,blank=True)
    otp = models.CharField(max_length=6,blank=True,null=True)
    otp_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    expirey_date = models.DateTimeField(blank=True,null=True)

    def __unicode__(self):
        return self.id

class Doctor(models.Model):
    doctor_name = models.CharField(max_length=900,blank=True,null=True)
    is_active = models.BooleanField(default=False)
    doctor_cred = models.ForeignKey(CustomUser,related_name="doctor_cred",on_delete=models.CASCADE,null=True,blank=True)


    def __unicode__(self):
        return self.id


class pathlogy(models.Model):
    labName = models.CharField(max_length=200,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    pathOwner = models.ForeignKey(CustomUser,related_name="pathOwner",on_delete=models.CASCADE,null=True,blank=True)
    district = models.CharField(max_length=100,blank=True,null=True)
    region_type = models.CharField(max_length=50,blank=True,null=True)
    municipal_corporation = models.CharField(max_length=100,blank=True,null=True)
    ward = models.CharField(max_length=200,blank=True,null=True)
    municipal_council = models.CharField(max_length=100,blank=True,null=True)
    taluka = models.CharField(max_length=100,blank=True,null=True)
    phc = models.CharField(max_length=100,blank=True,null=True)
    sc = models.CharField(max_length=100,blank=True,null=True)
    village = models.CharField(max_length=100,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.id

class Phlebotomist(models.Model):
    pathlab = models.ForeignKey('pathlogy',related_name="Phlebotomistpathlab",on_delete=models.CASCADE,null=True,blank=True)
    phlebotomist_info = models.ForeignKey('CustomUser',related_name="Phlebotomist_phlebotomist_info",on_delete=models.CASCADE,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    surveyour = models.ForeignKey('CustomUser',related_name="Phlebotomist_surveyour",on_delete=models.CASCADE,null=True,blank=True)
    is_occupied = models.BooleanField(default=False)
    occupied_datetime = models.DateTimeField(blank=True,null=True)

class AddressDetails(models.Model):

    district = models.CharField(max_length=100,blank=True,null=True)
    region_type = models.CharField(max_length=50,blank=True,null=True)
    municipal_corporation = models.CharField(max_length=100,blank=True,null=True)
    ward = models.CharField(max_length=200,blank=True,null=True)
    municipal_council = models.CharField(max_length=100,blank=True,null=True)
    taluka = models.CharField(max_length=100,blank=True,null=True)
    phc = models.CharField(max_length=100,blank=True,null=True)
    sc = models.CharField(max_length=100,blank=True,null=True)
    village = models.CharField(max_length=100,blank=True,null=True)
    other_place = models.CharField(max_length=200,blank=True,null=True)
    address1 = models.CharField(max_length=250,blank=True,null=True)
    address2 = models.CharField(max_length=250,blank=True,null=True)
    pincode = models.CharField(max_length=100,blank=True,null=True)
    total_family_count = models.IntegerField(default=0)
    selfBookAppoinment  = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)

    surveyor = models.ForeignKey(CustomUser,related_name="surveyor",on_delete=models.CASCADE,null=True,blank=True)

    def __unicode__(self):
        return self.id

# class FamilyDetails(models.Model):
#     Address = models.ForeignKey(AddressDetails,related_name="Address",on_delete=models.CASCADE,null=True,blank=True)
#     unique_family_key = models.CharField(max_length=150,blank=True,null=True)
#     family_head_name = models.CharField(max_length=500,blank=True,null=True)
#     family_head_mobile = models.CharField(max_length=20,blank=True,null=True)
#     total_family_members = models.IntegerField(default=0)
#     total_senior_citizen = models.IntegerField(default=0)
#     FamilyCompleted  = models.BooleanField(default=False)
#     selfBookAppointment  = models.BooleanField(default=False)
#     created_datetime = models.DateTimeField(auto_now_add=True)


#     def __unicode__(self):
#         return self.id

class familyHeadDetails(models.Model):

    familyAddress = models.ForeignKey(AddressDetails,related_name="familyAddress",on_delete=models.CASCADE,null=True,blank=True)
    unique_family_key = models.CharField(max_length=150,blank=True,null=True)
    family_head_name = models.CharField(max_length=500,blank=True,null=True)
    family_head_mobile = models.CharField(max_length=20,blank=True,null=True)
    total_family_members = models.IntegerField(default=0)
    total_senior_citizen = models.IntegerField(default=0)
    FamilyCompleted  = models.BooleanField(default=False)
    selfBookAppointment  = models.BooleanField(default=False)
    surveyCompleted  = models.BooleanField(default=False)
    labsampleTaken  = models.BooleanField(default=False)

    created_datetime = models.DateTimeField(auto_now_add=True)
    surveyDoneBy = models.ForeignKey(CustomUser,related_name="surveyDoneBy",on_delete=models.CASCADE,null=True,blank=True)


    def __unicode__(self):
        return self.id


SmokeOrGhutkaScore = (
        (0,'Never'),
        (1,'Used to consume in past/ sometimes now'),
        (2,'Daily')

    )
AlcoholScore = (
        (0,'No'),
        (1,'Sometimes'),
        (2,'Addicted')
    )
WaistScore = (
        ('Female',
            (
                (0,'80 cm or less'),
                (1,'81 - 90 cm'),
                (2,'More Than 90')
            )
        ),
        ('Male',
            (
                (0,'90 cm or less'),
                (1,'90 -100 cm'),
                (2,'More Than 100')
            )
        )
    )

#Need To Check By Madhuri
DailyMovements = (
        (0,'Can move normally'),
        (1,'Difficulty or obstruction during normal movement (need help to move ,with the help of external equipment e.g. stick, walker, crutch etc.)'),
        (2,'Bed Ridden')
    )       
IsDisease = (
        (0,'No'),
        (2,'Yes')
    )                           
           
TakeCareScore = (
        (1,'No'),
        (0,'Yes')
    )                


class familyMembers(models.Model):
    # family_head_id = models.CharField(max_length=50,blank=True,null=True)
    isClaimed = models.BooleanField(default=False)
    claimedBy = models.ForeignKey(CustomUser,related_name="familyMembers_claimedBy",on_delete=models.CASCADE,null=True,blank=True)
    member_unique_id = models.CharField(max_length=50,blank=True,null=True)

    member_name = models.CharField(max_length=900,blank=True,null=True)
    member_gender = models.CharField(max_length=10,blank=True,null=True)
    member_dob  = models.DateField(blank=True,null=True)
    member_age  = models.IntegerField(default=0)
    idProof = models.CharField(max_length=100,blank=True,null=True)
    idProofno = models.CharField(max_length=200,blank=True,null=True)
    state_health_insurance = models.BooleanField(default=False)
    self_mobile = models.BooleanField(default=True)
    mobile_relation = models.CharField(max_length=20,blank=True,null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)

    visualDisorder = models.BooleanField(default=False)
    physicalDisability = models.BooleanField(default=False)
    bedRidden_due_ailment = models.BooleanField(default=False)
    dependent_on_people = models.BooleanField(default=False)

    pulse = models.CharField(max_length=10,blank=True,null=True)
    blood_pressure = models.CharField(max_length=10,blank=True,null=True)
    respiratory_rate = models.CharField(max_length=10,blank=True,null=True)
    spo2_level = models.CharField(max_length=10,blank=True,null=True)
    weight = models.CharField(max_length=10,blank=True,null=True)
    height = models.CharField(max_length=10,blank=True,null=True)
    bmi = models.CharField(max_length=10,blank=True,null=True)
        
    above60 = models.IntegerField(default=4)
    consume_smoking_gutka_or_khaini = models.IntegerField(choices=SmokeOrGhutkaScore,default=0)
    consume_alcohol_daily = models.IntegerField(choices=AlcoholScore,default=0)
    smoke_score = models.IntegerField(choices=SmokeOrGhutkaScore,default=0)

    waist_measurement =  models.IntegerField(blank=True,null=True,choices=WaistScore,default=0)
    ability_to_perform_daily_movements = models.IntegerField(blank=True,null=True,choices=DailyMovements,default=0)

    isdisease = models.IntegerField(default=0,choices=IsDisease)
    disease = models.CharField(max_length=500,blank=True,null=True)
    anyone_to_takecare = models.IntegerField(default=0,choices=TakeCareScore)
    totalscore = models.IntegerField(default=0)
    shortness_of_breath = models.BooleanField(default=False)
    chest_pain =models.BooleanField(default=False)
    suspected_heart_disease =models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    dizziness = models.BooleanField(default=False)
    chest_throbbling = models.BooleanField(default=False)
    suspected_high_blood_pressure = models.BooleanField(default=False)
    coughing_more_than_two_weeks = models.BooleanField(default=False)
    blood_in_sputum = models.BooleanField(default=False)
    fever_for_more_than_two_weeks = models.BooleanField(default=False)
    loss_of_weight = models.BooleanField(default=False)
    night_sweats = models.BooleanField(default=False)
    suspected_tuberculosis = models.BooleanField(default=False)
    familyHistory_tuberculosis = models.BooleanField(default=False)
    currently_taking_anti_tb_drugs = models.BooleanField(default=False)

    wounds_or_ulcers_in_mouth_more_than_two_weeks = models.BooleanField(default=False)
    mouth_sores_or_lumps = models.BooleanField(default=False)
    white_or_red_patches_in_mouth = models.BooleanField(default=False)
    pain_while_chewing_food = models.BooleanField(default=False)
    difficulty_in_mouth_opening = models.BooleanField(default=False)
    suspected_mouth_cancer = models.BooleanField(default=False)

    frequently_difficulties_in_breathing = models.BooleanField(default=False)
    dry_cough_many_days = models.BooleanField(default=False)
    tired_or_exhaust = models.BooleanField(default=False)
    spitting_out_thick_cough = models.BooleanField(default=False)
    suspected_copd = models.BooleanField(default=False)

    slow_urination = models.BooleanField(default=False)
    reduced_urination = models.BooleanField(default=False)
    suspected_prostate_gland_disease = models.BooleanField(default=False)

    frequent_urination = models.BooleanField(default=False)
    irritation_while_urination = models.BooleanField(default=False)
    suspected_diabetes = models.BooleanField(default=False)
    suspected_urinary_tract_infection_inflammation = models.BooleanField(default=False)

    decreased_urination = models.BooleanField(default=False)
    feeling_tired = models.BooleanField(default=False)
    appetite_loss = models.BooleanField(default=False)
    limbs_swelling = models.BooleanField(default=False)
    heel_or_foot_swelling = models.BooleanField(default=False)
    feeling_nauseas = models.BooleanField(default=False)
    suspected_kidney = models.BooleanField(default=False)

    urinate_unknowningly = models.BooleanField(default=False)
    suspected_imbalanced_kidney_function = models.BooleanField(default=False)

    frequent_hunger_thirst = models.BooleanField(default=False)
    weight_loss = models.BooleanField(default=False)
    no_wound_healing = models.BooleanField(default=False)
    tingling_in_hands_and_feet = models.BooleanField(default=False)

    history_of_fits = models.BooleanField(default=False)
    suspected_brain_disease = models.BooleanField(default=False)
    suspected_fits = models.BooleanField(default=False)

    sudden_balance_loss_while_walking = models.BooleanField(default=False)
    trembling_feeling = models.BooleanField(default=False)
    things_falling_or_sleeping_out_of_hands = models.BooleanField(default=False)
    suspected_neurological_disorder = models.BooleanField(default=False)
    suspected_parkinson_disease = models.BooleanField(default=False)

    not_closing_of_eyelids_completely = models.BooleanField(default=False)
    feeling_weak_one_side = models.BooleanField(default=False)
    legs_weakness_difficult_walk = models.BooleanField(default=False)
    difficulty_swallowing = models.BooleanField(default=False)
    disability = models.BooleanField(default=False)
    suspected_heart_attack = models.BooleanField(default=False)
    suspected_paralysis = models.BooleanField(default=False)

    blurred_vision_and_reading_difficulty = models.BooleanField(default=False)
    suspected_blindness_or_cataracts = models.BooleanField(default=False)

    non_reducing_eye_pain_more_than_week = models.BooleanField(default=False)
    redness_in_eyes = models.BooleanField(default=False)
    suspected_glaucoma = models.BooleanField(default=False)

    splits_on_mouth_edges = models.BooleanField(default=False)
    tongue_redness = models.BooleanField(default=False)
    mouth_ulcers = models.BooleanField(default=False)
    fatigue_easily = models.BooleanField(default=False)
    suspected_anaemia = models.BooleanField(default=False)
    suspected_malnutrition = models.BooleanField(default=False)
    suspected_vitamins_deficiency = models.BooleanField(default=False)

    patches_on_skin_and_no_sensation = models.BooleanField(default=False)
    suspected_leprosy = models.BooleanField(default=False)

    unbearable_back_pain = models.BooleanField(default=False)
    frequent_fractures = models.BooleanField(default=False)
    joint_pain_at_night = models.BooleanField(default=False)
    pain_when_bones_pressed = models.BooleanField(default=False)
    suspected_osteoporosis = models.BooleanField(default=False)

    impairment_of_movement_physical_disabilities_rheumatism = models.BooleanField(default=False)
    bending_of_toes = models.BooleanField(default=False)
    suspected_osteoarthritis = models.BooleanField(default=False)

    change_in_voice = models.BooleanField(default=False)
    hoarse_voice = models.BooleanField(default=False)
    spitting_blood_while_coughing = models.BooleanField(default=False)
    suspected_cancer = models.BooleanField(default=False)

    lumps_on_skin = models.BooleanField(default=False)

    difficulty_in_hearing = models.BooleanField(default=False)
    suspected_ear_deafness = models.BooleanField(default=False)

    blood_in_stool_or_black_stool = models.BooleanField(default=False)
    suspected_internal_bleeding = models.BooleanField(default=False)
    suspected_piles = models.BooleanField(default=False)
    suspected_fissure = models.BooleanField(default=False)
    suspected_fistula = models.BooleanField(default=False)

    recent_fall = models.BooleanField(default=False)
    history_head_injury = models.BooleanField(default=False)
    suspected_injury = models.BooleanField(default=False)

    lump_in_the_breast = models.BooleanField(default=False)
    pain_in_the_breast = models.BooleanField(default=False)
    blood_stained_discharge_from_the_nipple = models.BooleanField(default=False)
    changes_in_skin_breast = models.BooleanField(default=False)
    change_in_shape_or_size_of_breast = models.BooleanField(default=False)
    suspected_breast_cancer = models.BooleanField(default=False)
    suspected_breast_disease = models.BooleanField(default=False)

    odour_discharge_from_vagina = models.BooleanField(default=False)
    irregular_or_accidental_bleeding = models.BooleanField(default=False)
    abdominal_pain = models.BooleanField(default=False)
    difficulty_while_urinating = models.BooleanField(default=False)
    limb_protrusion = models.BooleanField(default=False)
    bleeding_after_intercourse = models.BooleanField(default=False)
    suspected_cervical_cancer = models.BooleanField(default=False)

    forgetting_house_Address_or_family_member_name = models.BooleanField(default=False)
    not_remembering_life_memories = models.BooleanField(default=False)
    not_remembering_faces_individuals = models.BooleanField(default=False)
    suspected_alzheimers = models.BooleanField(default=False)

    lack_of_interest_in_life = models.BooleanField(default=False)
    depression = models.BooleanField(default=False)
    has_lost_contact_with_family = models.BooleanField(default=False)
    frequent_mood_swings = models.BooleanField(default=False)
    too_angry = models.BooleanField(default=False)
    less_sleep_or_more_sleep_night = models.BooleanField(default=False)
    thought_suicide_come_to_mind = models.BooleanField(default=False)
    suspected_depression = models.BooleanField(default=False)

    very_restless_anxious_after_physical_symptoms = models.BooleanField(default=False)
    feeling_daily_activities_cannot_perform = models.BooleanField(default=False)
    negative_attitude = models.BooleanField(default=False)
    unnecessary_pain = models.BooleanField(default=False)
    weakness = models.BooleanField(default=False)
    no_improvements_after_frequent_treatment = models.BooleanField(default=False)
    suspected_somatic_illness = models.BooleanField(default=False)
    disease_count = models.IntegerField(default=0)


    
    family_head = models.ForeignKey(familyHeadDetails,related_name="family_head_member",on_delete=models.CASCADE,null=True,blank=True)

    familysurveyor = models.ForeignKey(CustomUser,related_name="familysurveyor",on_delete=models.CASCADE,null=True,blank=True)
    pathlab = models.ForeignKey(pathlogy,related_name="pathlab",on_delete=models.CASCADE,null=True,blank=True)
    phlebotomist = models.ForeignKey('Phlebotomist',related_name="familymember_phlebotomist_info",on_delete=models.CASCADE,null=True,blank=True)

    LabSampleTaken = models.BooleanField(default=False)

    basicLabTest = models.BooleanField(default=False)
    AdvanceLabTest = models.BooleanField(default=False)
    
    current_isPending = models.BooleanField(default=True)
    current_isMedication = models.BooleanField(default=False)
    current_isSpecialistMedication = models.BooleanField(default=False)
    current_isHospitalisation = models.BooleanField(default=False)
    current_phcConsultation = models.BooleanField(default=False)
    current_specialistConsultation = models.BooleanField(default=False)
    current_isElderline = models.BooleanField(default=False)
    
    distHospital = models.ForeignKey(districtHospital,related_name="hospital",on_delete=models.CASCADE,null=True,blank=True)
    doctorAssigned = models.ForeignKey(CustomUser,related_name="doctorAssigned",on_delete=models.CASCADE,null=True,blank=True)
    isCaseClosed = models.BooleanField(default=False)
    caseClosedBy = models.ForeignKey(CustomUser,related_name="familyMemberCaseClosedBy",on_delete=models.CASCADE,null=True,blank=True)
    caseClosedReason = models.TextField(null=True,blank=True)
    caseClosedDate = models.DateTimeField(null=True,blank=True)
    # ClaimedBy = models.ForeignKey(CustomUser,related_name="Claimed",on_delete=models.CASCADE,null=True,blank=True)
    # isClaimed = models.BooleanField(default=False)

    # def __unicode__(self):
    #     return self.id


    # def save(self, *args, **kwargs):
    #     if self.no_improvements_after_frequent_treatment == True or self.unnecessary_pain == True or self.weakness==True or self.shortness_of_breath == True or self.negative_attitude == True or self.feeling_daily_activities_cannot_perform ==True or self.very_restless_anxious_after_physical_symptoms  :
    #         self.suspected_somatic_illness = True 

    #     if self.thought_suicide_come_to_mind == True or self.less_sleep_or_more_sleep_night == True or self.too_angry == True or self.frequent_mood_swings == True or self.has_lost_contact_with_family == True or self.depression == True or self.lack_of_interest_in_life ==True :
    #         self.suspected_depression = True 

    #     if self.not_remembering_life_memories == True or self.not_remembering_faces_individuals == True or self.forgetting_house_Address_or_family_member_name == True:
    #         self.suspected_alzheimers = True

    #     if self.bleeding_after_intercourse == True or self.limb_protrusion == True or self.difficulty_while_urinating == True or self.abdominal_pain == True or self.irregular_or_accidental_bleeding == True or self.odour_discharge_from_vagina == True :
    #         self.suspected_cervical_cancer = True 

    #     if self.lump_in_the_breast == True or self.pain_in_the_breast == True or self.blood_stained_discharge_from_the_nipple == True or self.changes_in_skin_breast == True or self.change_in_shape_or_size_of_breast == True:
    #         self.suspected_breast_cancer = True 
    #         self.suspected_breast_disease = True 

    #     if self.recent_fall == True or self.history_head_injury == True :
    #         self.suspected_injury = True 

    #     if self.blood_in_stool_or_black_stool == True:
    #         self.suspected_internal_bleeding = True 
    #         self.suspected_cancer = True 
    #         self.suspected_piles = True 
    #         self.suspected_fissure = True 
    #         self.suspected_fistula = True 

    #     if self.difficulty_in_hearing == True :
    #         self.suspected_ear_deafness = True 

    #     if self.lumps_on_skin == True :
    #         self.suspected_cancer = True 

    #     if self.spitting_blood_while_coughing == True or self.hoarse_voice == True or self.weight_loss == True or self.appetite_loss == True or self.change_in_voice == True:
    #         self.suspected_cancer = True 

    #     if self.bending_of_toes == True or self.impairment_of_movement_physical_disabilities_rheumatism == True :
    #         self.suspected_osteoarthritis = True 

    #     if self.pain_when_bones_pressed == True or self.joint_pain_at_night == True or self.frequent_fractures == True or self.unbearable_back_pain == True :
    #         self.suspected_osteoporosis = True       

    #     if self.patches_on_skin_and_no_sensation == True :
    #         self.suspected_leprosy = True 

    #     if self.fatigue_easily == True or self.appetite_loss == True or self.mouth_ulcers == True or self.tongue_redness == True or self.splits_on_mouth_edges == True:
    #         self.suspected_anaemia = True 
    #         self.suspected_vitamins_deficiency = True 
    #         self.suspected_malnutrition = True 

    #     if self.redness_in_eyes == True or self.non_reducing_eye_pain_more_than_week == True :
    #         self.suspected_diabetes = True
    #         self.suspected_glaucoma = True 

    #     if self.blurred_vision_and_reading_difficulty == True :
    #         self.suspected_blindness_or_cataracts = True 

    #     if self.disability == True or self.difficulty_swallowing == True or self.legs_weakness_difficult_walk == True or self.feeling_weak_one_side == True or self.not_closing_of_eyelids_completely == True:
    #         self.suspected_heart_attack = True
    #         self.suspected_paralysis = True 

    #     if self.things_falling_or_sleeping_out_of_hands == True or self.trembling_feeling == True or self.sudden_balance_loss_while_walking == True :
    #         self.suspected_neurological_disorder = True 
    #         self.suspected_parkinson_disease = True 

    #     if self.history_of_fits == True :
    #         self.suspected_fits = True 
    #         self.suspected_brain_disease = True 

    #     if self.tingling_in_hands_and_feet == True or self.no_wound_healing == True or self.weight_loss == True or self.frequent_hunger_thirst == True :
    #         self.suspected_diabetes = True 

    #     if self.urinate_unknowningly == True :
    #         self.suspected_imbalanced_kidney_function = True 

    #     if self.feeling_nauseas == True or self.heel_or_foot_swelling == True or self.limbs_swelling == True :
    #         self.suspected_kidney = True  

    #     if self.irritation_while_urination == True or self.frequent_urination == True :
    #         self.suspected_diabetes = True 
    #         self.suspected_urinary_tract_infection_inflammation = True
        
    #     #suspected_heart_disease
    #     if self.shortness_of_breath    == True or self.chest_pain   == True:
    #         self.suspected_heart_disease  = True

    #     #suspected_high_blood_pressure
    #     if self.shortness_of_breath    == True or self.chest_pain   == True:
    #         self.suspected_high_blood_pressure   = True

    #     #suspected_tuberculosis
    #     if self.coughing_more_than_two_weeks  == True or self.blood_in_sputum == True or self.fever_for_more_than_two_weeks == True or self.loss_of_weight  == True or self.night_sweats == True:
    #         self.suspected_tuberculosis   = True
        
    #     #suspected_mouth_cancer  
    #     if self.wounds_or_ulcers_in_mouth_more_than_two_weeks   == True or self.mouth_sores_or_lumps  == True or self.white_or_red_patches_in_mouth      == True or self.pain_while_chewing_food      == True or self.difficulty_in_mouth_opening      == True:
    #         self.suspected_mouth_cancer    = True

    #     #suspected_copd
    #     if self.frequently_difficulties_in_breathing    == True or self.dry_cough_many_days   == True or self.tired_or_exhaust  ==True or self.spitting_out_thick_cough   == True :
    #         self.suspected_copd   = True
        
    #     #suspected_prostate_gland_disease
    #     if self.slow_urination == True or self.reduced_urination    == True:
    #         self.suspected_prostate_gland_disease    = True

    def __unicode__(self):
        return self.id

class Notification(models.Model):
    family_head = models.ForeignKey(familyHeadDetails,related_name="Notification_family_head_member",on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True,null=True)
    isRead = models.BooleanField(default=False)
    readby = models.ForeignKey(CustomUser,related_name="Notification_readyby",on_delete=models.CASCADE,null=True,blank=True)
    read_date = models.DateTimeField(auto_now=True)
    isdeleted = models.BooleanField(default=False)
    def __unicode__(self):
        return self.id

# class Doctor(models.Model):
#     doctor_name = models.CharField(max_length=900,blank=True,null=True)
#     is_active = models.BooleanField(default=False)
#     doctor_cred = models.ForeignKey(CustomUser,related_name="doctor_cred",on_delete=models.CASCADE,null=True,blank=True)


#     def __unicode__(self):
#         return self.id


# class pathlogy(models.Model):
#     labName = models.CharField(max_length=200,blank=True,null=True)
#     is_active = models.BooleanField(default=True)
#     pathOwner = models.ForeignKey(CustomUser,related_name="pathOwner",on_delete=models.CASCADE,null=True,blank=True)
#     district = models.CharField(max_length=100,blank=True,null=True)
#     region_type = models.CharField(max_length=50,blank=True,null=True)
#     municipal_corporation = models.CharField(max_length=100,blank=True,null=True)
#     ward = models.CharField(max_length=200,blank=True,null=True)
#     municipal_council = models.CharField(max_length=100,blank=True,null=True)
#     taluka = models.CharField(max_length=100,blank=True,null=True)
#     phc = models.CharField(max_length=100,blank=True,null=True)
#     sc = models.CharField(max_length=100,blank=True,null=True)
#     village = models.CharField(max_length=100,blank=True,null=True)
#     created_date = models.DateTimeField(auto_now_add=True)

#     def __unicode__(self):
#         return self.id

# class labTest(models.Model):
#     pathlogy = models.ForeignKey(pathlogy,related_name="pathlogy",on_delete=models.CASCADE,null=True,blank=True)
#     testName = models.CharField(max_length=500,blank=True,null=True)
#     is_active = models.BooleanField(default=True)
#     testType = models.CharField(max_length=50,blank=True,null=True)
#     created_date = models.DateTimeField(auto_now_add=True)


#     def __unicode__(self):
#         return self.id

# #Remove Table
# class patientLabTest(models.Model):
    
#     labTest = models.ForeignKey(labTest,related_name="labTest",on_delete=models.CASCADE,null=True,blank=True)
#     patientLabTestDetail = models.ForeignKey(familyMembers,related_name="patientLabTestDetail",on_delete=models.CASCADE,null=True,blank=True)
#     barcode = models.CharField(max_length=50,blank=True,null=True)

#     created_date = models.DateTimeField(auto_now_add=True)
#     isCompleted = models.BooleanField(default=False)


#     def __unicode__(self):
#         return self.id

# #RemoveTable
# class PatientTestBarcode(models.Model):
#     barcode = models.CharField(max_length=50,blank=True,null=True)
#     labTest = models.ForeignKey(patientLabTest,related_name="PatientTestBarcode_labTest",on_delete=models.CASCADE,null=True,blank=True)
#     docpatient = models.ForeignKey('familyMembers',related_name="PatientTestBarcode_docpatient",on_delete=models.CASCADE,null=True,blank=True)
#     created_date = models.DateTimeField(auto_now_add=True) 

# #Remove
# class testReport(models.Model):
#     patientLabTest = models.ForeignKey(patientLabTest,related_name="patientLabTest",on_delete=models.CASCADE,null=True,blank=True)
#     parameterName = models.CharField(max_length=500,blank=True,null=True)
#     parameterValue = models.CharField(max_length=500,blank=True,null=True)
#     labRemarks = models.CharField(max_length=500,blank=True,null=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=500,blank=True,null=True)


#     def __unicode__(self):
#         return self.id


class doctorRemarksPathlab(models.Model):
    remarkreport = models.ForeignKey('PatientTestReport',related_name="remarkreport",on_delete=models.CASCADE,null=True,blank=True)
    remarkdoctor = models.ForeignKey(CustomUser,related_name="remarkdoctor",on_delete=models.CASCADE,null=True,blank=True)
    doctorRemarks = models.CharField(max_length=500,blank=True,null=True)
    respathlogy = models.ForeignKey(pathlogy,related_name="respathlogy",on_delete=models.CASCADE,null=True,blank=True)
    remarkpathlab = models.ForeignKey(CustomUser,related_name="doctorRemarksPathlab_remarkpathlab",on_delete=models.CASCADE,null=True,blank=True)
    pathologyResponse = models.CharField(max_length=500,blank=True,null=True)
    response_date = models.DateTimeField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    isCompleted = models.BooleanField(default=False)


    def __unicode__(self):
        return self.id


class doctorConsultancy(models.Model):
    #patientLabTest to patientTest
    patientLabTestreport = models.ForeignKey('PatientTest',related_name="patientLabTestreport",on_delete=models.CASCADE,null=True,blank=True)
    docpatient = models.ForeignKey(familyMembers,related_name="doctorConsultancy",on_delete=models.CASCADE,null=True,blank=True)
    assignedDoctor = models.ForeignKey(CustomUser,related_name="assignedDoctor",on_delete=models.CASCADE,null=True,blank=True)
    assignedDistrictHospital = models.ForeignKey(districtHospital,related_name="doctorConsultancy_assignedDistrictHospital",on_delete=models.CASCADE,null=True,blank=True)
    doctor_name = models.CharField(max_length=500,blank=True,null=True) 
    specialization = models.CharField(max_length=500,blank=True,null=True)
    isPending = models.BooleanField(default=True)
    isMedication = models.BooleanField(default=False)
    isSpecialistMedication = models.BooleanField(default=False)
    isHospitalisation = models.BooleanField(default=False)
    phcConsultation = models.BooleanField(default=False)
    specialistConsultation = models.BooleanField(default=False)
    isElderline = models.BooleanField(default=False)
  
    DoctorassignedBy = models.ForeignKey(CustomUser,related_name="DoctorassignedBy",on_delete=models.CASCADE,null=True,blank=True)
    DoctorassignedDate = models.DateTimeField(blank=True,null=True)
    suggestion_type = models.CharField(max_length=500,blank=True,null=True)

    doctorRemarks = models.CharField(max_length=500,blank=True,null=True)
    fileUpload = models.FileField(upload_to='doctorFolder',blank=True)
    appointDate = models.DateField(blank=True,null=True)
    appointTime = models.TimeField(blank=True,null=True)


    created_date = models.DateTimeField(auto_now_add=True)
    isCompleted = models.BooleanField(default=False)


    def __unicode__(self):
        return self.id

class phcConsultancy(models.Model):
    #patientLabTest to patientTest
    patientLabTestreport = models.ForeignKey('PatientTest',related_name="phcPatientLabTestreport",on_delete=models.CASCADE,null=True,blank=True)
    docpatient = models.ForeignKey(familyMembers,related_name="phcDoctorConsultancy",on_delete=models.CASCADE,null=True,blank=True)
    phcDoctor = models.ForeignKey(CustomUser,related_name="phcConsultancyPhcDoctor",on_delete=models.CASCADE,null=True,blank=True)
    isPending = models.BooleanField(default=True)
    isMedication = models.BooleanField(default=False)
    isHospitalisation = models.BooleanField(default=False)
    phcConsultation = models.BooleanField(default=False)
    isElderline = models.BooleanField(default=False)
  
    suggestion_type = models.CharField(max_length=500,blank=True,null=True)
    medicationDate = models.DateTimeField(blank=True,null=True)
    phcConsultationDate = models.DateTimeField(blank=True,null=True)
    hospitalisationDate = models.DateTimeField(blank=True,null=True)
    elderlineDate = models.DateTimeField(blank=True,null=True)

    medicationClosedDate = models.DateTimeField(blank=True,null=True)
    phcConsultationClosedDate = models.DateTimeField(blank=True,null=True)
    hospitalisationClosedDate = models.DateTimeField(blank=True,null=True)
    elderlineClosedDate = models.DateTimeField(blank=True,null=True)

    medicationRemarks = models.CharField(max_length=500,blank=True,null=True)
    hospitalizationRemarks = models.CharField(max_length=500,blank=True,null=True)
    consultationphcRemarks = models.CharField(max_length=500,blank=True,null=True)
    elderlineRemarks = models.CharField(max_length=500,blank=True,null=True)

    # phcRemarks = models.CharField(max_length=500,blank=True,null=True)
    fileUpload = models.FileField(upload_to='doctorFolder',blank=True)
    consultationFileUpload = models.FileField(upload_to='doctorFolder',blank=True)
    appointDate = models.DateField(blank=True,null=True)
    appointTime = models.TimeField(blank=True,null=True)

    isCaseClosed = models.BooleanField(default=False)
    caseClosedDate = models.DateTimeField(blank=True,null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    # isCompleted = models.BooleanField(default=False)


    def __unicode__(self):
        return self.id

class specialistConsultancy(models.Model):
    #patientLabTest to patientTest
    specialist_patientLabTestreport = models.ForeignKey('PatientTest',related_name="specialistPatientLabTestreport",on_delete=models.CASCADE,null=True,blank=True)
    specialist_docpatient = models.ForeignKey(familyMembers,related_name="specialistDoctorConsultancy",on_delete=models.CASCADE,null=True,blank=True)
    specialistDoctor = models.ForeignKey(CustomUser,related_name="specialistConsultancySpecialistDoctor",on_delete=models.CASCADE,null=True,blank=True)
    specialist_isPending = models.BooleanField(default=True)
    specialist_isMedication = models.BooleanField(default=False)
    specialist_isHospitalisation = models.BooleanField(default=False)
    specialist_Consultation = models.BooleanField(default=False)
    specialist_isElderline = models.BooleanField(default=False)
  
    specialist_suggestion_type = models.CharField(max_length=500,blank=True,null=True)
    # specialist_medicationDate = models.DateTimeField(blank=True,null=True)
    specialist_ConsultationDate = models.DateTimeField(blank=True,null=True)
    # specialist_hospitalisationDate = models.DateTimeField(blank=True,null=True)
    # specialist_elderlineDate = models.DateTimeField(blank=True,null=True)

    suggestion_type = models.CharField(max_length=500,blank=True,null=True)
    specialist_medicationDate = models.DateTimeField(blank=True,null=True)
    specialist_phcConsultationDate = models.DateTimeField(blank=True,null=True)
    specialist_hospitalisationDate = models.DateTimeField(blank=True,null=True)
    specialist_elderlineDate = models.DateTimeField(blank=True,null=True)

    specialist_medicationClosedDate = models.DateTimeField(blank=True,null=True)
    specialist_phcConsultationClosedDate = models.DateTimeField(blank=True,null=True)
    specialist_hospitalisationClosedDate = models.DateTimeField(blank=True,null=True)
    specialist_elderlineClosedDate = models.DateTimeField(blank=True,null=True)

    specialist_medicationRemarks = models.CharField(max_length=500,blank=True,null=True)
    specialist_hospitalizationRemarks = models.CharField(max_length=500,blank=True,null=True)
    specialist_consultationphcRemarks = models.CharField(max_length=500,blank=True,null=True)
    specialist_elderlineRemarks = models.CharField(max_length=500,blank=True,null=True)

    specialist_fileUpload = models.FileField(upload_to='doctorFolder',blank=True)
    specialist_consultationFileUpload = models.FileField(upload_to='doctorFolder',blank=True)
    specialist_appointDate = models.DateField(blank=True,null=True)
    specialist_appointTime = models.TimeField(blank=True,null=True)

    specialist_isCaseClosed = models.BooleanField(default=False)
    specialist_caseClosedDate = models.DateTimeField(blank=True,null=True)
    specialist_created_date = models.DateTimeField(auto_now_add=True)
    specialist_DoctorassignedBy = models.ForeignKey(CustomUser,related_name="specialistDoctorassignedBy",on_delete=models.CASCADE,null=True,blank=True)

    # specialist_isCompleted = models.BooleanField(default=False)


    def __unicode__(self):
        return self.id

class total_district_dashboard(models.Model):


    district = models.CharField(max_length=100,blank=True,null=True)
    no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
    no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
    no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
    no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):
        return self.id


class total_mcrop_dashboard(models.Model):
    district = models.CharField(max_length=100,blank=True,null=True)

    municipal_corporation = models.CharField(max_length=200,blank=True,null=True)
    no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
    no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
    no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
    no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)
    def __unicode__(self):
        return self.id



class total_ward_dashboard(models.Model):
    district = models.CharField(max_length=100,blank=True,null=True)

    municipal_corporation = models.CharField(max_length=200,blank=True,null=True)

    ward = models.CharField(max_length=200,blank=True,null=True)
    no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
    no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
    no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
    no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):

        return self.id



class total_taluka_dashboard(models.Model):
     district = models.CharField(max_length=100,blank=True,null=True)

     taluka = models.CharField(max_length=200,blank=True,null=True)
     no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
     no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
     no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
     no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
     no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
     no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
     no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
     no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)

     def __unicode__(self):
         return self.id


class total_council_dashboard(models.Model):
     district = models.CharField(max_length=100,blank=True,null=True)

     council = models.CharField(max_length=200,blank=True,null=True)
     no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
     no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
     no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
     no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
     no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
     no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
     no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
     no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)
     def __unicode__(self):

         return self.id


class total_phc_dashboard(models.Model):
    district = models.CharField(max_length=100,blank=True,null=True)

    taluka = models.CharField(max_length=200,blank=True,null=True)

    phc_name = models.CharField(max_length=200,blank=True,null=True)
    no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
    no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
    no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
    no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
    no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
    no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):
         return self.id


class total_sc_dashboard(models.Model):
     district = models.CharField(max_length=100,blank=True,null=True)
     taluka = models.CharField(max_length=200,blank=True,null=True)
     phc_name = models.CharField(max_length=200,blank=True,null=True)
     sc_name = models.CharField(max_length=200,blank=True,null=True)
     no_of_seneior_citizen =  models.CharField(max_length=100,blank=True,null=True)
     no_of_test_reported =  models.CharField(max_length=50,blank=True,null=True)
     no_of_test_completed =  models.CharField(max_length=50,blank=True,null=True)
     no_of_test_in_progress =  models.CharField(max_length=50,blank=True,null=True)
     no_of_health_facility =  models.CharField(max_length=50,blank=True,null=True)
     no_of_patients_attended_by_doctor =  models.CharField(max_length=50,blank=True,null=True)
     no_of_empaneled_doctors =  models.CharField(max_length=50,blank=True,null=True)
     no_of_empaneled_labs =  models.CharField(max_length=50,blank=True,null=True)
     def __unicode__(self):
         return self.id


TEST_CHOICE = (
    ('basic','Basic'),
    ('advance','Advance')
    )
class TestRange(models.Model):
    testName = models.CharField(max_length=100,blank=True,null=True)
    test_type = models.CharField(max_length=10,choices=TEST_CHOICE)
    machine_name = models.CharField(max_length=100,blank=True,null=True)
    # male_low_range = models.CharField(max_length=10,blank=True,null=True)
    # male_high_range = models.CharField(max_length=10,blank=True,null=True)
    # female_low_range = models.CharField(max_length=10,blank=True,null=True)
    # female_high_range = models.CharField(max_length=10,blank=True,null=True)
    # comment = models.CharField(max_length=250,blank=True,null=True)
    unit = models.CharField(max_length=10,blank=True,null=True)
    method_name = models.CharField(max_length=50,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

class MaleReference(models.Model):
    test = models.ForeignKey('TestRange',related_name='MaleReference_test',null=True,on_delete=models.CASCADE)
    low_range = models.DecimalField(max_digits = 7,
                         decimal_places = 3,blank=True,null=True)
    high_range = models.DecimalField(max_digits = 7,
                         decimal_places = 3,blank=True,null=True)
    test_range = models.CharField(max_length=10,blank=True,null=True)
    comment = models.CharField(max_length=250,blank=True,null=True)

class FemaleReference(models.Model):
    test = models.ForeignKey('TestRange',related_name='FemaleReference_test',null=True,on_delete=models.CASCADE)
    low_range = models.DecimalField(max_digits = 7,
                         decimal_places = 3,blank=True,null=True)
    high_range = models.DecimalField(max_digits = 7,
                         decimal_places = 3,blank=True,null=True)
    test_range = models.CharField(max_length=10,blank=True,null=True)
    comment = models.CharField(max_length=250,blank=True,null=True)
    
    
class PatientTest(models.Model):
    test = models.ForeignKey('TestRange',related_name='PatientTest_test',null=True,on_delete=models.CASCADE)
    pathlab = models.ForeignKey('pathlogy',related_name="PatientTest_pathlab",on_delete=models.CASCADE,null=True,blank=True)
    patientDetail = models.ForeignKey(familyMembers,related_name="PatientTestDetail",on_delete=models.CASCADE,null=True,blank=True)
    barcode = models.CharField(max_length=50,blank=True,null=True)
    phlebotomist = models.ForeignKey('Phlebotomist',related_name="PatientTest_phlebotomist_info",on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    isCompleted = models.BooleanField(default=False)
    # ReportCompleted = models.BooleanField(default=False)

class PatientTestReport(models.Model):
    patientLabTest = models.ForeignKey(PatientTest,related_name="PatientTestReport_patientLabTest",on_delete=models.CASCADE,null=True,blank=True)
    parameterName = models.CharField(max_length=500,blank=True,null=True)
    parameterValue = models.CharField(max_length=500,blank=True,null=True)
    labRemarks = models.CharField(max_length=500,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=500,blank=True,null=True)

    def __unicode__(self):
        return self.id

class RolePermissions(models.Model):
    authgroup = models.ForeignKey(Group,on_delete=models.CASCADE,null=True,blank=True,related_name="RolePermissions_authgroup")
    moduleName = models.CharField(max_length=500,blank=True,null=True)
    action = models.CharField(max_length=500,blank=True,null=True)
    status = models.BooleanField(default=False)


    def __unicode__(self):
        return self.id
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name','username','phone','signup_date','login_date_time')
class SCUserSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name','unique_id','username','phone','signup_date','login_date_time')

class SupervisorSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name','phone',)
#Surveyour Senior Citizen claimed
class SurveyourCitizenClaimederializer(serializers.Serializer):
    familyMemberId = serializers.IntegerField()
    claimStatus = serializers.BooleanField()

    class Meta:
        fields = ['familyMemberId','claimStatus']
class SurveyourUserSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    masterSupervisor = SupervisorSerializer(many=False)
    # supervisor_name = serializers.CharField(source="masterSupervisor.name")
    # supervisor_phone = serializers.CharField(source="masterSupervisor.phone")

    class Meta:
        model = CustomUser
        fields = ('id', 'name','username','phone','signup_date','login_date_time',"district","region_type","municipal_corporation","ward","municipal_council","taluka","phc","masterSupervisor")

class UpdateSurveyourUserSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # masterSupervisor = SupervisorSerializer(many=False)
    # supervisor_name = serializers.CharField(source="masterSupervisor.name")
    # supervisor_phone = serializers.CharField(source="masterSupervisor.phone")

    class Meta:
        model = CustomUser
        fields = ('id', 'name','username','phone',"district","region_type","municipal_corporation","ward","municipal_council","taluka","phc",)


def passwordGen():
    chars = string.letters
    chars_len = len(chars)
    return str().join(chars[int(ord(c) / 256. * chars_len)] for c in os.urandom(6))

# Register Serializer
class SurveyourRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id', 'phone')
        def validate(self,data):
            phone = validated_data["phone"]
            print(phone,"*********************")
            phone_exists = CustomUser.objects.filter(phone=phone)
            if phone_exists:
                raise serializers.ValidationError({"phone": "Phone Number Already Present."})

            username_exists = CustomUser.objects.filter(phone=phone)
            if username_exists:
                raise serializers.ValidationError({"phone": "Phone Number Already Present."})


            return validated_data




#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(username=validated_data['phone'],phone=validated_data['phone'],password=passwordGen(),confirm_password=passwordGen())
#         return user



# class LoginSerializer(serializers.Serializer):
#     class Meta:
#         model  = CustomUser
#         fields = ('id','phone','password')
#     email = serializers.CharField()
#     password = serializers.CharField()

#     # language_code = serializers.CharField()

#     def validate(self,data):
#         print(data,"****************")
#         customuser = authenticate(**data)
#         if customuser:
#             if customuser.is_active:
#                 if not customuser.is_superuser:
#                     # if customuser.is_verify:
#                     return customuser
#                     # else:
#                     #     return serializers.ValidationError("User is Blocked. Please Contact Admin.")


#                 else:
#                     raise serializers.ValidationError("Only Users are Allowed.")
#             else:
#                 raise serializers.ValidationError("User os Blocked. Please Contact Admin.")
#         else:
#             raise serializers.ValidationError("Incorrect Credentials.")




# class ResendOtpSerializer(serializers.ModelSerializer):
#     # otp_owner = serializers.ReadOnlyField(source='CustomUser.phone')
#     phone = serializers.CharField()
#     class Meta:
#         model = SendOtp
#         fields = ['phone']



class OtpVerifySerializer(serializers.ModelSerializer):
    # otp_owner = serializers.ReadOnlyField(source='CustomUser.phone')
    phone = serializers.CharField()
    # creation_date_time = serializers.DateTimeField()
    class Meta:
        model = CustomUser
        fields = ('phone','otp')


class AllQueryList(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='remarkdoctor.name')
    citizen_id = serializers.CharField(source='remarkreport.patientLabTest.patientDetail.member_unique_id')
    citizen_name = serializers.CharField(source='remarkreport.patientLabTest.patientDetail.member_name')
    class Meta:
        model = doctorRemarksPathlab
        fields = "__all__"



class SetNewPasswordSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        fields = ['new_password','confirm_password']


class SurveyourForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

    class Meta:
        fields = ['phone']


class SurveyourSetNewPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        fields = ['phone','new_password','confirm_password']


class loginSendOtpSerializer(serializers.Serializer):
    phone = serializers.CharField()

    class Meta:
        fields = ['phone']



# class formSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = formDetails
#         # fields = '__all__'
#         fields = ('name','address','phone','email','aadharNumber','panNumber','plotNumber','surveyNumber','subDivision','taluka','district','pincode','latitude','longitude','landArea','sizeOfplot','nearestLandmark','landType','presentUse','OwnerType','otherInfo','sign_image','created_date',)
class DoctorConsultancySerializer(serializers.ModelSerializer):

    class Meta:
        model = doctorConsultancy
        fields = ("patientLabTestreport","docpatient","doctorRemarks")


class AssignNewDoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = doctorConsultancy
        fields = ("patientLabTestreport","docpatient","assignedDoctor","appointDate","appointTime")

class DoctorRemarkPathlab(serializers.ModelSerializer):

    class Meta:
        model = doctorRemarksPathlab
        fields = ("remarkreport","doctorRemarks")

class ResponseRemarkPathlab(serializers.ModelSerializer):

    class Meta:
        model = doctorRemarksPathlab
        fields = ("id","pathologyResponse")

class AllDoctorRemarkPathlabList(serializers.ModelSerializer):

    class Meta:
        model = doctorRemarksPathlab
        fields = "__all__"

class GetTestReportSerializer(serializers.ModelSerializer):
    remarkreport = AllDoctorRemarkPathlabList(many=True)
    class Meta:
        model = PatientTestReport
        fields = '__all__'
        # fields = ["parameterName","parameterValue","status","remarkreport"]


class AddressDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressDetails
        fields = "__all__"


class SelfAddressDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressDetails
        exclude = ("surveyor",)

class familymemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # doctorConsultancy = DoctorConsultancySerializer(many=True)

    class Meta:
        model = familyMembers
        fields = ("member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness")

class familyHeadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields

    family_head = familymemberSerializer(many=True)
    class Meta:
        model = familyHeadDetails
        fields = "__all__"

    def create(self, validated_data):
        familyhead = validated_data.pop('family_head')
        head = familyHeadDetails.objects.create(**validated_data)
        for familyhead in familyhead:
            familyMembers.objects.create(family_head=head, **familyhead)
        return head


        






class doctorConsultancyserializers(serializers.ModelSerializer):
    class Meta:
        model = doctorConsultancy
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = "__all__"


class InsertdoctorConsultancyserializers(serializers.ModelSerializer):
    class Meta:
        model = doctorConsultancy
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = "__all__"

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    # valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension! Please upload files with .pdf, .doc, .docx,.jpg,.png, extension')
from django.core.validators import FileExtensionValidator
class SuggestToCitizenSerializers(serializers.ModelSerializer):
    fileUpload = serializers.FileField(required=False, validators=[validate_file_extension])
    # fileUpload = serializers.FileField(null=True, blank=True, upload_to="doctorFolder",validators=[FileExtensionValidator( ['pdf','.jpg', '.png',] ) ])
    class Meta:
        model = doctorConsultancy
        exclude = ("isPending","isElderline")


    def create(self,validated_data):

        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        # fields = "__all__"

        # field = [""]
        # validated_data
        familyMembers.objects.filter(id = validated_data["docpatient"].id).update(current_isPending=False,current_isMedication=validated_data["isMedication"],current_isHospitalisation=validated_data["isHospitalisation"],current_phcConsultation=validated_data["phcConsultation"],current_specialistConsultation=validated_data["specialistConsultation"])
        return super().create(validated_data)

class PhcSuggestToCitizenSerializers(serializers.ModelSerializer):
    fileUpload = serializers.FileField(required=False, validators=[validate_file_extension])
    consultationFileUpload = serializers.FileField(required=False, validators=[validate_file_extension])
    # fileUpload = serializers.FileField(null=True, blank=True, upload_to="doctorFolder",validators=[FileExtensionValidator( ['pdf','.jpg', '.png',] ) ])
    class Meta:
        model = phcConsultancy
        exclude = ("isPending","isElderline")


    def create(self,validated_data):

        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        # fields = "__all__"

        # field = [""]
        # validated_data
        familyMembers.objects.filter(id = validated_data["docpatient"].id).update(
            current_isPending=False,
            current_isMedication=validated_data["isMedication"],
            current_isHospitalisation=validated_data["isHospitalisation"],
            current_phcConsultation=validated_data["phcConsultation"]
            # current_specialistConsultation=validated_data["specialistConsultation"])
            )
        return super().create(validated_data)

class SpecialistSuggestToCitizenSerializers(serializers.ModelSerializer):
    specialist_fileUpload = serializers.FileField(required=False, validators=[validate_file_extension])
    specialist_consultationFileUpload = serializers.FileField(required=False, validators=[validate_file_extension])
    
    # fileUpload = serializers.FileField(null=True, blank=True, upload_to="doctorFolder",validators=[FileExtensionValidator( ['pdf','.jpg', '.png',] ) ])
    class Meta:
        model = specialistConsultancy
        exclude = ("specialist_isPending","specialist_isElderline")


    def create(self,validated_data):

        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        # fields = "__all__"

        # field = [""]
        # validated_data
        familyMembers.objects.filter(id = validated_data["specialist_docpatient"].id).update(
            current_isPending=False,
            current_isSpecialistMedication=validated_data["specialist_isMedication"],
            current_isHospitalisation=validated_data["specialist_isHospitalisation"],
            current_specialistConsultation=validated_data["specialist_Consultation"]
            # current_specialistConsultation=validated_data["specialistConsultation"])
            )
        return super().create(validated_data)

class PatientTestReportserializers(serializers.ModelSerializer):
    class Meta:
        model = PatientTestReport
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = "__all__"

    def create(self,validated_data):
        if PatientTestReport.objects.filter(patientLabTest=validated_data['patientLabTest']).exists():
            raise serializers.ValidationError({'responseMessage':"Record exists!"})    
        return super().create(validated_data)    
# ===========
class NewPatientLabTestserializers2(serializers.ModelSerializer):
    # patientLabTest = PatienttestReportserializers(many=True)
    patientLabTest = PatientTestReportserializers(many=True)

    class Meta:
        model = PatientTest

        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = ["test","barcode","pathlab","patientLabTest"]


class NewpatientLabTestserializers(serializers.ModelSerializer):
    # patientLabTest = PatienttestReportserializers(many=True)

    class Meta:
        model = PatientTest

        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = ["test","barcode","pathlab"]

class PatientTestReportserializers2(serializers.ModelSerializer):
    barcode = serializers.CharField(source="patientLabTest.barcode")
    test_name = serializers.CharField(source="patientLabTest.test.testName")
    test_type = serializers.CharField(source="patientLabTest.test.test_type")
    class Meta:
        model = PatientTestReport
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = "__all__"   

class CitizenLabTestserializers(serializers.ModelSerializer):
    # patientLabTest = PatienttestReportserializers(many=True)
    name = serializers.CharField(source='patientDetail.member_name')
    family_id = serializers.CharField(source='patientDetail.family_head.unique_family_key')
    citizen_id = serializers.CharField(source='patientDetail.member_unique_id')
    gender = serializers.CharField(source='patientDetail.member_gender')
    phone = serializers.CharField(source='patientDetail.mobile')
    class Meta:
        model = PatientTest
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = ["pathlab","barcode","name","family_id","citizen_id","gender","phone"]



class NewfamilymemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # doctorConsultancy = DoctorConsultancySerializer(many=True)
    doctorConsultancy = doctorConsultancyserializers(many=True)
    patientLabTestDetail = NewpatientLabTestserializers(many=True)
    class Meta:
        model = familyMembers
        fields = ("member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","patientLabTestDetail","doctorConsultancy")


class NewTestfamilymemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # doctorConsultancy = DoctorConsultancySerializer(many=True)
    member_id = serializers.SerializerMethodField()
    PatientTestDetail = NewpatientLabTestserializers(many=True)
    class Meta:
        model = familyMembers
        fields = ("id","member_id","member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","PatientTestDetail","member_unique_id","isClaimed","claimedBy_id")
    def get_member_id(self,obj):
       return obj.id


class PhcConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = phcConsultancy
        exclude = ('patientLabTestreport',)

class SpecialityDoctorConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = specialistConsultancy
        exclude = ('specialist_patientLabTestreport',)



class SelfNewTestfamilymemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    phcDoctorConsultancy = PhcConsultancySerializer(many=True)
    specialistDoctorConsultancy = SpecialityDoctorConsultancySerializer(many=True)
    PatientTestDetail = NewpatientLabTestserializers(many=True)
    class Meta:
        model = familyMembers
        fields = ("member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","member_unique_id","phcDoctorConsultancy","specialistDoctorConsultancy","PatientTestDetail")

class SelfFamilymemberSurveySerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = familyMembers
        fields = ("member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","member_unique_id")

# class SelfNewTestfamilymemberSerializer(serializers.ModelSerializer):
#     # profile_images=Base64ImageField() # From DRF Extra Fields
#     # doctorConsultancy = DoctorConsultancySerializer(many=True)
#     # doctorConsultancy = doctorConsultancyserializers(many=True)
#     # PatientTestDetail = NewpatientLabTestserializers(many=True)
#     class Meta:
#         model = familyMembers
#         exclude = ("basicLabTest","AdvanceLabTest","familysurveyor","pathlab","phlebotomist","LabSampleTaken","current_isPending","current_isMedication","current_isSpecialistMedication","current_isHospitalisation","current_phcConsultation","current_specialistConsultation","current_isElderline","distHospital","doctorAssigned","isCaseClosed","caseClosedBy","caseClosedReason","caseClosedDate",)

class doctorRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctorRemarksPathlab
        fields = '__all__'


class DisplayNewTestfamilymemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # doctorConsultancy = DoctorConsultancySerializer(many=True)
    doctorConsultancy = doctorConsultancyserializers(many=True)
    PatientTestDetail = NewpatientLabTestserializers(many=True)
    doctorPathlabRemarks = serializers.SerializerMethodField()
    class Meta:
        model = familyMembers
        fields = ("id","member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","PatientTestDetail","member_unique_id","doctorConsultancy","disease_count","doctorPathlabRemarks")
    def get_doctorPathlabRemarks(self,instance):
            print(instance.id,'-=====--')
            dr=doctorRemarksPathlab.objects.filter(remarkreport__patientLabTest__patientDetail_id=instance.id)
            print(dr,'-----------')
            if dr:
                return doctorRemarkSerializer(dr,many=True).data

class phcConsultancySerializers2(serializers.ModelSerializer):
    class Meta:
        model = phcConsultancy
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = "__all__"

class specialistConsultancySerializers2(serializers.ModelSerializer):
    class Meta:
        model = specialistConsultancy
        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = "__all__"

class DisplayNewTestfamilymemberSerializer2(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # doctorConsultancy = DoctorConsultancySerializer(many=True)
    phcDoctorConsultancy = phcConsultancySerializers2(many=True)
    specialistDoctorConsultancy = specialistConsultancySerializers2(many=True)
    PatientTestDetail = NewpatientLabTestserializers(many=True)
    doctorPathlabRemarks = serializers.SerializerMethodField()
    class Meta:
        model = familyMembers
        fields = ("id","member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","PatientTestDetail","member_unique_id","phcDoctorConsultancy","specialistDoctorConsultancy","disease_count","doctorPathlabRemarks")
    def get_doctorPathlabRemarks(self,instance):
            print(instance.id,'-=====--')
            dr=doctorRemarksPathlab.objects.filter(remarkreport__patientLabTest__patientDetail_id=instance.id)
            print(dr,'-----------')
            if dr:
                return doctorRemarkSerializer(dr,many=True).data


class InsertfamilyHeadDetails(serializers.ModelSerializer):
    family_head_member = NewTestfamilymemberSerializer(many=True)
    class Meta:
        model = familyHeadDetails
        fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member","surveyCompleted","surveyDoneBy"]

class InsertOnlyfamilyHeadDetails(serializers.ModelSerializer):
    # family_head_member = NewTestfamilymemberSerializer(many=True)
    
    class Meta:
        model = familyHeadDetails
        fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted"]


class NewSelfInsertOnlyfamilyHeadDetails(serializers.ModelSerializer):
    # family_head_member = NewTestfamilymemberSerializer(many=True)
    
    class Meta:
        model = familyHeadDetails
        fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","selfBookAppointment"]



class SelfInsertfamilyHeadDetails(serializers.ModelSerializer):
    # family_head_member = SelfNewTestfamilymemberSerializer(many=True)
    family_head_member = SelfFamilymemberSurveySerializer(many=True)
    class Meta:
        model = familyHeadDetails
        fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]


RoleCode = {'surveyour':'S','seniorcitizen':'F','phlebotomist':'P','pathlab':'L','phc':'PHC','doctor':'D'}
def generateFamilyID(uid,role):
  old_uid = uid
  uid=str(uid) 
  len_uid=8-len(str(uid))
  # old_uid = uid
  uid = len_uid*'0'+uid
  generate_id = RoleCode[role]+'SS'+uid
  if not familyHeadDetails.objects.filter(unique_family_key=generate_id).exists():
      return generate_id
  if familyHeadDetails.objects.filter(unique_family_key=generate_id).exists():
      return generateFamilyID(old_uid+1,role)
def generateFamCitID(citi_id,fam_id):
  old_uid = citi_id 
  citi_id =str(citi_id)
  # generate_id = RoleCode[role]+'SS'+str(uid)
  str_citi_id = citi_id if len(citi_id)!=1 else '0'+citi_id
  citi_id=fam_id +'-'+ str_citi_id
  if not familyMembers.objects.filter(member_unique_id=citi_id).exists():
      return citi_id
  if familyMembers.objects.filter(member_unique_id=citi_id).exists():
      return generateFamilyID(old_uid+1,fam_id)

class NewfamilyHeadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    familyAddress = AddressDetailSerializer()
    family_head_member = NewTestfamilymemberSerializer(many=True)
    class Meta:
        model = familyHeadDetails
        fields = "__all__"

class SelfNewfamilyHeadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    familyAddress = SelfAddressDetailSerializer()
    family_head_member = SelfNewTestfamilymemberSerializer(many=True)
    class Meta:
        model = familyHeadDetails
        exclude = ("surveyCompleted","labsampleTaken","surveyDoneBy")


class SelfListFamilySerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    familyAddress = SelfAddressDetailSerializer()
    family_head_member = DisplayNewTestfamilymemberSerializer(many=True)
    class Meta:
        model = familyHeadDetails
        fields ="__all__"



# class DisplayNewfamilyHeadSerializer(serializers.ModelSerializer):
#     # profile_images=Base64ImageField() # From DRF Extra Fields
#     familyAddress = AddressDetailSerializer()
#     family_head_member = DisplayNewTestfamilymemberSerializer(many=True)
#     class Meta:
#         model = familyHeadDetails
#         fields = "__all__"

class DisplayNewfamilyHeadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    familyAddress = AddressDetailSerializer()
    family_head_member = DisplayNewTestfamilymemberSerializer2(many=True)
    class Meta:
        model = familyHeadDetails
        fields = "__all__"
        
class InsertAddressDetails(serializers.ModelSerializer):
    familyAddress =  InsertfamilyHeadDetails(many=True)

    class Meta:
        model = AddressDetails
        fields = ["id","district","region_type","municipal_corporation","ward","municipal_council","taluka","phc","sc","village","other_place","address1","address2","pincode","total_family_count","familyAddress"]


    def create(self, validated_data):
        # print(validated_data,"############78")
        # test = list(validated_data["familyAddress"]['family_head_member'])
        # tr = 

        famAddress = validated_data.pop('familyAddress')
        # print(test,"*******************8")
        address = AddressDetails.objects.create(**validated_data)
        # try:
        # print(self.request.user.id,"************8")
        for famAddress in famAddress:
            # print(type(famAddress),"##########################")

            famMembers = famAddress.pop('family_head_member')
            print(type(famMembers[0]),type(famAddress),"##########################")

            fhead = familyHeadDetails.objects.create(familyAddress=address,**famAddress)
            fam_id = generateFamilyID(fhead.id,'seniorcitizen')
            # print(fhead.id,"&&&&&&&&&&&&&&&777777")
            citi_id = 1
            for famMem in famMembers:
                # print(famMem)
    
                print(type(famMem),"(((((((((((((((((")
                testData = famMem.pop('PatientTestDetail')
                memFam = familyMembers.objects.create(family_head = fhead,**famMem)
                # print(t111y,"@@@@@@@@@@@@#####")
                for test in testData:
                    tp = PatientTest.objects.create(patientDetail=memFam,**test)
                # str_citi_id = str(citi_id) if len(citi_id)!=1 else '0'+str(citi_id)

                memFam.member_unique_id = generateFamCitID(citi_id,fam_id)
                memFam.save()
                citi_id=citi_id+1
                # t111y.save()
                # famMembers.family_head.create(family_head = fhead,**famMem)
                # familyMembers.family_head(ty)
        # except Exception as e:
        #     print(e,"&&&&&&&&&&&&&&77")
            fhead.unique_family_key = fam_id
            fhead.save()
            default_password=fam_id
            email_fam=""
            try:
                user = CustomUser.objects.create_user(name=famAddress['family_head_name'],email=email_fam,unique_id=fam_id,username=famAddress['family_head_mobile'],phone=famAddress['family_head_mobile'],password=default_password,confirm_password=default_password,region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
                group = Group.objects.get(name="seniorcitizen")
                group.user_set.add(user)
            except:
                raise serializers.ValidationError({"error":"User "+famAddress['family_head_name']+" Already Exisit"})

        return address
        

class SeniorCitizenRegister2Serializer(serializers.ModelSerializer):
    familyHead=  NewSelfInsertOnlyfamilyHeadDetails()
    family_head_email = serializers.CharField(required=False)
    family_head_password = serializers.CharField(required=False)

    class Meta:
        model = AddressDetails
        fields = ["id","district","region_type","municipal_corporation","ward","municipal_council","taluka","phc","sc","village","other_place","address1","address2","pincode","total_family_count","familyHead","family_head_email","family_head_password"]

    def validate_familyHead(self,value):
        if value['family_head_mobile']=="":
            print('---------------Here')
            raise serializers.ValidationError("Phone Number is compulsory!")
        # if value['family_head_mobile']:
        if  CustomUser.objects.filter(phone=value['family_head_mobile']).exists():
            raise serializers.ValidationError("Phone Number is already exists!")
        return value
    def create(self, validated_data):
      
        famAddress = validated_data.pop('familyHead')
        # print(famAddress,type(famAddress),'----====')
        email = validated_data.pop('family_head_email')
        password = validated_data.pop('family_head_password')

        # print(test,"*******************8")
        address = AddressDetails.objects.create(**validated_data)
       
        fhead = familyHeadDetails.objects.create(familyAddress=address,**famAddress)
        fam_id = generateFamilyID(fhead.id,'seniorcitizen')
           
        fhead.unique_family_key = fam_id
        fhead.save()
        default_password=password
        email_fam=email
        user = CustomUser.objects.create_user(name=famAddress['family_head_name'],email=email_fam,username=fam_id,phone=famAddress['family_head_mobile'],password=default_password,confirm_password=default_password,region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        group = Group.objects.get(name="seniorcitizen")
        group.user_set.add(user)

        return address



class SelfInsertAddressDetails(serializers.ModelSerializer):
    familyAddress =  SelfInsertfamilyHeadDetails(many=True)

    class Meta:
        model = AddressDetails
        fields = ["id","district","region_type","municipal_corporation","ward","municipal_council","taluka","phc","sc","village","other_place","address1","address2","pincode","total_family_count","familyAddress"]


    def create(self, validated_data):
        # print(validated_data,"############78")
        # test = list(validated_data["familyAddress"]['family_head_member'])
        # tr = 

        famAddress = validated_data.pop('familyAddress')
        # print(test,"*******************8")
        address = AddressDetails.objects.create(**validated_data)
        # try:

        for famAddress in famAddress:
            # print(type(famAddress),"##########################")

            famMembers = famAddress.pop('family_head_member')
            print(type(famMembers[0]),type(famAddress),"##########################")

            fhead = familyHeadDetails.objects.create(familyAddress=address,**famAddress)
            fam_id = generateFamilyID(fhead.id,'seniorcitizen')
            # print(fhead.id,"&&&&&&&&&&&&&&&777777")
            citi_id = 1
            for famMem in famMembers:
                # print(famMem)
    
                print(type(famMem),"(((((((((((((((((")
                # testData = famMem.pop('PatientTestDetail')
                memFam = familyMembers.objects.create(family_head = fhead,**famMem)
                # # print(t111y,"@@@@@@@@@@@@#####")
                # for test in testData:
                #     tp = PatientTest.objects.create(patientDetail=memFam,**test)
                # str_citi_id = str(citi_id) if len(citi_id)!=1 else '0'+str(citi_id)

                memFam.member_unique_id = generateFamCitID(citi_id,fam_id)
                memFam.save()
                citi_id=citi_id+1
                # t111y.save()
                # famMembers.family_head.create(family_head = fhead,**famMem)
                # familyMembers.family_head(ty)
        # except Exception as e:
        #     print(e,"&&&&&&&&&&&&&&77")
            fhead.unique_family_key = fam_id
            fhead.save()
            default_password=fam_id
            email_fam=""
            user = CustomUser.objects.create_user(name=famAddress['family_head_name'],email=email_fam,username=fam_id,phone=famAddress['family_head_mobile'],password=default_password,confirm_password=default_password,region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
            group = Group.objects.get(name="seniorcitizen")
            group.user_set.add(user)

        return address



class AllPathologySerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields

    class Meta:
        model = pathlogy
        fields = "__all__"





class TestRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRange
        fields = "__all__"
        
class MaleReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaleReference
        exclude =['test']
        # fields = '__all__'

class FemaleReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FemaleReference
        # fields = '__all__'
        exclude =['test']

class AllTestRangeListSerializer(serializers.ModelSerializer):
    MaleReference_test = MaleReferenceSerializer(many=True)
    FemaleReference_test = FemaleReferenceSerializer(many=True)
    class Meta:
        model = TestRange
        fields = '__all__'
        # fields =['MaleReference_test','FemaleReference_test']

    def create(self, validated_data):
        print(validated_data,"############78")
        # # test = list(validated_data["familyAddress"]['family_head_member'])
        # # tr = 
        maleReference = validated_data.pop('MaleReference_test')
        femaleReference = validated_data.pop('FemaleReference_test')
        test_range = TestRange.objects.create(**validated_data)
        for each in maleReference:
            male=MaleReference.objects.create(test=test_range,**each)
        for each in femaleReference:
            female=FemaleReference.objects.create(test=test_range,**each)
        

        return test_range

class UploadTestReportSerializer(serializers.ModelSerializer):
    MaleReference_test = MaleReferenceSerializer(many=True)
    FemaleReference_test = FemaleReferenceSerializer(many=True)
    class Meta:
        model = TestRange
        fields = '__all__'
        # fields =['MaleReference_test','FemaleReference_test']

    def create(self, validated_data):
        print(validated_data,"############78")
        # # test = list(validated_data["familyAddress"]['family_head_member'])
        # # tr = 
        maleReference = validated_data.pop('MaleReference_test')
        femaleReference = validated_data.pop('FemaleReference_test')
        test_range = TestRange.objects.create(**validated_data)
        for each in maleReference:
            male=MaleReference.objects.create(test=test_range,**each)
        for each in femaleReference:
            female=FemaleReference.objects.create(test=test_range,**each)
        

        return test_range

class ViewUploadTestReportSerializer(serializers.ModelSerializer):
    remarkreport = AllDoctorRemarkPathlabList(many=True)
    PatientTest_test = AllTestRangeListSerializer(source='patientLabTest.test')

    class Meta:
        model = PatientTestReport
        fields = '__all__'

class GetCitizenTestListSerializer(serializers.ModelSerializer):
    PatientTest_test = AllTestRangeListSerializer(source='test')

    class Meta:
        model = PatientTest
        fields = '__all__'


class SelffamilyHeadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    familyAddress = InsertAddressDetails()

    family_head_member = SelfNewTestfamilymemberSerializer(many=True)
    class Meta:
        model = familyHeadDetails
        fields = "__all__"

    def create(self, validated_data):
        familyhead = validated_data.pop('family_head_member')
        head = familyHeadDetails.objects.create(**validated_data)
        for familyhead in familyhead:
            familyMembers.objects.create(family_head=head, **familyhead)
        return head



class UpdatePartialFamilyMemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    family_head_id = serializers.IntegerField()
    total_senior_citizen = serializers.IntegerField()
    FamilyCompleted = serializers.BooleanField()
    surveyCompleted = serializers.BooleanField()
    labsampleTaken = serializers.BooleanField()
    surveyDoneBy  = serializers.IntegerField()
    PatientTestDetail = NewpatientLabTestserializers(many=True)
    class Meta:
        model = familyMembers
        fields = ("family_head_id","member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","PatientTestDetail","member_unique_id","total_senior_citizen","FamilyCompleted","surveyCompleted","labsampleTaken","surveyDoneBy")

    def create(self, validated_data):
        family_head_id = validated_data.pop('family_head_id')

        total_senior_citizen = validated_data.pop('total_senior_citizen')
        FamilyCompleted = validated_data.pop('FamilyCompleted')
        surveyCompleted = validated_data.pop('surveyCompleted')
        labsampleTaken = validated_data.pop('labsampleTaken')
        surveyDoneBy = validated_data.pop('surveyDoneBy')

        headupdate = familyHeadDetails.objects.filter(family_head_id=family_head_id).update(total_senior_citizen=total_senior_citizen,FamilyCompleted=FamilyCompleted,labsampleTaken=labsampleTaken,surveyDoneBy_id=surveyDoneBy)
        # for familyhead in familyhead:
        testData = validated_data.pop('PatientTestDetail')

        ht = familyMembers.objects.create(family_head_id=family_head_id, **validated_data)

        citi_id = 1
        for test in testData:
            tp = PatientTest.objects.create(patientDetail=ht,**test)
        # str_citi_id = str(citi_id) if len(citi_id)!=1 else '0'+str(citi_id)
            citi_id = citi_id + 1
        ht.member_unique_id = generateFamCitID(int(citi_id),str(family_head_id))
        ht.save()


        return ht





class CitizenInsertFamilyMemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    family_head_id = serializers.IntegerField()
    total_senior_citizen = serializers.IntegerField()
    FamilyCompleted = serializers.BooleanField()
    # surveyCompleted = serializers.BooleanField()
    # labsampleTaken = serializers.BooleanField()
    citizenNo  = serializers.IntegerField()
    # PatientTestDetail = NewpatientLabTestserializers(many=True)
    class Meta:
        model = familyMembers
        fields = ("citizenNo","family_head_id","member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","member_unique_id","total_senior_citizen","FamilyCompleted")

    def create(self, validated_data):
        family_head_id = validated_data.pop('family_head_id')

        total_senior_citizen = validated_data.pop('total_senior_citizen')
        FamilyCompleted = validated_data.pop('FamilyCompleted')
        citizenNo = validated_data.pop('citizenNo')
        # labsampleTaken = validated_data.pop('labsampleTaken')
        # surveyDoneBy = validated_data.pop('surveyDoneBy')

        headupdate = familyHeadDetails.objects.filter(id=family_head_id).update(total_senior_citizen=total_senior_citizen,FamilyCompleted=FamilyCompleted)
        # for familyhead in familyhead:
        # testData = validated_data.pop('PatientTestDetail')

        ht = familyMembers.objects.create(family_head_id=family_head_id, **validated_data)

        # citi_id = 1
        # for test in testData:
        #     tp = PatientTest.objects.create(patientDetail=ht,**test)
        # # str_citi_id = str(citi_id) if len(citi_id)!=1 else '0'+str(citi_id)
        # citi_id = citizenNo + 1
        ht.member_unique_id = generateFamCitID(int(citizenNo),str(family_head_id))
        ht.save()


        return ht


class UpdateFamilyHeadAddressDetailSerializer(serializers.Serializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    family_head_id = serializers.IntegerField()
    family_head_name = serializers.CharField()
    total_senior_citizen = serializers.IntegerField()
    FamilyCompleted = serializers.BooleanField()
    surveyCompleted = serializers.BooleanField()
    labsampleTaken = serializers.BooleanField()
    district = serializers.CharField()
    region_type = serializers.CharField()
    municipal_corporation = serializers.CharField()
    ward = serializers.CharField()
    municipal_council = serializers.CharField()
    taluka = serializers.CharField()
    phc = serializers.CharField()
    sc = serializers.CharField()
    village = serializers.CharField()
    other_place = serializers.CharField()
    address1 = serializers.CharField()
    address2 = serializers.CharField()
    pincode = serializers.CharField()
    family_head_mobile = serializers.CharField()

    class Meta:
        fields = ("family_head_id","family_head_name","total_senior_citizen","FamilyCompleted","surveyCompleted","labsampleTaken","district","region_type","municipal_corporation","ward","municipal_council","taluka","phc","sc","village","other_place","address1","address2","pincode","family_head_mobile",)

    def update(self,validated_data):
        family_head_id = validated_data["family_head_id"]
        family_head_name = validated_data["family_head_name"]
        total_senior_citizen = validated_data["total_senior_citizen"]
        FamilyCompleted = validated_data["FamilyCompleted"]
        surveyCompleted = validated_data["surveyCompleted"]
        labsampleTaken = validated_data["labsampleTaken"]
        district = validated_data["district"]
        region_type = validated_data["region_type"]
        municipal_corporation = validated_data["municipal_corporation"]
        ward = validated_data["ward"]
        municipal_council = validated_data["municipal_council"]
        taluka = validated_data["taluka"]
        phc = validated_data["phc"]
        sc = validated_data["sc"]
        village = validated_data["village"]
        other_place = validated_data["other_place"]
        address1 = validated_data["address1"]
        address2 = validated_data["address2"]
        pincode = validated_data["pincode"]
        family_head_mobile = validated_data["family_head_mobile"]
        address = AddressDetails.objects.filter(familyAddress__family_head_id = family_head_id).update(district=district,region_type=region_type,municipal_corporation=municipal_corporation,ward=ward,municipal_council=municipal_council,taluka=taluka,phc=phc,sc=sc,village=village,other_place=other_place,address1=address1,address2=address2,pincode=pincode)
        head = familyHeadDetails.objects.filter(family_head_id=family_head_id).update(total_senior_citizen=total_senior_citizen,FamilyCompleted=FamilyCompleted,surveyCompleted=surveyCompleted,labsampleTaken=labsampleTaken,family_head_mobile=family_head_mobile)
        return head
    


class UpdatePatientLabTestserializers2(serializers.ModelSerializer):
    # patientLabTest = PatienttestReportserializers(many=True)
    # patientLabTest = PatientTestReportserializers(many=True)
    test_id = serializers.IntegerField()
    class Meta:
        model = PatientTest

        # fields = ["id","family_head_name","family_head_mobile","total_family_members","total_senior_citizen","FamilyCompleted","family_head_member"]
        fields = ["test_id","test","barcode","pathlab"]



class UpdateFamilyMemberDataSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    member_id = serializers.IntegerField()
    PatientTestDetail = UpdatePatientLabTestserializers2(many=True)
    class Meta:
        model = familyMembers
        fields = ("member_id","member_name","member_gender","member_age","idProof","idProofno","state_health_insurance","self_mobile",
        "mobile_relation","mobile","visualDisorder","physicalDisability","bedRidden_due_ailment","dependent_on_people","pulse",
    "blood_pressure","respiratory_rate","spo2_level","weight","height","bmi","above60","consume_smoking_gutka_or_khaini","consume_alcohol_daily","smoke_score","waist_measurement","ability_to_perform_daily_movements",
    "isdisease","disease","anyone_to_takecare","totalscore","shortness_of_breath","chest_pain","suspected_heart_disease",
    "headache","dizziness","chest_throbbling","suspected_high_blood_pressure","coughing_more_than_two_weeks","blood_in_sputum","fever_for_more_than_two_weeks",
    "loss_of_weight","night_sweats","suspected_tuberculosis","familyHistory_tuberculosis","currently_taking_anti_tb_drugs","wounds_or_ulcers_in_mouth_more_than_two_weeks"
    ,"mouth_sores_or_lumps","white_or_red_patches_in_mouth","pain_while_chewing_food","difficulty_in_mouth_opening","suspected_mouth_cancer",
    "frequently_difficulties_in_breathing","dry_cough_many_days","tired_or_exhaust","spitting_out_thick_cough","suspected_copd",
    "slow_urination","reduced_urination","suspected_prostate_gland_disease","frequent_urination","irritation_while_urination",
    "suspected_diabetes","suspected_urinary_tract_infection_inflammation","decreased_urination","feeling_tired","appetite_loss",
    "limbs_swelling","heel_or_foot_swelling","feeling_nauseas","suspected_kidney","urinate_unknowningly","suspected_imbalanced_kidney_function",
    "frequent_hunger_thirst","weight_loss","no_wound_healing","tingling_in_hands_and_feet","history_of_fits","suspected_brain_disease",    
    "suspected_fits","sudden_balance_loss_while_walking","trembling_feeling","things_falling_or_sleeping_out_of_hands","suspected_neurological_disorder",
    "suspected_parkinson_disease","not_closing_of_eyelids_completely","feeling_weak_one_side","legs_weakness_difficult_walk","difficulty_swallowing",
    "disability","suspected_heart_attack","suspected_paralysis","blurred_vision_and_reading_difficulty","suspected_blindness_or_cataracts",
    "non_reducing_eye_pain_more_than_week","redness_in_eyes","suspected_glaucoma","splits_on_mouth_edges","tongue_redness","mouth_ulcers",
    "fatigue_easily","suspected_anaemia","suspected_malnutrition","suspected_vitamins_deficiency","patches_on_skin_and_no_sensation",
    "suspected_leprosy","unbearable_back_pain","frequent_fractures","joint_pain_at_night","pain_when_bones_pressed",
    "suspected_osteoporosis","impairment_of_movement_physical_disabilities_rheumatism","bending_of_toes","suspected_osteoarthritis","change_in_voice",
    "hoarse_voice","spitting_blood_while_coughing","suspected_cancer","lumps_on_skin","difficulty_in_hearing",
    "suspected_ear_deafness","blood_in_stool_or_black_stool","suspected_internal_bleeding","suspected_piles",
    "suspected_fissure","suspected_fistula","recent_fall","history_head_injury","suspected_injury","lump_in_the_breast",
    "pain_in_the_breast","blood_stained_discharge_from_the_nipple","changes_in_skin_breast","change_in_shape_or_size_of_breast",
    "suspected_breast_cancer","suspected_breast_disease","odour_discharge_from_vagina","irregular_or_accidental_bleeding",
    "abdominal_pain","difficulty_while_urinating","limb_protrusion","bleeding_after_intercourse","suspected_cervical_cancer",
    "forgetting_house_Address_or_family_member_name","not_remembering_life_memories","not_remembering_faces_individuals","suspected_alzheimers",
    "lack_of_interest_in_life","depression","has_lost_contact_with_family","frequent_mood_swings","too_angry","less_sleep_or_more_sleep_night",
    "thought_suicide_come_to_mind","suspected_depression","very_restless_anxious_after_physical_symptoms",
    "feeling_daily_activities_cannot_perform","negative_attitude","unnecessary_pain","weakness","no_improvements_after_frequent_treatment",
    "suspected_somatic_illness","basicLabTest","AdvanceLabTest","pathlab","PatientTestDetail",)

    def update(self, validated_data):
        member_id = validated_data.pop('member_id')
        testData = validated_data.pop('PatientTestDetail')


        headupdate = familyMembers.objects.filter(id=member_id).update(**validated_data)
        # for familyhead in familyhead:
        

        # ht = familyMembers.objects.create(family_head_id=family_head_id, **validated_data)

        for testd in testData:
            tp = PatientTest.objects.filter(id=testd["test_id"]).update(test =testd["test"],barcode=testd["barcode"],pathlab=testd["patientLabTest"])



        return headupdate




class UpdateSelfRegisteredFamilyMemberSerializer(serializers.Serializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    family_head_id = serializers.IntegerField()
    member_id = serializers.IntegerField()
    surveyCompleted = serializers.BooleanField()
    labsampleTaken = serializers.BooleanField()
    PatientTestDetail = NewpatientLabTestserializers(many=True)
    class Meta:
        fields = ("family_head_id","member_id","surveyCompleted","labsampleTaken","PatientTestDetail",)

    def update(self, validated_data):
        member_id = validated_data.pop('member_id')
        family_head_id = validated_data.pop('member_id')
        surveyCompleted = validated_data.pop('member_id')
        labsampleTaken = validated_data.pop('member_id')

        testData = validated_data.pop('PatientTestDetail')


        headupdate = familyHeadDetails.objects.filter(id=family_head_id).update(surveyCompleted=surveyCompleted,labsampleTaken=labsampleTaken)
        # for familyhead in familyhead:
        

        # ht = familyMembers.objects.create(family_head_id=family_head_id, **validated_data)

        for testd in testData:
            # tp = PatientTest.objects.filter(id=testd["test_id"]).update(test =testd["test"],barcode=testd["barcode"],pathlab=testd["patientLabTest"])
            tp = PatientTest.objects.create(patientDetail_id=member_id,**test)



        return headupdate

from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import *
from django.db.models.signals import post_save,pre_save, pre_delete,post_delete,m2m_changed#,post_add
# import request
from django.db.models import When, F, Q, Value,Case
from django.db.models import DecimalField 
from decimal import Decimal  
@receiver(post_save, sender=familyMembers) 
def create_familyMembers(sender, instance, created, **kwargs):
    if created:
        print(created,'===created---')
        # instance.created_by=instance.updated_by
        # Data.objects.update(created_by=instance.updated_by)
    #     DataLogs.objects.create(user=instance.updated_by,latitude=instance.latitude,longitude=instance.longitude,location_data_id=instance.id,message="created")
    #     print('created---')
    #     print(created,'----created')
    #     # print(f'kwargs:{kwargs}')
    # else :
    #     print(instance.id)
    #     dt=DataLogs.objects.create(user=instance.updated_by,latitude=instance.latitude,longitude=instance.longitude,location_data_id=instance.id,message="updated")
    #     print('updated---')
    #     print(sender,'----')
    #     print(instance.latitude,'---latitude')
    #     print(created,'----created')
    #     print(f'kwargs:{kwargs}')

# def save(instance, *args, **kwargs):
        if instance.no_improvements_after_frequent_treatment == True or instance.unnecessary_pain == True or instance.weakness==True or instance.shortness_of_breath == True or instance.negative_attitude == True or instance.feeling_daily_activities_cannot_perform ==True or instance.very_restless_anxious_after_physical_symptoms  :
            instance.suspected_somatic_illness = True 

        if instance.thought_suicide_come_to_mind == True or instance.less_sleep_or_more_sleep_night == True or instance.too_angry == True or instance.frequent_mood_swings == True or instance.has_lost_contact_with_family == True or instance.depression == True or instance.lack_of_interest_in_life ==True :
            instance.suspected_depression = True 

        if instance.not_remembering_life_memories == True or instance.not_remembering_faces_individuals == True or instance.forgetting_house_Address_or_family_member_name == True:
            instance.suspected_alzheimers = True

        if instance.bleeding_after_intercourse == True or instance.limb_protrusion == True or instance.difficulty_while_urinating == True or instance.abdominal_pain == True or instance.irregular_or_accidental_bleeding == True or instance.odour_discharge_from_vagina == True :
            instance.suspected_cervical_cancer = True 

        if instance.lump_in_the_breast == True or instance.pain_in_the_breast == True or instance.blood_stained_discharge_from_the_nipple == True or instance.changes_in_skin_breast == True or instance.change_in_shape_or_size_of_breast == True:
            instance.suspected_breast_cancer = True 
            instance.suspected_breast_disease = True 

        if instance.recent_fall == True or instance.history_head_injury == True :
            instance.suspected_injury = True 

        if instance.blood_in_stool_or_black_stool == True:
            instance.suspected_internal_bleeding = True 
            instance.suspected_cancer = True 
            instance.suspected_piles = True 
            instance.suspected_fissure = True 
            instance.suspected_fistula = True 

        if instance.difficulty_in_hearing == True :
            instance.suspected_ear_deafness = True 

        if instance.lumps_on_skin == True :
            instance.suspected_cancer = True 

        if instance.spitting_blood_while_coughing == True or instance.hoarse_voice == True or instance.weight_loss == True or instance.appetite_loss == True or instance.change_in_voice == True:
            instance.suspected_cancer = True 

        if instance.bending_of_toes == True or instance.impairment_of_movement_physical_disabilities_rheumatism == True :
            instance.suspected_osteoarthritis = True 

        if instance.pain_when_bones_pressed == True or instance.joint_pain_at_night == True or instance.frequent_fractures == True or instance.unbearable_back_pain == True :
            instance.suspected_osteoporosis = True       

        if instance.patches_on_skin_and_no_sensation == True :
            instance.suspected_leprosy = True 

        if instance.fatigue_easily == True or instance.appetite_loss == True or instance.mouth_ulcers == True or instance.tongue_redness == True or instance.splits_on_mouth_edges == True:
            instance.suspected_anaemia = True 
            instance.suspected_vitamins_deficiency = True 
            instance.suspected_malnutrition = True 

        if instance.redness_in_eyes == True or instance.non_reducing_eye_pain_more_than_week == True :
            instance.suspected_diabetes = True
            instance.suspected_glaucoma = True 

        if instance.blurred_vision_and_reading_difficulty == True :
            instance.suspected_blindness_or_cataracts = True 

        if instance.disability == True or instance.difficulty_swallowing == True or instance.legs_weakness_difficult_walk == True or instance.feeling_weak_one_side == True or instance.not_closing_of_eyelids_completely == True:
            instance.suspected_heart_attack = True
            instance.suspected_paralysis = True 

        if instance.things_falling_or_sleeping_out_of_hands == True or instance.trembling_feeling == True or instance.sudden_balance_loss_while_walking == True :
            instance.suspected_neurological_disorder = True 
            instance.suspected_parkinson_disease = True 

        if instance.history_of_fits == True :
            instance.suspected_fits = True 
            instance.suspected_brain_disease = True 

        if instance.tingling_in_hands_and_feet == True or instance.no_wound_healing == True or instance.weight_loss == True or instance.frequent_hunger_thirst == True :
            instance.suspected_diabetes = True 

        if instance.urinate_unknowningly == True :
            instance.suspected_imbalanced_kidney_function = True 

        if instance.feeling_nauseas == True or instance.heel_or_foot_swelling == True or instance.limbs_swelling == True :
            instance.suspected_kidney = True  

        if instance.irritation_while_urination == True or instance.frequent_urination == True :
            instance.suspected_diabetes = True 
            instance.suspected_urinary_tract_infection_inflammation = True
        
        #suspected_heart_disease
        if instance.shortness_of_breath    == True or instance.chest_pain   == True:
            instance.suspected_heart_disease  = True

        #suspected_high_blood_pressure
        if instance.shortness_of_breath    == True or instance.chest_pain   == True:
            instance.suspected_high_blood_pressure   = True

        #suspected_tuberculosis
        if instance.coughing_more_than_two_weeks  == True or instance.blood_in_sputum == True or instance.fever_for_more_than_two_weeks == True or instance.loss_of_weight  == True or instance.night_sweats == True:
            instance.suspected_tuberculosis   = True
        
        #suspected_mouth_cancer  
        if instance.wounds_or_ulcers_in_mouth_more_than_two_weeks   == True or instance.mouth_sores_or_lumps  == True or instance.white_or_red_patches_in_mouth      == True or instance.pain_while_chewing_food      == True or instance.difficulty_in_mouth_opening      == True:
            instance.suspected_mouth_cancer    = True

        #suspected_copd
        if instance.frequently_difficulties_in_breathing    == True or instance.dry_cough_many_days   == True or instance.tired_or_exhaust  ==True or instance.spitting_out_thick_cough   == True :
            instance.suspected_copd   = True
        
        #suspected_prostate_gland_disease
        if instance.slow_urination == True or instance.reduced_urination    == True:
            instance.suspected_prostate_gland_disease    = True

        instance.save()
        fam_id=instance.id
        # fam=instance.save()
        # print(fam,'---')
        all_fields = [ f.name for f in familyMembers._meta.get_fields() if f.name.startswith("suspected_")]
        # print(all_fields,'-----')
        tableDiseaseList=dict(familyMembers.objects.filter(id=fam_id).values(*all_fields)[0])
        diseaseList =[k for k,v in tableDiseaseList.items() if v == True]
        diseaseCount =len(diseaseList)
        familyMembers.objects.filter(id=fam_id).update(disease_count=diseaseCount)
        intsance_addr = instance.family_head.familyAddress
        if intsance_addr.region_type.lower() == 'urban':
            phcDoc = CustomUser.objects.filter(
            region_type = intsance_addr.region_type,
            district = intsance_addr.district,
            municipal_corporation = intsance_addr.municipal_corporation,
            ward = intsance_addr.ward,
            groups__name__in=['phcUser']
            # phc = intsance_addr.phc
            )
        elif intsance_addr.region_type.lower() == 'rural':
            phcDoc = CustomUser.objects.filter(
            region_type = intsance_addr.region_type,
            district = intsance_addr.district,
            taluka = intsance_addr.taluka,
            groups__name__in=['phcUser'],
            phc = intsance_addr.phc
            )
        else:
            phcDoc = CustomUser.objects.filter(
            region_type = intsance_addr.region_type,
            district = intsance_addr.district,
            municipal_council = intsance_addr.municipal_council,
            groups__name__in=['phcUser']
            )
        if phcDoc:
            phcConsultancy.objects.create(docpatient_id=fam_id,phcDoctor_id=phcDoc[0].id,isPending=True)

# Create your views here.
RoleCode = {'surveyour':'S','seniorcitizen':'F','phlebotomist':'P','pathlab':'L','phc':'PHC','doctor':'D'}

def generatePhlebotomistID(role,uid,district_code,lab_name,no_id=''):
  generate_id = RoleCode[role]+'SS'+str(uid)+'-'+district_code[:3]+'-'+lab_name[:4]+no_id
  if CustomUser.objects.filter(unique_id=generate_id).exists():
      return generatePhlebotomistID(role,uid,district_code,lab_name,str(uid+1))
  print(generate_id,'======')
  return generate_id

def generateUserID(uid,role):
  len_uid=8-len(uid)
  uid = len_uid*'0'+uid
  generate_id = RoleCode[role]+'SS'+str(uid)
  # if role=='':
  family_mem=1
  while True:
          generate_id = RoleCode[role]+'SS'+str(uid)+'-'+str(family_mem)
          if not CustomUser.objects.filter(generate_id=generate_id).exists():
              return generate_id
          family_mem =family_mem+1
  if CustomUser.objects.filter(generate_id=generate_id).exists():
      return generateUserID(uid,role)
  return generate_id


# def generateHospitalID(uid,):
#   len_uid=8-len(uid)
#   uid = len_uid*'0'+uid
#   generate_id = RoleCode[role]+'SS'+uid
#   if role=='Doctor':
#       family_id=01
#       while True:
#           generate_id = RoleCode[role]+'SS'+uid+'-'+family_id
#           if not CustomUser.objects.filter(generate_id=generate_id).exists():
#               return generate_id
#           family_id =family_id+1
#   if CustomUser.objects.filter(generate_id=generate_id).exists():
#       generateUserID(uid,role)
#   return generate_id

# @receiver(post_add, sender=CustomUser.groups) 
@receiver(m2m_changed, sender=CustomUser.groups.through)
def on_tank_users_change(instance, action,pk_set, **_):
# def create_group(sender, instance, created, **kwargs):
        if action == 'post_add':
            print(instance,'-----inst',type(instance))
            # print(instance.groups.name)
            print(pk_set)
            print(instance.id)
            if instance.name == 'phlebotomist':
                print('============')
                li=Phlebotomist.objects.filter(phlebotomist_info_id__in=list(pk_set)).values('phlebotomist_info_id','pathlab_id__district','pathlab_id__labName')
                print('--==-=',li,type(li))
                latest_id=Phlebotomist.objects.latest('id')
                # li=list(li)
                phlebotomist_id=generatePhlebotomistID(instance.name,latest_id.id,li[0]['pathlab_id__district'],li[0]['pathlab_id__labName'])
                CustomUser.objects.filter(id__in=pk_set).update(unique_id=phlebotomist_id)
            if instance.name == 'pathlab':
                li=pathlogy.objects.filter(pathOwner_id__in=list(pk_set)).values('pathOwner_id','district','labName')
                latest_id=pathlogy.objects.latest('id')
                phlebotomist_id=generatePhlebotomistID(instance.name,latest_id.id,li[0]['district'],li[0]['labName'])
                print(phlebotomist_id,'----')
                CustomUser.objects.filter(id__in=pk_set).update(unique_id=phlebotomist_id)
            # if instance.name == 'seniorcitizen':
            #     user_id=generateUserID(pk_set,instance.name)
            #     # phlebotomist_id=generatePhlebotomistID(instance.name,li[0]['pathOwner_id'],li[0]['district'],li[0]['labName'])
            #     CustomUser.objects.filter(id__in=pk_set).update(unique_id=user_id)
        # print(instance.groups.all())
        # print(instance.groups.filter(name='surveyour').exists())

@receiver(post_save, sender=PatientTestReport)
def create_danger(sender, instance, created, **kwargs):
# def on_tank_users_change(instance, action,pk_set, **_):
# def create_group(sender, instance, created, **kwargs):
        test_comment=''
        if created :
            pat_gender = PatientTest.objects.filter(id=instance.patientLabTest_id).values_list('patientDetail__member_gender',flat=True)
            # print(pat_gender[0],'---===')
            if instance.parameterValue:
                parameterValue=instance.parameterValue
                if pat_gender[0].lower == "male": 
                    # test_comment = MaleReference.objects.annotate(
                    #     # parameterValue=parameterValue
                    #     parameterValue=Value(parameterValue, output_field=DecimalField()
                    #     )
                    #     ).filter(test__testName=instance.parameterName,parameterValue__range=[F('low_range'),F('high_range')]).values_list('comment',flat=True)
                    test_comment = MaleReference.objects.filter(test__testName=instance.parameterName).annotate(
                        parameterValue=Value(parameterValue, output_field=DecimalField()
                        )
                        ).values('low_range','high_range','comment')
                    found_comment = False
                    if test_comment:
                        for each in test_comment:
                            # print(Decimal(instance.parameterValue),'FLOAT')
                            dec_pv =  Decimal(instance.parameterValue)
                            # print(dec_pv.compare_total(each['high_range']),dec_pv.compare_total(each['low_range']))
                            # print(each['high_range'].compare_total(dec_pv),each['low_range'].compare_total(dec_pv))
                            # if (each['high_range']!='') or (dec_pv.compare(each['high_range']) ):
                            # if each['high_range']!='' or (dec_pv.compare_total(each['high_range'])==-1):
                            #     print('yes',each['high_range'],type(each['high_range']),type(dec_pv))

                            # if (each['low_range']!='' or each['low_range'] <= dec_pv) :
                            # # if each['low_range']!='' or (dec_pv.compare_total(each['low_range'])==1):
                            #     print('Yes Sachin',each['low_range'])
                            if ((each['high_range'] >= dec_pv)or each['high_range']=='') and  (( each['low_range'] <= dec_pv)or each['low_range']=='') :
                            # if (each['high_range']!='' or dec_pv.compare_total(each['high_range'])==-1) and  (each['low_range']!='' or dec_pv.compare_total(each['low_range'])==1) :
                                # print(each,'======')
                                # found_comment = True
                                instance.status = each['comment']
                                # return
                            else:
                        # if found_comment == False : 
                                instance.status = 'abnormal'
                            # instance.save()
                        instance.save()
                            # elif each['low_range']!='' or each['low_range']<float(instance.parameterValue):
                            #     instance.status = each['comment']

                    # else:
                    #     instance.status = 'abnormal'
                    #     instance.save()
                else: 
                    test_comment = FemaleReference.objects.filter(test__testName=instance.parameterName).annotate(
                        parameterValue=Value(parameterValue, output_field=DecimalField()
                        )
                        ).values('low_range','high_range','comment')
                    found_comment = False
                    if test_comment:
                        for each in test_comment:
                            dec_pv =  Decimal(instance.parameterValue)
                            if ((each['high_range'] >= dec_pv)or each['high_range']=='') and  (( each['low_range'] <= dec_pv)or each['low_range']=='') :
                                instance.status = each['comment']
                            else:
                                instance.status = 'abnormal'
                        instance.save()
# signed=Case(When(signed_agreement__member=F('member')),
#                     then=Value(True),
#                     default=Value(False),
#                     output_field=BooleanField()
            print(test_comment,'-----------')

from rest_framework import serializers
from database.models import *
from django.contrib.auth import authenticate
from database.serializers import AddressDetailSerializer,doctorConsultancyserializers

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class OtherUserDetailSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    groups_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name','username','email','phone','signup_date','login_date_time','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc','groups_name')
    def get_groups_name(self, obj):
    #     print("****************(((((((((")
        return obj.groups.values_list('name', flat=True)


class NewOtherUserSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields  
    # grpname = serializers.CharField()
    group_name = serializers.SerializerMethodField()  
    # def get_grpname(self, obj):
    #     print("****************(((((((((")
    #     return obj.groups.values_list()

    class Meta:
        model = CustomUser
        fields = ('id', 'name','username','phone','signup_date','login_date_time','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc','group_name')
    def get_group_name(self, obj):
        print("****************(((((((((")
        return obj.groups.values_list('name', flat=True)

class AdminLoginSerializer(serializers.Serializer):
    class Meta:
        model  = CustomUser
        fields = ('id','username','password')
    username = serializers.CharField()
    password = serializers.CharField()

    # language_code = serializers.CharField()

    def validate(self,data):
        print(data,"****************")
        customuser = authenticate(**data)
        if customuser:
            if customuser.is_active:
                if customuser.is_superuser:
                    # if customuser.is_verify:
                    return customuser
                    # else:
                    #     return serializers.ValidationError("User is Blocked. Please Contact Admin.")


                else:
                    raise serializers.ValidationError("Only Admin is Allowed.")
            else:
                raise serializers.ValidationError("User os Blocked. Please Contact Admin.")
        else:
            raise serializers.ValidationError("Incorrect Credentials.")

class PhcLoginSerializer(serializers.Serializer):
    class Meta:
        model  = CustomUser
        fields = ('id','username','password')
    username = serializers.CharField()
    password = serializers.CharField()

    # language_code = serializers.CharField()

    def validate(self,data):
        print(data,"****************")
        customuser = authenticate(**data)
        if customuser:
            if customuser.is_active:
                # if not customuser.is_superuser:
                    # if customuser.is_verify:
                return customuser
                    # else:
                    #     return serializers.ValidationError("User is Blocked. Please Contact Admin.")


                # else:
                #     raise serializers.ValidationError("Only user is Allowed.")
            else:
                raise serializers.ValidationError("User os Blocked. Please Contact Admin.")
        else:
            raise serializers.ValidationError("Incorrect Credentials.")



# class phcRegisterSerializer(serializers.ModelSerializer):
#     # profile_images=Base64ImageField() # From DRF Extra Fields

#     username = serializers.CharField()

#     class Meta:
#         model = CustomUser
#         fields = ('id','username', 'phone','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')
#         extra_kwargs = {'password': {'write_only': True}}
#         # phone = validated_data["phone"]
#         # print(phone,"*********************")
#         # phone_exists = CustomUser.objects.filter(phone=phone)
#         # if phone_exists:
#         #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

#         # return validated_data

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
#         return user




class phcRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    taluka = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 
    phc = serializers.CharField(required =False,default="")
    class Meta:
        model = CustomUser
        fields = ('id','username', 'phone','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')
        extra_kwargs = {'password': {'write_only': True}}
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        return user


class NewphcRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    taluka = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 
    phc = serializers.CharField(required =False,default="")
    name = serializers.CharField(required=False,allow_null=True)
    email = serializers.CharField(required=False,allow_null=True)
    class Meta:
        model = CustomUser
        fields = ('id','username', 'phone','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc','name','email')
        extra_kwargs = {'password': {'write_only': True}}
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data
    def validate(self, validated_data):
        if CustomUser.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('Username already exists!')
        return validated_data
    def create(self, validated_data):
        user = CustomUser.objects.create_user(name=validated_data['name'],email=validated_data['email'],username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        return user


class SurveyourSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    taluka = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 
    phc = serializers.CharField(required =False,default="")
    name = serializers.CharField(required=False,allow_null=True)
    email = serializers.CharField(required=False,allow_null=True)
    masterSupervisor = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id','username', 'phone','password','confirm_password','masterSupervisor','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc','name','email')
        extra_kwargs = {'password': {'write_only': True}}
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data
    def validate(self, validated_data):
        if CustomUser.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('Username already exists!')
        return validated_data
    def create(self, validated_data):
        user = CustomUser.objects.create_user(name=validated_data['name'],masterSupervisor_id=validated_data['masterSupervisor'],email=validated_data['email'],username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        return user

class SurveyourRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    taluka = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 
    phc = serializers.CharField(required =False,default="")
    name = serializers.CharField(required=False,allow_null=True)
    email = serializers.CharField(required=False,allow_null=True)
    masterSupervisor = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id','username', 'phone','password','confirm_password','masterSupervisor_id','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc','name','email')
        extra_kwargs = {'password': {'write_only': True}}
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(name=validated_data['name'],email=validated_data['email'],username=validated_data['username'],masterSupervisor_id=validated_data['masterSupervisor_id'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        return user



class familymemberSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = familyMembers
        fields = '__all__'

class AllMedicalSurveySerializer(serializers.ModelSerializer):
    family_id =  serializers.CharField(source='family_head.unique_family_key',default='')
    memberAddress =AddressDetailSerializer(source='family_head.familyAddress',default='')
    # doctorConsultancy = doctorConsultancyserializers(suggestion_type='instance.suggestion_type',many=True)
    doctorConsultancy = doctorConsultancyserializers(many=True)
    # doctorConsultancy = serializers.SerializerMethodField()
    class Meta:
        model = familyMembers
        fields = '__all__'

    # def get_doctorConsultancy(self,obj):
        # data=doctorConsultancy.objects.filter(id=obj.id,suggestion_type=obj.suggestion_type,isCompleted=True)
        # return doctorConsultancyserializers(data,many=True).data

class specialistConsultancyserializers(serializers.ModelSerializer):
    class Meta:
        model = specialistConsultancy
        fields = '__all__'

class SpecialistCitizenSerializer(serializers.ModelSerializer):
    family_id =  serializers.CharField(source='family_head.unique_family_key',default='')
    memberAddress =AddressDetailSerializer(source='family_head.familyAddress',default='')
    # doctorConsultancy = doctorConsultancyserializers(suggestion_type='instance.suggestion_type',many=True)
    specialistDoctorConsultancy = specialistConsultancyserializers(many=True)
    # doctorConsultancy = serializers.SerializerMethodField()
    class Meta:
        model = familyMembers
        fields = '__all__'


    # def get_doctorConsultancy(self,obj):
        # data=doctorConsultancy.objects.filter(id=obj.id,suggestion_type=obj.suggestion_type,isCompleted=True)
        # return doctorConsultancyserializers(data,many=True).data

class phcConsultancySerializers(serializers.ModelSerializer):
    class Meta:
        model = phcConsultancy
        fields = '__all__'

class PhcCitizenSerializer(serializers.ModelSerializer):
    family_id =  serializers.CharField(source='family_head.unique_family_key',default='')
    memberAddress =AddressDetailSerializer(source='family_head.familyAddress',default='')
    # doctorConsultancy = doctorConsultancyserializers(suggestion_type='instance.suggestion_type',many=True)
    phcDoctorConsultancy = phcConsultancySerializers(many=True)
    # doctorConsultancy = serializers.SerializerMethodField()
    class Meta:
        model = familyMembers
        fields = '__all__'

class PhcPatientSerializer(serializers.ModelSerializer):
    family_id =  serializers.CharField(source='family_head.unique_family_key',default='')
    memberAddress =AddressDetailSerializer(source='family_head.familyAddress',default='')
    # doctorConsultancy = doctorConsultancyserializers(suggestion_type='instance.suggestion_type',many=True)
    phcDoctorConsultancy = phcConsultancySerializers(many=True)
    specialistDoctorConsultancy = specialistConsultancyserializers(many=True)
    # doctorConsultancy = serializers.SerializerMethodField()
    class Meta:
        model = familyMembers
        fields = '__all__'


class HospitalCitizenSerializer(serializers.ModelSerializer):
    family_id =  serializers.CharField(source='family_head.unique_family_key',default='')
    memberAddress =AddressDetailSerializer(source='family_head.familyAddress',default='')
    # doctorConsultancy = doctorConsultancyserializers(suggestion_type='instance.suggestion_type',many=True)
    doctorConsultancy = doctorConsultancyserializers(many=True)
    # hospitalConcernPerson = serializers.IntegerField(required=False)
    class Meta:
        model = familyMembers
        fields = '__all__'

        
class familyHeadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields

    family_head = familymemberSerializer(many=True)
    
    class Meta:
        model = familyHeadDetails
        fields = "__all__"


class AlldistrictHospitalList(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = districtHospital
        fields = '__all__'



class Alldistrict(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = district
        fields = '__all__'

class Alltaluka(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = taluka
        fields = '__all__'


class AllprimaryHealthCenter(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = primaryHealthCenter
        fields = '__all__'

class AllsubCenter(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = subCenter
        fields = '__all__'


class Allvillage(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = village
        fields = '__all__'

class AllmunicipalCorporation(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = municipalCorporation
        fields = '__all__'

class AllmcWard(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = mcWard
        fields = '__all__'


class AllmunicipalCouncil(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = municipalCouncil
        fields = '__all__'


class AllcantonmentBoard(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = cantonmentBoard
        fields = '__all__'



class AdminDashboardSerializer(serializers.Serializer):
    district = serializers.CharField(required=False)

    region_type = serializers.CharField(required=False)
    municipal_corporation = serializers.CharField(required=False)
    ward = serializers.CharField(required=False)
    municipal_council = serializers.CharField(required=False)
    taluka = serializers.CharField(required=False)
    phc = serializers.CharField(required=False)

    class Meta:
        fields = ['district','region_type','municipal_corporation','ward','municipal_council','taluka','phc']

class OtherUserSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    class Meta:
        model = CustomUser
        fields = ('id', 'name','username','email','phone','signup_date','login_date_time','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')

class ChangePasswordSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        fields = ['old_password','new_password']

class CustomSetPasswordSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    # old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()
    # user_id = serializers.IntegerField()
    class Meta:
        fields = ['confirm_password','new_password']


class EditProfileSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    # class Meta:
    #     fields = ['name','email']




class TalukadashboardSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    district = serializers.CharField()
    # taluka = serializers.CharField()

    # class Meta:
    #     fields = ['district']


class PhcdashboardSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    district = serializers.CharField()
    taluka = serializers.CharField()

    # class Meta:
    #     fields = ['district','taluka']


class ScdashboardSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    district = serializers.CharField()
    taluka = serializers.CharField()
    phc_name = serializers.CharField()

    # class Meta:
    #     fields = ['district','taluka','phc_name']





class CouncildashboardSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    district = serializers.CharField()

    # class Meta:
    #     fields = ['district']


class WarddashboardSerializer(serializers.Serializer):
    district = serializers.CharField()
    municipal_corporation = serializers.CharField()

    # class Meta:
    #     fields = ['district','municipal_corporation']



class DoctorAssignedSerializer(serializers.Serializer):
    familyMember_id = serializers.IntegerField()
    Doctor_id = serializers.IntegerField()


class CustomDashboardSerializer(serializers.Serializer):
    district = serializers.CharField(required =False,default="")

    region_type = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    taluka = serializers.CharField(required =False,default="")
    phc = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 

    # Doctor_id = serializers.IntegerField()



class CustomRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    taluka = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 
    phc = serializers.CharField(required =False,default="")
    class Meta:
        model = CustomUser
        fields = ('id','username', 'phone','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')
        extra_kwargs = {'password': {'write_only': True}}
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        return user

class HospitalRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    # taluka = serializers.CharField(required =False,default="")
    # municipal_corporation = serializers.CharField(required =False,default="")
    # ward = serializers.CharField(required =False,default="")
    # municipal_council = serializers.CharField(required =False,default="") 
    # phc = serializers.CharField(required =False,default="")
    concernedName = serializers.CharField(required=False,allow_null=True)
    concernedEmail = serializers.CharField(required=False,allow_null=True)
    concernedPhone = serializers.CharField(required=False,allow_null=True)
    # hospitalName = serializers.CharField(required=True,validators = [
    #         UniqueValidator(
    #             queryset=districtHospital.objects.all(),
    #             message='Already registered with this Hospital Name!'
    #             # fields=('hospitalName')
    #         )])
    hospitalName = serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        # fields = ('id','username', 'phone','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc','name','email','hospitalName')
        fields = ('id','username', 'concernedPhone','password','confirm_password','district','region_type','concernedName','concernedEmail','hospitalName')
        extra_kwargs = {'password': {'write_only': True}}
        
        # ]
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data
    def validate(self, validated_data):
        district_id = district.objects.filter(districtName=validated_data['district']).values_list('id',flat=True)
        if len(district_id)<1:
            raise serializers.ValidationError('District Not Found!')
        if districtHospital.objects.filter(hospitalName=validated_data['hospitalName']).exists():
            raise serializers.ValidationError('Already registered with this Hospital Name!')
        if CustomUser.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('Username already exists!')

        return validated_data
    def create(self, validated_data):
        district_id = district.objects.filter(districtName=validated_data['district']).values_list('id',flat=True)
        user = CustomUser.objects.create_user(name=validated_data['concernedName'],email=validated_data['concernedEmail'],username=validated_data['username'],phone=validated_data['concernedPhone'],password=validated_data['password'],confirm_password=validated_data['password'],district=validated_data['district'],region_type=validated_data['region_type'],hospitalName=validated_data['hospitalName'])
        districtHospital.objects.create(hospitalName=validated_data['hospitalName'],concernedPerson=user,hospitaldistrict_id=district_id[0])
        return user

class CustomSupervisorRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # temp = ["t1","t2","t3"]
    # group = serializers.CharField()
    username = serializers.CharField()
    taluka = serializers.CharField(required =False,default="")
    municipal_corporation = serializers.CharField(required =False,default="")
    ward = serializers.CharField(required =False,default="")
    municipal_council = serializers.CharField(required =False,default="") 
    phc = serializers.CharField(required =False,default="")
    class Meta:
        model = CustomUser
        fields = ('id','name','username', 'phone','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')
        extra_kwargs = {'password': {'write_only': True}}
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        # phone_exists = CustomUser.objects.filter(phone=phone)
        # if phone_exists:
        #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

        # return validated_data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        return user



from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = Group
        fields = '__all__'
        # fields = ('id', 'name','username','phone','signup_date','login_date_time','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')

class RolePermissionSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = RolePermissions
        fields = '__all__'

class UpdateRolePermissionSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = RolePermissions
        fields = ('id','status')

class MultiUpdateRolePermissionSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    roles=UpdateRolePermissionSerializer(many=True)
    class Meta:
        model = RolePermissions
        fields = ('roles',)
        
class CloseCaseSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = familyMembers
        fields = ['caseClosedReason','member_unique_id']
        
class NotificationAddressDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressDetails
        exclude = ("id","total_family_count","selfBookAppoinment","created_datetime","surveyor") 
class NotificationSerializer(serializers.ModelSerializer):
    family_id =  serializers.CharField(source='family_head.unique_family_key',default='')
    famAddress =NotificationAddressDetailSerializer(source='family_head.familyAddress',default='')
    
    class Meta:
        model = Notification
        fields = "__all__"




class NewCustomdashboardSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    region_type = serializers.CharField()
    district = serializers.CharField()
    municipal_corporation = serializers.CharField()
    ward = serializers.CharField()
    municipal_council = serializers.CharField()
    taluka = serializers.CharField()
    phc_name = serializers.CharField()

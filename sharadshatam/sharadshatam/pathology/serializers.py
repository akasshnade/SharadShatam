from rest_framework import serializers
from database.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.db.models import Q
# Register Serializer
# class PathlabRegisterSerializer(serializers.ModelSerializer):
#     # profile_images=Base64ImageField() # From DRF Extra Fields
    
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username','phone','password','confirm_password','district','taluka','municipal_corporation','ward','municipal_council','phc')
#         extra_kwargs = {'password': {'write_only': True}}
#         # phone = validated_data["phone"]
#         # print(phone,"*********************")
#         # phone_exists = CustomUser.objects.filter(phone=phone)
#         # if phone_exists:
#         #     raise serializers.ValidationError({"phone": "Phone Number Already Present."})

#         # return validated_data

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['phone'],confirm_password=validated_data['phone'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
#         return user


class PathLabLoginSerializer(serializers.Serializer):
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
                if not customuser.is_superuser:
                    # if customuser.is_verify:
                    if customuser.groups.filter(name='pathlab').exists():
                        return customuser
                    else:
                        raise serializers.ValidationError("UnAuthorized.") 
                    # else:
                    #     return serializers.ValidationError("User is Blocked. Please Contact Admin.")


                else:
                    raise serializers.ValidationError("Only Users are Allowed.")
            else:
                raise serializers.ValidationError("User os Blocked. Please Contact Admin.")
        else:
            raise serializers.ValidationError("Incorrect Credentials.")

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class PhlebotomistSerializer(serializers.ModelSerializer):
    unique_id = serializers.CharField(source='phlebotomist_info.unique_id')
    name = serializers.CharField(source='phlebotomist_info.name')
    # family_id = serializers.CharField(source='phlebotomist_info.family_head.unique_family_key')
    # citizen_id = serializers.CharField(source='phlebotomist_info.member_unique_id')
    district = serializers.CharField(source='phlebotomist_info.district')
    phone = serializers.CharField(source='phlebotomist_info.phone')
    region_type = serializers.CharField(source='phlebotomist_info.region_type')
    class Meta:
        model = Phlebotomist
        fields = '__all__'

class PhlebotomistListSerializer(serializers.ModelSerializer):
    unique_id = serializers.CharField(source='phlebotomist_info.unique_id')
    name = serializers.CharField(source='phlebotomist_info.name')
    # family_id = serializers.CharField(source='phlebotomist_info.family_head.unique_family_key')
    # citizen_id = serializers.CharField(source='phlebotomist_info.member_unique_id')
    region_type = serializers.CharField(source='phlebotomist_info.region_type')
    district = serializers.CharField(source='phlebotomist_info.district')
    municipal_corporation = serializers.CharField(source='phlebotomist_info.municipal_corporation')
    ward = serializers.CharField(source='phlebotomist_info.ward')
    municipal_council = serializers.CharField(source='phlebotomist_info.municipal_council')
    taluka = serializers.CharField(source='phlebotomist_info.taluka')
    phone = serializers.CharField(source='phlebotomist_info.phone')
    # parameterName = serializers.CharField()
    # parameterValue = serializers.CharField()
    class Meta:
        model = Phlebotomist
        fields = '__all__'


    
# class TestReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = testReport
#         fields = '__all__'

# class PatientTestReport
# Register Serializer
class PathlabRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    pathlab_name = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username','phone','password','region_type','confirm_password','district','taluka','municipal_corporation','ward','municipal_council','phc','pathlab_name','name','email')
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
        # user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        user = CustomUser.objects.create_user(username=validated_data['username'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['password'],region_type=validated_data['region_type'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'],name=validated_data['name'],email=validated_data['email'])
        pathlogy.objects.create(pathOwner=user,labName=validated_data['pathlab_name'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        phlebotomist_group = Group.objects.get(name='pathlab')
        phlebotomist_group.user_set.add(user)
        validated_data.pop('pathlab_name')
        validated_data.pop('email')
        validated_data.pop('name')
        return user


class PathLabLoginSerializer(serializers.Serializer):
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
                if not customuser.is_superuser:
                    # if customuser.is_verify:
                    return customuser
                    # else:
                    #     return serializers.ValidationError("User is Blocked. Please Contact Admin.")


                else:
                    raise serializers.ValidationError("Only Users are Allowed.")
            else:
                raise serializers.ValidationError("User os Blocked. Please Contact Admin.")
        else:
            raise serializers.ValidationError("Incorrect Credentials.")


class PhlebotomistRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    # pathlab = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username','phone','name','password','confirm_password','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc')
        extra_kwargs = {'password': {'write_only': True}}

        # return validated_data

    def create(self, validated_data):
        phone = validated_data["phone"]
        # print(phone,"*********************")
        phone_exists = CustomUser.objects.filter(Q(phone=phone)|Q(username=phone))
        if phone_exists:
            raise serializers.ValidationError({"phone": "Phone Number Already Present."})
        user = CustomUser.objects.create_user(username=validated_data['username'],name=validated_data['name'],phone=validated_data['phone'],password=validated_data['phone'],confirm_password=validated_data['phone'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],municipal_council=validated_data['municipal_council'],region_type=validated_data['region_type'],phc=validated_data['phc'])
        u =  self.context['request'].user
        # print(u.id,'----')
        # u=self.context["request.user"]
        pathlab_id = pathlogy.objects.filter(pathOwner_id=u.id).values_list('id',flat=True)
        if not pathlab_id:
            raise serializers.ValidationError( "Pathlab login required.")
        Phlebotomist.objects.create(phlebotomist_info=user,pathlab_id=pathlab_id[0])
        phlebotomist_group = Group.objects.get(name='phlebotomist')
        phlebotomist_group.user_set.add(user)
        # validated_data.pop('pathlab')
        return user

class PhlebotomistUpdateSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields

    class Meta:
        model = CustomUser
        fields = ('id', 'name','district','taluka','municipal_corporation','ward','municipal_council','phc','region_type')
        extra_kwargs = {'password': {'read_only': True}}
    def update(self,instance,validated_data):
        print(validated_data.items(),'===--',instance)
        isupdated =CustomUser.objects.filter(id=instance.id).update(name=validated_data['name'],district=validated_data['district'],taluka=validated_data['taluka'],municipal_corporation=validated_data['municipal_corporation'],ward=validated_data['ward'],region_type=validated_data['region_type'],municipal_council=validated_data['municipal_council'],phc=validated_data['phc'])
        # Phlebotomist.objects.filter(phlebotomist_info_id=instance.id).update(pathlab_id=validated_data['pathlab'])
        # validated_data.pop('pathlab')
        return isupdated

class PhlebotomistReadSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    pathlab = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'name','district','taluka','municipal_corporation','ward','municipal_council','phc','pathlab','phone','region_type')
        extra_kwargs = {'password': {'read_only': True}}
   
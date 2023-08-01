from rest_framework import serializers
from database.models import *
from django.contrib.auth import authenticate





# Register Serializer
class CitizenRegisterSerializer(serializers.ModelSerializer):
    # profile_images=Base64ImageField() # From DRF Extra Fields
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name','email','phone','password','confirm_password')
        extra_kwargs = {'password': {'write_only': True}}
       
     

    def validate_phone(self,value):
        # phone = validated_data["phone"]
        # print(phone,"*********************")
        phone=value
        phone_exists = CustomUser.objects.filter(phone=phone)
        if phone_exists:
            raise serializers.ValidationError("Phone Number Already Present.")

        return value

    def create(self, validated_data):
    #     phone = validated_data["phone"]
    #     # print(phone,"*********************")
    #     phone_exists = CustomUser.objects.filter(phone=phone)
    #     if phone_exists:

    #         raise serializers.ValidationError("Phone Number Already Present.")
        user = CustomUser.objects.create_user(name=validated_data['name'],email=validated_data['email'],username=validated_data['phone'],phone=validated_data['phone'],password=validated_data['password'],confirm_password=validated_data['confirm_password'])
        return user

class CitizenOtpVerifySerializer(serializers.ModelSerializer):
    # otp_owner = serializers.ReadOnlyField(source='CustomUser.phone')
    phone = serializers.CharField()
    creation_date_time = serializers.DateTimeField()
    class Meta:
        model = CustomUser
        fields = ('phone','otp','creation_date_time')

class FamilyHeadMemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = familyMembers
        # fields = '__all__'
        fields=('member_unique_id','member_name','member_gender','member_gender','member_age')

class CitizenLoginSerializer(serializers.Serializer):
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



class CitizenForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

    class Meta:
        fields = ['phone']


class CitizenSetNewPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        fields = ['phone','new_password','confirm_password']



class SurveyourCitizenClaimederializer(serializers.Serializer):
    familyMemberId = serializers.IntegerField()
    claimStatus = serializers.BooleanField()

    class Meta:
        fields = ['familyMemberId','claimStatus']
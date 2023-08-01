from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from database.serializers import *
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from knox.models import AuthToken
from rest_framework import generics, permissions
from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
import json
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# Create your views here.
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
import random
import os
import string
from datetime import datetime
import hmac
import hashlib
from django.conf import settings

from adminportal.serializers import NotificationSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

class TalentSearchpagination(PageNumberPagination):
    page_size = 5


def validate_token(nonce,timestamp,token):
    app_seceret = settings.PRIVATE_KEY
    access_token = settings.HASH_KEY
    data = app_seceret+access_token+timestamp 
    key_bytes= bytes(data , 'utf-8') # Commonly 'latin-1' or 'utf-8'
    data_bytes = bytes(nonce, 'utf-8') # Assumes `data` is also a string.
    signature = hmac.new(key_bytes, data_bytes , hashlib.sha256).hexdigest()
    message = ""
    result = hmac.compare_digest(signature,token)
    if result:
        message = "valid"
    else:
        message = "invalid"

    return message

# Create your views here.

import re
phone_re = re.compile(r'\d{10}$')

def only_numerics(phone):
    valid_phone = False
    if phone.isdigit():
        valid_phone = True
    else:
        valid_phone = False
    return valid_phone


def check_phone(phone):
    valid_phone = False
    if len(phone)==10:
        valid_phone = True
    else:
        valid_phone = False

    return valid_phone
        #    0 print "You have entered an invalid choice"

def createOtp():
    temp = 0
    temp = int(''.join([str(random.randint(0,10)) for _ in range(4)]))
    otpexist = CustomUser.objects.filter(otp=temp)
    if otpexist:
        temp = int(''.join([str(random.randint(0,10)) for _ in range(length)]))
    else:
        pass
        # temp = int(''.join([str(random.randint(0,10)) for _ in range(length)]))
    
    return temp




def passwordGen():
    chars = string.letters
    chars_len = len(chars)
    return str().join(chars[int(ord(c) / 256. * chars_len)] for c in os.urandom(6))

# class resendOtp(generics.GenericAPIView):
    
#     serializer_class = ResendOtpSerializer
#     parser_classes = [MultiPartParser]

#     def post(self, request):    
        
#         email = ''
#         user_id = 0
#         token = ""
#         otp =""
#         phone = 0

#         if not request.data:
#             validation_message ='Please provide data'
#             return Response({"responseCode":400, 'responseMessage': validation_message},status=status.HTTP_400_BAD_REQUEST)


#         if 'phone' in request.data:
#             phone = request.data["phone"]
        
#         # if 'otp' in request.data:
#         #     otp = request.data["otp"]

        
#         otp = ''.join(random.sample("0123456789", 6))
#         # message,send_status,random_otp=send_msg_otp_signup_verification(customuser.phone,customuser.name,otp)
#         # status = email(customuser.email,customuser.name,otp)
#         # print('Email OTP Status: ',status)
#         # print('OTP Status ')
#         # print(send_status)
#         # otp = "000000"
#         import datetime
#         expirey_date = datetime.datetime.now() + datetime.timedelta(seconds=150)
#         user_detail = CustomUser.objects.get(phone=phone)

#         # if lang!=user_detail["language_code"]:

#         save_otp = SendOtp.objects.filter(otp_owner__phone=phone).update(otp=otp,expirey_date=expirey_date)

#         validation_message = 'Successfully Send otp on Registered Mobile.'
#         return Response({"responseCode":200, 'responseMessage': validation_message},status=status.HTTP_200_OK)

class loginSendOtp(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Send Otp For Login
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = loginSendOtpSerializer
    parser_classes = [FormParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
            )
        ],
        
    )

    def post(self, request):    
        
        validation_status = 'error'
        validation_message = 'Error'        
        data = {}
        print(request.data.keys())

        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide phone'
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'phone' in request.data.keys(): 
            if request.data["phone"]=="":
                validation_message = "Please Enter Valid phone"
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

            phone = request.data["phone"]

            if only_numerics(phone)==False:
                validation_message = "Only digits Allowed"
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


            if check_phone(phone)==False:
                validation_message = "Only 10 digits Allowed"
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

                

            phoneAlreadyRegistered= CustomUser.objects.filter(phone=phone)
            if not phoneAlreadyRegistered:

                validation_message = "Please register yourself with local PHC."
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

            # print(phone)

            user_exists = CustomUser.objects.filter(phone=phone)
            # print(user_exists[0].phone,"phone number")

            if user_exists:
    
                validation_message = "Otp Send on your phone.Existing"
                # data['id'] = user_exists[0].id
                import datetime

                otp = "000000"
                now = datetime.datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                        # import datetime
                expirey_date = now + datetime.timedelta(seconds=150)
                updateOtp = CustomUser.objects.filter(phone=phone).update(otp=otp,created_date=dt_string,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))
                data["phone"] =phone
            # else:
            #     otp="000000"
            #     import datetime
            #     validation_message = 'Otp Send on your phone.New'
            #     now = datetime.datetime.now()
            #     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            #             # import datetime
            #     expirey_date = now + datetime.timedelta(seconds=150)

            #     insertOtp = sendRegisterOtp(phone=phone,otp=otp,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))
            #     insertOtp.save()
            #     data["phone"] =phone
        return Response({'responseCode': 200, 'responseMessage': validation_message,'responseData':data},status = status.HTTP_200_OK)



class UpdateSurveyorProfileDetails(GenericAPIView):
    """
    Update Sureyor Profile Details
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UpdateSurveyourUserSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",   
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,   
                description="token",
                required=True,
                default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
            )
        ],
        
    )

    def get_object(self, pk):
        return CustomUser.objects.get(pk=pk)


    def patch(self, request,pk, format=None):
        # famhead=familyhead.objects.filter(unique_family_key=pk)
        testmodel_object = self.get_object(pk)
        serializer = UpdateSurveyourUserSerializer(testmodel_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class loginOtpVerify(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Login Otp Verify
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = OtpVerifySerializer
    parser_classes = [FormParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
            )
        ],
        
    )

    def post(self, request):    
        
        email = ''
        user_id = 0
        token = ""
        # created_date = ""
        otp =""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide otp'
            return Response({'status': 'error', 'message': validation_message})

        if 'phone' in request.data and request.data["phone"]=="":
            validation_message = "Please Enter phone"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'phone' in request.data:
            phone = request.data["phone"]
        
        if 'otp' in request.data:
            otp = request.data["otp"]
        # import datetime
        data={}
        user_exists = CustomUser.objects.filter(phone=phone,otp=otp)
        # print(user_exists,"**************")
        # timezone = user_exists[0].expirey_date.tzinfo
        # curr_date_time = datetime.now(timezone)
        # if curr_date_time < user_exists[0].expirey_date:

        #     validation_message = 'OTP Expired'

        #     return Response({'responseCode': 400, 'responseMessage':"User Not Found"},status = status.HTTP_400_BAD_REQUEST)

        if user_exists:



   
            temp = user_exists[0].id
            print(temp)
            customuser = CustomUser.objects.get(id=user_exists[0].id)
            user_exists.update(otp_verified=True,otp="")
            _ ,token = AuthToken.objects.create(customuser)
            data = SurveyourUserSerializer(customuser,context=self.get_serializer_context()).data
            data["token"] = token
            validation_status = 'Success'
            validation_message = 'OTP Verified '
            # CustomUser.objects.filter(phone=phone).update(is_verify = True,is_active=True)
            # print(token)
            return Response({'responseCode': 200, 'responseMessage': validation_message,"responseData":data},status=status.HTTP_200_OK)

        else:
            return Response({'responseCode': 400, 'responseMessage':"User Not Found"},status = status.HTTP_400_BAD_REQUEST)



class SurveyourSetNewPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Set new Password after first Login. 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = SetNewPasswordSerializer
    parser_classes = [FormParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    def post(self, request):    
        

        confirm_password = ""
        new_password = ""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})

        if 'new_password' in request.data and request.data["new_password"]=="":
            validation_message = "Please Enter new password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'confirm_password' in request.data and request.data["confirm_password"]=="":
            validation_message = "Please Enter  Confirm password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if request.data["new_password"]!=request.data["confirm_password"]:
            validation_message = "New Password and Confirm password must be same."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        
        if request.data["new_password"]!="":
            new_password = request.data["new_password"]

        if request.data["confirm_password"]!="":
            confirm_password = request.data["confirm_password"]


        # import datetime
        data={}
        user = request.user.id
        newpassword = make_password(new_password)
        user_exists = CustomUser.objects.filter(id=user).update(password=newpassword,confirm_password=new_password)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password","responseData":data},status=status.HTTP_200_OK)






class SurveyourClaimCitizen(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Claim Citizen. 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = SurveyourCitizenClaimederializer
    # parser_classes = [FormParser]s
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
            )
        ],
        
    )

    def post(self, request):    
        

        confirm_password = ""
        new_password = ""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})

        if 'familyMemberId' in request.data and request.data["familyMemberId"]=="":
            validation_message = "Please pass Family Member Id"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'claimStatus' in request.data and request.data["claimStatus"]=="":
            validation_message = "Please Enter Claim Status"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        
        if request.data["familyMemberId"]!="":
            familyMemberId = request.data["familyMemberId"]

        if request.data["claimStatus"]!="":
            claimStatus = request.data["claimStatus"]


        # import datetime
        data={}
        user = request.user.id

        claimstatus = familyMembers.objects.filter(id  =familyMemberId).update(isClaimed = claimStatus,claimedBy_id = user,familysurveyor_id=user)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully Claimed Citizen"},status=status.HTTP_200_OK)


class SurveyourForgotPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = [permissions.AllowAny,]
    serializer_class = SurveyourForgotPasswordSerializer
    parser_classes = [FormParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )        ],
        
    )
    def post(self, request):    
        
        validation_status = 'error'
        validation_message = 'Error'        
        data = {}
        print(request.data.keys())
        if not request.data:
            validation_message = 'Please provide phone'
            return Response({'status': 'error', 'message': validation_message})

        if 'phone' in request.data.keys(): 
            if request.data["phone"]=="":
                validation_message = "Please Enter Valid phone"
                return Response({'status': 'error', 'message': validation_message})

            # print(phone)
            phone = request.data["phone"]

            if only_numerics(phone)==False:
                validation_message = "Only digits Allowed"
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


            if check_phone(phone)==False:
                validation_message = "Only 10 digits Allowed"
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

            user_exists = CustomUser.objects.filter(phone=phone)
            # print(user_exists[0].phone,"phone number")

            if user_exists:
                import datetime

                otp = "000000"
                now = datetime.datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                        # import datetime
                expirey_date = now + datetime.timedelta(seconds=150)
                updateOtp = CustomUser.objects.filter(phone=phone).update(otp=otp,created_date=dt_string,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))
                data["phone"] = phone
                return Response({'responseCode': 200, 'responseMessage': "OTP Send on Registered Phone number.","responseData":data},status=status.HTTP_200_OK)

            else:

                validation_message = 'Invalid User'
                return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        # return Response({'status': validation_status, 'message': validation_message})
 


class SurveyourForgotPasswordOtpVerify(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Forgot Password Otp Verify
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = OtpVerifySerializer
    parser_classes = [FormParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    def post(self, request):    
        
        email = ''
        user_id = 0
        token = ""
        # created_date = ""
        otp =""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide otp'
            return Response({'status': 'error', 'message': validation_message})

        if 'phone' in request.data and request.data["phone"]=="":
            validation_message = "Please Enter phone"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        phone = request.data["phone"]

        if only_numerics(phone)==False:
            validation_message = "Only digits Allowed"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if check_phone(phone)==False:
            validation_message = "Only 10 digits Allowed"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'phone' in request.data:
            phone = request.data["phone"]
        
        if 'otp' in request.data:
            otp = request.data["otp"]
        # import datetime
        data={}
        user_exists = CustomUser.objects.filter(phone=phone,otp=otp)
        print(user_exists,"**************")

        if user_exists:   
            temp = user_exists[0].id
            print(temp)
            customuser = CustomUser.objects.get(id=user_exists[0].id)
            user_exists.update(otp_verified=True,otp="")
            # _ ,token = AuthToken.objects.create(customuser)
            # data = UserSerializer(customuser,context=self.get_serializer_context()).data
            # data["token"] = token
            validation_status = 'Success'
            validation_message = 'OTP Verified '
            # CustomUser.objects.filter(phone=phone).update(is_verify = True,is_active=True)
            # print(token)
            return Response({'responseCode': 200, 'responseMessage': validation_message},status=status.HTTP_200_OK)

        else:
            return Response({'responseCode': 400, 'responseMessage':"User Not Found"},status = status.HTTP_400_BAD_REQUEST)


class UpdatePartialMedicalSurvey(GenericAPIView):
    """
    create a new Medical Survey
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = familyHeadSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",   
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,   
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def patch(self, request,pk, format=None):
        famhead=familyhead.objects.filter(unique_family_key=pk)
        serializer = familyHeadSerializer(famhead,data=request.data)
        if serializer.is_valid():
            serializer.save(surveyor=request.user)
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

class NewUpdatePartialMedicalSurvey(GenericAPIView):
    """
    Update Partial Record
    """
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UpdatePartialFamilyMemberSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",   
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,   
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        # famhead=familyhead.objects.filter(unique_family_key=pk)
        serializer = UpdatePartialFamilyMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"responseCode":200, 'responseMessage': "Successfully Updated"},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class UpdateFamilyHeadDetails(GenericAPIView):
    """
    Update Family Head Details
    """
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UpdateFamilyHeadAddressDetailSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",   
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,   
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        # famhead=familyhead.objects.filter(unique_family_key=pk)


        serializer = UpdateFamilyHeadAddressDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"responseCode":200, 'responseMessage': "Successfully Updated"},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class UpdateFamilyMemberDetails(GenericAPIView):
    """
    Update Family Member Details
    """
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UpdateFamilyMemberDataSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",   
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,   
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        # famhead=familyhead.objects.filter(unique_family_key=pk)


        serializer = UpdateFamilyMemberDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"responseCode":200, 'responseMessage': "Successfully Updated"},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)




class CompleteSelfSurveyDetails(GenericAPIView):
    """
    Complete Self Survey
    """
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UpdateSelfRegisteredFamilyMemberSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",   
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,   
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        # famhead=familyhead.objects.filter(unique_family_key=pk)


        serializer = UpdateSelfRegisteredFamilyMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"responseCode":200, 'responseMessage': "Successfully Updated"},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class SurveyourForgotPasswordSetNewPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Forgot Password Set New Password. 
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = SurveyourSetNewPasswordSerializer
    parser_classes = [FormParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    def post(self, request):    
        

        confirm_password = ""
        new_password = ""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})
        phone = request.data["phone"]

        if only_numerics(phone)==False:
            validation_message = "Only digits Allowed"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if check_phone(phone)==False:
            validation_message = "Only 10 digits Allowed"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'new_password' in request.data and request.data["new_password"]=="":
            validation_message = "Please Enter new password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        if 'confirm_password' in request.data and request.data["confirm_password"]=="":
            validation_message = "Please Enter  Confirm password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if request.data["new_password"]!=request.data["confirm_password"]:
            validation_message = "New Password and Confirm password must be same."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        
        if request.data["new_password"]!="":
            new_password = request.data["new_password"]

        if request.data["confirm_password"]!="":
            confirm_password = request.data["confirm_password"]


        # import datetime
        data={}
        # user = request.user.id
        newpassword = make_password(new_password)
        user_exists = CustomUser.objects.filter(phone=phone).update(password=newpassword,confirm_password=new_password)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password","responseData":data},status=status.HTTP_200_OK)

from rest_framework import serializers, status, views

class MedicalSurvey(GenericAPIView):
    """
    create a new Medical Survey
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = familyHeadSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        serializer = familyHeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(surveyor=request.user)
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)




#############################


class InsertAddress(GenericAPIView):
    """
   Insert Family Head Detail
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InsertAddressDetails
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        serializer = InsertAddressDetails(data=request.data)
        print(serializer,"*********")
        if serializer.is_valid():
            serializer.save(surveyor_id = self.request.user.id)
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class InsertfamilyHead(GenericAPIView):
    """
   Insert Family Head Detail
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewfamilymemberSerializer
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        serializer = NewfamilymemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer,"*******************")

            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

from rest_framework.pagination import PageNumberPagination
class GetSurveyourMedicalSurveyList(GenericAPIView):
    """
    All Survey List
    """
    queryset = familyHeadDetails.objects.all().order_by('-id')

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewfamilyHeadSerializer
    # pagination_class = PageNumberPagination
    # parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # # filterset_fields = ('surveyCompleted', 'district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)
    # # filterset_fields = ('Address__district','Address__region_type','Address__municipal_corporation','Address__ward','Address__municipal_council','Address__taluka','Address__village','Address__phc','Address__sc',)
    filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','FamilyCompleted','selfBookAppointment','surveyCompleted','labsampleTaken')
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )
    
    def get(self, request, format=None):


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)




class SurveyourSurveyList(GenericAPIView):
    """
    Surveyour Wise Medical Survey List
    """
    queryset = familyHeadDetails.objects.all()

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewfamilyHeadSerializer
    # pagination_class = PageNumberPagination
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # # filterset_fields = ('surveyCompleted', 'district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)
    # # filterset_fields = ('Address__district','Address__region_type','Address__municipal_corporation','Address__ward','Address__municipal_council','Address__taluka','Address__village','Address__phc','Address__sc',)
    filterset_fields = ('selfBookAppointment','family_head_member__isClaimed','familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='nonce', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Nonce",
                required=True,
                default="12345654"
            ),

            openapi.Parameter(
                name='timestamp', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                # format="date-time",	
                description="Timestamp",
                required=True,
                default="12345654"
            ),
            openapi.Parameter(
                name='token', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,	
                description="token",
                required=True,
                default="8443ffba3dc434f6adb593702c9ebd4b70ade6a810e1eca9af7b587652615639"
            )
        ],
        
    )
    def get(self, request, format=None):

        print("********",self.request.user.id)
        qs = familyHeadDetails.objects.filter(surveyDoneBy_id=self.request.user.id)
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)











class SurveyourRegisterAPI(generics.GenericAPIView):
    serializer_class = SurveyourRegisterSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        phone = request.data["phone"]
        if 'phone' in request.data and request.data["phone"]=="":
            validation_message = "Please Enter phone"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        

        if only_numerics(phone)==False:
            validation_message = "Only digits Allowed"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if check_phone(phone)==False:
            validation_message = "Only 10 digits Allowed"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        print(request.data,"**********************&")
        if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)
            from datetime import datetime

            # datetime object containing current date and time
            now = datetime.now()
            
            print("now =", now)

            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            npass = make_password("123456")
            user = serializer.save(username=request.data["phone"],password=npass,confirm_password="123456")
            user.login_date_time=dt_string
            group = Group.objects.get(name="surveyour")
            group.user_set.add(user)

            return Response({
            "responseCode":200,
            # "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
        else:
            print(type(serializer.errors))
            return Response({"responseCode":400,"responseMessage":serializer.errors["non_field_errors"][0]},status=status.HTTP_400_BAD_REQUEST)



class GetLocationData(generics.GenericAPIView):
    
    def get(self,request,*args,**kwargs):
        ty = settings.BASE_DIR.joinpath('static', 'data.txt')
        # user = self.request.user.id
        with open(ty) as json_file:
            data = json.load(json_file)

        return Response({
                    "status":"Success",
                    "Message":"Successfully Fetched All Records",
                    "data":data,
        })

# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     parser_classes = [MultiPartParser]


#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             customuser = serializer.validated_data
#             _, token = AuthToken.objects.create(customuser)
#             data = UserSerializer(customuser,context=self.get_serializer_context()).data
#             print(data,"*********************^^^^^&")
#             from datetime import datetime

#             # datetime object containing current date and time
#             now = datetime.now()
            
#             print("now =", now)

#             # dd/mm/YY H:M:S
            
#             # dt_string = now.strftime("YYYY-MM-DD HH:MM :ss")

#             dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#             print(dt_string,"@@@@@@@@@@@##########")
#             # user = serializer.save()
#             temp = CustomUser.objects.filter(id=customuser.id).update(login_date_time=now)
#             # customuser.login_date_time=dt_string
#             groups=customuser.groups.values_list('name',flat = True)
#             print(groups)
#             data["user_group"] = groups
#             data["token"]=token
   
#             return Response({
#                 "responseCode":200,
#                 "responseData":data
                
#                 },status=status.HTTP_200_OK)
#         else:
#             print(serializer)
#             print(serializer.errors)

#             return Response({
#                "responseCode":400,
#                "responseMessage":serializer.errors["non_field_errors"][0],
#                 },status=status.HTTP_400_BAD_REQUEST)


class GetAllPathologyList(GenericAPIView):
    """
    List all Pathology
    """
    queryset = pathlogy.objects.all()

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllPathologySerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('surveyCompleted', 'district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)
    # filterset_fields = ('Address__district','Address__region_type','Address__municipal_corporation','Address__ward','Address__municipal_council','Address__taluka','Address__village','Address__phc','Address__sc',)
    filterset_fields = ('district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']

    def get(self, request, format=None):


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class NotificationListAPI(generics.GenericAPIView):
    queryset = Notification.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NotificationSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # # filterset_fields = ('surveyCompleted', 'district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc')
    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']

    def get(self, request, format=None):

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class GetAllLabTestList(GenericAPIView):
    """
    List all Pathology
    """
    queryset = TestRange.objects.all()

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = TestRangeSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # # filterset_fields = ('surveyCompleted', 'district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)
    # # filterset_fields = ('Address__district','Address__region_type','Address__municipal_corporation','Address__ward','Address__municipal_council','Address__taluka','Address__village','Address__phc','Address__sc',)
    # filterset_fields = ('district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']

    def get(self, request, format=None):


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

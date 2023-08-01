from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from seniorcetizen.serializers import *
from adminportal.serializers import *
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
from database.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.
from rest_framework.parsers import FormParser,MultiPartParser
import random
import os
import string
from datetime import datetime
import hmac
import hashlib
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from adminportal.paginations import CustomPagination
from django.db.models import Count
from rest_framework import filters
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


class DoctorRegisterAPI(generics.GenericAPIView):
    serializer_class = phcRegisterSerializer
    parser_classes = [MultiPartParser]
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

    def post(self, request, *args, **kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

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
            user = serializer.save()
            user.login_date_time=dt_string
            group = Group.objects.get(name="doctor")
            group.user_set.add(user)

            return Response({
            "responseCode":200,
            # "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
        else:
            print(type(serializer.errors))
            return Response({"responseCode":400,"responseMessage":serializer.errors["non_field_errors"][0]},status=status.HTTP_400_BAD_REQUEST)


class DoctorOtpVerify(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Citizen Otp Verify
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenOtpVerifySerializer
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
        print(user_exists,"**************")
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
            data = UserSerializer(customuser,context=self.get_serializer_context()).data
            data["token"] = token
            validation_status = 'Success'
            validation_message = 'OTP Verified '
            # CustomUser.objects.filter(phone=phone).update(is_verify = True,is_active=True)
            # print(token)
            return Response({'responseCode': 200, 'responseMessage': validation_message,"responseData":data},status=status.HTTP_200_OK)

        else:
            return Response({'responseCode': 400, 'responseMessage':"User Not Found"},status = status.HTTP_400_BAD_REQUEST)

class CompleteCaseAPI(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated,]
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
    def post(self, request,pk, format=None):
        dc=doctorConsultancy.objects.filter(id=pk).update(isCompleted=True)
        if dc:
            return Response({"responseCode":200, 'responseMessage': "Case Resolved"},status=status.HTTP_200_OK)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class DoctorLoginAPI(generics.GenericAPIView):
    serializer_class = CitizenLoginSerializer
    parser_classes = [MultiPartParser]
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


    def post(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data
            _, token = AuthToken.objects.create(customuser)
            data = UserSerializer(customuser,context=self.get_serializer_context()).data
            print(data,"*********************^^^^^&")
            from datetime import datetime

            # datetime object containing current date and time
            now = datetime.now()
            
            print("now =", now)

            # dd/mm/YY H:M:S
            
            # dt_string = now.strftime("YYYY-MM-DD HH:MM :ss")

            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print(dt_string,"@@@@@@@@@@@##########")
            # user = serializer.save()
            temp = CustomUser.objects.filter(id=customuser.id).update(login_date_time=now)
            # customuser.login_date_time=dt_string
            groups=customuser.groups.values_list('name',flat = True)
            print(groups)
            data["user_group"] = groups
            data["token"]=token
   
            return Response({
                "responseCode":200,
                "responseData":data
                
                },status=status.HTTP_200_OK)
        else:
            print(serializer)
            print(serializer.errors)

            return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)




class DoctorForgotPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenForgotPasswordSerializer
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
 


class DoctorForgotPasswordOtpVerify(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Forgot Password Otp Verify
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenOtpVerifySerializer
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



class DoctorForgotPasswordSetNewPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Forgot Password Set New Password. 
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenSetNewPasswordSerializer
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


class DoctorConsultancy(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Doctor Gives Remarks on Patients Report 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = DoctorConsultancySerializer
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
        
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})
        phone = request.data["phone"]

        if request.data["report"]=="":
            validation_message = "please provide report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        chk_report = testReport.objects.filter(id=request.data["report"])

        if chk_report:
            pass
        else:
            validation_message = "please provide valid report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if request.data["docpatient"]=="":
            validation_message = "please provide patient id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        chk_patients = familyMembers.objects.filter(id=request.data["docpatient"])

        if chk_patients:
            pass
        else:
            validation_message = "please provide valid patients id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)



        if request.data["doctorRemarks"]=="":
            validation_message = "please provide Remarks."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        
        save_doc = doctorConsultancy(report_id = request.data["report"],docpatient = request.data["report"],assignedDoctor = request.user.id )
        save_doc.save()
         
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password","responseData":data},status=status.HTTP_200_OK)

class SuggestToCitizen(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated,]
    serializer_class = SuggestToCitizenSerializers
    parser_classes = [MultiPartParser]
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
    def post(self, request, format=None):
        serializer = SuggestToCitizenSerializers(data=request.data)
        if serializer.is_valid():
            doctorConsultancy.objects.filter(docpatient_id=request.data.get('docpatient_id')).update(isCompleted=True)
            serializer.save(DoctorassignedBy=request.user)
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

def validate_file_extension2(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    # valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png']
    if not ext.lower() in valid_extensions:
        # return False
        msg='Unsupported file extension! Please upload files with '+" ".join(valid_extensions)+' extension'
        return {'resData':value,'resCode':400,'resMsg':msg} 
        # return Response({"responseCode":400, 'responseMessage': msg},status=status.HTTP_400_BAD_REQUEST)
        # raise ValidationError('Unsupported file extension! Please upload files with .pdf, .doc, .docx,.jpg,.png, extension')
    return {'resData':value,'resCode':200,'resMsg':'Success'}

class PhcSuggestToCitizen(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated,]
    serializer_class = PhcSuggestToCitizenSerializers
    parser_classes = [MultiPartParser]
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
    def patch(self, request, format=None):
        from datetime import datetime,date,time
        # data=dict(request.data)
        # print(data,'====')
        docpatient_id=request.data.get('docpatient')
        phcDoctor_id = request.data.get('phcDoctor')
        suggestion_type = request.data.get('suggestion_type')

        # print(docpatient_id,'===',phcDoctor_id)
        isPhcExist=phcConsultancy.objects.filter(docpatient_id=docpatient_id,phcDoctor_id=phcDoctor_id)
        # hc
        if isPhcExist:
            # print('-----------')
            isPhcExist.update(isPending=False)
            if isPhcExist[0].isMedication == True:
                isPhcExist.update(
                    medicationClosedDate = datetime.now()   
                    )
            if isPhcExist[0].phcConsultation == True:
                isPhcExist.update(
                    phcConsultationClosedDate = datetime.now()   
                    )
            if suggestion_type.lower() == 'medication':
                fileUpload = request.FILES.get('fileUpload')
                if fileUpload:
                    fu=validate_file_extension2(fileUpload)

                    if fu['resCode'] == 400 :
                            return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                    isPhcExist.update(
                        isMedication=True,
                        medicationRemarks = request.data.get('medicationRemarks'),
                        medicationDate=datetime.now(),
                        suggestion_type=suggestion_type.capitalize(),
                        fileUpload = fu['resData']
                        )
                else:
                    isPhcExist.update(
                        isMedication=True,
                        medicationRemarks = request.data.get('medicationRemarks'),
                        medicationDate=datetime.now(),
                        suggestion_type=suggestion_type.capitalize()
                        # fileUpload = fu['resData']
                        )
                familyMembers.objects.filter(id = docpatient_id).update(
                current_isPending=False,
                current_isMedication=True,
                current_phcConsultation=False
                )
            elif suggestion_type.lower() == 'consultation':
                fileUpload = request.FILES.get('consultationFileUpload')
                if fileUpload:
                    fu=validate_file_extension2(fileUpload)
                    if fu['resCode'] == 400 :
                            return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                    isPhcExist.update(
                        phcConsultation=True,
                        appointDate = datetime.today(),
                        appointTime=datetime.now(),
                        consultationphcRemarks = request.data.get('consultationphcRemarks'),
                        phcConsultationDate= datetime.now(),
                        suggestion_type=suggestion_type.capitalize(),
                        consultationFileUpload = fu['resData']   
                        )
                else:
                    isPhcExist.update(
                        phcConsultation=True,
                        appointDate = datetime.today(),
                        appointTime=datetime.now(),
                        consultationphcRemarks = request.data.get('consultationphcRemarks'),
                        phcConsultationDate= datetime.now(),
                        suggestion_type=suggestion_type.capitalize()
                        # consultationFileUpload = fu['resData']   
                        )
                familyMembers.objects.filter(id = docpatient_id).update(
                current_isPending=False,
                current_isMedication=False,
                current_phcConsultation=True
                )
            elif suggestion_type.lower() == 'specialist':
                     specialistConsultancy.objects.create(
                        specialist_docpatient_id=docpatient_id,
                        specialistDoctor_id=phcDoctor_id,
                        # )
                    # isPhcExist.update(
                        specialist_isPending=True,
                        specialist_DoctorassignedBy=request.user
                        # specialist_medicationRemarks = request.data.get('specialist_medicationRemarks'),
                        # specialist_medicationDate=datetime.now(),
                        # specialist_suggestion_type=suggestion_type.capitalize()
                        )
                     familyMembers.objects.filter(id = docpatient_id).update(
                        current_isPending=False,
                        current_isMedication=False,
                        current_phcConsultation=False,
                        current_isElderline=False,
                        current_isHospitalisation=False,
                        current_isSpecialistMedication=False,
                        current_specialistConsultation=True

                    )
            elif suggestion_type.lower() == 'hospitalization':
                    isPhcExist.update(
                    isHospitalisation=True,
                    hospitalizationRemarks = request.data.get('hospitalizationRemarks'),
                    hospitalisationDate=datetime.now(),
                    suggestion_type=suggestion_type.capitalize()
                    )
                    familyMembers.objects.filter(id = docpatient_id).update(
                        current_isPending=False,
                        current_isMedication=False,
                        current_phcConsultation=False,
                        current_isElderline=False,
                        current_isHospitalisation=True,
                        current_isSpecialistMedication=False,
                        current_specialistConsultation=False

                    )
            elif suggestion_type.lower() == 'close':
                isPhcExist.update(
                    isCaseClosed=True,
                    current_isPending=False,
                current_isMedication=False,
                current_phcConsultation=False
                    )
                familyMembers.objects.filter(id = docpatient_id).update(
                     current_isPending=False,
                current_isMedication=False,
                current_phcConsultation=False,
                isCaseClosed=True
                    )
            # serializer = PhcSuggestToCitizenSerializers(isPhcExist,data=request.data)
            # if serializer.is_valid():
            #     isPhcExist.update(isCompleted=True)
            #     serializer.save()
            
            return Response({"responseCode":200, 'responseMessage': "Success"},status=status.HTTP_200_OK)

        else:
            # isPhcExist.update()
            serializer = PhcSuggestToCitizenSerializers(data=request.data)
            if serializer.is_valid():
                if suggestion_type.lower() == 'medication':
                    fileUpload = request.FILES.get('fileUpload')
                    if fileUpload:
                        fu=validate_file_extension2(fileUpload)
                        if fu['resCode'] == 400 :
                            return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                        phcConsultancy.objects.create(
                            docpatient_id=docpatient_id,
                            phcDoctor_id=phcDoctor_id,
                            # )
                        # isPhcExist.update(
                            isMedication=True,
                            medicationRemarks = request.data.get('medicationRemarks'),
                            medicationDate=datetime.now(),
                            suggestion_type=suggestion_type.capitalize(),
                            fileUpload = fu['resData']
                            )
                    else:
                        phcConsultancy.objects.create(
                            docpatient_id=docpatient_id,
                            phcDoctor_id=phcDoctor_id,
                            # )
                        # isPhcExist.update(
                            isMedication=True,
                            medicationRemarks = request.data.get('medicationRemarks'),
                            medicationDate=datetime.now(),
                            suggestion_type=suggestion_type.capitalize()
                            # fileUpload = fu['resData']
                            )
                    familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isMedication=True,
                    current_phcConsultation=False,
                    current_isElderline=False,
                    current_isHospitalisation=False,
                    current_isSpecialistMedication=False,
                    current_specialistConsultation=False

                    )
                elif suggestion_type.lower() == 'consultation':
                    fileUpload = request.FILES.get('consultationFileUpload')
                    if fileUpload:
                        fu=validate_file_extension2(fileUpload)
                        if fu['resCode'] == 400 :
                                return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                        phcConsultancy.objects.create(
                        docpatient_id=docpatient_id,
                        phcDoctor_id=phcDoctor_id,
                        # )
                    # isPhcExist.update(
                            phcConsultation=True,
                            appointDate = datetime.today(),
                            appointTime=datetime.now(),
                            consultationphcRemarks = request.data.get('consultationphcRemarks'),
                            phcConsultationDate= datetime.now(),
                            suggestion_type=suggestion_type.capitalize(),
                            consultationFileUpload = fu['resData']   
                            )
                    else:
                        phcConsultancy.objects.create(
                        docpatient_id=docpatient_id,
                        phcDoctor_id=phcDoctor_id,
                        # )
                    # isPhcExist.update(
                            phcConsultation=True,
                            appointDate = datetime.today(),
                            appointTime=datetime.now(),
                            consultationphcRemarks = request.data.get('consultationphcRemarks'),
                            phcConsultationDate= datetime.now(),
                            suggestion_type=suggestion_type.capitalize()
                            # consultationFileUpload = fu['resData']   
                            )
                    familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isMedication=False,
                    current_phcConsultation=True,
                    current_isElderline=False,
                    current_isHospitalisation=False,
                    current_isSpecialistMedication=False,
                    current_specialistConsultation=False

                    )
                elif suggestion_type.lower() == 'specialist':
                     specialistConsultancy.objects.create(
                        specialist_docpatient_id=docpatient_id,
                        specialistDoctor_id=phcDoctor_id,
                        # )
                    # isPhcExist.update(
                        specialist_isPending=True,
                        specialist_DoctorassignedBy=request.user
                        # specialist_medicationRemarks = request.data.get('specialist_medicationRemarks'),
                        # specialist_medicationDate=datetime.now(),
                        # specialist_suggestion_type=suggestion_type.capitalize()
                        )
                     familyMembers.objects.filter(id = docpatient_id).update(
                        current_isPending=False,
                        current_isMedication=False,
                        current_phcConsultation=False,
                        current_isElderline=False,
                        current_isHospitalisation=False,
                        current_isSpecialistMedication=False,
                        current_specialistConsultation=True

                    )
                elif suggestion_type.lower() == 'hospitalization':
                    # isPhcExist.update(
                    # isHospitalisation=True,
                    # hospitalizationRemarks = request.data.get('hospitalizationRemarks'),
                    # hospitalisationDate=datetime.now(),
                    # )
                    phcConsultancy.objects.create(
                    docpatient_id=docpatient_id,
                    phcDoctor_id=phcDoctor_id,
                    # )
                # isPhcExist.update(
                    isHospitalisation=True,
                    hospitalizationRemarks = request.data.get('hospitalizationRemarks'),
                    hospitalisationDate=datetime.now(),
                    suggestion_type=suggestion_type.capitalize()   
                        )
                    familyMembers.objects.filter(id = docpatient_id).update(
                        current_isPending=False,
                        current_isMedication=False,
                        current_phcConsultation=False,
                        current_isElderline=False,
                        current_isHospitalisation=True,
                        current_isSpecialistMedication=False,
                        current_specialistConsultation=False
                    )

                # phcConsultancy.objects.filter(docpatient_id=request.data.get('docpatient_id')).update(isCompleted=True)
                # serializer.save()
                # return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class SpecialistSuggestToCitizen(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated,]
    serializer_class = SpecialistSuggestToCitizenSerializers
    parser_classes = [MultiPartParser]
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
    def patch(self, request, format=None):
        from datetime import datetime,date,time
        # data=dict(request.data)
        # print(data,'====')
        docpatient_id=request.data.get('specialist_docpatient')
        phcDoctor_id = request.data.get('specialistDoctor')
        suggestion_type = request.data.get('specialist_suggestion_type')

        # print(docpatient_id,'===',phcDoctor_id)
        isPhcExist=specialistConsultancy.objects.filter(specialist_docpatient_id=docpatient_id,specialistDoctor_id=phcDoctor_id)
        # hc
        if isPhcExist:
            # print('-----------')
            isPhcExist.update(specialist_isPending=False)
            if isPhcExist[0].specialist_isMedication == True:
                isPhcExist.update(
                    specialist_medicationClosedDate = datetime.now()   
                    )
            if isPhcExist[0].specialist_Consultation == True:
                isPhcExist.update(
                    specialist_phcConsultationClosedDate = datetime.now()   
                    )
            if suggestion_type.lower() == 'medication':
                fileUpload = request.FILES.get('specialist_fileUpload')
                if fileUpload:
                    fu=validate_file_extension2(fileUpload)
                    if fu['resCode'] == 400 :
                            return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                    isPhcExist.update(
                        specialist_isMedication=True,
                        specialist_Consultation=False,
                        specialist_medicationRemarks = request.data.get('medicationRemarks'),
                        specialist_medicationDate=datetime.now(),
                        specialist_suggestion_type=suggestion_type.capitalize(),
                        specialist_fileUpload=fu['resData']
                        )
                else:
                    isPhcExist.update(
                        specialist_isMedication=True,
                        specialist_Consultation=False,
                        specialist_medicationRemarks = request.data.get('medicationRemarks'),
                        specialist_medicationDate=datetime.now(),
                        specialist_suggestion_type=suggestion_type.capitalize()
                        # specialist_fileUpload=fu['resData']
                        )
                familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isSpecialistMedication=True,
                    current_phcConsultation=False,
                    current_specialistConsultation=False,
                    current_isMedication=False,
                    current_isElderline=False,
                    current_isHospitalisation=False
                )
            elif suggestion_type.lower() == 'consultation':
                fileUpload = request.FILES.get('specialist_consultationFileUpload')
                if fileUpload:
                    fu=validate_file_extension2(fileUpload)
                    if fu['resCode'] == 400 :
                            return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                    isPhcExist.update(
                        specialist_Consultation=True,
                        specialist_isMedication=False,
                        specialist_appointDate = datetime.today(),
                        specialist_appointTime=datetime.now(),
                        specialist_consultationphcRemarks = request.data.get('specialist_consultationphcRemarks'),
                        specialist_phcConsultationDate= datetime.now(),
                        specialist_suggestion_type=suggestion_type.capitalize(),
                        specialist_consultationFileUpload=fu['resData']   
                        )
                else:
                    isPhcExist.update(
                        specialist_Consultation=True,
                        specialist_isMedication=False,
                        specialist_appointDate = datetime.today(),
                        specialist_appointTime=datetime.now(),
                        specialist_consultationphcRemarks = request.data.get('specialist_consultationphcRemarks'),
                        specialist_phcConsultationDate= datetime.now(),
                        specialist_suggestion_type=suggestion_type.capitalize()
                        # specialist_consultationFileUpload=fu['resData']   
                        )
                familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isMedication=False,
                    current_specialistConsultation=True,
                    current_isSpecialistMedication=False,
                    current_phcConsultation=False,
                    current_isElderline=False,
                    current_isHospitalisation=False
                )
            elif suggestion_type.lower() == 'hospitalization':
                isPhcExist.update(
                    specialist_isHospitalisation=True,
                    specialist_hospitalizationRemarks = request.data.get('specialist_hospitalizationRemarks'),
                    specialist_hospitalisationDate=datetime.now(),
                    specialist_suggestion_type=suggestion_type.capitalize()
                    )
                familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isSpecialistMedication=False,
                    current_phcConsultation=False,
                    current_specialistConsultation=False,
                    current_isMedication=False,
                    current_isElderline=False,
                    current_isHospitalisation=True
                )
            # else:

            # serializer = PhcSuggestToCitizenSerializers(isPhcExist,data=request.data)
            # if serializer.is_valid():
            #     isPhcExist.update(isCompleted=True)
            #     serializer.save()
            
            return Response({"responseCode":200, 'responseMessage': "Success"},status=status.HTTP_200_OK)

        else:
            # isPhcExist.update()
            serializer = SpecialistSuggestToCitizenSerializers(data=request.data)
            if serializer.is_valid():
                if suggestion_type.lower() == 'medication':
                    fileUpload = request.FILES.get('specialist_fileUpload')
                    if fileUpload:
                        fu=validate_file_extension2(fileUpload)
                        if fu['resCode'] == 400 :
                                return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                        specialistConsultancy.objects.create(
                            specialist_docpatient_id=docpatient_id,
                            specialistDoctor_id=phcDoctor_id,
                            # )
                        # isPhcExist.update(
                            specialist_isMedication=True,
                            specialist_medicationRemarks = request.data.get('specialist_medicationRemarks'),
                            specialist_medicationDate=datetime.now(),
                            specialist_suggestion_type=suggestion_type.capitalize(),
                            specialist_fileUpload=fu['resData']
                            )
                    else:
                        specialistConsultancy.objects.create(
                            specialist_docpatient_id=docpatient_id,
                            specialistDoctor_id=phcDoctor_id,
                            # )
                        # isPhcExist.update(
                            specialist_isMedication=True,
                            specialist_medicationRemarks = request.data.get('specialist_medicationRemarks'),
                            specialist_medicationDate=datetime.now(),
                            specialist_suggestion_type=suggestion_type.capitalize()
                            # specialist_fileUpload=fu['resData']
                            )
                    familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isSpecialistMedication=True,
                    current_phcConsultation=False,
                    current_specialistConsultation=False,
                    current_isMedication=False,
                    current_isElderline=False,
                    current_isHospitalisation=False
                    )
                elif suggestion_type.lower() == 'consultation':
                    fileUpload = request.FILES.get('specialist_consultationFileUpload')
                    if fileUpload:
                        fu=validate_file_extension2(fileUpload)
                        if fu['resCode'] == 400 :
                                return Response({"responseCode":400, 'responseMessage': fu['resMsg']},status=status.HTTP_400_BAD_REQUEST)
                        specialistConsultancy.objects.create(
                        specialist_docpatient_id=docpatient_id,
                        specialistDoctor_id=phcDoctor_id,
                        # )
                    # isPhcExist.update(
                            specialist_Consultation=True,
                            specialist_appointDate = datetime.today(),
                            specialist_appointTime=datetime.now(),
                            specialist_consultationphcRemarks = request.data.get('consultationphcRemarks'),
                            specialist_phcConsultationDate= datetime.now(),
                            specialist_suggestion_type=suggestion_type.capitalize(),
                            specialist_consultationFileUpload=fu['resData']   
                            )
                    else:
                        specialistConsultancy.objects.create(
                        specialist_docpatient_id=docpatient_id,
                        specialistDoctor_id=phcDoctor_id,
                        # )
                    # isPhcExist.update(
                            specialist_Consultation=True,
                            specialist_appointDate = datetime.today(),
                            specialist_appointTime=datetime.now(),
                            specialist_consultationphcRemarks = request.data.get('consultationphcRemarks'),
                            specialist_phcConsultationDate= datetime.now(),
                            specialist_suggestion_type=suggestion_type.capitalize()
                            # specialist_consultationFileUpload=fu['resData']   
                            )
                    familyMembers.objects.filter(id = docpatient_id).update(
                    current_isPending=False,
                    current_isMedication=False,
                    current_specialistConsultation=True,
                    current_isSpecialistMedication=False,
                    current_phcConsultation=False,
                    current_isElderline=False,
                    current_isHospitalisation=False
                    )

                elif suggestion_type.lower() == 'specialist':
                     specialistConsultancy.objects.create(
                        specialist_docpatient_id=docpatient_id,
                        specialistDoctor_id=phcDoctor_id,
                        specialist_isPending=True,
                        specialist_DoctorassignedBy=request.user
                        )
                     familyMembers.objects.filter(id = docpatient_id).update(
                        current_isPending=False,
                        current_isMedication=False,
                        current_phcConsultation=False,
                        current_isElderline=False,
                        current_isHospitalisation=False,
                        current_isSpecialistMedication=False,
                        current_specialistConsultation=True

                    )
                elif suggestion_type.lower() == 'hospitalization':
                    # isPhcExist.update(
                    #     specialist_isHospitalisation=True,
                    #     specialist_hospitalizationRemarks = request.data.get('specialist_hospitalizationRemarks'),
                    #     specialist_hospitalisationDate=datetime.now(),
                    #     specialist_suggestion_type=suggestion_type.capitalize()
                    #     )
                    specialistConsultancy.objects.create(
                        specialist_docpatient_id=docpatient_id,
                        specialistDoctor_id=phcDoctor_id,
                        specialist_isHospitalisation=True,
                        specialist_hospitalizationRemarks = request.data.get('specialist_hospitalizationRemarks'),
                        specialist_hospitalisationDate=datetime.now(),
                        specialist_suggestion_type=suggestion_type.capitalize()
                        )
                    familyMembers.objects.filter(id = docpatient_id).update(
                        current_isPending=False,
                        current_isSpecialistMedication=False,
                        current_phcConsultation=False,
                        current_specialistConsultation=False,
                        current_isMedication=False,
                        current_isElderline=False,
                        current_isHospitalisation=True
                    )
                # phcConsultancy.objects.filter(docpatient_id=request.data.get('docpatient_id')).update(isCompleted=True)
                # serializer.save()
                # return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class SpecialistCitizensList(generics.GenericAPIView):

    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = SpecialistCitizenSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','specialistDoctorConsultancy__specialistDoctor_id','specialistDoctorConsultancy__specialist_isPending','specialistDoctorConsultancy__specialist_isMedication','specialistDoctorConsultancy__specialist_isHospitalisation','specialistDoctorConsultancy__specialist_Consultation','specialistDoctorConsultancy__specialist_isElderline','specialistDoctorConsultancy__specialist_isCaseClosed')
    pagination_class = CustomPagination
    pagination_class.page_size = 10
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
            ),       

        ],
        
    )

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']
    def get(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
    def get_queryset(self):
        assignedDoctor_id = self.kwargs.get('specialistConsultancy__specialistDoctor_id')
        dc_fm=[]
        if assignedDoctor_id is not None:
            dc_fm = specialistConsultancy.objects.filter(specialist_assignedDoctor_id=assignedDoctor_id).values_list('specialist_docpatient_id').distinct()
            #dc_fm = doctorConsultancy.objects.filter(assignedDoctor_id=self.request.user.id).values_list('docpatient_id').distinct()
        else:
            dc_fm = specialistConsultancy.objects.values_list('specialist_docpatient_id').distinct()
        return familyMembers.objects.filter(id__in=dc_fm)

class SpecialistCitizensListNoPage(generics.GenericAPIView):

    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = SpecialistCitizenSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','specialistDoctorConsultancy__specialistDoctor_id','specialistDoctorConsultancy__specialist_isPending','specialistDoctorConsultancy__specialist_isMedication','specialistDoctorConsultancy__specialist_isHospitalisation','specialistDoctorConsultancy__specialist_Consultation','specialistDoctorConsultancy__specialist_isElderline','specialistDoctorConsultancy__specialist_isCaseClosed')
    # pagination_class = CustomPagination
    # pagination_class.page_size = 5
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
            ),       

        ],
        
    )

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']
    def get(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
    def get_queryset(self):
        assignedDoctor_id = self.kwargs.get('specialistConsultancy__specialistDoctor_id')
        dc_fm=[]
        if assignedDoctor_id is not None:
            dc_fm = specialistConsultancy.objects.filter(specialist_assignedDoctor_id=assignedDoctor_id).values_list('specialist_docpatient_id').distinct()
            #dc_fm = doctorConsultancy.objects.filter(assignedDoctor_id=self.request.user.id).values_list('docpatient_id').distinct()
        else:
            dc_fm = specialistConsultancy.objects.values_list('specialist_docpatient_id').distinct()
        return familyMembers.objects.filter(id__in=dc_fm)

class PhcCitizensList(generics.GenericAPIView):

    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = PhcCitizenSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','phcDoctorConsultancy__phcDoctor_id','phcDoctorConsultancy__isPending','phcDoctorConsultancy__isMedication','phcDoctorConsultancy__isHospitalisation','phcDoctorConsultancy__phcConsultation','phcDoctorConsultancy__isElderline')
    pagination_class = CustomPagination
    pagination_class.page_size = 10
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
            ),       

        ],
        
    )

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']
    def get(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
    def get_queryset(self):
        assignedDoctor_id = self.kwargs.get('phcDoctorConsultancy_Doctor_id')
        dc_fm=[]
        if assignedDoctor_id is not None:
            dc_fm = phcConsultancy.objects.filter(assignedDoctor_id=assignedDoctor_id).values_list('docpatient_id').distinct()
            #dc_fm = doctorConsultancy.objects.filter(assignedDoctor_id=self.request.user.id).values_list('docpatient_id').distinct()
        else:
            dc_fm = phcConsultancy.objects.values_list('docpatient_id').distinct()
        return familyMembers.objects.filter(id__in=dc_fm)

class PhcPatientList(generics.GenericAPIView):
    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    queryset = familyMembers.objects.all()
    # permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = PhcPatientSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','phcDoctorConsultancy__suggestion_type','phcDoctorConsultancy__phcDoctor','current_isPending','current_isMedication','current_isHospitalisation','current_phcConsultation','current_specialistConsultation','current_isElderline','isCaseClosed')
    search_fields = ['mobile','family_head__family_head_member__member_unique_id','member_name','member_gender','member_age']
    pagination_class = CustomPagination
    pagination_class.page_size = 5
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
            ),       

        ],
        
    )

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']

    def get(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
    
class PhcPatientListNoPage(generics.GenericAPIView):
    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    queryset = familyMembers.objects.all()
    # permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = PhcPatientSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','phcDoctorConsultancy__suggestion_type','phcDoctorConsultancy__phcDoctor','current_isPending','current_isMedication','current_isHospitalisation','current_phcConsultation','current_specialistConsultation','current_isElderline','isCaseClosed')
    search_fields = ['mobile','family_head__family_head_member__member_unique_id','member_name','member_gender','member_age']
    # pagination_class = CustomPagination
    # pagination_class.page_size = 5
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
            ),       

        ],
        
    )

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']

    def get(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class AssignNewDoctor(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Assign New Doctor to Patients 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AssignNewDoctorSerializer
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
        
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})
        #phone = request.data["phone"]

        if request.data["patientLabTestreport"]=="":
            validation_message = "please provide report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        # chk_report = testReport.objects.filter(id=request.data["report"])
        chk_report = PatientTest.objects.filter(id=request.data["patientLabTestreport"])

        if chk_report:
            pass
        else:
            validation_message = "please provide valid report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        if request.data["docpatient"]=="":
            validation_message = "please provide patient id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        chk_patients = familyMembers.objects.filter(id=request.data["docpatient"])

        if chk_patients:
            pass
        else:
            validation_message = "please provide valid patients id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)



        if request.data["assignedDoctor"]=="":
            validation_message = "please provide Remarks."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        
        save_doc = doctorConsultancy(DoctorassignedBy_id = request.user.id,patientLabTestreport_id = request.data["patientLabTestreport"],docpatient_id = request.data["docpatient"],assignedDoctor_id = request.data["assignedDoctor"],appointDate=request.data['appointDate'],appointTime=request.data['appointTime'] )
        save_doc.save()
         
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password","responseData":save_doc.data},status=status.HTTP_200_OK)


class GetDoctorRemarkPathlabList(GenericAPIView):
    """
    List all Doctor Query and Pathlab Response
    """
    queryset = doctorRemarksPathlab.objects.all()

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllDoctorRemarkPathlabList
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('isCompleted', 'created_date','response_date',)
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

    # search_fields = ['first_name','last_name','email','username','is_active','signup_date']

    def get(self, request, format=None):

        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)








class QueryToPathLab(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Doctor Gives Remarks on Patients Report 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = DoctorRemarkPathlab
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
        
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})
        #phone = request.data["phone"]

        if request.data["remarkreport"]=="":
            validation_message = "please provide report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        chk_report = PatientTestReport.objects.filter(id=request.data["remarkreport"])

        if chk_report:
            pass
        else:
            validation_message = "please provide valid report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        # if request.data["docpatient"]=="":
        #     validation_message = "please provide patient id."
        #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        # chk_patients = familyMembers.objects.filter(id=request.data["docpatient"])

        # if chk_patients:
        #     pass
        # else:
        #     validation_message = "please provide valid patients id."
            # return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)



        if request.data["doctorRemarks"]=="":
            validation_message = "please provide Remarks."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        
        save_doc = doctorRemarksPathlab(remarkreport_id = request.data["remarkreport"],doctorRemarks = request.data["doctorRemarks"],remarkdoctor_id = request.user.id )
        save_doc.save()
         
            
        return Response({'responseCode': 200, 'responseMessage': "Success"},status=status.HTTP_200_OK)





class DoctorUserDetail(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated,]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    serializer_class = OtherUserSerializer
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
            ),       

        ],
        
    )
    # def get_object(self, pk):
    #     # Returns an object instance that should 
    #     # be used for detail views.


    #     try:
    #         return CustomUser.objects.get(pk=pk)
    #     except CustomUser.DoesNotExist:
    #         raise Http404

    def get(self, request,pk, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        queryset = CustomUser.objects.filter(id=pk)
        if queryset:
            card = get_object_or_404(queryset, pk=pk)
            # card = CustomUser.objects.get(pk=pk)
            temp = OtherUserSerializer(card).data
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':temp},status=status.HTTP_200_OK)

        else:
            validation_message ='data not found'
            return Response({"responseCode":400, 'responseMessage': validation_message},status=status.HTTP_400_BAD_REQUEST)

        # temp["group"] = card.group
        # return Response(serializer.data)



class DoctorChangeNewPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Set new Password after first Login. 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
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

        if 'old_password' in request.data and request.data["old_password"]=="":
            validation_message = "Please Enter  Old password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        chk_user = CustomUser.objects.get(id=request.user.id)

        chk_pass = chk_user.check_password(request.data["old_password"])
        if chk_pass:
            pass
        else:
            validation_message = "Please Enter correct old password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        # if request.data["new_password"]!=request.data["old_password"]:
        #     validation_message = "New Password and Old password must be same."
        #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        
        if request.data["new_password"]!="":
            new_password = request.data["new_password"]

        if request.data["old_password"]!="":
            old_password = request.data["old_password"]


        # import datetime
        data={}
        user = request.user.id
        newpassword = make_password(new_password)
        user_exists = CustomUser.objects.filter(id=user).update(password=newpassword,confirm_password=new_password)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password"},status=status.HTTP_200_OK)



class DoctorEditProfile(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Edit Profile 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = EditProfileSerializer
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
        

        name = ""
        email = ""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})


        
        if request.data["name"]!="":
            name = request.data["name"]

        if request.data["email"]!="":
            email = request.data["email"]

        user_exists = CustomUser.objects.filter(id=request.user.id).update(name=name,email=email)
        queryset = CustomUser.objects.filter(id=pk)
        if queryset:
            card = get_object_or_404(queryset, pk=request.user.id)
            # card = CustomUser.objects.get(pk=pk)
            temp = OtherUserSerializer(card).data
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully Edit Profile","responseData":temp},status=status.HTTP_200_OK)


class InsertdoctorConsultancy(GenericAPIView):
    """
    create a new doctor Consultancy
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InsertdoctorConsultancyserializers
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

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        serializer = InsertdoctorConsultancyserializers(data=request.data)
        if serializer.is_valid():
            serializer.save(surveyor=request.user)
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class AssignDoctor(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Assign Doctor
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = DoctorRemarkPathlab
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
        
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})
        phone = request.data["phone"]

        if request.data["report"]=="":
            validation_message = "please provide report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        chk_report = testReport.objects.filter(id=request.data["report"])

        if chk_report:
            pass
        else:
            validation_message = "please provide valid report id."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)




        if request.data["doctorRemarks"]=="":
            validation_message = "please provide Remarks."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        
        save_doc = doctorRemarksPathlab(remarkreport = request.data["remarkreport"],doctorRemarks = request.data["doctorRemarks"],remarkdoctor = request.user.id )
        save_doc.save()
         
            
        return Response({'responseCode': 200, 'responseMessage': "Success"},status=status.HTTP_200_OK)


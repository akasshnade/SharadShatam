from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from seniorcetizen.serializers import *
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
from adminportal.serializers import *
# from adminportal.serializers import SelffamilyHeadSerializer
# from
# Create your views here.
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
import random
import os
import string
from datetime import datetime
import hmac
import hashlib
from django.conf import settings
# Create your views here.
from rest_framework.pagination import PageNumberPagination

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
class CitizenloginSendOtp(generics.GenericAPIView):
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

                

            # phoneAlreadyRegistered= CustomUser.objects.filter(phone=phone)
            # if not phoneAlreadyRegistered:

            #     validation_message = "Please register yourself with local PHC."
            #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

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
            else:
                otp="000000"
                import datetime
                validation_message = 'Otp Send on your phone.New'
                now = datetime.datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                        # import datetime
                expirey_date = now + datetime.timedelta(seconds=150)
                insertOtp = CustomUser(username=phone,phone=phone,otp=otp,created_date=dt_string,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))
                insertOtp.save()
                getuser = CustomUser.objects.get(phone = phone )
                group = Group.objects.get(name="surveyour")
                group.user_set.add(getuser)
                # insertOtp = sendRegisterOtp(phone=phone,otp=otp,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))
                # insertOtp.save()
                data["phone"] =phone
        return Response({'responseCode': 200, 'responseMessage': validation_message,'responseData':data},status = status.HTTP_200_OK)



class CitizenInsertFamilyMemberMedicalSurvey(GenericAPIView):
    """
    Citizen Insert Family Member Medical Survey

    """
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = CitizenInsertFamilyMemberSerializer
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
        serializer = CitizenInsertFamilyMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"responseCode":200, 'responseMessage': "Successfully Inserted Family Member"},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class CitizenloginOtpVerify(generics.GenericAPIView):
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
            data = SCUserSerializer(customuser,context=self.get_serializer_context()).data
            data["token"] = token
            validation_status = 'Success'
            validation_message = 'OTP Verified '
            # CustomUser.objects.filter(phone=phone).update(is_verify = True,is_active=True)
            # print(token)
            return Response({'responseCode': 200, 'responseMessage': validation_message,"responseData":data},status=status.HTTP_200_OK)

        else:
            return Response({'responseCode': 400, 'responseMessage':"User Not Found"},status = status.HTTP_400_BAD_REQUEST)



from rest_framework import serializers, status, views

class SelfMedicalSurvey(GenericAPIView):
    """
    create a new Self Medical Survey
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = SelfInsertAddressDetails
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

    # def get(self, request, format=None):
    #     card = familyHeadDetails.objects.all()
    #     serializer = familyHeadSerializer(card, many=True)
    #     # return Response(serializer.data)
    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
  
    def post(self, request, format=None):
        serializer = SelfInsertAddressDetails(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"responseCode":400, 'responseMessage': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class ViewCitizenReportAPI(generics.GenericAPIView):
    serializer_class = ViewUploadTestReportSerializer
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

    def get(self,request,parameter_value,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        # if parameter_name == "barcode":
        #         labTest_data=PatientTestReport.objects.filter(patientLabTest__barcode=parameter_value)
        #         patient_details=PatientTest.objects.filter(barcode=parameter_value)[:1]
        # elif parameter_name == "citizen":
        labTest_data=PatientTestReport.objects.filter(patientLabTest__patientDetail__member_unique_id=parameter_value)
        if not labTest_data:
            return Response({
                    "responseCode":400,
                    # "responseData":report_data
                    },status=status.HTTP_400_BAD_REQUEST)
                    # },status=status.HTTP_200_OK)
        patient_details=PatientTest.objects.filter(patientDetail__member_unique_id=parameter_value)               
        if not patient_details:
            return Response({
                    "responseCode":400,
                    # "responseData":report_data
                    },status=status.HTTP_400_BAD_REQUEST)
        patient_details=patient_details[:1]
        
        # else:
        #     return Response({
        #             "responseCode":400,
        #             # "responseData":report_data
        #             },status=status.HTTP_400_BAD_REQUEST)
                    # },status=status.HTTP_200_OK)
        # print(labTest_data)
        patient_serializer = CitizenLabTestserializers(patient_details,many=True)
        serializer = ViewUploadTestReportSerializer(labTest_data,many=True)
        report_data = {}
        report_data['citizen_details']=patient_serializer.data
        report_data['report']=serializer.data     
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":report_data
                    
                    },status=status.HTTP_200_OK)

class ViewCitizenSummaryAPI(generics.GenericAPIView):
    serializer_class = ViewUploadTestReportSerializer
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

    def get(self,request,parameter_value,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        
        phcSummary=phcConsultancy.objects.filter(docpatient__member_unique_id=parameter_value)
        specialistSummary=specialistConsultancy.objects.filter(specialist_docpatient__member_unique_id=parameter_value)
        if not phcSummary:
            return Response({
                    "responseCode":400,
                    # "responseData":report_data
                    },status=status.HTTP_400_BAD_REQUEST)
                    # },status=status.HTTP_200_OK)
        # print(labTest_data)
        patient_serializer = PhcConsultancySerializer(phcSummary,many=True)
        serializer = SpecialityDoctorConsultancySerializer(specialistSummary,many=True)
        report_data = {}
        report_data['citizen_details']=patient_serializer.data
        report_data['report']=serializer.data     
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":report_data
                    
                    },status=status.HTTP_200_OK)

class ViewCitizenSummarySortedAPI(generics.GenericAPIView):
    # serializer_class = ViewUploadTestReportSerializer
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

    def get(self,request,parameter_value,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        
        phcSummary=phcConsultancy.objects.filter(docpatient__member_unique_id=parameter_value)
        specialistSummary=specialistConsultancy.objects.filter(specialist_docpatient__member_unique_id=parameter_value)
        if not phcSummary:
            return Response({
                    "responseCode":400,
                    "responseMessage":"No Summary Found"
                    # "responseData":report_data
                    },status=status.HTTP_400_BAD_REQUEST)
        summary_list=[]

        for each in phcSummary:
            # print(each,'-------------')
            phc_dict ={}
            phc_dict['doc_name']=each.phcDoctor.name if each.phcDoctor else ''
            phc_dict['suggestion_type'] =each.suggestion_type
            phc_dict['doc_type'] = 'phc'
            if phc_dict['suggestion_type'].lower() == 'consultation':
                phc_dict['date'] = each.phcConsultationDate
                phc_dict['closedDate'] = each.phcConsultationClosedDate
                phc_dict['remarks'] = each.consultationphcRemarks
                phc_dict['prescriptionFile'] = each.consultationFileUpload if each.consultationFileUpload else ''
            if phc_dict['suggestion_type'].lower() == 'medication':
                phc_dict['date'] = each.medicationDate
                phc_dict['closedDate'] = each.medicationClosedDate
                phc_dict['remarks'] = each.medicationRemarks
                phc_dict['prescriptionFile'] = each.fileUpload if each.fileUpload else ''
            summary_list.append(phc_dict)
        for each in specialistSummary:
            spc_dict ={}
            spc_dict['doc_name']=each.specialistDoctor.name
            spc_dict['doc_type'] = 'specialist'
            spc_dict['suggestion_type'] =each.specialist_suggestion_type
            if spc_dict['suggestion_type'].lower() == 'consultation':
                spc_dict['date'] = each.specialist_phcConsultationDate
                spc_dict['closedDate'] = each.specialist_phcConsultationClosedDate
                spc_dict['remarks'] = each.specialist_consultationphcRemarks
                spc_dict['prescriptionFile'] = each.specialist_consultationFileUpload if each.specialist_consultationFileUpload else ''
            if spc_dict['suggestion_type'].lower() == 'medication':
                spc_dict['date'] = each.specialist_medicationDate
                spc_dict['closedDate'] = each.specialist_medicationClosedDate
                spc_dict['remarks'] = each.specialist_medicationRemarks
                spc_dict['prescriptionFile'] = each.specialist_fileUpload if each.specialist_fileUpload else ''
            summary_list.append(spc_dict)
            # phc_dict['suggestion_type']=each.phcDoctor.name            
                    # },status=status.HTTP_200_OK)
        # print(labTest_data)
        # patient_serializer = PhcConsultancySerializer(phcSummary,many=True)
        # serializer = SpecialityDoctorConsultancySerializer(specialistSummary,many=True)
        report_data = {}
        report_data['summary_list'] = sorted(summary_list, key=lambda x: x['date'], reverse=True)
        # report_data['citizen_details']=patient_serializer.data
        # report_data['report']=serializer.data     
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":report_data
                    
                    },status=status.HTTP_200_OK)

class CitizenRegisterAPI(generics.GenericAPIView):
    serializer_class = CitizenRegisterSerializer
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
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"},status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        print(request.data,"**********************&")
        if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)
            import datetime
            # from datetime import datetime
            data = {}
            # datetime object containing current date and time
            # now = datetime.now()
            
            # print("now =", now)

            # dd/mm/YY H:M:S
            now = datetime.datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            user = serializer.save()
            # data = UserSerializer(customuser,context=self.get_serializer_context()).data
            user.login_date_time=dt_string
            group = Group.objects.get(name="seniorcitizen")
            group.user_set.add(user)
            otp = "000000"
            expirey_date = now + datetime.timedelta(seconds=150)
            # now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            updateOtp = CustomUser.objects.filter(phone=request.data['phone']).update(otp=otp,created_date=dt_string,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))

            # group = Group.objects.get(name="buyer")
            # group.user_set.add(user)
            # otp = ''.join(random.sample("0123456789", 6))
            # message,send_status,random_otp=send_msg_otp_signup_verification(customuser.phone,customuser.name,otp)
            # status = email(customuser.email,customuser.name,otp)
            # print('Email OTP Status: ',status)
            # print('OTP Status ')
            # print(send_status)
            # otp = "000000"
            # import datetime

            # expirey_date = datetime.datetime.now() + datetime.timedelta(seconds=150)
            
            # save_otp = SendOtp(otp_owner=user,otp=otp,expirey_date=expirey_date)
            # save_otp.save()

            # email_body = 'Hello, \n Your Otp for Account Verification is '+otp
            # data = {'email_body': email_body, 'to_email': user.email,
            #             'email_subject': 'Account Verification'}
            #     # try:
            # ty = Util.send_email(data)
            # print(ty,"&&&&&&&&&&&7")
            
            # return Response({
            # "status":"success",
            # "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]})

            return Response({
            "responseCode":200,
            "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
            # "responseMessage":"User is Successfully registered.OTP is send on registered phone"},status=status.HTTP_200_OK)
        else:
            #print(type(serializer.errors))
            #print(serializer.errors["phone"][0])
            if "phone" in serializer.errors:
                return Response({"responseCode":400,"responseMessage":serializer.errors["phone"][0]},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)

class SeniorCitizenRegisterAPI(generics.GenericAPIView):
    # serializer_class = SeniorCitizenRegisterSerializer
    serializer_class = SeniorCitizenRegister2Serializer
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

    def post(self, request, *args, **kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"},status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        print(request.data,"**********************&")
        if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)
            import datetime
            # from datetime import datetime
            data = {}
            # datetime object containing current date and time
            # now = datetime.now()
            
            # print("now =", now)

            # dd/mm/YY H:M:S
            now = datetime.datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            user = serializer.save()
            # data = UserSerializer(customuser,context=self.get_serializer_context()).data
            user.login_date_time=dt_string
            # group = Group.objects.get(name="seniorcitizen")
            # group.user_set.add(user)
            otp = "000000"
            expirey_date = now + datetime.timedelta(seconds=150)
            # now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            updateOtp = CustomUser.objects.filter(phone=request.data['familyHead']['family_head_mobile']).update(otp=otp,created_date=dt_string,expirey_date=expirey_date.strftime("%Y-%m-%d %H:%M:%S"))
            user_data=CustomUser.objects.filter(phone=request.data['familyHead']['family_head_mobile'])
            return Response({
            "responseCode":200,
            "responseData":UserSerializer(instance=user_data[0]).data,
            # "responseData":self.get_serializer(instance=user_add).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
            # "responseMessage":"User is Successfully registered.OTP is send on registered phone"},status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            #print(serializer.errors["phone"][0])
            if "familyHead" in serializer.errors:
                return Response({"responseCode":400,"responseMessage":serializer.errors["familyHead"][0]},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)


class CitizenOtpVerify(generics.GenericAPIView):
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

from django.http import QueryDict

class CitizenLoginAPI(generics.GenericAPIView):
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
        dmdata = {}

        # else:
        #     username =request.data["username"]
        username = ""
        serializer = self.get_serializer(data=request.data)
        if request.data["username"].isnumeric():
            getusername = CustomUser.objects.filter(phone__iexact = request.data["username"] )
            if getusername:
                # querydict_dict = serializer
                # dmdata1 ={}
                dmdata["username"]=getusername[0].username
                dmdata["password"]=request.data["password"]
                # print(getusername[0].username,"Username")
                username = getusername[0].username
                # dmdata = QueryDict('', mutable=True)
                # dmdata1.update(dmdata) 
                serializer = self.get_serializer(data=dmdata)

            else:
                username =request.data["username"]

                return Response({"responseCode":400,"responseMessage":"Invalid Phone Number"},status=status.HTTP_400_BAD_REQUEST)


        print(dmdata,"*********")
        if serializer.is_valid():

            # serializer.validated_data["username"] = username

            customuser = serializer.validated_data
            _, token = AuthToken.objects.create(customuser)
            data = UserSerializer(customuser,context=self.get_serializer_context()).data
            print(data,"*********************^^^^^&")
            from datetime import datetime
            family_head_details = familyHeadDetails.objects.filter(unique_family_key = username).values()
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
            data["family_head_details"]= family_head_details
   
            return Response({
                "responseCode":200,
                "responseData":data
                
                },status=status.HTTP_200_OK)
        else:
            print(serializer)
            print(serializer.errors,"787878677676")

            return Response({
               "responseCode":400,
               "responseMessage":serializer.errors.values(),
                },status=status.HTTP_400_BAD_REQUEST)




class CitizenForgotPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenForgotPasswordSerializer
    # parser_classes = [FormParser]
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
 

 
class HeadCitizenList(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny,]
    # serializer_class = CitizenOtpVerifySerializer
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

    def get(self, request,familyhead_id):    
        
        email = ''
        user_id = 0
        token = ""
        # created_date = ""
        otp =""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        # if not request.data:
        #     validation_message = 'Please provide otp'
        #     return Response({'status': 'error', 'message': validation_message})

        # if 'phone' in request.data and request.data["phone"]=="":
        #     validation_message = "Please Enter phone"
        #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        # phone = request.data["phone"]

        # if only_numerics(phone)==False:
        #     validation_message = "Only digits Allowed"
        #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        # if check_phone(phone)==False:
        #     validation_message = "Only 10 digits Allowed"
        #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)

        # if 'phone' in request.data:
        #     phone = request.data["phone"]
        
        # if 'otp' in request.data:
        #     otp = request.data["otp"]
        # import datetime
        data={}
        
        user_exists = familyMembers.objects.filter(family_head__unique_family_key=familyhead_id)
        print(user_exists,"**************")

        if user_exists:   
            

            # _ ,token = AuthToken.objects.create(customuser)
            # data = UserSerializer(customuser,context=self.get_serializer_context()).data
            # data["token"] = token
            validation_status = 'Success'
            validation_message = 'Fetched Successfully '
            famHead = FamilyHeadMemberListSerializer(user_exists,many=True)
            # CustomUser.objects.filter(phone=phone).update(is_verify = True,is_active=True)
            # print(token)
            return Response({'responseCode': 200, 'responseMessage': validation_message,'responseData':famHead.data},status=status.HTTP_200_OK)

        else:
            return Response({'responseCode': 400, 'responseMessage':"User Not Found"},status = status.HTTP_400_BAD_REQUEST)

class CitizenForgotPasswordOtpVerify(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Forgot Password Otp Verify
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenOtpVerifySerializer
    # parser_classes = [FormParser]
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



class CitizenForgotPasswordSetNewPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Surveyour Forgot Password Set New Password. 
    """
    permission_classes = [permissions.AllowAny,]
    serializer_class = CitizenSetNewPasswordSerializer
    # parser_classes = [FormParser]
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
        user_exists = CstomUser.objects.filter(phone=phone).update(password=newpassword,confirm_password=new_password)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password","responseData":data},status=status.HTTP_200_OK)




class FamilySurveyList(GenericAPIView):
    """
    Family Survey List
    """
    queryset = familyHeadDetails.objects.all()

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = SelfListFamilySerializer
    # pagination_class = PageNumberPagination
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # # filterset_fields = ('surveyCompleted', 'district','region_type','municipal_corporation','ward','municipal_council','taluka','village','phc','sc',)
    # # filterset_fields = ('Address__district','Address__region_type','Address__municipal_corporation','Address__ward','Address__municipal_council','Address__taluka','Address__village','Address__phc','Address__sc',)
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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
                default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
            )
        ],
        
    )
    def get(self, request, format=None):

        print("********",self.request.user.username)
        # qs = familyHeadDetails.objects.filter(unique_family_key=self.request.user.username)
        qs = familyHeadDetails.objects.filter(unique_family_key="FSS00000318")
        print(qs,"&&&&&&&&&")
        # qs = self.filter_queryset(qs)
        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)



class FamilySurveysdfsdList(generics.GenericAPIView):
    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    queryset = familyMembers.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = AllMedicalSurveySerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    # filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type','current_isPending','current_isMedication','current_isHospitalisation','current_phcConsultation','current_specialistConsultation','current_isElderline','isCaseClosed')
    # search_fields = ['mobile','family_head__family_head_member__member_unique_id','member_name','member_gender','member_age']
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

        print(self.request.user.username,"$$$$$$$$$$$$$$")
        t = self.request.user.username
        qs = familyMembers.objects.filter(family_head_id =int(t[7:])).values()
        # qs = familyMembers.objects.filter()

        # print(qs,"#######")
        # qs = self.filter_queryset(qs)
        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':qs},status=status.HTTP_200_OK)

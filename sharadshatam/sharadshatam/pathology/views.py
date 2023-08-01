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
from .serializers import *
from database.serializers import *
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
import re
phone_re = re.compile(r'\d{10}$')
from django_filters.rest_framework import DjangoFilterBackend
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


class PathLabLoginAPI(generics.GenericAPIView):
    serializer_class = PathLabLoginSerializer
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




class TestReportAPI(generics.GenericAPIView):
    serializer_class = PatientTestReportserializers
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


    def get(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        labTest_data=PatientTestReport.objects.filter(pathlogy_id=pk)
        serializer = PatientTestReportserializers(labTest_data,many=True)
        
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data
            data = PatientTestReportserializers(customuser,context=self.get_serializer_context()).data
            
             
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
class ScanBarCodeAPI(generics.GenericAPIView):
    # serializer_class = patientLabTestserializers
    serializer_class = PatientTestReportserializers2
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


    def get(self,request,barcode,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        labTest_data=PatientTestReport.objects.filter(patientLabTest__barcode=barcode)
        if not labTest_data:
            return Response({
               "responseCode":400,
               "responseMessage":"Invalid Barcode!",
                },status=status.HTTP_400_BAD_REQUEST)
        serializer = PatientTestReportserializers2(labTest_data,many=True)
        
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)

class CitizensListAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitizenLabTestserializers
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


    def get(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        # print(request.user.id)
        labTest_data=PatientTest.objects.filter(pathlab__pathOwner_id=request.user.id)
        # print(labTest_data)
        serializer = CitizenLabTestserializers(labTest_data,many=True)
        # serializer = TestReportSerializer(labTest_data,many=True)
        # if serializer.data:
        unique_data = {v['citizen_id']:v for v in serializer.data}.values()                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":unique_data
                    
                    },status=status.HTTP_200_OK)


class TestReportAPI(generics.GenericAPIView):
    serializer_class = PatientTestReportserializers
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


    def post(self,request,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data
            # data = TestReportSerializer(customuser,context=self.get_serializer_context()).data
            data =serializer.save()
             
            return Response({
                "responseCode":200,
                "responseData":serializer.data
                
                },status=status.HTTP_200_OK)
        else:
            print(serializer)
            print(serializer.errors)

            return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)

class GetTestReportAPI(generics.GenericAPIView):
    serializer_class = GetTestReportSerializer
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
    def get(self,request,parameter_name,parameter_value,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        # pk=6
        labTest_data=PatientTestReport.objects.filter(patientLabTest__barcode=parameter_value)
        serializer = GetTestReportSerializer(labTest_data,many=True)
        
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)
class PhlebotomistListAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhlebotomistSerializer
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


    def get(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        
                        
        labTest_data=Phlebotomist.objects.filter(pathlab__pathOwner_id=request.user.id,is_active=True).order_by('-id')
        print(labTest_data,'========')
        serializer = PhlebotomistSerializer(labTest_data,many=True)
        
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)

class PhlebotomistListParameterAPI(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset=Phlebotomist.objects.filter(is_active=False)
    serializer_class = PhlebotomistListSerializer
    parser_classes = [JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('phlebotomist_info__region_type','phlebotomist_info__district','phlebotomist_info__municipal_corporation','phlebotomist_info__ward','phlebotomist_info__municipal_council','phlebotomist_info__taluka')
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


    def get(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        serializer = self.get_serializer(instance=qs, many=True)
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)

    

class PhlebotomistDeleteAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhlebotomistSerializer
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

   
    def delete(self,request,pk):
        # phlebotomist = CustomUser.objects.filter(id=pk)
        CustomUser.objects.filter(id=pk).update(is_delete=True)
        Phlebotomist.objects.filter(phlebotomist_info_id=pk).update(is_active=False)
        return Response({
               "responseCode":200,
               "responseMessage":"Deleted Successfully",
                },status=status.HTTP_400_BAD_REQUEST)

class QueryList(generics.GenericAPIView):
    serializer_class = AllQueryList
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
            ),       

        ],
        
    )
    def get(self,request):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        user_id=request.user.id
        pt_t=PatientTestReport.objects.filter(patientLabTest__pathlab__pathOwner_id=user_id).values_list('id',flat=True)
        # qs = self.get_queryset()
        # qs = self.filter_queryset(id__in=qs)
        qs = doctorRemarksPathlab.objects.filter(remarkreport_id__in=pt_t)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class QueryResponseAPI(generics.GenericAPIView):
    serializer_class = PhlebotomistSerializer
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


    def get(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        labTest_data=Phlebotomist.objects.all()
        serializer = PhlebotomistSerializer(labTest_data,many=True)
        
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data
            # data = TestReportSerializer(customuser,context=self.get_serializer_context()).data
            data =serializer.save()
             
            return Response({
                "responseCode":200,
                "responseData":serializer.data
                
                },status=status.HTTP_200_OK)
        else:
            print(serializer)
            print(serializer.errors)

            return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)

class ResponseToDoctor(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Doctor Gives Remarks on Patients Report 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = ResponseRemarkPathlab
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
    
    def post(self,request,pk,*args,**kwargs):
    # def post(self,pk, request):    
        
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid Token"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})

        if request.data["pathologyResponse"]=="":
            validation_message = "please provide Remarks."
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        print(pk,'----',type(pk))
        doctorRemarksPathlab.objects.filter(id=pk).update(pathologyResponse = request.data["pathologyResponse"],remarkpathlab_id = request.user.id)
        # save_doc = doctorRemarksPathlab(remarkreport= request.data["remarkreport"],pathologyResponse = request.data["pathologyResponse"],respathlogy = request.user.id )
        # save_doc.save()
         
            
        return Response({'responseCode': 200, 'responseMessage': "Success"},status=status.HTTP_200_OK)

class PhlebotomistRegisterAPI(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = PhlebotomistRegisterSerializer
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


    def post(self,request,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data

            data = PhlebotomistRegisterSerializer(customuser,context=self.get_serializer_context()).data
            serializer.save()
             
            return Response({
                "responseCode":200,
                "responseData":data,
                "responseMessage":"Successfully Phlebotomist Created",
                
                },status=status.HTTP_200_OK)
        else:
            print(serializer)
            print(serializer.errors)

            return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)

class PhlebotomistUpdateAPI(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = PhlebotomistUpdateSerializer
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


    def post(self,request,pk,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        phlebotomist = CustomUser.objects.get(id=pk)
        print(phlebotomist,'---=')
        serializer = self.get_serializer(phlebotomist,data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data

            data = PhlebotomistUpdateSerializer(customuser,context=self.get_serializer_context()).data
            serializer.save()
             
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

class PhlebotomistGetAPI(generics.GenericAPIView):
    serializer_class = PhlebotomistReadSerializer
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


    def get(self,request,pk,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        phlebotomist = CustomUser.objects.get(id=pk)
        print(phlebotomist,'---=')
        # serializer = self.get_serializer(phlebotomist,data=request.data)
        # if serializer.is_valid():
            # customuser = serializer.validated_data
        if phlebotomist:
            data = PhlebotomistReadSerializer(phlebotomist,context=self.get_serializer_context()).data
            # serializer.save()
             
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

class PathlabRegisterAPI(generics.GenericAPIView):
    serializer_class = PathlabRegisterSerializer
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


    # def get(self,request,*args,**kwargs):
    #     token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
    #     print(token_check,"************")
    #     if token_check=="invalid":
    #         return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
    #     labTest_data=pathlogy.objects.filter(pathlogy_id=pk)
    #     serializer = PathlabRegisterSerializer(labTest_data,many=True)
        
                        
    #     # if serializer.is_valid():        
    #     return Response({
    #                 "responseCode":200,
    #                 "responseData":serializer.data
                    
    #                 },status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        # print(token_check,"************")
        # if token_check=="invalid":
        #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customuser = serializer.validated_data

            data = PathlabRegisterSerializer(customuser,context=self.get_serializer_context()).data
            serializer.save()
             
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


class TestRangeListAPI(generics.GenericAPIView):
    serializer_class = AllTestRangeListSerializer
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


    # def get(self,request,*args,**kwargs):
    #     token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
    #     print(token_check,"************")
    #     if token_check=="invalid":
    #         return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
    #     testRange_data=TestRange.objects.all()
    #     serializer = TestRangeSerializer(testRange_data,many=True)
        
                        
    #     # if serializer.is_valid():        
    #     return Response({
    #                 "responseCode":200,
    #                 "responseData":serializer.data
                    
    #                 },status=status.HTTP_200_OK)

    def get(self,request,test_type='',*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        if test_type =='' or test_type =='complete':
                testRange_data=TestRange.objects.all()
        else:    
                testRange_data=TestRange.objects.filter(test_type=test_type)
        serializer = AllTestRangeListSerializer(testRange_data,many=True)
        
                        
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":serializer.data
                    
                    },status=status.HTTP_200_OK)

class AddTestRangeListAPI(generics.GenericAPIView):
    serializer_class = AllTestRangeListSerializer
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


    
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            testrange = serializer.validated_data

            data = AllTestRangeListSerializer(testrange,context=self.get_serializer_context()).data
            serializer.save()
             
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



class ViewReportTestRangeListAPI(generics.GenericAPIView):
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

    def get(self,request,parameter_name,parameter_value,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        if parameter_name == "barcode":
                labTest_data=PatientTestReport.objects.filter(patientLabTest__barcode=parameter_value)
                patient_details=PatientTest.objects.filter(barcode=parameter_value)[:1]
        elif parameter_name == "citizen":
                labTest_data=PatientTestReport.objects.filter(patientLabTest__patientDetail__member_unique_id=parameter_value)
                patient_details=PatientTest.objects.filter(patientDetail__member_unique_id=parameter_value)[:1]
        else:
            return Response({
                    "responseCode":400,
                    # "responseData":report_data
                    },status=status.HTTP_400_BAD_REQUEST)
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
class UploadTestReportAPI(generics.GenericAPIView):
    serializer_class = PatientTestReportserializers
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

    def post(self,request,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        serializer = self.get_serializer(data=request.data,many=True)
        if serializer.is_valid():
            customuser = serializer.validated_data
            data = PatientTestReportserializers(customuser,context=self.get_serializer_context()).data
            serializer.save()
             
            return Response({
                "responseCode":200,
                "responseMessage":"Data Submitted Successfully"
                
                },status=status.HTTP_200_OK)
        else:
            print(serializer)
            print(serializer.errors)

            return Response({
               "responseCode":400,
               "responseMessage":serializer.errors["non_field_errors"][0],
                },status=status.HTTP_400_BAD_REQUEST)


class GetCitizenTestListAPI(generics.GenericAPIView):
    serializer_class = GetCitizenTestListSerializer
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

    def get(self,request,parameter_name,parameter_value,*args,**kwargs):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        if parameter_name == "barcode":
                patient_details=PatientTest.objects.filter(barcode=parameter_value)#[:1]
                if not patient_details:
                    return Response({
                        "responseCode":400,
                        "responseMessage":"Invalid Barcode"
                        },status=status.HTTP_400_BAD_REQUEST)
                    # },status=status.HTTP_200_OK)
        elif parameter_name == "citizen":
                patient_details=PatientTest.objects.filter(patientDetail__member_unique_id=parameter_value)#[:1]
                if not patient_details:
                    return Response({
                        "responseCode":400,
                        "responseMessage":"Invalid Citizen ID"
                        },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                    "responseCode":400,
                    # "responseData":report_data
                    },status=status.HTTP_400_BAD_REQUEST)
                    # },status=status.HTTP_200_OK)
        # print(labTest_data)
        patient_serializer = CitizenLabTestserializers(patient_details,many=True)
        serializer = GetCitizenTestListSerializer(patient_details,many=True)
        report_data = {}
        report_data['citizen_details']=patient_serializer.data
        report_data['report']=serializer.data     
        # if serializer.is_valid():        
        return Response({
                    "responseCode":200,
                    "responseData":report_data
                    
                    },status=status.HTTP_200_OK)
from django.contrib.auth import logout
class LogoutAPI(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated]
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
    def get(self, request):
        # simply delete the token to force a login
        logout(request)#request.user.knox_authtoken.delete()
        return Response({
                    "responseCode":200,
                    "responseMessage":"Successfully Logged Out" 
                    },status=status.HTTP_200_OK)
    # def post(self,request,*args,**kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         testrange = serializer.validated_data

    #         data = AllTestRangeListSerializer(testrange,context=self.get_serializer_context()).data
    #         serializer.save()
             
    #         return Response({
    #             "responseCode":200,
    #             "responseData":data
                
    #             },status=status.HTTP_200_OK)
    #     else:
    #         print(serializer)
    #         print(serializer.errors)

    #         return Response({
    #            "responseCode":400,
    #            "responseMessage":serializer.errors["non_field_errors"][0],
    #             },status=status.HTTP_400_BAD_REQUEST)


# class API(generics.GenericAPIView):
#     serializer_class = TestReportSerializer
#     parser_classes = [FormParser]
#     @swagger_auto_schema(
#         manual_parameters=[
#               openapi.Parameter(
#                 name='nonce', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_STRING,
#                 description="Nonce",
#                 required=True,
#                 default="12345654"
#             ),

#             openapi.Parameter(
#                 name='timestamp', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_STRING,
#                 # format="date-time",   
#                 description="Timestamp",
#                 required=True,
#                 default="12345654"
#             ),
#             openapi.Parameter(
#                 name='token', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_STRING,   
#                 description="token",
#                 required=True,
#                 default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
#             )
#         ],
        
#     )

#     def get(self,request,pk,*args,**kwargs):
#         token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
#         print(token_check,"************")
#         if token_check=="invalid":
#             return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
#         labTest_data=labReport.objects.filter(pathlogy_id=pk)
#         serializer = labReportSerializer(labTest_data,many=True)
        
                        
#         # if serializer.is_valid():        
#         return Response({
#                     "responseCode":200,
#                     "responseData":serializer.data
                    
#                     },status=status.HTTP_200_OK)

#     def post(self,request,pk,*args,**kwargs):
#         # token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
#         # print(token_check,"************")
#         # if token_check=="invalid":
#         #     return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             customuser = serializer.validated_data
#             data = labReportSerializer(customuser,context=self.get_serializer_context()).data
            
             
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
# class LabTestCUAPI(generics.GenericAPIView):
#     serializer_class = labTestSerializer
#     parser_classes = [FormParser]
#     @swagger_auto_schema(
#         manual_parameters=[
#               openapi.Parameter(
#                 name='nonce', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_STRING,
#                 description="Nonce",
#                 required=True,
#                 default="12345654"
#             ),

#             openapi.Parameter(
#                 name='timestamp', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_STRING,
#                 # format="date-time",   
#                 description="Timestamp",
#                 required=True,
#                 default="12345654"
#             ),
#             openapi.Parameter(
#                 name='token', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_STRING,   
#                 description="token",
#                 required=True,
#                 default="c91112c5c0475c411639e7b224962807e6ca38b8639529f6ebf3d3fdb0112b38"
#             )
#         ],
        
#     )


#     def post(self,request,*args,**kwargs):
#         token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
#         print(token_check,"************")
#         if token_check=="invalid":
#             return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
#         labTest_data=labTest.objects.filter(pathlogy_id=pk)
#         serializer = labTestSerializer(labTest_data,many=True)
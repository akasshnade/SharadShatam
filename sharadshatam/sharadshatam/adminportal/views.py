from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import generics
from adminportal.serializers import *
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from knox.models import AuthToken
from rest_framework import generics, permissions
from django.contrib.auth.hashers import make_password,check_password
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from database.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
import random
import os
import string
from datetime import datetime
import hmac
import hashlib
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .paginations import CustomPagination
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



class AdminLoginAPI(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
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
            groups=customuser.groups.values_list('name',flat = True)
            print(groups)
            
            
            
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
            # Establish connection to MySQL database
            import mysql.connector

            mydb = mysql.connector.connect(
                host="database-2.cxt35h3oleim.ap-south-1.rds.amazonaws.com",
                user="admin",
                password="Insulated10*",
                database="shatamdb"
            )

            # Create a cursor object
            mycursor = mydb.cursor()

            # Execute the query
            query1 = "SELECT count(*) FROM shatamdb.database_familymembers"

            query2 = "SELECT count(*) FROM shatamdb.database_patienttest"
            query3 = "SELECT count(*) FROM shatamdb.database_patienttest WHERE isCompleted=1"
            query4 = "SELECT  count(*) FROM shatamdb.database_patienttest WHERE isCompleted=0"
            query5 = "SELECT  count(*) FROM shatamdb.database_pathlogy"
            # query6 = "SELECT count(*)  FROM SELECT count(*) FROM shatamdb.database_familymembers;"
            queries = [query1,query2,query3,query4,query5]
            results = mycursor.execute(";".join(queries), data, multi=True)

            count = 1
            dashboard = {}
            lst = []
            for result in results:

                if result.with_rows:
                    for row in result:
                        print(row)
                        lst.append(row[0])
                        # dashboard.update()

            mycursor.close()
            # Close database connection
            mydb.close()
            print(lst,"$$$$$$$44444444")
            lst.append(5)
            lst.append(6)
            lst.append(8)
            name = ["no_of_seneior_citizen","no_of_test_reported","no_of_test_completed","no_of_test_in_progress","no_of_health_facility","no_of_patients_attended_by_doctor","no_of_empaneled_doctors","no_of_empaneled_labs"]
           
            data["user_group"] = "Admin"
            data["token"]=token
            data["dashboard"]= dict(zip(name, lst))
   
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



class PhcLoginAPI(generics.GenericAPIView):
    serializer_class = PhcLoginSerializer
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
            groups=customuser.groups.values_list('name',flat = True)
            print(groups)
            
            
            
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




class PhcRegisterAPI(generics.GenericAPIView):
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
            group = Group.objects.get(name="phcUser")
            group.user_set.add(user)

            return Response({
            "responseCode":200,
            # "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
        else:
            print(type(serializer.errors))
            return Response({"responseCode":400,"responseMessage":serializer.errors["non_field_errors"][0]},status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedSpecialistCitizenList(generics.GenericAPIView):

    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = AllMedicalSurveySerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type','doctorConsultancy__isPending','doctorConsultancy__isMedication','doctorConsultancy__isHospitalisation','doctorConsultancy__isElderline','doctorConsultancy__phcConsultation','doctorConsultancy__specialistConsultation','doctorConsultancy__assignedDoctor_id')
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
    def get_queryset(self):
        assignedDoctor_id = self.kwargs.get('doctorConsultancy__assignedDoctor_id')
        dc_fm=[]
        if assignedDoctor_id is not None:
            dc_fm = doctorConsultancy.objects.filter(assignedDoctor_id=assignedDoctor_id).values_list('docpatient_id').distinct()
            #dc_fm = doctorConsultancy.objects.filter(assignedDoctor_id=self.request.user.id).values_list('docpatient_id').distinct()
        else:
            dc_fm = doctorConsultancy.objects.values_list('docpatient_id').distinct()
        return familyMembers.objects.filter(id__in=dc_fm)

class HospitalRegisterAPI(generics.GenericAPIView):
    '''
    corporationUser,talukaUser,councilUser,wardUser
    '''
    serializer_class = HospitalRegisterSerializer
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='group', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Group name",
                required=True,
                
            ),
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
        groupname = self.request.headers["group"]
        print(groupname,"@@@@@@@@@@@@@@@@@@@@22")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        serializer = self.get_serializer(data=request.data)
        phone = request.data["concernedPhone"]
        if 'concernedPhone' in request.data and request.data["concernedPhone"]=="":
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
            group = Group.objects.get(name=groupname)
            group.user_set.add(user)

            return Response({
            "responseCode":200,
            # "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
        else:
            print(type(serializer.errors))
            print(serializer.errors,'----------Error')
            # hh
            return Response({"responseCode":400,"responseMessage":serializer.errors["non_field_errors"][0]},status=status.HTTP_400_BAD_REQUEST)
            
class AllMedicalSurveyList(generics.GenericAPIView):
    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    queryset = familyMembers.objects.all()
    # permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = AllMedicalSurveySerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type','current_isPending','current_isMedication','current_isHospitalisation','current_phcConsultation','current_specialistConsultation','current_isElderline','isCaseClosed')
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


class HospitalCitizenList(generics.GenericAPIView):

    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = HospitalCitizenSerializer
    # serializer_class = AllMedicalSurveySerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type','doctorConsultancy__isPending','doctorConsultancy__isMedication','doctorConsultancy__isHospitalisation','doctorConsultancy__isElderline','doctorConsultancy__phcConsultation','doctorConsultancy__specialistConsultation','doctorConsultancy__isCompleted','doctorConsultancy__assignedDistrictHospital__concernedPerson_id','current_isPending','current_isMedication','current_isHospitalisation','current_phcConsultation','current_specialistConsultation','current_isElderline','isCaseClosed')
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
    def get_queryset(self):
        assignedDistrictHospital_id = self.kwargs.get('doctorConsultancy__assignedDistrictHospital__concernedPerson_id')
        dc_fm=[]
        if assignedDistrictHospital_id is not None:
            dc_fm = doctorConsultancy.objects.filter(assignedDistrictHospital__concernedPerson_id=assignedDistrictHospital_id).values_list('docpatient_id').distinct()
            #dc_fm = doctorConsultancy.objects.filter(assignedDoctor_id=self.request.user.id).values_list('docpatient_id').distinct()
        else:
            dc_fm = doctorConsultancy.objects.values_list('docpatient_id').distinct()
        return familyMembers.objects.filter(id__in=dc_fm)
        

class AllMedicalSurveyListNoPage(generics.GenericAPIView):
    """
    List all Survey Records with Filters
    """
    # queryset = familyHeadDetails.objects.all()
    queryset = familyMembers.objects.all()
    # permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = AllMedicalSurveySerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type','current_isPending','current_isMedication','current_isHospitalisation','current_phcConsultation','current_specialistConsultation','current_isElderline','isCaseClosed')
    search_fields = ['mobile','family_head__family_head_member__member_unique_id','member_name','member_gender','member_age']
    
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
        
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class Custdashboard(generics.GenericAPIView):
    """
    Dashboard district,Corporation, Ward, council,taluka,phc Wise
    """

    serializer_class = CustomDashboardSerializer
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


    def post(self, request, format=None):
        data = {}

        filter_dict={}
        filter_dict1={}
        filter_dict2={}
        filter_dict3={}
        filter_dict4={}
        filter_dict5={}
        filter_dict6={}

        filter_dict11={}
        filter_dict12={}
        filter_dict13={}
        filter_dict14={}
        filter_dict15={}
        filter_dict16={}

        if request.data.get('district') != None:
            filter_dict['family_head__familyAddress__district']=request.data.get('district')
            filter_dict1['familyAddress__district']=request.data.get('district')
            filter_dict2['district']=request.data.get('district')
            filter_dict3['patientDetail__family_head__familyAddress__district']=request.data.get('district')
            filter_dict4['hospitaldistrict__districtName']=request.data.get('district')
            filter_dict5['taluka__dist__districtName']=request.data.get('district')
            filter_dict6['docpatient__family_head__familyAddress__district']=request.data.get('district')
            filter_dict11['familyAddress__district']=request.data.get('district')
            filter_dict12['specialist_docpatient__family_head__familyAddress__district']=request.data.get('district')



        if request.data.get('region_type') != None:
            filter_dict['family_head__familyAddress__region_type']=request.data.get('region_type')
            filter_dict1['familyAddress__region_type']=request.data.get('region_type')
            filter_dict2['region_type']=request.data.get('region_type')
            filter_dict3['patientDetail__family_head__familyAddress__region_type']=request.data.get('region_type')
            filter_dict6['docpatient__family_head__familyAddress__region_type']=request.data.get('region_type')

            filter_dict11['familyAddress__region_type']=request.data.get('region_type')
            filter_dict12['specialist_docpatient__family_head__familyAddress__region_type']=request.data.get('region_type')


        if request.data.get('municipal_corporation') != None:
            filter_dict['family_head__familyAddress__municipal_corporation']=request.data.get('municipal_corporation')
            filter_dict1['familyAddress__municipal_corporation']=request.data.get('municipal_corporation')
            filter_dict2['municipal_corporation']=request.data.get('municipal_corporation')
            filter_dict3['patientDetail__family_head__familyAddress__municipal_corporation']=request.data.get('municipal_corporation')
            filter_dict6['docpatient__family_head__familyAddress__municipal_corporation']=request.data.get('municipal_corporation')
            filter_dict11['familyAddress__municipal_corporation']=request.data.get('municipal_corporation')
            filter_dict12['specialist_docpatient__family_head__familyAddress__municipal_corporation']=request.data.get('municipal_corporation')




        if request.data.get('ward') != None:
            filter_dict['family_head__familyAddress__ward']=request.data.get('ward')
            filter_dict1['familyAddress__ward']=request.data.get('ward')
            filter_dict2['ward']=request.data.get('ward')
            filter_dict3['patientDetail__family_head__familyAddress__ward']=request.data.get('ward')
            filter_dict6['docpatient__family_head__familyAddress__ward']=request.data.get('ward')
            filter_dict11['familyAddress__ward']=request.data.get('ward')
            filter_dict12['specialist_docpatient__family_head__familyAddress__ward']=request.data.get('ward')



        if request.data.get('taluka') != None:
            filter_dict['family_head__familyAddress__taluka']=request.data.get('taluka')
            filter_dict1['familyAddress__taluka']=request.data.get('taluka')
            filter_dict2['taluka']=request.data.get('taluka')
            filter_dict3['patientDetail__family_head__familyAddress__taluka']=request.data.get('taluka')
            filter_dict5['taluka__talukaName']=request.data.get('taluka')
            filter_dict6['docpatient__family_head__familyAddress__taluka']=request.data.get('taluka')
            filter_dict11['familyAddress__taluka']=request.data.get('taluka')
            filter_dict12['specialist_docpatient__family_head__familyAddress__taluka']=request.data.get('taluka')



        if request.data.get('phc') != None:
            filter_dict['family_head__familyAddress__phc']=request.data.get('phc')
            filter_dict1['familyAddress__phc']=request.data.get('phc')
            filter_dict2['phc']=request.data.get('phc')
            filter_dict3['patientDetail__family_head__familyAddress__phc']=request.data.get('phc')
            filter_dict5['phcName']=request.data.get('phc')
            filter_dict6['docpatient__family_head__familyAddress__phc']=request.data.get('phc')
            filter_dict11['familyAddress__phc']=request.data.get('phc')
            filter_dict12['specialist_docpatient__family_head__familyAddress__phc']=request.data.get('phc')




        if request.data.get('municipal_council') != None:
            filter_dict['family_head__familyAddress__municipal_council']=request.data.get('municipal_council')
            filter_dict1['familyAddress__municipal_council']=request.data.get('municipal_council')
            filter_dict2['municipal_council']=request.data.get('municipal_council')
            filter_dict3['patientDetail__family_head__familyAddress__municipal_council']=request.data.get('municipal_council')
            filter_dict6['docpatient__family_head__familyAddress__municipal_council']=request.data.get('municipal_council')
            filter_dict11['familyAddress__municipal_council']=request.data.get('municipal_council')

            filter_dict12['specialist_docpatient__family_head__familyAddress__municipal_council']=request.data.get('municipal_council')


        no_of_seneior_citizen = familyMembers.objects.filter(**filter_dict).count()
        # total_no_of_families = familyHeadDetails.objects.filter(**filter_dict1).count()
        no_of_test_reported  = PatientTest.objects.filter(**filter_dict3).count()
        no_of_test_completed  = PatientTest.objects.filter(**filter_dict3,isCompleted=True).count()
        no_of_test_in_progress  = PatientTest.objects.filter(**filter_dict3,isCompleted=False).count()

        no_empaneled_labs  = pathlogy.objects.filter(**filter_dict2).count()
        no_health_facility  = districtHospital.objects.filter(**filter_dict4).count() + primaryHealthCenter.objects.filter(**filter_dict5).count()
        # no_health_facility = 58
        no_empaneled_doctor  = CustomUser.objects.filter(**filter_dict2,groups__name = "doctor").count()
        no_of_patients_attended_by_doctor  = phcConsultancy.objects.filter(**filter_dict6,isPending=False).count()

        no_of_families_visited = familyHeadDetails.objects.filter(**filter_dict11).count()
        no_of_seneior_citizen_surveyed = familyMembers.objects.filter(**filter_dict).count()


        no_of_seneior_citizen_surveyed_in_consultation = phcConsultancy.objects.filter(**filter_dict6,phcConsultation=True).count() + specialistConsultancy.objects.filter(**filter_dict12,specialist_Consultation=True).count()
        no_of_seneior_citizen_surveyed_in_medication = phcConsultancy.objects.filter(**filter_dict6,isMedication=True).count() + specialistConsultancy.objects.filter(**filter_dict12,specialist_isMedication=True).count()
        no_of_seneior_citizen_surveyed_in_hospitalisation = phcConsultancy.objects.filter(**filter_dict6,isHospitalisation=True).count() + specialistConsultancy.objects.filter(**filter_dict12,specialist_isHospitalisation=True).count()

        total_no_of_closed_medical_cases = phcConsultancy.objects.filter(**filter_dict6,isCaseClosed=True).count() + specialistConsultancy.objects.filter(**filter_dict12,specialist_isCaseClosed=True).count()



        total_no_of_primary_health_center = primaryHealthCenter.objects.filter(**filter_dict5).count()
        total_no_district_hospital  = districtHospital.objects.filter(**filter_dict4).count()
        total_no_phc_supervisors  = CustomUser.objects.filter(**filter_dict2,groups__name = "supervisors").count()
        total_no_phc_doctors  = CustomUser.objects.filter(**filter_dict2,groups__name = "phcUser").count()

        total_no_phc_surveyors  = CustomUser.objects.filter(**filter_dict2,groups__name = "surveyors").count()



#pathology
        #PatientTestReport
        data["no_of_seneior_citizen"]= no_of_seneior_citizen
        data["no_of_test_reported"]= no_of_test_reported
        data["no_of_test_completed"]= no_of_test_completed
        data["no_of_test_in_progress"]= no_of_test_in_progress
        data["no_empaneled_labs"]= no_empaneled_labs
        data["no_health_facility"]= no_health_facility
        data["no_empaneled_doctor"]=no_empaneled_doctor
        data["no_of_patients_attended_by_doctor"]=no_of_patients_attended_by_doctor




        data["no_of_families_visited"]= no_of_families_visited
        data["no_of_seneior_citizen_surveyed"]= no_of_test_reported
        data["gender_wise_count"]= {"male":familyMembers.objects.filter(**filter_dict,member_gender="male").count(),"female":familyMembers.objects.filter(**filter_dict,member_gender="female").count(),"others":familyMembers.objects.filter(**filter_dict,member_gender="others").count()}
        data["no_of_seneior_citizen_surveyed_in_consultation"]= no_of_seneior_citizen_surveyed_in_consultation
        data["no_of_seneior_citizen_surveyed_in_medication"]= no_of_seneior_citizen_surveyed_in_medication
        data["no_of_seneior_citizen_surveyed_in_hospitalisation"]= no_of_seneior_citizen_surveyed_in_hospitalisation
        data["total_no_of_closed_medical_cases"]=total_no_of_closed_medical_cases
        data["total_no_senior_citizen_diagnosed_with_tb"]=familyMembers.objects.filter(**filter_dict,suspected_tuberculosis=True).count()
        data["total_no_senior_citizen_diagnosed_with_cancer"]=familyMembers.objects.filter(Q(suspected_mouth_cancer =True)|Q(suspected_cancer=True)|Q(suspected_breast_cancer=True)|Q(suspected_cervical_cancer=True),**filter_dict).count()



        data["total_no_of_health_facility"]= no_health_facility
        data["total_no_of_primary_health_center"]= total_no_of_primary_health_center
        data["total_no_district_hospital"]= total_no_district_hospital
        data["total_no_phc_doctors"]= total_no_phc_doctors
        data["total_no_phc_supervisors"]= total_no_phc_supervisors
        data["total_no_phc_surveyors"]= total_no_phc_surveyors


        data["total_no_of_empaneled_labs"]= no_empaneled_labs
        data["total_no_of_test_reported"]= no_of_test_reported
        data["total_no_test_completed"]= no_of_test_completed
        data["total_no_test_in_progress"]= no_of_test_in_progress
        data["total_no_sample_collected"]= no_of_test_in_progress




        #no_of_seneior_citizen.count()


        # print(request.data["district"],"@@@@@@@@@@@@@@@@")

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':data},status=status.HTTP_200_OK)

class CustomDashboard(generics.GenericAPIView):
    """
    Dashboard
    """
    from django.db.models import Count
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.filter().order_by('-id')
    # queryset = familyMembers.objects.aggregate(no_of_seneior_citizen = Count('pk'))
    # permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = CustomDashboardSerializer
    # parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    # filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type')
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
    # def get_extra_counts(self): ## in this function first get the filtered queryset then do the aggregate and return it
    #     from django.db.models import Count
    #     queryset = self.filter_queryset(self.get_queryset())
    #     return queryset.aggregate(
    #         no_of_seneior_citizen=Count('pk')
    #         # estados=Count('pk', filter=Q(cidade__isnull=True)),
    #         # estados_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=True))),
    #         # municipios_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=False))),
    #     )
    def get(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        extra_counts = self.get_extra_counts() ## get the extra_counts on the filtered queryset
        print(extra_counts)
        # qs['no_of_seneior_citizen'] = extra_counts['no_of_seneior_citizen']

        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        # serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':qs},status=status.HTTP_200_OK)




class NewCustomDashboard(generics.ListAPIView):
    """
    Dashboard
    """
    
    # queryset = familyHeadDetails.objects.all()
    # queryset = familyMembers.objects.all()
    queryset = familyMembers.objects.filter().order_by('-id')
    # permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = NewfamilyHeadSerializer
    serializer_class = AllMedicalSurveySerializer
    # parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc','family_head_member__member_unique_id')
    filterset_fields = ('family_head__familyAddress__district','family_head__familyAddress__region_type','family_head__familyAddress__municipal_corporation','family_head__familyAddress__ward','family_head__familyAddress__municipal_council','family_head__familyAddress__taluka','family_head__familyAddress__village','family_head__familyAddress__phc','family_head__familyAddress__sc','family_head__family_head_member__member_unique_id','doctorConsultancy__suggestion_type')
    # pagination_class = CustomPagination
    # pagination_class.page_size = 5

    def get_extra_counts(self): ## in this function first get the filtered queryset then do the aggregate and return it
        from django.db.models import Count
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.aggregate(
            no_of_seneior_citizen=Count('pk')
            # estados=Count('pk', filter=Q(cidade__isnull=True)),
            # estados_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=True))),
            # municipios_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=False))),
        )
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



    def list(self, request):
        response = super(NewCustomDashboard, self).list(self, request)
        extra_counts = self.get_extra_counts() ## get the extra_counts on the filtered queryset
        response.data.pop("results")




        response.data['total_no_of_families'] = extra_counts['no_of_seneior_citizen']
        response.data['no_of_seneior_citizen'] = extra_counts['no_of_seneior_citizen']
        response.data['gender_wise_count'] = {"male":25,"female":35,"others":10}

        response.data['no_of_seneior_citizen_in_consultation'] = extra_counts['no_of_seneior_citizen']
        response.data['no_of_seneior_citizen_in_medication'] = extra_counts['no_of_seneior_citizen']
        response.data['no_of_seneior_citizen_in_hospitalisation'] = extra_counts['no_of_seneior_citizen']


        response.data['total_no_of_closed_cases'] = extra_counts['no_of_seneior_citizen']
        response.data['no_of_seneior_citizen_diagnosed_with_cancer'] = extra_counts['no_of_seneior_citizen']
        response.data['no_of_seneior_citizen_diagnosed_with_tb'] = extra_counts['no_of_seneior_citizen']


        # response.data['estados'] = extra_counts['estados']
        # response.data['estados_aderidos'] = extra_counts['estados_aderidos']
        # response.data['municipios_aderidos'] = extra_counts['municipios_aderidos']
        return response
    # def get(self, request, format=None):
    #     token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
    #     print(token_check,"************")
    #     if token_check=="invalid":
    #         return Response({"responseCode":204,"responseMessage":"Invalid TOken"})


    #     qs = self.get_queryset()
    #     # qs = self.filter_queryset(qs)
    #     # page = self.paginate_queryset(qs)

    #     # if page is not None:
    #     #     serializer = self.serializer_class(page, many=True)
    #     #     return self.get_paginated_response(serializer.data)
    #     # serializer = self.get_serializer(instance=qs, many=True)
    #     # serializer = self.get_serializer(instance=qs, many=True)

    #     return Response({"responseCode":200, 'responseMessage': "Success",'responseData':qs},status=status.HTTP_200_OK)





class MedicalSurveyDetail(generics.GenericAPIView):

    # permission_classes = [permissions.IsAuthenticated,]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    serializer_class = NewfamilyHeadSerializer
    # parser_classes = [FormParser]
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
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})



        queryset = familyHeadDetails.objects.filter(id=pk)
        if queryset:
            card = get_object_or_404(queryset, pk=pk)
            # card = CustomUser.objects.get(pk=pk)
            temp = DisplayNewfamilyHeadSerializer(card).data
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':temp},status=status.HTTP_200_OK)

        else:
            validation_message ='data not found'
            return Response({"responseCode":400, 'responseMessage': validation_message},status=status.HTTP_400_BAD_REQUEST)




class GetDistrictWiseHospitalList(GenericAPIView):
    """
    List District Wise Hospital List

    """
    queryset = districtHospital.objects.all()

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AlldistrictHospitalList
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('hospitalName', 'category','hospitaldistrict__id','hospitaldistrict__districtName',)
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


class GetdistrictList(GenericAPIView):
    """
    List all District
    """
    queryset = district.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = Alldistrict
    parser_classes = [FormParser]
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
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['isCompleted', 'created_date','response_date']

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



class GettalukaList(GenericAPIView):
    """
    List all District wise Taluka
    """
    queryset = taluka.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = Alltaluka
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('talukaName', 'dist__id','dist__districtName',)
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



class GetprimaryHealthCenterList(GenericAPIView):
    """
    List Primary Health Center
    """
    queryset = primaryHealthCenter.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllprimaryHealthCenter
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['phcName', 'taluka__id','taluka__talukaName']
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




class GetsubCenterList(GenericAPIView):
    """
    List Sub Center
    """
    queryset = subCenter.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllsubCenter
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scName', 'Phc__id','Phc__phcName']
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



class GetvillageList(GenericAPIView):
    """
    List Village List
    """
    queryset = village.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = Allvillage
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['villageName', 'Sc__id','Sc__scName']
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



class GetmunicipalCorporationList(GenericAPIView):
    """
    List of Municipal Corporation
    """
    queryset = municipalCorporation.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllmunicipalCorporation
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mcName', 'dist__id','dist__districtName']
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
            # return self.get_paginated_response(serializer.data)
        # serializer = self.get_serializer(instance=qs, many=True)
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)


class GetmunicipalWardList(GenericAPIView):
    """
    List of Municipal Corporation Ward
    """
    queryset = mcWard.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllmcWard
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ward', 'mcrop__id','mcrop__mcName']
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



class GetmunicipalCouncilList(GenericAPIView):
    """
    List of Municipal Council
    """
    queryset = municipalCouncil.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AllmunicipalCouncil
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['councilName', 'dist__id','dist__districtName']
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


class GetcantonmentBoardList(GenericAPIView):
    """
    List of CantonmentBoard
    """
    queryset = cantonmentBoard.objects.all()

    # permission_classes = [permissions.A,]
    serializer_class = AllcantonmentBoard
    parser_classes = [FormParser]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['canttName', 'dist__id','dist__districtName']
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












class AdminDashboard(GenericAPIView):
    """
    Admin Dashboard
    """
    # queryset = cantonmentBoard.objects.all()

    # # permission_classes = [permissions.A,]
    serializer_class = AdminDashboardSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
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
    def post(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})

        data= {}
        import mysql.connector

        mydb = mysql.connector.connect(
            host="database-2.cxt35h3oleim.ap-south-1.rds.amazonaws.com",
            user="admin",
            password="Insulated10*",
            database="shatamdb"
        )
        mycursor = mydb.cursor()

        if "district" and "taluka" in request.data:
            print(request.data["district"],"@@@@@@@@@@@@@@@@@")
            # print(request.data["taluka"],"@@@@@@@@@@@@@@@@@")

            if  "taluka"   in request.data:
                print(request.data["taluka"],"@@@@@@@@@@@@@@@@@")
                query1 = "SELECT count(*) FROM shatamdb.database_familymembers"

                query2 = "SELECT count(*) FROM shatamdb.database_patienttest"
                query3 = "SELECT count(*) FROM shatamdb.database_patienttest WHERE isCompleted=1"
                query4 = "SELECT  count(*) FROM shatamdb.database_patienttest WHERE isCompleted=0"
                query5 = "SELECT  count(*) FROM shatamdb.database_pathlogy"
                # query6 = "SELECT count(*)  FROM SELECT count(*) FROM shatamdb.database_familymembers;"
                queries = [query1,query2,query3,query4,query5]
                results = mycursor.execute(";".join(queries), data, multi=True)

                count = 1
                dashboard = {}
                lst = []
                for result in results:

                    if result.with_rows:
                        for row in result:
                            print(row)
                            lst.append(row[0])
                            # dashboard.update()

                mycursor.close()
                # Close database connection
                mydb.close()
                print(lst,"$$$$$$$44444444")
                lst.append(5)
                lst.append(6)
                lst.append(8)
                name = ["no_of_seneior_citizen","no_of_test_reported","no_of_test_completed","no_of_test_in_progress","no_of_health_facility","no_of_patients_attended_by_doctor","no_of_empaneled_doctors","no_of_empaneled_labs"]

                data["dashboard"]= dict(zip(name, lst))

            else:
                query1 = "SELECT count(*) FROM shatamdb.database_familymembers"

                query2 = "SELECT count(*) FROM shatamdb.database_patienttest"
                query3 = "SELECT count(*) FROM shatamdb.database_patienttest WHERE isCompleted=1"
                query4 = "SELECT  count(*) FROM shatamdb.database_patienttest WHERE isCompleted=0"
                query5 = "SELECT  count(*) FROM shatamdb.database_pathlogy"
                # query6 = "SELECT count(*)  FROM SELECT count(*) FROM shatamdb.database_familymembers;"
                queries = [query1,query2,query3,query4,query5]
                results = mycursor.execute(";".join(queries), data, multi=True)

                count = 1
                dashboard = {}
                lst = []
                for result in results:

                    if result.with_rows:
                        for row in result:
                            print(row)
                            lst.append(row[0])
                            # dashboard.update()

                mycursor.close()
                # Close database connection
                mydb.close()
                print(lst,"$$$$$$$44444444")
                lst.append(5)
                lst.append(6)
                lst.append(8)
                name = ["no_of_seneior_citizen","no_of_test_reported","no_of_test_completed","no_of_test_in_progress","no_of_health_facility","no_of_patients_attended_by_doctor","no_of_empaneled_doctors","no_of_empaneled_labs"]

                data["dashboard"]= dict(zip(name, lst))


            
        
        else:



        # Create a cursor object

            # Execute the query
            query1 = "SELECT count(*) FROM shatamdb.database_familymembers"

            query2 = "SELECT count(*) FROM shatamdb.database_patienttest"
            query3 = "SELECT count(*) FROM shatamdb.database_patienttest WHERE isCompleted=1"
            query4 = "SELECT  count(*) FROM shatamdb.database_patienttest WHERE isCompleted=0"
            query5 = "SELECT  count(*) FROM shatamdb.database_pathlogy"
            # query6 = "SELECT count(*)  FROM SELECT count(*) FROM shatamdb.database_familymembers;"
            queries = [query1,query2,query3,query4,query5]
            results = mycursor.execute(";".join(queries), data, multi=True)

            count = 1
            dashboard = {}
            lst = []
            for result in results:

                if result.with_rows:
                    for row in result:
                        print(row)
                        lst.append(row[0])
                        # dashboard.update()

            mycursor.close()
            # Close database connection
            mydb.close()
            print(lst,"$$$$$$$44444444")
            lst.append(5)
            lst.append(6)
            lst.append(8)
            name = ["no_of_seneior_citizen","no_of_test_reported","no_of_test_completed","no_of_test_in_progress","no_of_health_facility","no_of_patients_attended_by_doctor","no_of_empaneled_doctors","no_of_empaneled_labs"]

            data["dashboard"]= dict(zip(name, lst))


        # qs = self.get_queryset()
        # qs = self.filter_queryset(qs)
        # serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':data},status=status.HTTP_200_OK)



class UserDetail(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated,]
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    serializer_class = OtherUserDetailSerializer
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
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})



        queryset = CustomUser.objects.filter(id=pk)
        if queryset:
            card = get_object_or_404(queryset, pk=pk)
            # card = CustomUser.objects.get(pk=pk)
            temp = OtherUserDetailSerializer(card).data
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':temp},status=status.HTTP_200_OK)

        else:
            validation_message ='data not found'
            return Response({"responseCode":400, 'responseMessage': validation_message},status=status.HTTP_400_BAD_REQUEST)

        # temp["group"] = card.group
        # return Response(serializer.data)



class ChangeNewPassword(generics.GenericAPIView):
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
            ),       

        ],
        
    )
    def post(self, request):    
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        

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



class EditSelfProfile(generics.GenericAPIView):
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
            ),       

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


        
        if request.data.get("name")!="" or request.data.get("name")!=None:
            name = request.data["name"]

        if request.data.get("email")!="" and request.data.get("email")!=None:
            email = request.data["email"]

        user_id=request.user.id
        queryset = CustomUser.objects.filter(id=user_id)
        if queryset:
            if name!="":
                user_exists = CustomUser.objects.filter(id=user_id).update(name=name)
            if email!="":
                user_exists = CustomUser.objects.filter(id=user_id).update(email=email)
            card = get_object_or_404(queryset, pk=user_id)
            # card = CustomUser.objects.get(pk=pk)
            temp = OtherUserSerializer(card).data

        else:
            card = get_object_or_404(queryset, pk=user_id)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Profile edited successfully","responseData":temp},status=status.HTTP_200_OK)

class EditProfile(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Edit Profile 
    """
    # permission_classes = [permissions.IsAuthenticated,]
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
            ),       

        ],
        
    )

    def post(self, request,user_id):    
        

        name = ""
        email = ""
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":400,"responseMessage":"Invalid TOken"})

        if not request.data:
            validation_message = 'Please provide data'
            return Response({'status': 'error', 'message': validation_message})


        
        if request.data.get("name")!="" or request.data.get("name")!=None:
            name = request.data["name"]

        if request.data.get("email")!="" and request.data.get("email")!=None:
            email = request.data["email"]

        queryset = CustomUser.objects.filter(id=user_id)
        if queryset:
            if name!="":
                user_exists = CustomUser.objects.filter(id=user_id).update(name=name)
            if email!="":
                user_exists = CustomUser.objects.filter(id=user_id).update(email=email)
            card = get_object_or_404(queryset, pk=user_id)
            # card = CustomUser.objects.get(pk=pk)
            temp = OtherUserSerializer(card).data

        else:
            card = get_object_or_404(queryset, pk=user_id)
        return Response({'responseCode': 200, 'responseMessage': "Profile edited successfully!","responseData":temp},status=status.HTTP_200_OK)



class dashboardDistrict(generics.GenericAPIView):
    """
    Dashboard District Wise
    """
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


    def get(self, request, format=None):

        temp = "no_of_seneior_citizen"
        alldistrict = total_district_dashboard.objects.all().values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)




class dashboardTaluka(generics.GenericAPIView):
    """
    Dashboard Taluka Wise
    """
    serializer_class = TalukadashboardSerializer
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


    def post(self, request, format=None):
        print(request.data["district"],"@@@@@@@@@@@@@@@@")
        temp = "no_of_seneior_citizen"
        alldistrict = total_taluka_dashboard.objects.filter(district = request.data["district"]).values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)



class dashboardPHC(generics.GenericAPIView):
    """
    Dashboard PHC Wise
    """

    serializer_class = PhcdashboardSerializer
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


    def post(self, request, format=None):
        print(request.data["district"],"@@@@@@@@@@@@@@@@")
        temp = "no_of_seneior_citizen"
        alldistrict = total_phc_dashboard.objects.filter(district = request.data["district"],taluka=request.data["taluka"]).values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)






class dashboardSC(generics.GenericAPIView):
    """
    Dashboard SC Wise
    """

    serializer_class = ScdashboardSerializer
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


    def post(self, request, format=None):
        print(request.data["district"],"@@@@@@@@@@@@@@@@")
        temp = "no_of_seneior_citizen"
        alldistrict = total_sc_dashboard.objects.filter(district = request.data["district"],taluka=request.data["taluka"],phc_name = request.data["phc_name"]).values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)



class dashboardCouncil(generics.GenericAPIView):
    """
    Dashboard Council Wise
    """

    serializer_class = CouncildashboardSerializer
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


    def post(self, request, format=None):
        print(request.data["district"],"@@@@@@@@@@@@@@@@")
        temp = "no_of_seneior_citizen"
        alldistrict = total_council_dashboard.objects.filter(district = request.data["district"]).values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)


class dashboardCorporation(generics.GenericAPIView):
    """
    Dashboard Municipal Corporation Wise
    """

    serializer_class = CouncildashboardSerializer
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


    def post(self, request, format=None):
        print(request.data["district"],"@@@@@@@@@@@@@@@@")
        temp = "no_of_seneior_citizen"
        alldistrict = total_mcrop_dashboard.objects.filter(district = request.data["district"]).values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)



class dashboardWard(generics.GenericAPIView):
    """
    Dashboard Corporation Ward Wise
    """

    serializer_class = WarddashboardSerializer
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


    def post(self, request, format=None):
        print(request.data["district"],"@@@@@@@@@@@@@@@@")
        temp = "no_of_seneior_citizen"
        alldistrict = total_ward_dashboard.objects.filter(district = request.data["district"],municipal_corporation=request.data["municipal_corporation"]).values()

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':alldistrict},status=status.HTTP_200_OK)




















# def DistrictSchedular():

#     dist = district.objects.all()

#     for i in dist:

#         no_of_seneior_citizen = familyMembers.objects.filter(family_head__district=i.districtName).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.districtName).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.districtName,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.districtName,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.districtName,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_district_dashboard.objects.filter(district = i.districtName)
#         if chk_district:
#             total_district_dashboard.objects.filter(district = i.districtName).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             print("Existing")
#         else:
#             print("New")
#             saveNew = total_district_dashboard(district = i.districtName,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()


# def TalukaSchedular():


#     tal = taluka.objects.all()

#     for i in tal:
#         print(i.dist.districtName,"@@@@@@@@@@@@@@@@@")

#         no_of_seneior_citizen = familyMembers.objects.filter(family_head__district=i.dist.districtName,family_head__taluka=i.talukaName).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__taluka=i.talukaName).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__taluka=i.talukaName,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__taluka=i.talukaName,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__taluka=i.talukaName,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_taluka_dashboard.objects.filter(district = i.dist.districtName,taluka=i.talukaName)
#         if chk_district:
#             total_taluka_dashboard.objects.filter(district = i.dist.districtName,taluka=i.talukaName).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#         else:

#             saveNew = total_taluka_dashboard(district = i.dist.districtName,taluka=i.talukaName,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()





# def phcSchedular():


#     tal = primaryHealthCenter.objects.all()

#     for i in tal:
#         # print(i.dist.districtName,"@@@@@@@@@@@@@@@@@")

#         no_of_seneior_citizen = familyMembers.objects.filter(family_head__district=i.taluka.dist.districtName,family_head__taluka=i.taluka.talukaName,family_head__phc=i.phcName).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.taluka.dist.districtName,patient__family_head__taluka=i.taluka.talukaName,patient__family_head__phc=i.phcName).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.taluka.dist.districtName,patient__family_head__taluka=i.taluka.talukaName,patient__family_head__phc=i.phcName,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.taluka.dist.districtName,patient__family_head__taluka=i.taluka.talukaName,patient__family_head__phc=i.phcName,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.taluka.dist.districtName,patient__family_head__taluka=i.taluka.talukaName,patient__family_head__phc=i.phcName,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_phc_dashboard.objects.filter(district = i.taluka.dist.districtName,taluka=i.taluka.talukaName,phc_name= i.phcName)
#         if chk_district:
#             total_phc_dashboard.objects.filter(district = i.taluka.dist.districtName,taluka=i.taluka.talukaName,phc_name = i.phcName).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#         else:

#             saveNew = total_phc_dashboard(district = i.taluka.dist.districtName,taluka=i.taluka.talukaName,phc_name = i.phcName,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()


# def scSchedular():

#     dist = subCenter.objects.all()
#     print("@@@@@@@@@@@@@@@@@@@@@")

#     for i in dist:
#         print("@@@@@@@@@@@@@@@@@@@@@")

#         no_of_seneior_citizen = familymembers.objects.filter(family_head__district=i.Phc.taluka.dist__districtName,family_head__taluka=i.Phc.taluka__talukaName,family_head__phc=i.Phc__phcName,family_head__sc=i.scName).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.Phc.taluka.dist__districtName,patient__family_head__taluka=i.Phc.taluka__talukaName,patient__family_head__phc=i.Phc__phcName,patient__family_head__sc=i.scName).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.Phc.taluka.dist__districtName,patient__family_head__taluka=i.Phc.taluka__talukaName,patient__family_head__phc=i.Phc__phcName,patient__family_head__sc=i.scName,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.Phc.taluka.dist__districtName,patient__family_head__taluka=i.Phc.taluka__talukaName,patient__family_head__phc=i.Phc__phcName,patient__family_head__sc=i.scName,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.Phc.taluka.dist__districtName,patient__family_head__taluka=i.Phc.taluka__talukaName,patient__family_head__phc=i.Phc__phcName,patient__family_head__sc=i.scName,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_sc_dashboard.objects.filter(district=i.Phc.taluka.dist__districtName,taluka=i.Phc.taluka__talukaName,phc_name=i.Phc__phcName,sc_name=i.scName)
#         if chk_district:
#             print("##################")
#             total_sc_dashboard.objects.filter(district=i.Phc.taluka.dist__districtName,taluka=i.Phc.taluka__talukaName,phc_name=i.Phc__phcName,sc_name=i.scName).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#         else:
#             print("@@@@@@@@@@@@@@@@@@@@@")
#             saveNew = total_sc_dashboard.objects.filter(district=i.Phc.taluka.dist__districtName,taluka=i.Phc.taluka__talukaName,phc_name=i.Phc__phcName,sc_name=i.scName,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()




# def CouncilSchedular():


#     tal = municipalCouncil.objects.all()

#     for i in tal:
#         print(i.dist.districtName,"@@@@@@@@@@@@@@@@@")

#         no_of_seneior_citizen = familyMembers.objects.filter(family_head__district=i.dist.districtName,family_head__municipal_council=i.councilName).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_council=i.councilName).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_council=i.councilName,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_council=i.councilName,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_council=i.councilName,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_council_dashboard.objects.filter(district = i.dist.districtName,council=i.councilName)
#         if chk_district:
#             total_council_dashboard.objects.filter(district = i.dist.districtName,council=i.councilName).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#         else:

#             saveNew = total_council_dashboard(district = i.dist.districtName,council=i.councilName,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()


# def municipalCorporationSchedular():


#     tal = municipalCorporation.objects.all()

#     for i in tal:
#         print(i.dist.districtName,"@@@@@@@@@@@@@@@@@")

#         no_of_seneior_citizen = familyMembers.objects.filter(family_head__district=i.dist.districtName,family_head__municipal_corporation=i.mcName).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_corporation=i.mcName).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_corporation=i.mcName,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_corporation=i.mcName,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.dist.districtName,patient__family_head__municipal_corporation=i.mcName,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_mcrop_dashboard.objects.filter(district = i.dist.districtName,municipal_corporation=i.mcName)
#         if chk_district:
#             total_mcrop_dashboard.objects.filter(district = i.dist.districtName,municipal_corporation=i.mcName).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#         else:

#             saveNew = total_mcrop_dashboard(district = i.dist.districtName,municipal_corporation=i.mcName,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()




# def mwardSchedular():


#     tal = mcWard.objects.all()

#     for i in tal:
#         # print(i.dist.districtName,"@@@@@@@@@@@@@@@@@")

#         no_of_seneior_citizen = familyMembers.objects.filter(family_head__district=i.mcrop.dist.districtName,family_head__municipal_corporation=i.mcrop.mcName,family_head__ward=i.ward).count()
#         no_of_test_reported = patientLabTest.objects.filter(patient__family_head__district=i.mcrop.dist.districtName,patient__family_head__municipal_corporation=i.mcrop.mcName,patient__family_head__ward=i.ward).count()
#         no_of_test_completed = patientLabTest.objects.filter(patient__family_head__district=i.mcrop.dist.districtName,patient__family_head__municipal_corporation=i.mcrop.mcName,patient__family_head__ward=i.ward,isCompleted=True).count()
#         no_of_test_in_progress = patientLabTest.objects.filter(patient__family_head__district=i.mcrop.dist.districtName,patient__family_head__municipal_corporation=i.mcrop.mcName,patient__family_head__ward=i.ward,isCompleted=False).count()
#         no_of_health_facility = patientLabTest.objects.filter(patient__family_head__district=i.mcrop.dist.districtName,patient__family_head__municipal_corporation=i.mcrop.mcName,patient__family_head__ward=i.ward,isCompleted=False).count()
#         no_of_patients_attended_by_doctor = 520
#         no_of_empaneled_doctors = 250
#         no_of_empaneled_labs = 250

#         chk_district = total_ward_dashboard.objects.filter(district = i.mcrop.dist.districtName,municipal_corporation=i.mcrop.mcName,ward=i.ward)
#         if chk_district:
#             total_ward_dashboard.objects.filter(district = i.mcrop.dist.districtName,municipal_corporation=i.mcrop.mcName,ward=i.ward).update(no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#         else:

#             saveNew = total_ward_dashboard(district = i.mcrop.dist.districtName,municipal_corporation=i.mcrop.mcName,ward=i.ward,no_of_seneior_citizen=no_of_seneior_citizen,no_of_test_reported=no_of_test_reported,no_of_test_completed=no_of_test_completed,no_of_test_in_progress=no_of_test_in_progress,no_of_health_facility=no_of_health_facility,no_of_patients_attended_by_doctor=no_of_patients_attended_by_doctor,no_of_empaneled_doctors=no_of_empaneled_doctors,no_of_empaneled_labs=no_of_empaneled_labs)
#             saveNew.save()





class CustomLoginAPI(generics.GenericAPIView):
    serializer_class = PhcLoginSerializer
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
            data = OtherUserSerializer(customuser,context=self.get_serializer_context()).data
            groups=customuser.groups.values_list('name',flat = True)
            print(groups)

            
            
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
            if customuser.is_superuser:
                print("Super User")
                data["user_group"] = "Admin"

            else:

                data["user_group"] = groups
            data["token"]=token
            # data["role_perm_queryset"] = list(RolePermissions.objects.filter(authgroup__name=data["user_group"]).values())
            role_qs=RolePermissions.objects.filter(authgroup__name__in=data["user_group"])
            data["config_setting"] =RolePermissionSerializer(role_qs,many=True).data
   
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




class CustomRegisterAPI(generics.GenericAPIView):
    '''
    corporationUser,talukaUser,councilUser,wardUser
    '''
    serializer_class = NewphcRegisterSerializer
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
              openapi.Parameter(
                name='group', in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Group name",
                required=True,
                
            ),
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
        groupname = self.request.headers["group"]
        print(groupname,"@@@@@@@@@@@@@@@@@@@@22")
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
            group = Group.objects.get(name=groupname)
            group.user_set.add(user)

            return Response({
            "responseCode":200,
            # "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
        else:
            print(type(serializer.errors))
            return Response({"responseCode":400,"responseMessage":serializer.errors["non_field_errors"][0]},status=status.HTTP_400_BAD_REQUEST)



class CustomSurveyourRegisterAPI(generics.GenericAPIView):
    '''
    SurveyourRegisterSerializer
    '''
    serializer_class = SurveyourSerializer
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
            #   openapi.Parameter(
            #     name='group', in_=openapi.IN_HEADER,
            #     type=openapi.TYPE_STRING,
            #     description="Group name",
            #     required=True,
                
            # ),
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
        # groupname = self.request.headers["group"]
        # print(groupname,"@@@@@@@@@@@@@@@@@@@@22")
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
            group = Group.objects.get(name="surveyour")
            group.user_set.add(user)

            return Response({
            "responseCode":200,
            # "responseData":UserSerializer(user, context=self.get_serializer_context()).data,
            "responseMessage":"User is Successfully registered."},status=status.HTTP_200_OK)
        else:
            print(type(serializer.errors))
            return Response({"responseCode":400,"responseMessage":serializer.errors["non_field_errors"][0]},status=status.HTTP_400_BAD_REQUEST)





class CustomUserList(generics.GenericAPIView):
    """
    Group Wise User List 
     """
    queryset = CustomUser.objects.filter(is_delete=False)

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewOtherUserSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('groups__name',)
    filterset_fields = ('groups__name','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc',)
    search_fields = ['first_name','name','last_name','email','phone','username','is_active','signup_date','region_type','municipal_corporation','municipal_council','phc','ward']
    pagination_class = CustomPagination
    pagination_class.page_size = 15
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
        # serializer = self.get_serializer(instance=qs, many=True)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)


        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)


class DepartmentUserList(generics.GenericAPIView):
    """
    Department User List 
     """
    queryset = CustomUser.objects.filter(is_delete=False,groups__name__in=['dho','nhm','health_dept','social_justice_ministry','talukaUser'])

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewOtherUserSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('groups__name',)
    filterset_fields = ('groups__name','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc',)
    search_fields = ['first_name','name','last_name','email','phone','username','is_active','signup_date','region_type','municipal_corporation','municipal_council','phc','ward']
    pagination_class = CustomPagination
    pagination_class.page_size = 15
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
        # serializer = self.get_serializer(instance=qs, many=True)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)


        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class DepartmentUserListNoPage(generics.GenericAPIView):
    """
    Department User List 
     """
    queryset = CustomUser.objects.filter(is_delete=False,groups__name__in=['dho','nhm','health_dept','social_justice_ministry','talukaUser'])

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewOtherUserSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ('groups__name',)
    filterset_fields = ('groups__name','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc',)
    search_fields = ['first_name','name','last_name','email','phone','username','is_active','signup_date','region_type','municipal_corporation','municipal_council','phc','ward']
    # pagination_class = CustomPagination
    # pagination_class.page_size = 15
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
        # serializer = self.get_serializer(instance=qs, many=True)
        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)


        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)


class CustomUserListNoPage(generics.GenericAPIView):
    """
    Group Wise User List 
     """
    queryset = CustomUser.objects.filter(is_delete=False)

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewOtherUserSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('groups__name',)
    filterset_fields = ('groups__name','region_type','district','taluka','municipal_corporation','ward','municipal_council','phc',)
    # pagination_class = CustomPagination
    # pagination_class.page_size = 15
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
        # serializer = self.get_serializer(instance=qs, many=True)
        # page = self.paginate_queryset(qs)

        # if page is not None:
            # serializer = self.serializer_class(page, many=True)
            # return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)


        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class SurveyourList(generics.GenericAPIView):
    """
    Surveyour User List 
     """
    queryset = CustomUser.objects.filter(groups__name="surveyour")

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewOtherUserSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ('masterSupervisor',)
    # filterset_fields = ('region_type','district','taluka','municipal_corporation','ward','municipal_council','phc',)
    search_fields = ['name','phone','username']
    pagination_class = CustomPagination
    pagination_class.page_size = 15
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
        # serializer = self.get_serializer(instance=qs, many=True)
        group_name = request.user.groups.values_list('name',flat = True)
        if 'supervisor' in group_name:
            qs=qs.filter(masterSupervisor_id=request.user.id)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)


        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)


class SurveyourListNoPage(generics.GenericAPIView):
    """
    Surveyour User List 
     """
    queryset = CustomUser.objects.filter(groups__name="surveyour")

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = NewOtherUserSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ('masterSupervisor',)
    # filterset_fields = ('region_type','district','taluka','municipal_corporation','ward','municipal_council','phc',)
    search_fields = ['name','phone','username']
    # pagination_class = CustomPagination
    # pagination_class.page_size = 15
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
        # serializer = self.get_serializer(instance=qs, many=True)
        group_name = request.user.groups.values_list('name',flat = True)
        if 'supervisor' in group_name:
            qs=qs.filter(masterSupervisor_id=request.user.id)
        # page = self.paginate_queryset(qs)

        # if page is not None:
        #     serializer = self.serializer_class(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)


        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class GroupList(generics.GenericAPIView):
    """
    List all Groups
    """
    queryset = Group.objects.all()

    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = GroupSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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
        serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)



class CustomSetNewPassword(generics.GenericAPIView):
    # Allow any user (authenticated or not) to access this url 
    """
    Set new Password after first Login. 
    """
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = CustomSetPasswordSerializer
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
    def post(self, request,pk):    
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        

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
            validation_message = "Please Enter Confirm password"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        # chk_user = CustomUser.objects.get(id=pk)

        # chk_pass = chk_user.check_password(request.data["old_password"])
        if request.data["confirm_password"] == request.data["new_password"]:
            pass
        else:
            validation_message = "New password and confirm password must match!"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)


        # if request.data["new_password"]!=request.data["old_password"]:
        #     validation_message = "New Password and Old password must be same."
        #     return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
        
        if request.data["new_password"]!="":
            new_password = request.data["new_password"]

        if request.data["confirm_password"]!="":
            old_password = request.data["confirm_password"]


        # import datetime
        data={}
        # user = request.user.id
        newpassword = make_password(new_password)
        user_exists = CustomUser.objects.filter(id=pk).update(password=newpassword,confirm_password=new_password)
        if not user_exists:
            validation_message = "User does not exist!"
            return Response({'responseCode': 400, 'responseMessage': validation_message},status = status.HTTP_400_BAD_REQUEST)
            
            
        return Response({'responseCode': 200, 'responseMessage': "Successfully changed password"},status=status.HTTP_200_OK)
        
        
class GetConfigSetting(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RolePermissionSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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
        # hi=RolesPermissionsConfig.objects.all()    
        # print(hi)
        role_permission = RolePermissions.objects.all()
        # qs = self.get_queryset()
        # qs = self.filter_queryset(qs)
        serializer = self.get_serializer(instance=role_permission, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

class CreateConfigSetting(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = RolePermissionSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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

    def post(self, request, format=None):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        # hi=RolesPermissionsConfig.objects.all()    
        # print(hi)
        # role_permission = RolePermissions.objects.all()
        # qs = self.get_queryset()
        # qs = self.filter_queryset(qs)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ser=serializer.save()
            return Response({"responseCode":200, 'responseMessage': "Success",'responseData':serializer.data},status=status.HTTP_200_OK)

        return Response({"responseCode":400, 'responseMessage': "Error",'responseData':serializer.data},status=status.HTTP_400_BAD_REQUEST)

class UpdateConfigSetting(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MultiUpdateRolePermissionSerializer
    parser_classes = [JSONParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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

    def put(self, request):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        # hi=RolesPermissionsConfig.objects.all()    
        # print(hi)
        serializers = MultiUpdateRolePermissionSerializer(data=request.data)
        if serializers.is_valid():
            roles=request.data['roles']
            for each in roles:
                RolePermissions.objects.filter(id=each['id']).update(status=each['status'])
        else:
            return Response({"responseCode":400, 'responseMessage': "Error",'responseMessage':"Updated Failed"},status=status.HTTP_400_BAD_REQUEST)
       # RolePermissions.objects.filter(id__in=pk_set).update(status=)
        # qs = self.get_queryset()
        # qs = self.filter_queryset(qs)
        # serializer = self.get_serializer(instance=qs, many=True)

        return Response({"responseCode":200, 'responseMessage': "Success",'responseMessage':"Updated Successfully"},status=status.HTTP_200_OK)



class CloseCaseAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = CloseCaseSerializer
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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

    def put(self, request):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
        
        # qs = self.get_queryset()
        # qs = self.filter_queryset(qs)

        fam=familyMembers.objects.filter(member_unique_id=request.data['member_unique_id'])
        # print(fam)
        # serializer = self.get_serializer(instance=fam,data=request.data)
        # print(serializer)
        # if serializer.is_valid():
        #     serializer.save()
        if fam:
            date_now=datetime.now()
            fam.update(isCaseClosed=True,caseClosedReason=request.data['caseClosedReason'],caseClosedDate=date_now,caseClosedBy=request.user)
        else:
            return Response({"responseCode":400, 'responseMessage': "Error",'responseMessage':"Failed to close!"},status=status.HTTP_400_BAD_REQUEST)       
        return Response({"responseCode":200, 'responseMessage': "Success",'responseMessage':"Case Closed Successfully!"},status=status.HTTP_200_OK)

class CustomRemoveUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    parser_classes = [FormParser]

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ('familyAddress__district','familyAddress__region_type','familyAddress__municipal_corporation','familyAddress__ward','familyAddress__municipal_council','familyAddress__taluka','familyAddress__village','familyAddress__phc','familyAddress__sc',)
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

   
    def put(self, request,user_id):
        token_check = validate_token(self.request.headers["nonce"],self.request.headers["timestamp"],self.request.headers["token"])
        print(token_check,"************")
        if token_check=="invalid":
            return Response({"responseCode":204,"responseMessage":"Invalid TOken"})
    

        is_removed = CustomUser.objects.filter(id=user_id).update(is_delete=True,is_active=False)
        if is_removed:
            return Response({"responseCode":200, 'responseMessage': "Success",'responseMessage':"User Removed Successfully!"},status=status.HTTP_200_OK)    
        return Response({"responseCode":400, 'responseMessage': "Error",'responseMessage':"User Not Removed!"},status=status.HTTP_400_BAD_REQUEST)
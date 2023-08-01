
from django.urls import path,include
from .views import TestReportAPI,ScanBarCodeAPI,CitizensListAPI,PhlebotomistListAPI,PhlebotomistRegisterAPI,PathlabRegisterAPI,PathLabLoginAPI,TestRangeListAPI,PhlebotomistUpdateAPI,PhlebotomistDeleteAPI,GetTestReportAPI,PhlebotomistGetAPI,ResponseToDoctor,PhlebotomistListParameterAPI,AddTestRangeListAPI,ViewReportTestRangeListAPI,UploadTestReportAPI,GetCitizenTestListAPI,LogoutAPI,QueryList
# from all_authentications.admin_views import *
urlpatterns = [

    
    # path('LabTestListAPI/<int:pk>', LabTestListAPI.as_view(), name='LabTestListAPI'),
    path('TestReportAPI/', TestReportAPI.as_view(), name='TestReportAPI'),
    path('GetTestReportAPI/<str:parameter_name>/<str:parameter_value>', GetTestReportAPI.as_view(), name='GetTestReportAPI'),
    path('ScanBarCodeAPI/<str:barcode>', ScanBarCodeAPI.as_view(), name='ScanBarCodeAPI'),
    path('CitizensListAPI/', CitizensListAPI.as_view(), name='CitizensListAPI'),
    path('PhlebotomistListAPI/', PhlebotomistListAPI.as_view(), name='PhlebotomistListAPI'),
    path('PhlebotomistListParameterAPI/', PhlebotomistListParameterAPI.as_view(), name='PhlebotomistListParameterAPI'),
    path('PhlebotomistUpdateAPI/<int:pk>', PhlebotomistUpdateAPI.as_view(), name='PhlebotomistUpdateAPI'),
    path('PhlebotomistRegisterAPI/', PhlebotomistRegisterAPI.as_view(), name='PhlebotomistRegisterAPI'),
    path('PhlebotomistDeleteAPI/<int:pk>',PhlebotomistDeleteAPI.as_view(), name='PhlebotomistDeleteAPI'),
    path('PhlebotomistGetAPI/<int:pk>',PhlebotomistGetAPI.as_view(), name='PhlebotomistGetAPI'),
    path('PathlabRegisterAPI/', PathlabRegisterAPI.as_view(), name='PathlabRegisterAPI'),
    path('PathLabLoginAPI/', PathLabLoginAPI.as_view(), name='PathLabLoginAPI'),
    path('ResponseToDoctor/<int:pk>', ResponseToDoctor.as_view(), name='ResponseToDoctor'),
    # path('TestRangeListAPI/', TestRangeListAPI.as_view(), name='TestRangeListAPI'),
    path('TestRangeListAPI/<str:test_type>/', TestRangeListAPI.as_view(), name='TestRangeListAPI'),
    path('AddTestRangeListAPI/', AddTestRangeListAPI.as_view(), name='AddTestRangeListAPI'),
    path('ViewReportTestRangeListAPI/<str:parameter_name>/<str:parameter_value>', ViewReportTestRangeListAPI.as_view(), name='ViewReportTestRangeListAPI'),
    path('UploadTestReportAPI/', UploadTestReportAPI.as_view(), name='UploadTestReportAPI'),
    path('GetCitizenTestListAPI/<str:parameter_name>/<str:parameter_value>', GetCitizenTestListAPI.as_view(), name='GetCitizenTestListAPI'),
    path('QueryList/', QueryList.as_view(), name='QueryList'),
    path('LogoutAPI', LogoutAPI.as_view(), name='LogoutAPI'),
    
    

]
from django.urls import path,include
from seniorcetizen.views import CitizenInsertFamilyMemberMedicalSurvey,FamilySurveyList,SelfMedicalSurvey,CitizenloginSendOtp,CitizenloginOtpVerify,CitizenRegisterAPI,CitizenOtpVerify,CitizenLoginAPI,CitizenForgotPassword,CitizenForgotPasswordOtpVerify,CitizenForgotPasswordSetNewPassword,SeniorCitizenRegisterAPI,HeadCitizenList,ViewCitizenReportAPI,ViewCitizenSummaryAPI,ViewCitizenSummarySortedAPI
# from all_authentications.admin_views import *
urlpatterns = [

    path('CitizenloginSendOtp', CitizenloginSendOtp.as_view(), name='CitizenloginSendOtp'),
    path('CitizenloginOtpVerify', CitizenloginOtpVerify.as_view(), name='CitizenloginOtpVerify'),
    path('SelfMedicalSurvey', SelfMedicalSurvey.as_view(), name='SelfMedicalSurvey'),
    path('FamilySurveyList', FamilySurveyList.as_view(), name='FamilySurveyList'),
    path('HeadCitizenList/<str:familyhead_id>', HeadCitizenList.as_view(), name='HeadCitizenList'),
    path('ViewCitizenReportAPI/<str:parameter_value>', ViewCitizenReportAPI.as_view(), name='ViewCitizenReportAPI'),
    path('ViewCitizenSummaryAPI/<str:parameter_value>', ViewCitizenSummaryAPI.as_view(), name='ViewCitizenSummaryAPI'),
    path('ViewCitizenSummarySortedAPI/<str:parameter_value>', ViewCitizenSummarySortedAPI.as_view(), name='ViewCitizenSummarySortedAPI'),

    path('CitizenInsertFamilyMemberMedicalSurvey', CitizenInsertFamilyMemberMedicalSurvey.as_view(), name='CitizenInsertFamilyMemberMedicalSurvey'),


    
    path('CitizenRegisterAPI', CitizenRegisterAPI.as_view(), name='CitizenRegisterAPI'),
    path('SeniorCitizenRegisterAPI', SeniorCitizenRegisterAPI.as_view(), name='SeniorCitizenRegisterAPI'),
    # path('CitizenOtpVerify', CitizenOtpVerify.as_view(), name='CitizenOtpVerify'),
    path('CitizenLoginAPI', CitizenLoginAPI.as_view(), name='CitizenLoginAPI'),
    path('CitizenForgotPassword', CitizenForgotPassword.as_view(), name='CitizenForgotPassword'),
    path('CitizenForgotPasswordOtpVerify', CitizenForgotPasswordOtpVerify.as_view(), name='CitizenForgotPasswordOtpVerify'),
    path('CitizenForgotPasswordSetNewPassword', CitizenForgotPasswordSetNewPassword.as_view(), name='CitizenForgotPasswordSetNewPassword'),



]
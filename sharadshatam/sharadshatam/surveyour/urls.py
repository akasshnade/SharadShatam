from django.urls import path,include
from surveyour.views import SurveyourClaimCitizen,CompleteSelfSurveyDetails,UpdateFamilyMemberDetails,UpdateFamilyHeadDetails,NewUpdatePartialMedicalSurvey,UpdateSurveyorProfileDetails,SurveyourSurveyList,GetAllPathologyList,GetAllLabTestList,InsertAddress,InsertfamilyHead,GetSurveyourMedicalSurveyList,GetLocationData,SurveyourRegisterAPI,MedicalSurvey,loginSendOtp,loginOtpVerify,SurveyourSetNewPassword,SurveyourForgotPassword,SurveyourForgotPasswordOtpVerify,SurveyourForgotPasswordSetNewPassword,UpdatePartialMedicalSurvey,NotificationListAPI
# from all_authentications.admin_views import *
urlpatterns = [
    path('loginSendOtp', loginSendOtp.as_view(), name='loginSendOtp'),
    path('loginOtpVerify', loginOtpVerify.as_view(), name='loginOtpVerify'),
    path('UpdateSurveyorProfileDetails/<int:pk>/', UpdateSurveyorProfileDetails.as_view(), name='UpdateSurveyorProfileDetails'),


    path('SurveyourSetNewPassword', SurveyourSetNewPassword.as_view(), name='SurveyourSetNewPassword'),
    path('SurveyourForgotPassword', SurveyourForgotPassword.as_view(), name='SurveyourForgotPassword'),
    path('SurveyourForgotPasswordOtpVerify', SurveyourForgotPasswordOtpVerify.as_view(), name='SurveyourForgotPasswordOtpVerify'),
    path('SurveyourForgotPasswordSetNewPassword', SurveyourForgotPasswordSetNewPassword.as_view(), name='SurveyourForgotPasswordSetNewPassword'),
    path('SurveyourRegisterAPI', SurveyourRegisterAPI.as_view(), name='SurveyourRegisterAPI'),
    path('GetSurveyourMedicalSurveyList', GetSurveyourMedicalSurveyList.as_view(), name='GetSurveyourMedicalSurveyList'),
    path('SurveyourSurveyList', SurveyourSurveyList.as_view(), name='SurveyourSurveyList'),
    path('UpdatePartialMedicalSurvey', UpdatePartialMedicalSurvey.as_view(), name='UpdatePartialMedicalSurvey'),
    path('NewUpdatePartialMedicalSurvey', NewUpdatePartialMedicalSurvey.as_view(), name='NewUpdatePartialMedicalSurvey'),
    path('UpdateFamilyHeadDetails', UpdateFamilyHeadDetails.as_view(), name='UpdateFamilyHeadDetails'),
    
    path('UpdateFamilyMemberDetails', UpdateFamilyMemberDetails.as_view(), name='UpdateFamilyMemberDetails'),
    path('CompleteSelfSurveyDetails', CompleteSelfSurveyDetails.as_view(), name='CompleteSelfSurveyDetails'),

    path('SurveyourClaimCitizen', SurveyourClaimCitizen.as_view(), name='SurveyourClaimCitizen'),
    
    
    
    path('NotificationListAPI', NotificationListAPI.as_view(), name='NotificationListAPI'),

    path('GetLocationData', GetLocationData.as_view(), name='GetLocationData'),

    path('GetAllPathologyList', GetAllPathologyList.as_view(), name='GetAllPathologyList'),
    path('GetAllLabTestList', GetAllLabTestList.as_view(), name='GetAllLabTestList'),

    # path('MedicalSurvey', MedicalSurvey.as_view(), name='MedicalSurvey'),
    path('MedicalSurvey', InsertAddress.as_view(), name='MedicalSurvey'),
    path('InsertfamilyHead', InsertfamilyHead.as_view(), name='InsertfamilyHead'),




]
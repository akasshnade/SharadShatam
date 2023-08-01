from django.urls import path,include
from doctor.views import AssignNewDoctor,DoctorUserDetail,DoctorChangeNewPassword,DoctorEditProfile,QueryToPathLab,GetDoctorRemarkPathlabList,DoctorConsultancy,DoctorRegisterAPI,DoctorOtpVerify,DoctorLoginAPI,DoctorForgotPassword,DoctorForgotPasswordOtpVerify,DoctorForgotPasswordSetNewPassword,SuggestToCitizen,CompleteCaseAPI,PhcSuggestToCitizen,SpecialistSuggestToCitizen,SpecialistCitizensList,PhcCitizensList,PhcPatientList,PhcPatientListNoPage,SpecialistCitizensListNoPage
# from all_authentications.admin_views import *
urlpatterns = [

    # path('CitizenloginSendOtp', CitizenloginSendOtp.as_view(), name='CitizenloginSendOtp'),
    # path('CitizenloginOtpVerify', CitizenloginOtpVerify.as_view(), name='CitizenloginOtpVerify'),


    
    path('DoctorRegisterAPI', DoctorRegisterAPI.as_view(), name='DoctorRegisterAPI'),
    path('DoctorOtpVerify', DoctorOtpVerify.as_view(), name='DoctorOtpVerify'),
    path('DoctorLoginAPI', DoctorLoginAPI.as_view(), name='DoctorLoginAPI'),
    path('DoctorForgotPassword', DoctorForgotPassword.as_view(), name='DoctorForgotPassword'),
    path('DoctorForgotPasswordOtpVerify', DoctorForgotPasswordOtpVerify.as_view(), name='DoctorForgotPasswordOtpVerify'),
    path('DoctorForgotPasswordSetNewPassword', DoctorForgotPasswordSetNewPassword.as_view(), name='DoctorForgotPasswordSetNewPassword'),
    path('DoctorConsultancy', DoctorConsultancy.as_view(), name='DoctorConsultancy'),
    path('GetDoctorRemarkPathlabList', GetDoctorRemarkPathlabList.as_view(), name='GetDoctorRemarkPathlabList'),
    path('QueryToPathLab', QueryToPathLab.as_view(), name='QueryToPathLab'),

    path('DoctorUserDetail/<int:pk>/', DoctorUserDetail.as_view(), name='DoctorUserDetail'),
    path('DoctorChangeNewPassword', DoctorChangeNewPassword.as_view(), name='DoctorChangeNewPassword'),
    path('DoctorEditProfile', DoctorEditProfile.as_view(), name='DoctorEditProfile'),
    path('SuggestToCitizen', SuggestToCitizen.as_view(), name='SuggestToCitizen'),
    path('CompleteCaseAPI/<int:pk>', CompleteCaseAPI.as_view(), name='CompleteCaseAPI'),
    path('PhcSuggestToCitizen', PhcSuggestToCitizen.as_view(), name='PhcSuggestToCitizen'),
    path('SpecialistSuggestToCitizen', SpecialistSuggestToCitizen.as_view(), name='SpecialistSuggestToCitizen'),
    path('SpecialistCitizensList', SpecialistCitizensList.as_view(), name='SpecialistCitizensList'),
    path('SpecialistCitizensListNoPage', SpecialistCitizensListNoPage.as_view(), name='SpecialistCitizensListNoPage'),
    path('PhcCitizensList', PhcCitizensList.as_view(), name='PhcCitizensList'),
    path('PhcPatientList', PhcPatientList.as_view(), name='PhcPatientList'),
    path('PhcPatientListNoPage', PhcPatientListNoPage.as_view(), name='PhcPatientListNoPage'),
    path('AssignNewDoctor', AssignNewDoctor.as_view(), name='AssignNewDoctor'),



]
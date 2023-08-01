from django.urls import path,include
from adminportal.views import DepartmentUserList,Custdashboard,SurveyourList,CustomSurveyourRegisterAPI,GroupList,CustomUserList,CustomRegisterAPI,CustomLoginAPI,dashboardDistrict,dashboardTaluka,dashboardPHC,dashboardSC,dashboardCouncil,dashboardCorporation,dashboardWard,EditProfile,EditSelfProfile,ChangeNewPassword,UserDetail,AdminDashboard,GetdistrictList,GettalukaList,GetprimaryHealthCenterList,GetsubCenterList,GetvillageList,GetmunicipalCorporationList,GetmunicipalWardList,GetmunicipalCouncilList,GetcantonmentBoardList,GetDistrictWiseHospitalList,AdminLoginAPI,PhcRegisterAPI,PhcLoginAPI,AllMedicalSurveyList,MedicalSurveyDetail,CustomSetNewPassword,GetConfigSetting,UpdateConfigSetting,CreateConfigSetting,CloseCaseAPI,CustomRemoveUser,CustomUserListNoPage,AuthenticatedSpecialistCitizenList,AllMedicalSurveyListNoPage,HospitalRegisterAPI,HospitalCitizenList,DepartmentUserListNoPage,SurveyourListNoPage

from adminportal import views

from apscheduler.schedulers.background import BackgroundScheduler
import threading
scheduler = BackgroundScheduler()
scheduler.start()




# from all_authentications.admin_views import *
urlpatterns = [
    path('AdminLoginAPI', AdminLoginAPI.as_view(), name='AdminLoginAPI'),
    path('CustomSurveyourRegisterAPI', CustomSurveyourRegisterAPI.as_view(), name='CustomSurveyourRegisterAPI'),
    # path('CustomDashboard', CustomDashboard.as_view(), name='CustomDashboard'),
    # path('NewCustomDashboard', NewCustomDashboard.as_view(), name='NewCustomDashboard'),
    path('CustomDashboard', Custdashboard.as_view(), name='Custdashboard'),
    path('AuthenticatedSpecialistCitizenList', AuthenticatedSpecialistCitizenList.as_view(), name='AuthenticatedSpecialistCitizenList'),
    path('HospitalCitizenList', HospitalCitizenList.as_view(), name='HospitalCitizenList'),
    path('DepartmentUserList', DepartmentUserList.as_view(), name='DepartmentUserList'),
    path('DepartmentUserListNoPage', DepartmentUserListNoPage.as_view(), name='DepartmentUserListNoPage'),






    path('CustomRegisterAPI', CustomRegisterAPI.as_view(), name='CustomRegisterAPI'),
    path('HospitalRegisterAPI', HospitalRegisterAPI.as_view(), name='HospitalRegisterAPI'),
    path('CustomUserList', CustomUserList.as_view(), name='CustomUserList'),
    path('CustomUserListNoPage', CustomUserListNoPage.as_view(), name='CustomUserListNoPage'),
    path('SurveyourList', SurveyourList.as_view(), name='SurveyourList'),
    path('SurveyourListNoPage', SurveyourListNoPage.as_view(), name='SurveyourListNoPage'),

    
    path('GroupList', GroupList.as_view(), name='GroupList'),


    path('PhcRegisterAPI', PhcRegisterAPI.as_view(), name='PhcRegisterAPI'),
    path('PhcLoginAPI', PhcLoginAPI.as_view(), name='PhcLoginAPI'),

    path('AllMedicalSurveyList', AllMedicalSurveyList.as_view(), name='AllMedicalSurveyList'),
    path('AllMedicalSurveyListNoPage', AllMedicalSurveyListNoPage.as_view(), name='AllMedicalSurveyListNoPage'),
    path('MedicalSurveyDetail/<int:pk>/', MedicalSurveyDetail.as_view(), name='MedicalSurveyDetail'),
    path('GetDistrictWiseHospitalList', GetDistrictWiseHospitalList.as_view(), name='GetDistrictWiseHospitalList'),

    path('GetdistrictList', GetdistrictList.as_view(), name='GetdistrictList'),
    path('GettalukaList', GettalukaList.as_view(), name='GettalukaList'),
    path('GetprimaryHealthCenterList', GetprimaryHealthCenterList.as_view(), name='GetprimaryHealthCenterList'),
    path('GetsubCenterList', GetsubCenterList.as_view(), name='GetsubCenterList'),
    path('GetvillageList', GetvillageList.as_view(), name='GetvillageList'),
    path('GetmunicipalCorporationList', GetmunicipalCorporationList.as_view(), name='GetmunicipalCorporationList'),
    path('GetmunicipalWardList', GetmunicipalWardList.as_view(), name='GetmunicipalWardList'),

    path('GetmunicipalCouncilList', GetmunicipalCouncilList.as_view(), name='GetmunicipalCouncilList'),
    path('GetcantonmentBoardList', GetcantonmentBoardList.as_view(), name='GetcantonmentBoardList'),
    path('AdminDashboard', AdminDashboard.as_view(), name='AdminDashboard'),
    path('UserDetail/<int:pk>/', UserDetail.as_view(), name='UserDetail'),
    path('ChangeNewPassword', ChangeNewPassword.as_view(), name='ChangeNewPassword'),
    path('EditSelfProfile', EditSelfProfile.as_view(), name='EditSelfProfile'),
    path('EditProfile/<int:user_id>', EditProfile.as_view(), name='EditProfile'),

    path('dashboardDistrict', dashboardDistrict.as_view(), name='dashboardDistrict'),
    path('dashboardTaluka', dashboardTaluka.as_view(), name='dashboardTaluka'),
    path('dashboardPHC', dashboardPHC.as_view(), name='dashboardPHC'),
    path('dashboardSC', dashboardSC.as_view(), name='dashboardSC'),

    path('dashboardCouncil', dashboardCouncil.as_view(), name='dashboardCouncil'),
    path('dashboardCorporation', dashboardCorporation.as_view(), name='dashboardCorporation'),
    path('dashboardWard', dashboardWard.as_view(), name='dashboardWard'),
    path('CustomLoginAPI', CustomLoginAPI.as_view(), name='CustomLoginAPI'),

    path('CustomSetNewPassword/<int:pk>', CustomSetNewPassword.as_view(), name='CustomSetNewPassword'),
    path('GetConfigSetting/', GetConfigSetting.as_view(), name='GetConfigSetting'),
    path('UpdateConfigSetting/', UpdateConfigSetting.as_view(), name='UpdateConfigSetting'),
    path('CreateConfigSetting/', CreateConfigSetting.as_view(), name='CreateConfigSetting'),
    path('CloseCaseAPI/', CloseCaseAPI.as_view(), name='CloseCaseAPI'),
    path('CustomRemoveUser/<int:user_id>', CustomRemoveUser.as_view(), name='CustomRemoveUser'),


]

# scheduler.add_job(views.DistrictSchedular, 'interval',seconds=5)
# scheduler.add_job(views.TalukaSchedular, 'interval',seconds=5)
# scheduler.add_job(views.phcSchedular, 'interval',seconds=5)
# scheduler.add_job(views.scSchedular, 'interval',seconds=5)
# scheduler.add_job(views.CouncilSchedular, 'interval',seconds=5)
# scheduler.add_job(views.municipalCorporationSchedular, 'interval',seconds=5)
# scheduler.add_job(views.mwardSchedular, 'interval',seconds=5)



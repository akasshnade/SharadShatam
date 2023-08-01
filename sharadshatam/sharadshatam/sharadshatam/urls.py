"""sharadshatam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from drf_yasg.openapi import OpenAPISchemaGenerator
# class CustomerGeneratorSchema(OpenAPISchemaGenerator):
#    def get_operation(self, *args, **kwargs):

#       operation = super().get_operation(*args, **kwargs)
#       your_header = openapi.Parameter(
#       name='Accept-Language',
#       description="Description",
#       required=True,
#       in_=openapi.IN_HEADER,
#       type=openapi.TYPE_STRING,
#       default='en'
#       )
#       operation.parameters.append(your_header)
#       return operation

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),

   ),

   public=True,
   permission_classes=(permissions.AllowAny,),

)

# schema_view = get_schema_view(
#          openapi.Parameter(
#                   title="Snippets API",

#                 name='accept-language', in_=openapi.IN_HEADER,
#                 type=openapi.TYPE_INTEGER,
#                 description="path parameter override",
#                 required=True
#             ),

# )
urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('adminportal/', include('adminportal.urls')),
    path('surveyour/', include('surveyour.urls')),
    path('seniorcetizen/', include('seniorcetizen.urls')),
    path('doctor/', include('doctor.urls')),
    path('pathology/', include('pathology.urls')),

]

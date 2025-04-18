from django.urls import path,include
from .views import *
from drf_yasg import openapi
from django.urls import re_path
from drf_yasg.views import get_schema_view
from api.providers_views import UpdateServiceProviderProfile,AddService,ServicesList,ServiceUpdate,ServiceDelete,ViewService,ServiceProviderProfile
from api.users_view import UserProfile,UpdateUserProfile,BookService
from drf_yasg.generators import OpenAPISchemaGenerator
import os
app_name='api'

class SchemaGenrator(OpenAPISchemaGenerator):
    def get_schema(self,request=None,public=False):
        schema=super(SchemaGenrator,self).get_schema(request,public)
        schema.basepath= os.path.join(schema.basePath,'api/')
        schema.schemes=["http","https"]
        return schema
schema_view = get_schema_view(
    openapi.Info(
        title="Service Api's",
        description="Api documentation for Corsec Project",
        default_version="1.0.0",
        terms_of_service="",
        contact=openapi.Contact(email = ""),
        license=openapi.License(name = "Service")

    ),
    public = True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    re_path(r'^swagger-collection/$',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    re_path(r'^documentaion/$',schema_view.with_ui('redoc',cache_timeout=0),name='schema-redoc'),
    re_path(r'^send-otp/$',SendOtp.as_view(),name="send_otp"),
    re_path(r'^resend-otp/$',ResendOTP.as_view(),name="resend_otp"),
    re_path(r'^verify-otp/$',VerifyOtp.as_view(),name="verify_otp"),
    re_path(r'^service-provider-signup/$',ServiceproviderSignup.as_view(),name="service_provider_signup"),
    re_path(r'^service-provider-login/$',ServiceproviderLogin.as_view(),name="service_provider_login"),
    #service Provider
    re_path(r'^service-provider-profile/$',ServiceProviderProfile.as_view(),name="service_provider_profile"),
    re_path(r'^update-service-provider-profile/$',UpdateServiceProviderProfile.as_view(),name="update_service_provider_profile"),
    re_path(r'^add-service/$',AddService.as_view(),name="add_service"),
    re_path(r'^services-list/$',ServicesList.as_view(),name="services_list"),
    re_path(r'^services-update/(?P<pk>\d+)$', ServiceUpdate.as_view(), name="services_update"),
    re_path(r'^services-delete/(?P<pk>\d+)$', ServiceDelete.as_view(), name="services_delete"),
    re_path(r'^service-details/(?P<pk>\d+)$', ViewService.as_view(), name="services_details"),

    #User
    re_path(r'^user-profile/$',UserProfile.as_view(),name="user_profile"),
    re_path(r'^update-user-profile/$',UpdateUserProfile.as_view(),name="update_user_profile"),
    re_path(r'^book-service/$',BookService.as_view(),name="book_service"),

]


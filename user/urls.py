from django.conf.urls import re_path
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from user import views
urlpatterns = [
    # Views are defined in Djoser, but we're assigning custom paths.
    re_path(r'^view/$', djoser_views.UserView.as_view(), name='user-view'),
    re_path(r'^delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    re_path(r'^create/$', djoser_views.UserCreateView.as_view(), name='user-create'),
    re_path(r'^password/$', djoser_views.SetPasswordView.as_view(), name='user-change-password'),

    # Views are defined in Rest Framework JWT, but we're assigning custom paths.
    re_path(r'^login/$', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
    re_path(r'^login/refresh/$', jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
    re_path(r'^logout/all/$', views.UserLogoutAllView.as_view(), name='user-logout-all'),

    re_path(r'^details/(?P<userId>\d+)', views.UserRetrieveAPIView.as_view(), name='user-details'),
    re_path(r'^change', views.UserChangeInfoAPIView.as_view(), name='user-update')

]
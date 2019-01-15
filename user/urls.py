from django.conf.urls import re_path
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from user import views
urlpatterns = [
    # Views are defined in Djoser, but we're assigning custom paths.
    re_path(r'^user/view/$', djoser_views.UserView.as_view(), name='user-view'),
    re_path(r'^user/delete/$', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    re_path(r'^user/create/$', djoser_views.UserCreateView.as_view(), name='user-create'),

    # Views are defined in Rest Framework JWT, but we're assigning custom paths.
    re_path(r'^user/login/$', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
    re_path(r'^user/login/refresh/$', jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
    re_path(r'^user/logout/all/$', views.SpaUserLogoutAllView.as_view(), name='user-logout-all'),

    # re_path(r'^user/details/$', views.UserRetrieveUpdateAPIView.as_view(), name='user-details')
    # re_path(r'^user/details/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})', views.RetrieveUserByUsernameView.as_view(), name='user-detailsUsername'),
    re_path(r'^user/details/(?P<userId>\d+)', views.UserRetrieveUpdateAPIView.as_view(), name='user-details')

]
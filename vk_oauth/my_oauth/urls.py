from django.urls import path, include
from .import views
from .auth.services import *
from .auth.vk_oauth import *


urlpatterns = [
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('index/', views.index, name='index'),
    path('my_oauth/', my_oauth, name='my_oauth'),
    path('login', LoginView.as_view(), name='login'),
    path('get_vk_code/', get_vk_code, name='get_vk_code'),
    path('get_vk_access_token', get_vk_access_token, name='get_vk_access_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:pk>/', UserDestroyView.as_view(), name='delete'),
    path('registr/', RegistrUserView.as_view(), name='registr'),
    path('get_profile/<int:pk>/', GetProfileView.as_view(), name='get_profile'),
    path('new_username/<int:pk>/', LoginChangeView.as_view(), name='new_credentials'),
    path('change_password/<int:pk>/', PasswordChangeView.as_view(), name='change_password'),
    path('changeclientcredential/<int:pk>/', ChangeClientCredentialsView.as_view(), name='change_credential'),
    path('social_links/<int:pk>/', SocialLinkListView.as_view(), name='social_links'),
    path('change_social_link/<int:pk>/', ChangeSocialLinkView.as_view(), name='change_links'),
    path('create_social_link/<int:pk>/', SocialLinkCreateView.as_view(), name='create_link'),    
 ]



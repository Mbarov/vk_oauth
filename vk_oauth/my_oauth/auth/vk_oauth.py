from django.conf import settings
from django.shortcuts import redirect
import requests
from ..models import MyUser, SocialLink
from django.contrib.auth.models import User
from datetime import datetime


def get_url(base_url, params):
    '''построение url с параметрами запроса'''
    url = base_url + '?'
    for param in params:
        url = url + '&' + param + '=' +  params[param] 
    return url



def get_vk_code(request):
    '''получение авторизационного кода от VK'''
    params = {
        'client_id' : settings.SOCIAL_AUTH_VK_OAUTH2_KEY,
        'redirect_uri' : settings.REDIRECT_URI,
        'scope' : settings.SCOPE[0]
    }
    url = get_url(settings.AUTHORIZE_URL, params)
    return redirect(url)


def my_oauth(request):
    '''авторизация через VK '''
    code = request.GET['code']
    get_access_token = get_vk_access_token(code)
    access_token = get_access_token['access_token']
    email = get_access_token['email']
    vk_id = get_access_token['user_id']
    user_info = get_vk_info(vk_id, access_token)
    server_access_token = get_convert_token(access_token)
    user = User.objects.get(username=user_info['screen_name'])
    user.email = email
    user.save()
    my_user,_ = MyUser.objects.get_or_create(
            user=user,
            bday = datetime.strptime(user_info['bdate'], '%d.%m.%Y'),
            authorization_type = 'VK',
            )
    social_link,_ = SocialLink.objects.get_or_create(
        link = 'vk.com/id' + str(user_info['id']),
        user = user
    )
    return redirect(settings.LOGIN_URL)



def get_vk_access_token(code):
    '''получение access токена от VK на основе полученного авторизационного кода'''
    params = {
            'client_id' : settings.SOCIAL_AUTH_VK_OAUTH2_KEY,
            'client_secret' : settings.SOCIAL_AUTH_VK_OAUTH2_SECRET,
            'redirect_uri' : settings.REDIRECT_URI,
            'code' : code
        }
    response = requests.get(settings.ACCESS_TOKEN_URL, params=params)
    response_json = response.json()
    if response_json['access_token']:
        return response_json
    else:
        return {'error': 'Ошибка при получении access token'}


def get_convert_token(access_token):
    '''выдача access токена сервером на основе полученного access токена от VK'''
    params_access = {
            'grant_type':'convert_token',
            'client_id': settings.CLIENT_ID,
            'backend':'vk-oauth2',
            'token': access_token,
            }
    get_token = requests.post('http://127.0.0.1:8000/api/auth/convert-token/', params=params_access)
    get_token_json = get_token.json()
    token = get_token_json['access_token']
    return token


def get_vk_info(vk_id, access_token):
    '''получение информации о пользователе от VK'''
    params = {
        'uids' : vk_id,
        'fields' : settings.USER_INFO_FIELDS,
        'access_token' : access_token,
        'v' : '5.131'
    }
    user_info_json = requests.get(settings.USER_INFO_URL, params=params).json()
    user_info = user_info_json['response'][0]
    return user_info

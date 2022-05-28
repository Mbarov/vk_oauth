from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from ..permissions import IsOwner
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import User, SocialLink
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView,RetrieveAPIView,DestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView


class RegistrUserView(CreateAPIView):
    '''Создание нового пользователя'''

    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny,]
    

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)



class LoginView(CreateAPIView):
    '''Вход пользователя в аккаунт'''
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny,]

    def post(self, request):
        password = request.POST['password']
        if request.POST['username']:
            username = request.POST['username'].lower()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser or  user.myuser.authorization_type == 'LP':
                    login(request, user, backend ='django.contrib.auth.backends.ModelBackend')
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.POST['email']:      
            email = request.POST['email'].lower()  
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_superuser or user.myuser.authorization_type == 'LP' :
                    login(request, user, backend='my_oauth.backend.EmailBackend')
                    return Response(status=status.HTTP_200_OK)
            else:
                return  Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(RetrieveAPIView):
    '''Выход из аккаунта'''
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]

    def get(self, request):        
        logout(request) 
        return Response(status=status.HTTP_200_OK)

    

class UserDestroyView(DestroyAPIView):
    '''Удаление аккаунта'''
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class GetProfileView(RetrieveAPIView):
    '''получение профиля пользователя'''
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = ProfileDetailSerializer
    queryset = User.objects.all()


class PasswordChangeView(UpdateAPIView):
    '''изменение пароля пользователя'''
    queryset = User.objects.all()
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated, IsOwner]


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']
        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']
        if not check_password(old_password, instance.password):
            raise serializers.ValidationError({'Ошибка': "Старый пароль неверен"})
        else:
            if password != password2:
                raise serializers.ValidationError({'Ошибка': "Пароли не совпадает"})
            if password == old_password:
                raise serializers.ValidationError({'Ошибка': "Старый и новые пароли должны отличаться"})
            instance.set_password(password)    
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}            
        return Response(serializer.data)



class LoginChangeView(RetrieveUpdateAPIView):
    '''изменение логина пользователя'''
    serializer_class = LoginChangeSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SocialLinkListView(RetrieveAPIView):
    '''Ссылки на социальные сети'''
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = SocialLinkListSerializer
    queryset = User.objects.all()


class SocialLinkCreateView(CreateAPIView):
    '''Добавить ссылку на социальные сети'''
    serializer_class = SocialLinkSerializer
    queryset = SocialLink.objects.all()
    permission_classes = [IsAuthenticated]


    def post(self, request, pk):
        user = User.objects.get(id=pk)
        if user == request.user:
            link = request.POST['link']
            social_link = SocialLink(
                link = link,
                user = user
            )
            social_link.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class ChangeSocialLinkView(RetrieveUpdateDestroyAPIView):
    '''Изменить ссылки на социальные сети'''
    serializer_class = SocialLinkSerializer
    queryset = SocialLink.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


    def retrieve(self, request, pk):
        instance = self.get_object()
        if instance.user == request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class ChangeClientCredentialsView(RetrieveUpdateAPIView):
    '''изменение профиля пользователя'''
    serializer_class = ChangeClientCredentialsSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

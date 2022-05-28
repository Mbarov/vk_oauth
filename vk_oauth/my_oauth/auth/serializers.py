from rest_framework import serializers
from ..models import User, MyUser, SocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['link']
        

class SocialLinkListSerializer(serializers.ModelSerializer):
    sociallink = SocialLinkSerializer(many=True)
    class Meta:
        model = User
        fields = ['username', 'sociallink']



class SocialLinkCreateSerializer(serializers.ModelSerializer):
    sociallink = SocialLinkSerializer()
    class Meta:
        model = User
        fields = ['username', 'sociallink']
        extra_kwargs = {'username':{'read_only': True, },}

    

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['bday']



class MyUserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['bday', 'authorization_type' ]
        read_only_fields = ['authorization_type']


class UserRegistrSerializer(serializers.ModelSerializer):
    myuser = MyUserSerializer()
    social_link = SocialLinkSerializer()
    password2 = serializers.CharField(label='Повторите пароль')
    class Meta:
        model = User
        fields = ['username', 'password', 'password2' ,'email', 'first_name', 'last_name', 'myuser', 'social_link']
        extra_kwargs = {
            'username': {
                'label': 'Логин'
            },}

    def create(self, validated_data):
        '''Создание нового пользователя'''
        user = User(
            email=self.validated_data['email'].lower(), 
            username=self.validated_data['username'].lower(), 
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        social_link = SocialLink(
            link = self.validated_data['social_link']['link'],
            user = user
        )
        social_link.save()
        myuser = MyUser(
            user = user,
            bday = self.validated_data['myuser']['bday'],
            authorization_type = 'LP'
        )
        myuser.save()
        return user


class ProfileDetailSerializer(serializers.ModelSerializer):
    myuser = MyUserSerializer()
    sociallink = SocialLinkSerializer(many=True)
    class Meta:
        model = User
        fields = ['id','username' ,'email', 'first_name', 'last_name', 'myuser', 'sociallink']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='Логин', required=False)
    class Meta:
        model = User
        fields = ['username', 'email',  'password']


class PasswordChangeSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Повторите пароль')
    old_password = serializers.CharField(label='Введите старый пароль')
    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2' ]


class ChangeClientCredentialsSerializer(serializers.ModelSerializer):
    myuser = MyUserCredentialsSerializer()
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'myuser']


    def update(self, instance, validated_data):
        myuser_data = validated_data.pop('myuser')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()        
        bday = myuser_data['bday']
        myuser = instance.myuser
        myuser.bday = bday
        myuser.save()
        return instance


class LoginChangeSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username' ]



class SocialLinkDeleteSerializer(serializers.ModelSerializer):
    myuser = MyUserSerializer()
    class Meta:
        model = User
        fields = ['id','username' ,'email', 'first_name']
        extra_kwargs = {
            'first_name':'readonly'
        }

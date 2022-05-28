from django.db import models
from django.contrib.auth.models import User


class SocialLink(models.Model):
    link = models.URLField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sociallink')

    def __str__(self):
        return self.link


class MyUser(models.Model):
    CHOICES = (
        ('LP', 'Login/password'),
        ('VK', 'VKOauth'),
        ('G', 'GoogleOauth'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bday = models.DateField('Дата рождения',blank=True,)
    authorization_type = models.CharField('Тип авторизации', max_length=200, choices = CHOICES)

    @property
    def is_authenticated(self):
        return True 


    def __str__(self):
        return self.user.username



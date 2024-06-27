from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField

class ArteForm(ModelForm):
    #captcha = CaptchaField()
    captcha = ReCaptchaField()

    class Meta:
        model = Arte
        fields = ['nombre','descripcion','autor','tipo_arte','descripcion','dimensiones','correo_propietario','imagen','precio']
        #fields = '__all__'


class TipoArteForm(ModelForm):

    class Meta:
        model = TipoArte
        #fields = ['nombre','descripcion']
        fields = '__all__'




#Usuarios
class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField()
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        #fields = '__all__'

     
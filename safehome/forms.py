# coding=utf-8
import django.forms as forms
from captcha.fields import CaptchaField
from django.core.validators import MaxValueValidator, MinValueValidator


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True,
                               error_messages={'required': 'Username can not be empty'},
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Enter username:'}))
    password = forms.CharField(label='Password', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Enter password:'}))
    captcha = CaptchaField(label='Captcha')


# 控制面板的form
class ControlPanelForm(forms.Form):
    # 开启或关闭系统
    system_status = (('Stay', 'Stay'),
                     ('Away', 'Away'))

    status = forms.ChoiceField(label='Status', choices=system_status, widget=forms.RadioSelect())
    phone_number = forms.RegexField(label='Telephone number', required=True,
                                    regex=r'^1\d{10}$',
                                    error_messages={'required': 'Telephone number can not be empty'},
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Enter telephone number:'}))
    delay = forms.IntegerField(label='Dial delay in seconds', required=True,
                               validators=[MinValueValidator(0), MaxValueValidator(60)])

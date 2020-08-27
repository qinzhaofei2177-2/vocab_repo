from django.db import models
from django import forms
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="static/avatar/", blank=True)
    invitecode = models.CharField(max_length = 127, blank=True, verbose_name="Invitation Code", help_text="You can obtain this from our members")
    wechat_openid = models.CharField(max_length = 127, blank=True)
    wechat_unionid = models.CharField(max_length = 127, blank=True)
    nickname = models.CharField(max_length = 63, blank=True, unique=False)
    gender = models.BooleanField('Gender', max_length = 1, choices={(0,'Female'),(1,'Male')}, default=0, blank=False)
    phone = models.CharField(max_length = 14, blank=False, unique=True)
    dob = models.DateField(blank=False, verbose_name="Date of Birth")
    signature = models.TextField(blank=True, verbose_name="Motto", help_text="Tell us about yourself")

    def __str__(self):
        gender = "Female"
        if self.gender:
            gender = "Male"
        return f"{self.user}: 【Gender】{gender}, 【DoB】{self.dob}, 【phone】{self.phone}, 【motto】{self.signature}; "

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(), help_text="Required. 10~20 characters. Letters, digits and _ only.")
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']
        labels = {
            'email':_('电子邮箱'),
            'username':_('用户名'),    #Setting field labels 
        }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-required'}),   #setting styles
            'password':forms.TextInput(attrs={'class':'form-required'}),
        }
        #error_messages = {
        #    'username':{'required':_('Required by Alex!!!')},                    #setting wrong messages
        #    'password':{'required':_('Required by Alex!!!')},
        #}
    
    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get("password")
        pw2 = cleaned_data.get("confirm_password")
        if len(pw) < 10:
            self.add_error('password', _('Too short! Password should have at least 10 characters'))
        elif len(pw) > 20:
            self.add_error('password', _('Too long! Password should have at most 20 characters'))
        if re.match("^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[._~!@#$^&*])[A-Za-z0-9._~!@#$^&*]{10,20}$", pw) == False:
            self.add_error('password', _('Password can contain letters, digits and ._~!@#$^&* only'))
        if pw != pw2:
            self.add_error('password', _('Passwords should be identical'))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar','invitecode','nickname','gender','phone','dob','signature']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Phone number can only be 11 digits
        if str(phone).isdigit() == False:
            # [RAISE nonfield error] self.add_error('phone', forms.ValidationError(_('Phone # should be digits'), code="phone invalid"))
            raise forms.ValidationError(_('Phone # should be digits'), code="phone invalid")
        if len(phone) != 11:
            # [RAISE nonfield error] self.add_error('phone', forms.ValidationError(_('Valid cell number should be 11 digits'), code="phone invalid"))
            raise forms.ValidationError(_('Valid cell number should be 11 digits'), code="phone invalid")
        return phone

class Dictionary(models.Model):
    BaseWord = models.CharField(max_length = 255)
    Defn = models.TextField()
    CEFR = models.CharField(max_length = 255)
    Guideword = models.CharField(max_length = 255)
    Level = models.TextField()
    PartOfSpeech = models.CharField(max_length = 255)
    EngDefn = models.TextField()
    Pron = models.TextField()
    Audio = models.TextField()
    Comments = models.TextField()
    Type = models.CharField(max_length = 255)
    Topic = models.CharField(max_length = 255)
    Grammar = models.CharField(max_length = 255)

    def __str__(self):
        return f"{self.BaseWord} - {self.Defn}<br/>"
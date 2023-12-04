from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
# from django.core.exceptions import ValidationError
# from django.forms import fields



from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200,help_text='you have enter email')

    class Meta:
        model = User
        fields = ('email','username','password1','password2')

    def cleaned_email(self):
        email = self.cleaned_data['email'].lower()

        try:
            account = User.objects.exclude(pk=self.instanc.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("email is already" % account)

    def cleaned_username(self):
        username = self.cleaned_data['username']

        try:
            account = User.objects.exclude(pk=self.instanc.pk).get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("username is already" % account)



class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('invalid login')



class EditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','email','avatar')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise ValueError("email '%s' is already" % account)

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            account = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise ValueError("username '%s' is already" % account)


    def save(self, commit=True):
        account = super(EditForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.avatar = self.cleaned_data['avatar']

        if commit:
            account.save()
        return account




















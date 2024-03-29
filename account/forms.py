from django import forms
from .models import CustomUser, Message
from django.contrib.auth.forms import UserChangeForm

class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    firstname = forms.CharField()
    lastname = forms.CharField()
    inputCity = forms.CharField()
    dob = forms.DateField()

    def save(self):
        # Extract cleaned data from the form
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        inputCity = self.cleaned_data['inputCity']
        dob = self.cleaned_data['dob']

        CustomUser.objects.create_user(email=email,
            password=password,
            first_name=firstname,
            last_name=lastname,
            current_place=inputCity,
            date_of_birth=dob)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'current_place', 'working_as', 'profile_picture', 'relationship_status', 'interested_in', 'gender']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
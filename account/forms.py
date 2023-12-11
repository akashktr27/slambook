from django import forms
from .models import CustomUser
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
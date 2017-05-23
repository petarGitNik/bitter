from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from bitter_app.models import Profile
from bitter_app.models import Bitts

# Registration form (Sign up form)
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'First name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'Last name'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder' : 'Enter password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm password'}))

    # If custom form fields and models fields do not match, save method must be
    # overriden (User model has only one field for passwrod, self titled)
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password = self.clean_password()

        if commit:
            user.save()

        return user

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    class Meta:
        # Validate form agains this model
        model = User
        # Render fields in this order
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

# Profile form
class EditProfileForm(forms.ModelForm):
    biography = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'id' : 'biography',
        'placeholder' : 'Enter your short bio here.',
        'maxlength' : '250',
        # Why does django automatically sets rows and cols?
    }))
    avatar = forms.FileField(required=False, widget=forms.FileInput(attrs={
        # No attributes
    }))

    class Meta:
        model = Profile
        fields = ['biography', 'avatar']

# Authentication/Log in form
class LogInForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

# Bitt form (bitt is like tweet)
class BittForm(forms.ModelForm):
    bitt = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'id' : 'new-bitt-text',
        'placeholder' : "What's bothering you today?",
        'maxlength' : '140',
        'rows' : '2',
    }))

    class Meta:
        model = Bitts
        fields = ['bitt']
        exclude = ('user',)

from django import forms
from myapp.models import Order, Review, Member, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    CATEGORY_CHOICES=[
        ('S','Science&Tech'),
        ('F','Friction'),
        ('B','Biography'),
        ('T','Travel'),
        ('O','Other')
    ]
    # name=forms.CharField(max_length=100, required=False, label='Your Name')
    category=forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY_CHOICES, required=False, label='Select a category')
    max_price=forms.IntegerField(label='Maximum Price', min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields=['books','order_type']
        widgets={'books':forms.CheckboxSelectMultiple(),
                 'order_type':forms.RadioSelect}
        labels={'member':'Member name'}


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['book','rating','comments']
        widgets={'book':forms.RadioSelect()}
        labels={'reviewer':'Please enter a valid email','rating':'Rating: An integer between 1(worst) and 5(best)'}


class RegisterForm(UserCreationForm):
    email=forms.EmailField()
    first_name = forms.CharField(max_length=100, required=False, label='First Name')
    last_name = forms.CharField(max_length=100, required=False, label='Last Name')

    class Meta:
        model=Member
        fields=['username','first_name','last_name','email','password1','password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model=Member
        fields=['username','password']


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model=Member
        fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']


class PasswordRequestForm(forms.ModelForm):
    email=forms.EmailField()
    last_name=forms.CharField()
    first_name=forms.CharField()

    class Meta:
        model=User
        fields=['first_name','last_name','email']


class PasswordChangeForm(SetPasswordForm):
     class Meta:
        model=Member
        fields=['password1','password2']
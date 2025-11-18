from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Flights,Hotels,BookPackage,BookFlight,BookHotel,Famous
import datetime


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    last_name = forms.CharField(max_length=30,widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    username = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    password1=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form form-control'}))
    password2=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form form-control'}))

    class Meta:
        model = User

class FlightForm(forms.Form):
    source = forms.CharField(max_length=20,label='SOURCE',widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'Source'}),required=True)
    destination = forms.CharField(max_length=20,label='DESTINATION',widget=forms.TextInput(attrs={'class' : 'fds-forms form-control','placeholder':'Destination'}),required=True)
    date = forms.DateField(initial=datetime.date.today,label='DATE',widget=forms.TextInput(attrs={'class' : 'fd-form form-control','placeholder':'YYYY-MM-DD'}),required=True)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("Date cannot be in the past.")
        return date

    class Meta:
        model = Flights
        fields = ('source','destination','city')


class HotelForm(forms.Form):
    city = forms.CharField(max_length=20,label='CITY',widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'City'}),required=False)
    date = forms.DateField(initial=datetime.date.today,label='Date ',widget=forms.TextInput(attrs={'class' : 'fd-form form-control','placeholder':'YYYY-MM-DD'}),required=False)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < datetime.date.today():
            raise forms.ValidationError("Date cannot be in the past.")
        return date

    class Meta:
        model = Hotels
        fields = ('city')

class ChoiceForm(forms.Form):
    flight = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'Choose Flight'}),required=False)
    seats = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'SEATS'}),required=False)
    hotel = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'Choose Hotel'}),required=False)
    rooms = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'ROOMS'}),required=False)

    class Meta:
        models = BookPackage
        fields = ('flight','seat','hotel_name','room')

class SeatForm(forms.Form):
    seats = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'SEATS'}),required=False)

    class Meta:
        models = BookFlight
        fields = ('seats')

class RoomForm(forms.Form):
    rooms = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'ROOMS'}),required=False)

    class Meta:
        models = BookHotel
        fields = ('room')

class CityForm(forms.Form):
    city = forms.CharField(max_length=20,label='CITY',widget=forms.TextInput(attrs={'class' : 'fs-form form-control','placeholder':'City'}),required=False)

    class Meta:
        models = Famous

class PassengerDetailsForm(forms.Form):
    passenger_name = forms.CharField(max_length=200, label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}), required=True)
    passenger_email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}), required=True)
    passenger_phone = forms.CharField(max_length=20, label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}), required=True)
    passenger_address = forms.CharField(label='Address', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}), required=True)
    passenger_id_number = forms.CharField(max_length=50, label='ID/Passport Number', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ID or Passport number'}), required=False)

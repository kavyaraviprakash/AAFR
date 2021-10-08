from .models import CustomUser, Event, Feedback, Properties, Reservation, Review
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'address', 'city', 'state', 'zipcode', 'phone_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'address', 'city', 'state', 'zipcode', 'phone_number')

class AdminCreationForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'address', 'city', 'state', 'zipcode', 'phone_number', 'is_renter', 'is_employee', 'is_park_attendant')

class DateInput(forms.DateInput):
    input_type = 'date'

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        #self.fields['Amount'].widget.attrs['readonly'] = True
       

    class Meta:
        model = Reservation
        fields = ['Slot','Event_Date','Team_Size']
        widgets = {
            'Event_Date': DateInput(),
        }

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('Name', 'Comments_Or_Questions', 'Email', 'Phone_Number')

class EditProfileForm(UserChangeForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'address', 'city', 'state', 'zipcode')
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Properties
        fields =('Property_id', 'Property_Name', 'slug', 'Park_Id', 'image', 'Type', 'Guest_capacity', 'Location', 'Available', 'Amount')



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('renter','Property_ID','penalty_amount','uploaded_picture','status')

class SendEmailForm(forms.Form):
    #print(forms.)
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(label="To",
                                           queryset=CustomUser.objects.all(),
                                           widget=forms.SelectMultiple())

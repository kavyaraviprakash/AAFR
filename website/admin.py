import calendar
import datetime
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm, AdminCreationForm, SendEmailForm
from .models import CustomUser, Reservation, Review, Event, Feedback
from django.contrib import admin
from .models import Park, Properties
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.safestring import mark_safe


from django.shortcuts import render, get_object_or_404, redirect

from .admin_calendar import EventCalendar



@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ('Park_Id', 'Park_Name', 'City', 'State', 'Attendant_Email', 'Phone')

    def Park_Id(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.park.park_id
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Park_Name(self, instance):
        try:
            return instance.park.name
        except ObjectDoesNotExist:
            return 'ERROR!!'


    def City(self, instance):
        try:
            return instance.park.city
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Attendant_Email(self, instance):
        try:
            return instance.park.Attendant_email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Phone(self, instance):
        try:
            return instance.park.phone
        except ObjectDoesNotExist:
            return 'ERROR!!'


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = ['Property_id', 'Park_Id', 'Property_Name','slug', 'Type', 'Guest_capacity', 'Location','Amount']
    prepopulated_fields = {'slug': ('Property_Name',)}

    def Property_id(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.Properties.Property_id
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Park_Id(self, instance):
        try:
            return instance.Properties.Park_id
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Property_Name(self, instance):  # name of the method should be same as the field given in `list_display`
            try:
                return instance.Properties.Property_Name
            except ObjectDoesNotExist:
                return 'ERROR!!'

    def Type(self, instance):
        try:
            return instance.Properties.Type
        except ObjectDoesNotExist:
            return 'ERROR!!'


    def Guest_capacity(self, instance):
        try:
            return instance.Properties.Guest_capacity
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Location(self, instance):
        try:
            return instance.Properties.Location
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def Amount(self, instance):
        try:
            return instance.Properties.Amount
        except ObjectDoesNotExist:
            return 'ERROR!!'

    class Meta:
        verbose_name_plural = 'Properties'

class AdminUserCreationForm(UserAdmin):
    class Meta:
        """
        password = ReadOnlyPasswordHashField(
            label= ("Password"),
            help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))
        """
        model = CustomUser
        fields = "__all__"

"""
class AdminUserChangeForm(UserAdmin):
    class Meta:
        model = CustomUser
        fields = "__all__"
"""

class CustomUserAdmin(admin.ModelAdmin):
    add_form = AdminCreationForm
    form = AdminCreationForm
    model = CustomUser
    list_display = ['username', 'email', 'address', 'city', 'state', 'zipcode', 'is_staff']
    """
    def save_model(self, request, obj, form, change):
        print("SAVING PASSWORD")
        obj.password = obj.password
        obj.save()
    """

admin.site.register(CustomUser, CustomUserAdmin)
def send_email(self, request, queryset):
    form = SendEmailForm(initial={'users': queryset[0].renter})
    return render(request, 'send_email.html', {'form': form})




class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id','renter', 'status', 'Property_ID',
                    'penalty_amount']
    list_filter = ['renter', 'penalty_amount', 'Property_ID', 'status']
    actions = [send_email]



class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ['User', 'Park_ID', 'Property_ID', 'Event_Date', 'Slot', 'Team_Size']


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = [ 'title','day', 'start_time', 'end_time','notes']



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Comments_Or_Questions', 'Email', 'Phone_Number', 'created_date']

    class Meta:
        verbose_name_plural = 'Feedback'


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Event,EventAdmin)

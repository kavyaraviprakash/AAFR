#from pdb import pm
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse




from TM_3_8210 import settings


class CustomUser(AbstractUser):
    email = models.EmailField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=50, default='0000000000')
    is_renter = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_park_attendant = models.BooleanField(default=False)


class Park(models.Model):
    Park_Id = models.AutoField(primary_key=True)
    Park_Name = models.CharField(max_length=200, default=' ', null=False)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Zipcode = models.CharField(max_length=10)
    Attendant_Email = models.EmailField()
    Phone = models.CharField(max_length=20, null=False)

    class Meta:
        ordering = ('Park_Id',)
        verbose_name = 'park'
        verbose_name_plural = 'parks'

    def __str__(self):
        return self.Park_Name

    def get_absolute_url(self):
        return reverse('property_list_by_park',
                       args=[self.Park_Id])


Type_choices = [('Atheletic_Field', 'Atheletic Field'),
                ('Pavilion', 'Pavilion'), ('Others', 'Others')]


class Properties(models.Model):
    Property_id = models.AutoField(primary_key=True)
    Property_Name = models.CharField(max_length=50, default=' ')
    slug = models.SlugField(max_length=200, unique=True)
    Park_Id = models.ForeignKey(Park,
                                related_name='properties',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/%Y/%m/%d', blank=True)
    Type = models.CharField(max_length=100, choices=Type_choices)
    Guest_capacity = models.CharField(max_length=50)
    Location = models.CharField(max_length=100)
    Available = models.BooleanField(default=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('Property_id',)
        verbose_name = 'properties'
        verbose_name_plural = 'properties'

    def __str__(self):
        return self.Property_Name

    def get_absolute_url(self):
        return reverse('property_detail', args=[self.Property_id, self.slug])


Slot_choices = [('7AM-9AM', '7am-9am'),
                ('10AM-12PM', '10am-12pm'),
                ('3PM-5PM', '3pm-5pm'),
                ('5PM-7PM', '5pm-7pm'),
                ('7PM-9PM', '7pm-9pm'), ]


class Reservation(models.Model):
    price = models.IntegerField(default=0)
    Res_ID = models.TextField(primary_key=True, null=False)
    Park_ID = models.ForeignKey(Park, on_delete=models.CASCADE)
    Property_ID = models.ForeignKey(Properties, on_delete=models.CASCADE)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    Event_Date = models.DateField()
    Slot = models.CharField(max_length=50, choices=Slot_choices)
    Team_Size = models.CharField(max_length=50)

    def __str__(self):
        return 'Reservation {}'.format(self.Res_ID)



class Transaction(models.Model):

    trn_ID = models.AutoField(primary_key=True)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    Property_ID = models.ForeignKey(Properties, on_delete=models.CASCADE, default=1)
    Reservation_ID = models.ForeignKey(Reservation, on_delete=models.CASCADE, default=1)
    Event_Date = models.DateField()
    Slot = models.CharField(max_length=50, choices=Slot_choices)
    Team_Size = models.CharField(max_length=50)
    paid_date = models.DateTimeField(auto_now=True)
    updated = models.DateField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-paid_date',)

    def __str__(self):
        return 'TRANSACTION U {} R {}'.format(self.User, self.Property_ID, self.Reservation_ID)

status_choices = [('Ready', 'Ready'),
                ('Not Ready', 'Not Ready'),]
class Review(models.Model):
    renter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    Property_ID = models.ForeignKey(Properties, on_delete=models.CASCADE, default=1)
    penalty_amount = models.CharField(max_length=30)
    uploaded_picture = models.ImageField(upload_to='review/%Y/%m/%d', blank=True)
    status = models.CharField(max_length=100, choices=status_choices)


    class Meta:
        ordering = ('renter',)

    def __str__(self):
        return format(self.renter)




class Event(models.Model):
    title = models.CharField(u'Title', help_text=u'Title', max_length=50)
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    Property_ID = models.ForeignKey(Properties, on_delete=models.CASCADE)
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'


    def __str__(self):
        return self.title




class Feedback(models.Model):
    Name = models.CharField(max_length=200)
    Comments_Or_Questions = models.CharField(max_length=500)
    Email = models.EmailField(max_length=200)
    Phone_Number = models.CharField(max_length=20, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name



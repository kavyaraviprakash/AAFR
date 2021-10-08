import random
import calendar
from pyexpat.errors import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from .forms import ReservationForm, VisitorForm, SendEmailForm, PropertyForm
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from .admin_calendar import EventCalendar
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Park, Properties, Event, Reservation, Review, CustomUser
from .filter import PropertiesFilter
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import stripe
from datetime import timedelta

stripe.api_key = "sk_test_51Ibg2OJpyrKc2M05n0pLLYCcoahRWm6jt4MjIl0b2rZ1ZD5neKFDq5QtzH3be6B1vjFFIcObleLd3BGyfsoxYwl200TsiHRhIY"
from django.http import HttpResponse


def park(request):
    park = Park.objects.filter()
    return render(request, 'park.html',
                  {'park': park})


def property_list(request):
    global park
    parks = Park.objects.all()
    properties = Properties.objects.filter(Available=True)
    propertiesFilter = PropertiesFilter(request.GET, queryset=properties)
    properties = propertiesFilter.qs
    return render(request, 'properties.html',
                  {'properties': properties,
                   'parks': parks,
                   'park': park,
                   'propertiesFilter': propertiesFilter})


def property_list_by_park(request, Park_Id):
    properties = Properties.objects.filter(Park_Id=Park_Id).filter(Available=True)
    # properties = list(filter(lambda obj: str(obj.Park_Id) == str(Park_Id), Properties.objects.filter(
    #    Available=True)))

    return render(request, 'park_detail.html',
                  {'properties': properties})


def property_detail(request, Property_id, slug):
    properties = list(filter(lambda obj: str(obj.Property_id) == str(Property_id),
                             Properties.objects.filter(slug=slug, Available=True)))
    user = request.user
    Reservation_form = ReservationForm(initial={'Amount': properties[0].Amount, 'Property_ID': 1})
    return render(request, 'property_detail.html',
                  {'properties': properties,
                   'Reservation_form': Reservation_form,
                   'user': user})


@login_required
def rent(request, Property_id, slug):
    print("RENTING")
    properties = list(
        filter(lambda obj: str(obj.Property_id) == str(Property_id), Properties.objects.filter(Available=True)))

    # properties = get_object_or_404(Properties, Property_id=Property_id)

    print(request.user)
    userobj = request.user
    print(request.method)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
    properties = list(filter(lambda obj: str(obj.Property_id) == str(Property_id), Properties.objects.filter(
        Available=True)))
    # properties = get_object_or_404(Properties, Property_id=Property_id)
    if request.method == 'POST':
        print("METHOD = POST")
        # form = ReservationForm(request.POST)
        # if True:
        if form.is_valid():
            useProperty = Properties.objects.get(Property_id=Property_id)
            print(useProperty)
            print("FORM")
            ResInput = form.save(commit=False)
            ResInput.Property_ID = useProperty
            ResInput.Property_ID_id = ResInput.Property_ID.Property_id
            ResInput.Park_ID = useProperty.Park_Id
            ResInput.Park_ID_id = ResInput.Park_ID.Park_Id
            ResInput.Res_ID = random.randrange(1000000000)
            ResInput.User = request.user
            print("  Res ID: " + str(ResInput.Res_ID))
            print("Property: " + str(ResInput.Property_ID_id))
            print("    Park: " + str(ResInput.Park_ID))
            print("    User: " + str(ResInput.User))
            print("    Date: " + str(ResInput.Event_Date))
            print("    Slot: " + str(ResInput.Slot))
            print("    Team: " + str(ResInput.Team_Size))
            print("Checking for duplicates...")
            duplicate = True
            go = Reservation.objects.filter(Park_ID=ResInput.Park_ID).filter(Event_Date=ResInput.Event_Date).filter(Slot=ResInput.Slot)
            print(go)
            if not go:
                duplicate = False
            if duplicate is True:
                print("Duplicate found...")
                Reservation_form = ReservationForm(
                    initial={'Amount': useProperty.Amount, 'Property_ID': useProperty.Property_id})
                return render(request, 'property_detail.html',
                              {'properties': properties,
                               'Reservation_form': Reservation_form,
                               'user': userobj,
                               'message': "That time is booked. Please choose another slot."})
            else:
                ResInput.save()
                return render(request, 'paystripe.html')
    else:
        form = ReservationForm()

    return render(request,
                  'paystripe.html',
                  {'rent': rent, 'form': form})


"""
class rental_edit(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'rental_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
"""


def rental_edit(request):
    editUser = request.user
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'is_renter': editUser.is_renter})
        print(updated_request)
        form = CustomUserChangeForm(updated_request, instance=request.user)
        print("FORM SUBMITTED")
        print(form)
        if form.is_valid():
            print("FORM IS VALID")
            print("USER TO CHANGE")
            print(editUser)
            form.save()
            return redirect('renters_homepage')
    else:
        print(request.user)
        form = CustomUserChangeForm(initial=model_to_dict(request.user))
    return render(request, 'rental_edit.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        userT = request.user
        if userT.is_superuser or userT.is_employee:
            print("SENDING A SUPERUSER")
            return redirect('empfindpark')
            # return HttpResponseRedirect(reverse('admin:index'))
        elif userT.is_renter:
            return redirect('renters_homepage')
        elif userT.is_park_attendant:
            return redirect('park_attendant_homepage')
    else:
        return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'is_renter': True})
        form = CustomUserCreationForm(updated_request)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(request)
            print(user)
            login(request, user)
            user.is_renter = True
            user.save()
            subject = 'AAFR Signup'
            message = f"Your registration with AAFR has been verified and your account has been created, you can login to  your account by " \
                      f"using the Username:{username} and Password:{raw_password} "
            # email_from = 'AAFR team'
            # recipient_list = [user.email]

            print(user)
            print (user.email)
            mail = EmailMessage(
                subject,
                'Hi''\n' + user.username + '\n' + message,
                'team@AAFR.com',
                [user.email])

            mail.send()
            return redirect('renters_homepage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print(user)

        if user is not None:
            if user.is_active:
                login(request, user)
            if user.is_superuser or user.is_employee:
                print("SENDING A SUPERUSER")
                return redirect('empfindpark')
                # return HttpResponseRedirect(reverse('admin:index'))
            elif user.is_renter:
                return redirect('renters_homepage')
            elif user.is_park_attendant:
                return redirect('park_attendant_homepage')
        else:
            info = 'Username OR password is incorrect'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'info': info})
    else:
        form = AuthenticationForm(request.POST)
        return render(request, 'login.html', {'form': form})


def account(request):
    return render(request, 'account.html')


def renters_homepage(request):
    return render(request, 'renters_homepage.html')


def renters_homepage(request):
    return render(request, 'renters_homepage.html')


def park_attendant_homepage(request):
    return render(request, 'park_attendant_homepage.html')


def park_attendant_homepage(request):
    return render(request, 'park_attendant_homepage.html')


def logoutuser(request):
    logout(request)
    return redirect('home')


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        temp = datetime(year, month, 1)
        return temp
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get requested month

        d = get_date(self.request.GET.get('month', None))

        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')

        context['calendar'] = mark_safe(html_calendar)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def visitor_new(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitors = form.save(commit=False)
            visitors.created_date = timezone.now()
            visitors.save()
            return render(request, 'feedback_done.html')

    else:
        form = VisitorForm()
        # print("Else")
    return render(request, 'contact.html', {'form': form})


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


def thanks(request):
    return render(request, 'success.html')


@csrf_exempt
def CreateCheckoutSessionView(request):
    # YOUR_DOMAIN = "http://127.0.0.1:8000"--> Need to use this while deploying it in heroku -->change the domain.
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1IbtZ1JpyrKc2M05MqOTQQWj',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',

        cancel_url=request.build_absolute_uri(reverse('renters_homepage')),

    )

    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }

    return render(request, 'paystripe.html', context)


@csrf_exempt
def stripe_webhook(request):

    print('WEBHOOK!')
    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = 'whsec_RF7IKpf205gfoP3Iyah7ZewrGih4JMFe'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret, event
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)

    return HttpResponse(status=200)


def empfindpark(request):
    park = Park.objects.filter()
    user = request.user
    if user.is_superuser or user.is_employee:
        print("SENDING A SUPERUSER")
        return render(request, 'park.html',
                      {'park': park})
    elif user.is_renter:
        return redirect('renters_homepage')
    elif user.is_park_attendant:
        return redirect('park_attendant_homepage')
    else:
        return redirect('home')


class empparkEdit(LoginRequiredMixin, UpdateView):
    model = Park
    fields = ('Park_Name', 'City', 'State', 'Zipcode', 'Attendant_Email', 'Phone')
    template_name = 'employee_parkedit.html'
    success_url = reverse_lazy('empfindpark')


class empparkDelete(LoginRequiredMixin, DeleteView):
    model = Park
    template_name = 'employee_pardelete.html'
    success_url = reverse_lazy('empfindpark')


class empparkAdd(LoginRequiredMixin, CreateView):
    model = Park
    template_name = 'employee_parkadd.html'
    fields = ('Park_Id', 'Park_Name', 'City', 'State', 'Zipcode', 'Attendant_Email', 'Phone')
    success_url = reverse_lazy('empfindpark')


def profile(request):
    user = request.user
    reservations = Reservation.objects.filter(User=user)

    return render(request, 'profile.html', {'user': user, 'reservations': reservations})


class newproperty(LoginRequiredMixin, CreateView):
    model = Properties
    template_name = 'property_new.html'

    fields = (
        'Property_id', 'Property_Name', 'slug', 'Park_Id', 'image', 'Type', 'Guest_capacity', 'Location', 'Available',
        'Amount')
    success_url = reverse_lazy('property_list')


class property_edit(LoginRequiredMixin, UpdateView):
    model = Properties
    template_name = 'property_edit.html'
    fields = (
        'Property_id', 'Property_Name', 'slug', 'Park_Id', 'image', 'Type', 'Guest_capacity', 'Location', 'Available',
        'Amount')
    success_url = reverse_lazy('property_list')



class property_delete(LoginRequiredMixin, DeleteView):
    model = Properties
    template_name = 'property_delete.html'
    success_url = reverse_lazy('property_list')


class remove_res(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservation_delete.html'
    success_url = reverse_lazy('profile')


def review(request):
    review = Review.objects.filter()
    return render(request, 'review.html',
                  {'review': review})


class Addreview(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review_add.html'
    fields = ('renter', 'Property_ID', 'penalty_amount', 'uploaded_picture', 'status')
    success_url = reverse_lazy('Approval_request')


def Approval_request(request):
    return render(request, 'Approval_request.html')


class SendUserEmails(FormView):
    template_name = 'send_email.html'
    form_class = SendEmailForm
    success_url = reverse_lazy('mail_sent')

    def form_valid(self, form):
        users = form.cleaned_data['users']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        for user in users:
            print(user)
            print(user.email)
            mail = EmailMessage(
                subject,
                'Hi''\n' + user.username + '\n' + message,
                'admin@AAFR.com',
                [user.email])

            mail.send()
        return redirect('mail_sent')


def mail_sent(request):
    return render(request, 'mail_sent.html')


class remove_res(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservation_delete.html'
    success_url = reverse_lazy('profile')


def about(request):
    return render(request, 'about.html')

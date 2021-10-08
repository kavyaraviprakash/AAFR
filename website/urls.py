

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('account/', views.account, name='account'),
    path('renters_homepage/', views.renters_homepage, name='renters_homepage'),
    path('about/', views.about, name='about'),
    path('park_attendant_homepage/', views.park_attendant_homepage, name='park_attendant_homepage'),
    path('signup/', views.signup, name='signup'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('', views.home, name="home"),
    path('view/', views.park, name="park"),
    path('facilities/', views.property_list, name='property_list'),
    path('<int:Park_Id>/', views.property_list_by_park, name='property_list_by_park'),
    path('<int:Property_id>/<slug:slug>', views.property_detail, name='property_detail'),
    path('<slug:slug>/<int:Property_id>', views.rent, name='property_rent'),
    path(r'^calendar/', views.CalendarView.as_view(), name='calendar'),
    path('contact_page/', views.visitor_new, name='visitor_new'),
    #path('cancel/', CancelView.as_view(), name='cancel'),
    #path('', SuccessView.as_view(), name='success'),
    #path('rental_edit/', rental_edit.as_view(), name='rental_edit'),
    path(r'^email-users/$',
    views.SendUserEmails.as_view(),
    name='email'),



    path('mail_sent/', views.mail_sent, name='mail_sent'),
    path('checkout/', views.CreateCheckoutSessionView, name='create-checkout-session'),
    path('thanks/', views.thanks, name='thanks'),
    path('empfindpark/', views.empfindpark, name='empfindpark'),
    path('<int:pk>/edit/', empparkEdit.as_view(), name='empparkEdit'),
    path('<int:pk>/delete/', empparkDelete.as_view(), name='empparkDelete'),
    path('addpark/', empparkAdd.as_view(), name='empparkAdd'),
    path('newproperty/', newproperty.as_view(), name='newproperty'),
    path('property/<int:pk>/edit/', property_edit.as_view(), name='property_edit'),
    path('property/<int:pk>/delete/', property_delete.as_view(), name='property_delete'),
    path('reservation/<int:pk>/delete/', remove_res.as_view(), name='remove_res'),
    path('review/', views.review, name="review"),
    path('Addreview/', Addreview.as_view(), name='Addreview'),
    path('Approval_request', views.Approval_request, name='Approval_request'),
    path('cancel/', views.CancelView, name='cancel'),
    path('success/', views.SuccessView, name='success'),
    path('<slug:slug>/create-checkout-session/<int:pk>/', views.CreateCheckoutSessionView, name='create-checkout-session'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

    path('cancel/', views.CancelView, name='cancel'),
    path('success/', views.SuccessView, name='success'),

    path('rental_edit/', views.rental_edit, name='rental_edit'),
    path('profile/', views.profile, name='profile'),
    path('login/password-reset/', auth_views.PasswordResetView.as_view(template_name='password_Reset_form.html'), name='password_Reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_Reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_Reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_Reset_complete.html'), name='password_reset_complete'),
    path('login/password-reset/', auth_views.PasswordResetView.as_view(template_name='password_Reset_form.html'),
         name='password_Reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_Reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_Reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_Reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

]

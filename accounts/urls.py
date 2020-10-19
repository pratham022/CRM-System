from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('customer/<str:id>/', customer, name='customer'),
    # path('create_order/', create_order, name='create_order'),
    path('create_order/<str:id>/', create_order, name='create_order'),
    path('update_order/<str:id>/', update_order, name='update_order'),
    path('delete_order/<str:id>/', delete_order, name='delete_order'),

    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('user/', user_page, name='user'),
    path('settings/', user_settings, name='settings'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html'
            ), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_sent.html'
            ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_form.html'
            ), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_done.html'
            ), name='password_reset_complete'),

]


'''
PASSWORD RESET MECHANISM WORKFLOW
1. Submit email form                                PasswordResetView.as_view()
2. Email sent success message                       PasswordResetDoneView.as_view()
3. Link to password reset form in email             PasswordResetConfirmView.as_view()
4. Password successfully changed message            PasswordResetCompleteView.as_view()

'''
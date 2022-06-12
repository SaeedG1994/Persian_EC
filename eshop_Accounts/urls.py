from django.urls import path
from . import views
urlpatterns=[

    path('login/',views.login_user,name='login_user'),
    path('logout/',views.logout_user,name='logout_user'),
    path('dashboard/',views.dashboard_user,name='dashboard_user'),

    # REGISTER AND ACTIVATE ACCOUNT

    path('register/',views.register_user,name='register_user'),
    path('email_activate/<uidb64>/<token>/', views.email_activate, name='email_activate'),



    # SEND FOR FORGOT EMAIL __  GOT ACTIVATE LINK IN USER EMAIL __  RESET PASSWORD EMAIL

    path('forgotPassword/',views.forgotPassword_user,name='forgotPassword_user'),
    path('resetPassword_Validate/<uidb64>/<token>/',views.resetPassword_value, name='resetPassword_value'),
    path('restPassword/',views.emailResetPassword,name='emailResetPassword'),



    ]
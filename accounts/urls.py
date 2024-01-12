from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView.as_view(), nam='login'),
    path('register/', views.RegisterView.as_view(), nam='register'),
    path('logout/', views.LogoutView.as_view(), nam='logout'),
    path('account/', views.account_result, nam='account'),
    path('forget_password/', views.ForgetPasswordView.as_view(), name='forget_password'),
    path('forget_password_code/', views.ForgetPasswordEmailCode.as_view(), name='forget_password_code'),
]
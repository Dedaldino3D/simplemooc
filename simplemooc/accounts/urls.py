from django.urls import path, include
from django.contrib.auth import views as auth_views

# from simplemooc.accounts import views

# include(LoginView(template_name='accounts/login.html'))
from simplemooc.accounts import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('login/', views.auth_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('changePassword/', views.edit_password, name='editPassword'),
    path('passwordreset/', views.passwordReset, name='password_reset'),
    path('passwordresetconfirm/<str:key>/', views.password_reset_confirm, name='password_reset_confirm'),
]

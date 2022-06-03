from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/user_form.html'), name='login'),
    path('logout_confirm/', views.UserLogoutConfirm.as_view(), name='logout-confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

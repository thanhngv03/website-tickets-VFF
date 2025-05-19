from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # Nếu bạn có view đăng ký thì thêm:
    #path('register/', your_register_view, name='register'),
]

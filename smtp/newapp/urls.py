from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', home, name='home'),  # Home page
    path('logout/', LogoutView.as_view(next_page='newapp:login'), name='logout'),
    path('user/', user, name='user'),
    path('add_user', add_user , name='add_user'),
    path('edit_user', edit_user , name='edit_user'),
    path('edit/<int:id>/', edit , name='edit'),
    path('delete/<str:id>/', delete , name='delete'),
    path('send-alert/', send_alert, name='send_alert'),
    path('send_individual_email', send_individual_email , name='send_individual_email'),
    path('table_view', table_view , name='table_view'),
    
]

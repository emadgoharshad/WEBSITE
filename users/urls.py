from django.urls import path

from .views import register,home,login_view,edit_profile,profile_view,logout_view

app_name = 'users'

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout_view'),
    path('edit/<int:user_id>', edit_profile, name='edit_profile'),
    path('profile/<int:user_id>', profile_view, name='profile'),

]
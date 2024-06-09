from django.urls import path

from django.views.generic.base import RedirectView
from . import views
urlpatterns = [
    path('google/login/', RedirectView.as_view(url='/accounts/google/login/'), name='google_login'),
    path('signup/', views.signup, name='signup'),
    path('choose_role/<int:user_id>/', views.choose_role, name='choose_role'),
    path('', views.home,name='home'),
    # Add other URLs as needed
]

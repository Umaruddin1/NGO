from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', views.home, name='home'), 
    path('signup/', views.volunteer_signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('donate/', views.donate, name='donate'),
    path('donations/', views.donation_list, name='donation_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

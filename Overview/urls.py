from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from Overview import views

app_name = 'overview'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ProjectACCT/', views.ACCTView.as_view(), name='ACCTT'),
    path('Career/', views.CareerView.as_view(), name='career'),
    path('Education/', views.EducationView.as_view(), name='education'),
    path('ProjectPenetrationTester/', views.PenTView.as_view(), name='pent'),
    path('ProjectWebsite/', views.WebView.as_view(), name='web'),
    path('ProjectArduino/', views.ArduinoView.as_view(), name='arduino'),
    path('PowerFromUnderground/', views.PFUView.as_view(), name='pfu'),
    path('CV/', views.CVView.as_view(), name='CV'),
    path('Portfolio/', views.portfolio, name='portfolio'),
    path('FlashCyclePlot/', views.plot_flash, name='plot_flash'),
    path('BinaryCyclePlot/', views.plot_binary, name='plot_binary'),
    path('load_binary_parametric/', views.simple_binary_parametric, name='simple_binary_parametric'),   
    path('WorkingFluidComparision/', views.comparison_table, name='comparison_table'),
    path('Examples', views.HTMLView.as_view(), name='examples'),

]
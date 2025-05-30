from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from PowerFromUndergroundApp import views

app_name = 'pfu'

urlpatterns = [
    path('', views.PFUView.as_view(), name='powerfromunderground'),
    path('FlashCyclePlot/', views.plot_flash, name='plot_flash'),
    path('BinaryCyclePlot/', views.plot_binary, name='plot_binary'),       
    path('WorkingFluidComparision/', views.comparison_table, name='comparison_table'),

]
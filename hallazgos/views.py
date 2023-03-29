import csv
from io import TextIOWrapper
import calendar
from operator import countOf
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Count

from .models import Hallazgo, Colectivo, Modalidad, Municipio

def translate_to_percentage(C, A, B):
    # calculate the width and height of the area A to B
    width = abs(A[1] - B[1])
    height = abs(A[0] - B[0])
    
    # calculate the distance between C and A, and express it as a percentage of the width and height
    distance_x = abs(C[1] - A[1])
    distance_y = abs(C[0] - A[0])
    percentage_x = (distance_x / width) * 100
    percentage_y = (distance_y / height) * 100
    
    # return the percentage as a tuple
    return (percentage_x, percentage_y)

def lat_lon_convert(lat_lon: list):
    lat_lon_list = []
    lat_start = 32.509600774356244 # esquina 
    lat_end = 26.410299210278374 # esquina 
    lon_start = -115.05720122875945 # esquina
    lon_end= -108.24102851631902 # esquina 

    # for lat, lon in lat_lon:
            # lat_lon_list.append(translate_to_percentage((lat, lon), (lat_start, lon_start), (lat_end, lon_end)))
    return lat_lon_list

class HallazgoListView(ListView): 
    model = Hallazgo
    template_name = 'hallazgos/hallazgo_list.html'
    
    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markers'] = self.model.objects.all().values_list('geo_latitud', 'geo_longitud', 'source_id','fecha', 'observaciones')
        context['colectivos'] = Colectivo.objects.all().values_list('nombre', flat=True)
        context['modalidades'] = Modalidad.AllWithCount()
        context['municipios'] = Municipio.AllWithCount()
        context['tipos'] = set(Hallazgo.objects.values_list('tipo', flat=True).distinct())
        context['anos'] = filter(lambda x: x > 1900, Hallazgo.all_dates_anios())
        context['meses'] = filter(lambda x: x, Hallazgo.all_dates_meses())
        return context


# Create your views here.

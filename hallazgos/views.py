import csv
from io import TextIOWrapper
import calendar
from operator import countOf
from django.http import HttpResponse, HttpResponseBadRequest

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db import models
from .models import Hallazgo, Colectivo

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
    lon_start= -115.05720122875945 # esquina
    lon_end= -108.24102851631902 # esquina 

    for lat, lon in lat_lon:
            lat_lon_list.append(translate_to_percentage((lat, lon), (lat_start, lon_start), (lat_end, lon_end)))
    return lat_lon_list


def upload_data_from_post(request):
    """_summary_
    Upload data from a POST request
    Args:
        request (_type_): request.
    """
    # get the uploaded file from the POST request
    csv_file = request.FILES['csv_file']

    # read the csv data
    csv_reader = csv.reader(TextIOWrapper(csv_file))

    # skip the header row
    next(csv_reader)

    # iterate over each row in the csv data
    for row in csv_reader:
        # extract the Colectivo data from the row
        colectivo_name = row[0]
        colectivo_description = row[1]
        colectivo_location = row[2]

        # check if the Colectivo already exists in the database
        try:
            colectivo = Colectivo.objects.get(name=colectivo_name)
        except Colectivo.DoesNotExist:
            # if the Colectivo doesn't exist, create a new one
            colectivo = Colectivo(name=colectivo_name, description=colectivo_description, location=colectivo_location)
            colectivo.save()

        # extract the Hallazgo data from the row
        hallazgo_name = row[3]
        hallazgo_description = row[4]
        hallazgo_location = row[5]

        # create a new Hallazgo and associate it with the Colectivo
        hallazgo = Hallazgo(name=hallazgo_name, description=hallazgo_description, location=hallazgo_location, colectivo=colectivo)
        hallazgo.save()

def hallazgo_bulk_upload(request):
    if request.method== 'post':
        # check if the CSV file is in the POST request
        if 'csv_file' not in request.FILES:
            return HttpResponseBadRequest('No file uploaded')

        # call the upload function with the POST request
        upload_data_from_post(request)

        # return a success response
        return HttpResponse('Upload successful')
    else: 
        return render(request, 'hallazgos/hallazgo_bulk_upload.html')
        
class HallazgoListView(ListView):
    model = Hallazgo
    all = model.objects.all()
    colectivos = Colectivo.objects.all().values_list('nombre', flat=True)
    template_name = 'hallazgos/hallazgo_list.html'
    extra_context = {
        'colectivos': colectivos,
        'calendar': calendar,
        'meses': all.values_list('fecha__month', flat=True).distinct(),
        'anos': all.values_list('fecha__year', flat=True).distinct(),
        'municipios': all.values_list('municipio', flat=True).distinct(),
        'modalidades': all.values_list('modalidad', flat=True).distinct(),
        'markers': lat_lon_convert(lat_lon= all.values_list('geo_latitud', 'geo_longitud')),
        'tipos': all.values_list('tipo', flat=True),
    }
    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha')


# Create your views here.

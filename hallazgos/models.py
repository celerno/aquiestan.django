"""models related to the hallazgos app.
Returns:
    _type_: _description_
"""
from django.utils import timezone
from django.db import models
from django.db.models.aggregates import Aggregate
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
import logging
from datetime import datetime
logger = logging.getLogger("aquiestan")


def lon_convert(lon: float):
        lon_start= -115.05720122875945;
        lon_end= -108.24102851631902;
        return (lon / (lon_start-lon_end)) * 100

def lat_convert(lat: float):
    lat_start = 32.509600774356244
    lat_end = 26.410299210278374
    return (lat / (lat_start-lat_end)) * 100

# Create your models here.
class Colectivo(models.Model):
    nombre = models.CharField(max_length=100)
    link_facebook = models.CharField(max_length=100, blank=True)
    link_instagram = models.CharField(max_length=100, blank=True)
    link_twitter = models.CharField(max_length=100, blank=True)
    link_web = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    fecha = models.DateField()
    logo = models.ImageField(upload_to='static', null=True, blank=True)
    
    def __str__(self):
        return '{self.nombre}'.format(self=self)
    def exist_or_create(nombre: str):
        colectivo = Colectivo.objects.filter(nombre=nombre)
        if colectivo:
            return colectivo[0]
        else:
            logger.info('Creando colectivo: %s', nombre)
            colectivo = Colectivo(nombre=nombre, fecha=timezone.now(), slug=nombre.replace(' ', '-'))
            colectivo.save()
            return colectivo


class ColectivoMedia(models.Model):
    colectivo = models.ForeignKey(Colectivo, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='static')
    def __str__(self):
        return '{self.colectivo.slug}/{self.imagen.name}'.format(self=self)

class Modalidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ['nombre']
    def AllWithCount():
        return set(Hallazgo.objects.values_list('modalidad__nombre', flat= True))
    def __str__(self):
        return '{self.nombre}'.format(self=self)
    def exist_or_create(nombre: str):
        if(nombre == ''):
            return None
        modalidad = Modalidad.objects.filter(nombre=nombre)
        if modalidad:
            return modalidad[0]
        else:
            logger.info('Creando modalidad: %s', nombre)
            modalidad = Modalidad(nombre=nombre)
            modalidad.save()
            return modalidad


class Municipio(models.Model):
    nombre = models.CharField(max_length=250, unique=True)
    def AllWithCount():
        return set(Hallazgo.objects.values_list('municipio__nombre', flat= True))
    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return '{self.nombre}'.format(self=self) 
    def exist_or_create(nombre: str):
        if nombre == '':
            return None
        municipio = Municipio.objects.filter(nombre=nombre)
        if municipio:
            return municipio[0]
        else:
            logger.info('Creando municipio: %s', nombre)
            municipio = Municipio(nombre=nombre)
            municipio.save()
            return municipio


class Hallazgo(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    source_id = models.IntegerField(blank=False)
    colectivo = models.ForeignKey(Colectivo, on_delete=models.CASCADE)
    fecha = models.DateField(blank=True)
    def all_dates_anios():
        return set(Hallazgo.objects.values_list('fecha__year', flat= True))
    def all_dates_meses():
        return set(Hallazgo.objects.values_list('fecha__month', flat= True))
    
    
    estado = models.CharField(max_length=100, default='Sonora', blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True, default=None)
    localidad = models.CharField(max_length=200, blank=True)
    geo_latitud = models.CharField(max_length=13, blank=True)
    geo_longitud = models.CharField(max_length=13, blank=True)
    tipo = models.CharField(max_length=100, blank=True)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, blank=True, null=True, default=None)
    observaciones = models.TextField(blank=True)
    informacion_adicional = models.TextField(blank=True)
    fuente = models.CharField(max_length=500, blank=True)
    link = models.CharField(max_length=500, blank=True, )
    contiene_imagenes = models.BooleanField(default=False, blank=True)
    notas_internas = models.TextField(blank=True)
    class Meta:
        ordering = ['-source_id']
        unique_together = ('source_id', 'colectivo')

    def __str__(self):
        return '{self.colectivo.nombre} - {self.source_id}'.format(self=self)

def parse_date(date_string:str):
    """
    Parse a date string in any of the following formats:
    1. 01/01/2018
    2. 01-01-2018
    3. 01 January 2018
    4. 01 de Enero 2018
    5. 01 de Enero del 2018
    6. Jan 01 2018
    7. Jan 01 18
    If the date string cannot be parsed, return 1900-01-01
    """
    formats = ['%d %B, %Y','%d/%m/%Y', '%d-%m-%Y', '%d %B %Y', '%d de %B %Y', '%d de %B del %Y', '%b %d %Y', '%b %d %y']
    for fmt in formats:
        try:
            dt = datetime.strptime(date_string.strip().strip('"'), fmt)
            return dt.date()
        except ValueError:
            pass
    return datetime(1900,1,1)

class HallazgoMedia(models.Model):
    hallazgo = models.ForeignKey(Hallazgo, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='hallazgo/{hallazgo.source_id}', null=True, blank=True)
    def __str__(self):
        return '{self.hallazgo.fecha}/{self.hallazgo.source_id}/{self.imagen.name}'.format(self=self)

class HallazgoCSVFile(models.Model):
    csv_file = models.FileField(upload_to="hallazgos_csv",validators=[FileExtensionValidator(['csv'])] )
    uploaded_at = models.DateField(default=timezone.now)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
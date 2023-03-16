"""models related to the hallazgos app.
Returns:
    _type_: _description_
"""
from django.utils import timezone
 
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator

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

class ColectivoMedia(models.Model):
    colectivo = models.ForeignKey(Colectivo, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='static')
    def __str__(self):
        return '{self.colectivo.slug}/{self.imagen.name}'.format(self=self)


    
class Hallazgo(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    source_id = models.IntegerField(blank=True)
    colectivo = models.ForeignKey(Colectivo, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=100, default='Sonora', blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    localidad = models.CharField(max_length=200, blank=True)
    geo_latitud = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)], default=0, blank=True)
    geo_longitud = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], default=0, blank=True)
    tipo = models.CharField(max_length=100, blank=True)
    modalidad = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    informacion_adicional = models.TextField( blank=True)
    fuente = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=500, blank=True, )
    contiene_imagenes = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return '{self.fecha}/{self.source_id}/'.format(self=self)

class HallazgoMedia(models.Model):
    hallazgo = models.ForeignKey(Hallazgo, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='hallazgo/{hallazgo.source_id}', null=True, blank=True)
    def __str__(self):
        return '{self.hallazgo.fecha}/{self.hallazgo.source_id}/{self.imagen.name}'.format(self=self)

class HallazgoCSVFile(models.Model):
    csv_file = models.FileField(upload_to="hallazgos_csv",validators=[FileExtensionValidator(['csv'])] )
    uploaded_at = models.DateField(default=timezone.now)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
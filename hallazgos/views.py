from django.views.generic import ListView
from django.db import models

from .models import Hallazgo, Colectivo, Modalidad, Municipio

class HallazgoListView(ListView): 
    model = Hallazgo
    template_name = 'hallazgos/hallazgo_list.html'
    
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['markers'] = self.model.objects.all().values_list('geo_latitud', 'geo_longitud', 'source_id','fecha', 'observaciones')
        context['colectivos'] = Colectivo.objects.all().values_list('nombre', flat=True)
        context['modalidades'] = Modalidad.AllWithCount()
        context['municipios'] = Municipio.AllWithCount()
        context['municipiostop'] = Municipio.AllWithCount()[:10]
        context['tipos'] = Hallazgo.objects.values('tipo').annotate(c=models.Count('tipo')).order_by('-c')
        context['anos'] = filter(lambda x: x > 1900, Hallazgo.all_dates_anios())
        context['meses'] = filter(lambda x: x, Hallazgo.all_dates_meses())
        context['c'] = self.model.objects.count()
        return context


# Create your views here.

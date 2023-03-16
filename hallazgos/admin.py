from django.contrib import admin
from .actions import bulk_upload_action
from django.db.models.options import Options
from .models import Hallazgo, Colectivo, ColectivoMedia, HallazgoMedia, HallazgoCSVFile
# Register your models here.
colectivo_fields = [field.name for field in Colectivo._meta.get_fields(include_hidden=False, include_parents=False)]
colectivo_fields.remove('colectivomedia')
colectivo_fields.remove('hallazgo')

hallazgo_fields = [field.name for field in Hallazgo._meta.get_fields(include_hidden=False, include_parents=False)]
hallazgo_fields.remove('hallazgomedia')


@admin.register(Colectivo)
class ColectivoAdmin(admin.ModelAdmin):
    list_display = colectivo_fields
    list_filter = ('nombre', 'link_facebook', 'link_instagram', 'link_twitter', 'link_web')
    search_fields = ('nombre', 'link_facebook', 'link_instagram', 'link_twitter', 'link_web')

@admin.register(Hallazgo)
class HallazgoAdmin(admin.ModelAdmin):
    actions = [bulk_upload_action]
    list_display = hallazgo_fields
    list_filter = ('fecha', 'municipio', 'localidad')
    search_fields = ('observaciones', 'informacion_adicional', 'municipio', 'localidad')

@admin.register(ColectivoMedia)
class ColectivoMediaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ColectivoMedia._meta.get_fields( include_hidden=False)]

@admin.register(HallazgoMedia)
class HallazgoMediaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HallazgoMedia._meta.get_fields()]

@admin.register(HallazgoCSVFile)
class HallazgoCSVFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HallazgoCSVFile._meta.get_fields()]
    error_message = 'Error: No se pudo cargar el archivo'

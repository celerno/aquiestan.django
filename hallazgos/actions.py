from django.core.management import call_command

def bulk_upload_action(modeladmin, request, queryset):
    call_command('bulk_upload', request.FILES['csv_file'])
    
bulk_upload_action.short_description = "Carga Masiva de Hallazgos"

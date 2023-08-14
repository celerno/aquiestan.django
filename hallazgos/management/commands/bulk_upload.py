"""Upload to command
"""
import logging
logger = logging.getLogger("aquiestan")
from os import path
from django.db import transaction

from django.core.management.base import BaseCommand, CommandError
from hallazgos.models import Hallazgo, Municipio, Modalidad, Colectivo, parse_date
import csv


class Command(BaseCommand):
    help = 'Carga masiva de hallazgos'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Archivo CSV con los hallazgos')
    
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        logging.info('Cargando archivo CSV: %s', csv_file)
        with open(path.join('/data/media/',csv_file), 'r') as file_stream:
            csv_reader = csv.reader(file_stream, delimiter=',')
            next(csv_reader) # Skip header
            for row in csv_reader:
                if row:
                    try:
                        with transaction.atomic():
                            #SOURCE_ID	COLECTIVO	FECHA	Municipio	Localidad	latitud longitud		TIPO HALLAZGO	MODALIDAD DE HALLAZGO	OBSERVACIONES	INFORMACIÓN ADICIONAL 	FUENTE	LINK 	FOTOS
                            hallazgo, created = Hallazgo.objects.update_or_create(
                                source_id = row[0].strip(),
                                defaults = { "colectivo" : Colectivo.exist_or_create( nombre =row[1].strip()),
                                            "fecha" : parse_date(row[2]),
                                            "municipio" :  Municipio.exist_or_create(row[3].strip()), 
                                            "localidad" : row[4].strip(),
                                            "tipo" : row[7].strip().capitalize(),
                                            "modalidad" : Modalidad.exist_or_create(row[8].strip().capitalize()), 
                                            "observaciones" : row[9].strip(),
                                            "informacion_adicional" : row[10].strip(),
                                            "fuente" : row[11].strip(),
                                            "link" : row[12].strip(),
                                            "contiene_imagenes" : True if row[13] else False,
                                            "notas_internas" : row[14].strip(),
                                            "geo_latitud": 0 if not row[5] else row[5].strip(),
                                            "geo_longitud":  0 if not row[6] else row[6].strip(),
                                            }
                                )
                    except Exception as exception:
                        logger.error('Error al cargar hallazgo: %s', exception)
                    else:
                        logger.info('Hallazgo cargado: %s', hallazgo)
                    
        return 'Hallazgos cargados exitosamente'
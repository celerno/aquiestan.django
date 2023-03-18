"""Upload to command
"""
import logging
logger = logging.getLogger("aquiestan")
from os import path
from django.db import transaction

from django.core.management.base import BaseCommand, CommandError
from hallazgos.models import Hallazgo, Colectivo, colectivo_exist_or_create, parse_date
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
            next(csv_reader) # Skip header
            for row in csv_reader:
                if row:
                    #SOURCE_ID	COLECTIVO	FECHA	Municipio	Localidad	latitud longitud		TIPO HALLAZGO	MODALIDAD DE HALLAZGO	OBSERVACIONES	INFORMACIÓN ADICIONAL 	FUENTE	LINK 	FOTOS
                    hallazgo = Hallazgo(source_id = row[0].strip(),
                                        colectivo = colectivo_exist_or_create(nombre= row[1].strip()), 
                                        fecha = parse_date(row[2]),
                                        municipio = row[3].strip(), 
                                        localidad = row[4].strip(),
                                        tipo = row[6].capitalize(),
                                        modalidad = row[7].capitalize(), 
                                        observaciones = row[8].strip(), 
                                        informacion_adicional = row[9].strip(), 
                                        fuente = row[10].strip().capitalize(), 
                                        contiene_imagenes = True if row[11] else False,
                                        )
                    try:
                        hallazgo.geo_latitud = 0 if not row[5] else float(row[5])
                    except ValueError:
                        try:
                            hallazgo.geo_latitud = 0 if not row[5] else float(row[5].split(",")[0])
                            hallazgo.geo_longitud = 0 if not row[5] else float(row[5].split(",")[1])
                        except ValueError:
                            hallazgo.geo_latitud = 0
                    if hallazgo.geo_longitud != 0:
                        try:
                            hallazgo.geo_longitud = 0 if not row[6] else float(row[6])
                        except ValueError:
                            hallazgo.geo_longitud = 0
                                                            

                        hallazgo.fecha = parse_date(row[2])
                    try:
                        with transaction.atomic():
                            hallazgo.save()
                    except Exception as e:
                        logger.error('Error al cargar hallazgo: %s', e)
                    else:
                        logger.info('Hallazgo cargado: %s', hallazgo)
                    
        return 'Hallazgos cargados exitosamente'
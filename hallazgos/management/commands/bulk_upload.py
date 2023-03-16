"""Upload to command
"""
import logging
from os import path
from django.core.management.base import BaseCommand, CommandError
from hallazgos.models import Hallazgo
import csv
from io import TextIOWrapper

class Command(BaseCommand):
    help = 'Carga masiva de hallazgos'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Archivo CSV con los hallazgos')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        logging.info('Cargando archivo CSV: %s', csv_file)
        with open(path.join('/data/media/',csv_file), 'r') as file_stream:
            csv_reader = csv.reader(file_stream, delimiter=',')
            for row in csv_reader:
                if row:
                    # COLECTIVOS,FECHA,Municipio,GEOLOCALIZACION Lat,Geolocalizacion Lng,TIPO HALLAZGO,MODALIDAD DE HALLAZGO,OBSERVACIONES,INFORMACIÓN ADICIONAL ,FUENTE,FOTOS,SEXO
                    hallazgo = Hallazgo()
                    hallazgo.source_id = row[0]
                    self.stdout.write('Hallazgo cargado exitosamente: ' " ".join(row))
                    # hallazgo.save()
        return 'Hallazgos cargados exitosamente'
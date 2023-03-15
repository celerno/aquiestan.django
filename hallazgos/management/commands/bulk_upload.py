from django.core.management.base import BaseCommand, CommandError
from hallazgos.models import Hallazgo
import csv
from io import TextIOWrapper

class Command(BaseCommand):
    help = 'Carga masiva de hallazgos'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Archivo CSV con los hallazgos')

    def handle(self, *args, **options):
        csv_file = options['file']
        with csv.reader(TextIOWrapper(open(csv_file, 'r'))) as csv_reader:
            for r in csv_reader:
                
                if r:
                    # COLECTIVOS,FECHA,Municipio,GEOLOCALIZACION Lat,Geolocalizacion Lng,TIPO HALLAZGO,MODALIDAD DE HALLAZGO,OBSERVACIONES,INFORMACIÓN ADICIONAL ,FUENTE,FOTOS,SEXO
                    hallazgo = Hallazgo()
                    hallazgo.source_id = r[0]
                    self.stdout.write(self.style.SUCCESS('Hallazgo cargado exitosamente', r))
                    # hallazgo.save()

        self.stdout.write(self.style.SUCCESS('Hallazgos cargados exitosamente'))
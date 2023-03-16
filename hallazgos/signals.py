"""trigger bulk upload when a new csv file is uploaded
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command

from .models import HallazgoCSVFile
logger = logging.getLogger('aquiestan')
logger.addHandler(logging.StreamHandler)


@receiver(post_save, sender=HallazgoCSVFile)
def bulk_upload_action(sender, instance, created, **kwargs):
    if created and instance.csv_file:
        call_command('bulk_upload', instance.csv_file)


# Generated by Django 3.2 on 2023-07-12 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hallazgos', '0003_auto_20230412_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallazgomedia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='hallazgo/{self.hallazgo.source_id}'),
        ),
    ]
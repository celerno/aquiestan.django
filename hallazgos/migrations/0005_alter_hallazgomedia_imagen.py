# Generated by Django 3.2 on 2023-07-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hallazgos', '0004_alter_hallazgomedia_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallazgomedia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='hallazgo/'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-24 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0003_rename_vacinacao_vacinacao_vacina_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diadasemana',
            name='dia',
            field=models.CharField(max_length=20),
        ),
    ]

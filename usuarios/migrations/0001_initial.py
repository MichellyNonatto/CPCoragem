# Generated by Django 4.2.7 on 2023-12-02 00:40

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import usuarios.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nome_completo', models.CharField(max_length=100)),
                ('telefone', models.IntegerField(null=True)),
                ('documento', models.CharField(max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(7), django.core.validators.MaxLengthValidator(14), usuarios.models.validar_tamanho_documento])),
                ('categoria', models.CharField(choices=[('FUNCIONARIO', 'Funcionário'), ('TUTOR', 'Tutor')], max_length=12, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.IntegerField()),
                ('estado', models.CharField(blank=True, max_length=2)),
                ('cidade', models.CharField(blank=True, max_length=45)),
                ('bairro', models.CharField(max_length=45)),
                ('rua', models.CharField(max_length=45)),
                ('numero', models.CharField(blank=True, max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Funcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_vencimento', models.DateField(default=django.utils.timezone.now)),
                ('total_pagamento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pagamento', models.DateField(default=django.utils.timezone.now)),
                ('tipo', models.CharField(choices=[('PIX', 'Pix'), ('DEBITO', 'Débito'), ('CREDITO', 'Crédito')], max_length=8)),
                ('total_pago', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pagamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.pagamento')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imagens_funcionario/')),
                ('turno', models.CharField(choices=[('PRIMEIRO_TURNO', '1º Turno'), ('SEGUNDO_TURNO', '2º Turno')], max_length=40)),
                ('funcao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcao', to='usuarios.funcao')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funcionarios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='endereco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.endereco'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]

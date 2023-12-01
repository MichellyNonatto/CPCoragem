from django.apps import AppConfig


class ServicosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicos'

    def ready(self):
        import servicos.signals

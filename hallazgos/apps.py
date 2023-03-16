from django.apps import AppConfig


class HallazgosConfig(AppConfig):
    """_summary_

    Args:
        AppConfig (_type_): _description_

    Returns:
        _type_: _description_
    """
    default_auto_field = 'django.db.models.BigAutoField'
    comment = 'Manejo de hallazgos, colectivos y medios. Carga masiva, individual y edición.'
    name = 'hallazgos'
    def ready(self) -> None:
        import hallazgos.signals
        return super().ready()

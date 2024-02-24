from django.apps import AppConfig


class WomenConfig(AppConfig):
    verbose_name = 'Женщины мира' #Отображение в админке названия на синем фоне
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'

from django.apps import AppConfig


class LanScoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lan_scores'

    def ready(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='event_admin')

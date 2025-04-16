from django.contrib import admin

from .models import Event, Game,Player,Scores,EventPlayers, GameInstance
# Register your models here.

admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Scores)
admin.site.register(EventPlayers)
admin.site.register(GameInstance)

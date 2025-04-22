from django.contrib import admin

from .models import Event, Game,Player,Scores,EventPlayers, GameInstance
# Register your models here.

class ShowIDAdmin(admin.ModelAdmin):
    list_display = ['id']
    readonly_fields = ['id']

admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Scores)
admin.site.register(EventPlayers)
admin.site.register(GameInstance, ShowIDAdmin)

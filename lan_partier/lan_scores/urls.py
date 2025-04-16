from django.urls import path
from . import views

urlpatterns = [
    path('kissa', views.home, name='home'),
    path('login/', views.sign_in, name='login'),
    path('edit/', views.edit_panel, name='edit'),
    path('event-<str:event_name>-<int:event_id>/', views.event, name='event'),
    path('manage_<str:name>-<int:id>/', views.manage, name='manage_event'),
   
    #BACK
    path('update-player/', views.update_player, name='update_player'),
    path('update-game/', views.update_game, name='update_game'),
    path('update-score/', views.update_score, name='update_score'),
    path('update-event/', views.update_event, name='update_event'),
    path('add-game-event/', views.add_game_event, name='add_game_event'),

]
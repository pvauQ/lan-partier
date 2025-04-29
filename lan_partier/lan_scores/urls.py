from django.urls import path
from . import views

urlpatterns = [
    path('kissa', views.home, name='home'),
    path('front/', views.front_page, name = 'front_page'),
    path('login/', views.sign_in, name='login'),
    path('edit/', views.edit_panel, name='edit'),
    path('event-<str:event_name>-<int:event_id>/', views.event, name='event'),
    path('manage-<str:event_name>-<int:event_id>/', views.manage, name='manage_event'),
   
    #BACK
    path('update-player/', views.update_player, name='update_player'),
    path('update-game/', views.update_game, name='update_game'),
    path('update-score/', views.update_score, name='update_score'),
    path('update-event/', views.update_event, name='update_event'),
    path('finish-event/', views.finish_event, name='finish_event'),
    path('add-event', views.add_event, name = 'add_event'),
    path('add-game-event/', views.add_game_event, name='add_game_event'),
    path('add-player-event/', views.add_player_event, name='add_player_event'),
    path('delete-player-event/', views.delete_player_event, name='delete_player_event'),
    path('hide-gameinstance', views.hide_gameinstance, name = 'hide_gameinstance'),
    path('delete-gameinstance', views.delete_gameinstance, name = 'delete_gameinstance'),

]
from django.shortcuts import render,redirect, get_object_or_404
from .models import Event, EventPlayers, Player, GameInstance,Game,Scores
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from .forms import LoginForm, AddGameForm, AddPlayerForm
from django.http import HttpResponse


def sign_in(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('home')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})

def sign_out(request):
    logout(request)
    return redirect('login')  # or wherever you want to send users after logout

def event(request, event_name, event_id):
    event = Event.objects.filter(id = event_id).first()
    #latest_event = Event.objects.latest('event_date')
    players = event.players.all() 


    event_games =  GameInstance.objects.filter(event = event)
    games = Game.objects.filter(id__in = event_games.values('game'))
    
    scores =(Scores.objects.filter(game_instance__in=event_games.values_list('id'))
                                .select_related('player','game_instance')
                                .order_by('player', "game_instance")
    ) 
    pelaajat = [None]*len(players.values())
    pelit =   [None]*len(event_games.values())
    for i in range(len(pelaajat)):
        pelaajat[i] = players[i]
    for i in range(len(pelit)):
        pelit[i] = event_games[i]
        #print(pelit[i])
    pisteet = [[0 for _ in range(len(pelaajat))] for _ in range(len(pelit))]
    total_pisteet = [0 for _ in range(len(pelaajat))] 

    for x in range(len(pelit)):
        if pelit[x].hiden == True:
            pisteet[x][y] = (0, pelaajat[y].id)
            continue
        for y in range(len(pelaajat)):
            s = scores.filter(game_instance = pelit[x], player = pelaajat[y])
            s = list(s.values_list('score', flat=True))
            if len(s)==1: 
                pisteet[x][y] = s[0]
                total_pisteet[y] += s[0]
            else: pisteet[x][y] = 0

    high = -9999
    winner_index = 0
    for i, piste in enumerate(total_pisteet):
        if piste > high:
            high = piste
            winner_index = i
    winner_index += 1 #tasapeli ei oo kiva :D


    pisteet_pelit = zip(pelit,pisteet)

    context = {
        'event': event,
        'players': players,
        'event_games': event_games,
        'games': games,
        'scores': pisteet_pelit,
        'total_scores': total_pisteet ,
        'winner' :winner_index
    }
    return render(request, "score_page.html", context)



# Create your views here.
def home(request):
    latest_event = Event.objects.last()
    return redirect('event', event_name = latest_event.name, event_id = latest_event.id)

def front_page(request):

    events = Event.objects.all()

    context = {
        'events':events

    }
    return render(request, 'front_page.html' ,context)



def manage(request, event_name, event_id):
    if not request.user.groups.filter(name='event_admin').exists():
        return redirect('login')

    event = Event.objects.filter(id = event_id).first()
    #latest_event = Event.objects.latest('event_date')
    players = event.players.all() 


    event_games =  GameInstance.objects.filter(event = event)
    games = Game.objects.filter(id__in = event_games.values('game'))
    
    #print(games.values_list('id'))
    scores =(Scores.objects.filter(game_instance__in=event_games.values_list('id'))
                                .select_related('player','game_instance')
                                .order_by('player', "game_instance")
    ) 
    pelaajat = [None]*len(players.values())
    pelit =   [None]*len(event_games.values())
    for i in range(len(pelaajat)):
        pelaajat[i] = players[i]
    for i in range(len(pelit)):
        pelit[i] = event_games[i]
        #print(pelit[i])
    pisteet = [[0 for _ in range(len(pelaajat))] for _ in range(len(pelit))]
    total_pisteet = [0 for _ in range(len(pelaajat))] 

    for x in range(len(pelit)):
        for y in range(len(pelaajat)):
            s = scores.filter(game_instance = pelit[x], player = pelaajat[y])
            s = list(s.values_list('score', flat=True))
            temp =[]

            if pelit[x].hiden == True:
                pisteet[x][y] = (s[0], pelaajat[y].id)
                ## ei kasvateta total scorea
            elif len(s)==1:
                pisteet[x][y] = (s[0],pelaajat[y].id )
                total_pisteet[y] += s[0]
            else: 
                pisteet[x][y] = (0, pelaajat[y].id)


    pisteet_pelaajat = (pisteet,pelaajat)
    pisteet_pelit = zip(pelit,pisteet) #game_instance, 2dlist
    form = AddGameForm(request.POST)
    player_form = AddPlayerForm(request.POST)

    context = {
        'event': event,
        'players': players,
        'event_games': event_games,
        'games': games,
        'scores': pisteet_pelit,
        'total_scores': total_pisteet,
        'add_form': form,
        'add_player_form': player_form
    }
    return render(request, "manage_event.html", context)




def edit_panel(request):
    if not request.user.groups.filter(name='event_admin').exists():
        return redirect('login')
    players = Player.objects.all()
    games = Game.objects.all()
    events = Event.objects.all()
    context = {
        'players' : players,
        'games' : games,
        'events': events
    }

    return render(request, 'admin_edit.html' ,context)

def update_score(request):
    
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():

    ##TODO: THIS CAN BUG OUT IF DB RETURNS PLAYERS IN DIFFERENT ORDER THAN IN MANAGE VIEW...(new player added in between?)
        GI = get_object_or_404(GameInstance, id =request.POST.get('game_instance_id'))
        #print(request.POST.get(f"{0}"))
        scores =(Scores.objects.filter(game_instance = GI)
                            .select_related('player','game_instance')
                            .order_by('player', "game_instance")
        ) 
        p_ids = request.POST.getlist("player_id")

        for i, id in enumerate(p_ids):
            new_score = request.POST.get(f'{i}')
            player = Player.objects.filter(id = id).first()
            score = Scores.objects.filter(player = player, game_instance = GI).first()
            if not score:
                score = Scores()
                score.player = player
                score.game_instance = GI
                score.score = new_score
                score.save()   
            else:
                score.score = new_score
                score.save()
        return redirect('manage_event', event_name = GI.event.name, event_id = GI.event.id)
    
    else: return redirect('login')

def add_player_event(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        form = AddPlayerForm(request.POST)
        event_id = request.POST.get('event_id')
        if form.is_valid():
            data = form.cleaned_data
        else: return Http404
        player = Player()
        if data["name"] != "":
            player.name = data['name']
            player.link = data['link']
            player.pic_link = data['pic_link']
            player.save()
        else:
            #print(f"adding existing player {data['existing_player']}")
            player = Player.objects.filter(name = data['existing_player']).first()

        event = Event.objects.filter(id =event_id).first()
        if not EventPlayers.objects.filter(event = event, player = player).exists():
            event_player = EventPlayers()
            event_player.player = player
            event_player.event = event
            event_player.save()
        return redirect('manage_event', event_name = event.name, event_id = event.id)
    
    else: return redirect('login')


def delete_player_event(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():

        event = Event.objects.filter(id =request.POST.get('event_id')).first()
        player = Player.objects.filter(id = request.POST.get('player_id')).first()

        EventPlayers.objects.filter(event  =event, player = player).first().delete()
        return redirect('manage_event', event_name = event.name, event_id = request.POST.get('event_id') )
    
    else: return redirect('login')

def add_game_event(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        form = AddGameForm(request.POST)
        game = Game()
        event_id = request.POST.get('event_id')
        if form.is_valid():
            data = form.cleaned_data
        else: return Http404 
        if data["name"] !="": ## uusi
            #print(f" adding game : {data["name"]}")
            game = Game()
            game.name = data["name"]
            game.link = data["link"]
            game.extra_link = data["extra_link"]
            game.extra_text = data["extra_text"]
            game.save()
        else: # vanha
            #(data["existing_game"])
            game = Game.objects.filter(name = data["existing_game"]).first()
        #print(GameInstance.objects.filter(id = event_id))

        event = Event.objects.filter(id =event_id).first()
        GI = GameInstance()
        GI.game = game
        GI.event = event
        #print(GI)
        GI.hiden = False
        GI.save()
        return redirect('manage_event', event_name=event.name, event_id=event_id)
    
    else: return redirect('login')



def hide_gameinstance(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        gi_id = request.POST.get('game_instance_id')
        GI = GameInstance.objects.filter(id = gi_id).first()
        GI.hiden = not GI.hiden
        GI.save()
        return redirect('manage_event', event_name=GI.event.name, event_id=GI.event_id)
    else: return redirect('login')


def delete_gameinstance(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        gi_id = request.POST.get('game_instance_id')
        GI = GameInstance.objects.filter(id = gi_id).first()
        GI.delete()
        return redirect('manage_event', event_name=GI.event.name, event_id=GI.event_id)
    
    else: return redirect('login')

def finish_event(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        event_id =request.POST.get('event_id')
        event = get_object_or_404(Event, id = event_id)
        event.finished =  not event.finished
        event.save()
        return redirect('event', event_name=event.name, event_id=event_id)
    else: return redirect('login')
def update_event(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        event_id =request.POST.get('event_id')
        event_time = request.POST.get('event_time')
        event_name = request.POST.get('name')

        event = get_object_or_404(Event, id = event_id)
        event.event_time =event_time
        event.name = event_name
        event.save()
        return redirect('edit')
    
    else: return redirect('login')


def add_event(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        event = Event()
        event.name = "i'm a blank event edit mee"
        event.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else: return redirect('login')

def update_player(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        player_id = request.POST.get('player_id')
        name = request.POST.get('name')
        pic_link = request.POST.get('pic_link')
        link = request.POST.get('link')
        
        # Get the player object (replace Player with your actual model)
        player = get_object_or_404(Player, id=player_id)
        
        # Update fields
        player.name = name
        player.pic_link = pic_link
        player.link = link
        player.save()
        
        #messages.success(request, 'Player updated successfully!')
        return redirect('edit')

    else: return redirect('login')


def update_game(request):
    if request.method == 'POST' and request.user.groups.filter(name='event_admin').exists():
        game_id = request.POST.get('game_id')
        name = request.POST.get('name')
        link = request.POST.get('link')
        extra_text = request.POST.get('extra_text')
        extra_link = request.POST.get('extra_link')
        
        # Get the game object
        game = get_object_or_404(Game, id=game_id)
        game.name = name
        game.link = link if link else ""  
        game.extra_text = extra_text if extra_text else ""
        game.extra_link = extra_link if extra_link else ""
        game.save()
        
        return redirect('edit') 
    
    else: return redirect('login')
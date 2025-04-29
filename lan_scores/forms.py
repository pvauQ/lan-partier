from django import forms
from .models import Game,Player


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class AddGameForm(forms.Form):
    existing_game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        required=False,
        label="Or select existing game"
    )
    name = forms.CharField(max_length=256, required=False, label="Game Name")
    link = forms.CharField(max_length=1024, required=False, label="Game Link")
    extra_text = forms.CharField(max_length=256, required=False, label="Extra Text")
    extra_link = forms.CharField(max_length=1024, required=False, label="Extra Link")
    
    def clean(self):
        data = super().clean()
        if not data.get('existing_game') and not data.get('name'):
            raise forms.ValidationError("You must either select a game or create a new one!")
        return data


class AddPlayerForm(forms.Form):
    existing_player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        required=False,
        label="Or select existing player"
    )
    name = forms.CharField(max_length=256, required=False, label="Player Name")
    link = forms.CharField(max_length=1024, required=False, label="Player Link")
    pic_link = forms.CharField(max_length=1024, required=False, label="Picture Link")

    def clean(self):
        data = super().clean()
        if not data.get('existing_player') and not data.get('name'):
            raise forms.ValidationError("You must either select a player or create a new one!")
        return data


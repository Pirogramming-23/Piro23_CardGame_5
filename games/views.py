from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Game
from django.contrib.auth import get_user_model
import random
from django.db.models import Q
# Create your views here.

User = get_user_model()

@login_required
def start_game(request): # 시작 (공격하기)
    if request.method == 'POST':
        defender_id = request.POST['defender_id']
        selected_card = int(request.POST['selected_card'])

        defender = get_object_or_404(User, id=defender_id)

        game = Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=selected_card,
            winning_condition=random.choice(['high', 'low'])  # 룰은 랜덤
        )
        return redirect('games:history')

    # 카드 뽑기 + 상대 선택
    cards = random.sample(range(1, 11), 5)
    opponent = User.objects.exclude(id=request.user.id)
    return render(request, 'games/start_game.html', {
        'cards': cards,
        'users': opponent
    })

@login_required
def cancel_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if game.attacker != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
    
    if request.method == "POST" :
        game.delete()
    return redirect('games:history')

@login_required
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.user != game.defender or game.status !='waiting':
        return HttpResponseForbidden("반격 권한이 없습니다.")
    
    if request.method == 'POST': # 카드 뽑기 
        selected_card = int(request.POST['selected_card'])
        game.defender_card = selected_card
        game.status = 'finished'

        if game.attacker.card == selected_card:
            game.result = 'draw'
        elif game.winning_condition == 'high':
            game.result = 'attacker' if game.attacker_card > selected_card else 'defender'
        elif game.winning_condition == 'low':
            game.result = 'attacker' if game.attacker_card < selected_card else 'defender'
        
        game.save()
        return redirect('games:detail', game.id)

    cards = random.sample(range(1, 11), 5)
    return render(request, 'games/counter_attack.html', {'game': game, 'cards': cards})

@login_required
def game_history(request) :
    users = request.user

    games = Game.objects.filter(Q(attacker=users) | Q(defender=users)).order_by('-id')

    wins = 0
    losses = 0
    draws = 0

    for game in games:
        if game.status != 'finished':
            continue

        if game.result == 'draw':
            draws += 1
        elif (game.result == 'attacker' and game.attacker == users) or (game.result == 'defender' and game.defender == users):
            wins += 1
        else:
            losses += 1

    context = {
        'games': games,
        'wins': wins,
        'losses': losses,
        'draws': draws,
    }

    return render(request, 'games/game_history.html', context)

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    context = {
        'game': game,
        'is_attacker': user == game.attacker,
        'is_defender': user == game.defender,
    }

    return render(request, 'games/game_detail.html', context)
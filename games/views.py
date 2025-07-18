from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Game
from django.contrib.auth import get_user_model
import random
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
    opponent = User.objects.filter(is_superuser=False, is_staff=False).exclude(id=request.user.id)
    return render(request, 'games/start_game.html', {
        'cards': cards,
        'users': opponent
    })

@login_required
def cancel_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if game.attacker != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

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

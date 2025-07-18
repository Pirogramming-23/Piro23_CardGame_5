from django.urls import path
from .views import *

app_name = 'games'

urlpatterns = [
    path('start/', start_game, name='start'),  # 게임 생성 (공격하기)
    path('cancel/<int:game_id>/', cancel_game, name='cancel'),  # 내가 건 게임 삭제 #예원님
    path('counter/<int:game_id>/', counter_attack, name='counter'),  # 반격하기
    path('detail/<int:game_id>/', game_detail, name='detail'),  # 게임 결과 상세 #예원님
    path('history/', game_history, name='history'),  # 게임 전적 #예원님
    # path('rank/', rank_view, name='rank'),  # 랭킹 보기 #지원님
]

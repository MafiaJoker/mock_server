# mock_data.py
import random
from datetime import datetime, timedelta

EVENT_STATUSES = {
    "PLANNED": "planned",
    "ACTIVE": "active",
    "COMPLETED": "completed"
}

EVENT_CATEGORIES = {
    "FUNKY": "funky",
    "MINICAP": "minicap",
    "TOURNAMENT": "tournament",
    "CHARITY": "charity_tournament"
}

# Новые статусы игр
GAME_STATUSES = {
    "CREATED": "created",
    "SEATING_READY": "seating_ready",
    "ROLE_DISTRIBUTION": "role_distribution",
    "IN_PROGRESS": "in_progress",
    "FINISHED_NO_SCORES": "finished_no_scores",
    "FINISHED_WITH_SCORES": "finished_with_scores"
}

# Подстатусы для процесса игры
GAME_SUBSTATUS = {
    "DISCUSSION": "discussion",
    "CRITICAL_DISCUSSION": "critical_discussion",
    "VOTING": "voting",
    "SUSPECTS_SPEECH": "suspects_speech",
    "FAREWELL_MINUTE": "farewell_minute",
    "NIGHT": "night"
}

# Функция для генерации статического списка игроков
def generate_players(count, revealed=False):
    roles = ["Мирный", "Мирный", "Мирный", "Мирный", "Мирный", "Мирный", "Мафия", "Мафия", "Дон", "Шериф"]
    players = []
    
    for i in range(1, count + 1):
        role = roles[i-1]
        players.append({
            "id": i,
            "name": f"Игрок {i}",
            "role": role,
            "originalRole": role,
            "fouls": random.randint(0, 2),
            "nominated": None,
            "isAlive": True if not revealed else random.random() > 0.3,
            "isEliminated": False,
            "isSilent": False,
            "silentNextRound": False
        })
        
    return players

def default_players(count, revealed=False):
    roles = ["Мирный"] * 10
    players = []
    
    for i in range(1, count + 1):
        role = roles[i-1]
        players.append({
            "id": i,
            "name": f"Игрок {i}",
            "role": role,
            "originalRole": role,
            "fouls": 0,
            "nominated": None,
            "isAlive": True,
            "isEliminated": False,
            "isSilent": False,
            "silentNextRound": False
        })
        
    return players

# Функция для генерации баллов игроков
def generate_player_scores(players, game_result=None):
    scores = {}
    
    for player in players:
        base_score = 0
        additional_score = 0
        
        if game_result:
            # Определяем базовый балл в зависимости от результата
            is_winner = (
                (game_result == "city_win" and player["originalRole"] in ["Мирный", "Шериф"]) or
                (game_result == "mafia_win" and player["originalRole"] in ["Мафия", "Дон"])
            )
            
            if game_result == "draw":
                base_score = 0.5
            elif is_winner:
                base_score = 1.0
            else:
                base_score = 0.0
            
            # Случайные дополнительные баллы для завершенных игр
            additional_score = round(random.uniform(-1, 2), 1)
        
        scores[player["id"]] = {
            "baseScore": base_score,
            "additionalScore": additional_score
        }
    
    return scores

# Список тестовых ведущих
judges = [
    {"id": 1, "name": "Иван Петров"},
    {"id": 2, "name": "Анна Смирнова"},
    {"id": 3, "name": "Михаил Судейкин"},
    {"id": 4, "name": "Елена Правилова"}
]

# Создаем мероприятия с разными столами и играми
events = [
    {
        "id": 1001,
        "name": "Мафия Club - Еженедельная игра",
        "description": "Еженедельная встреча клуба любителей мафии. Приходите поиграть в классическую версию игры!",
        "date": "2025-05-23",
        "language": "ru",
        "status": EVENT_STATUSES["ACTIVE"],
        "category": EVENT_CATEGORIES["FUNKY"],
        "tables": [
            {
                "id": 2001,
                "name": "Стол 1",
                "capacity": 10,
                "seatingType": "free",
                "judge": "Иван Петров",
                "games": [
                    {
                        "id": 3001,
                        "name": "Игра #1",
                        "created": "2025-05-23T18:00:00",
                        "status": "not_started",
                        "currentRound": 0,
                        "result": None,
                        # Новые поля
                        "gameStatus": GAME_STATUSES["CREATED"],
                        "gameSubstatus": None,
                        "isCriticalRound": False
                    },
                    {
                        "id": 3002,
                        "name": "Игра #2",
                        "created": "2025-05-23T19:30:00",
                        "status": "in_progress",
                        "currentRound": 3,
                        "result": None,
                        # Новые поля
                        "gameStatus": GAME_STATUSES["IN_PROGRESS"],
                        "gameSubstatus": GAME_SUBSTATUS["DISCUSSION"],
                        "isCriticalRound": False
                    },
                    {
                        "id": 3003,
                        "name": "Финальная игра",
                        "created": "2025-05-23T21:00:00",
                        "status": "finished",
                        "currentRound": 7,
                        "result": "city_win",
                        # Новые поля
                        "gameStatus": GAME_STATUSES["FINISHED_WITH_SCORES"],
                        "gameSubstatus": None,
                        "isCriticalRound": False
                    },
                    {
                        "id": 3005,
                        "name": "Тестовая игра (рассадка готова)",
                        "created": "2025-05-23T17:00:00",
                        "status": "not_started",
                        "currentRound": 0,
                        "result": None,
                        # Новые поля - статус SEATING_READY для отладки
                        "gameStatus": GAME_STATUSES["SEATING_READY"],
                        "gameSubstatus": None,
                        "isCriticalRound": False
                    }
                ]
            },
            {
                "id": 2002,
                "name": "Стол 2",
                "capacity": 10,
                "seatingType": "fixed",
                "judge": "Анна Смирнова",
                "games": [
                    {
                        "id": 3004,
                        "name": "Тренировочная игра",
                        "created": "2025-05-23T18:30:00",
                        "status": "finished",
                        "currentRound": 5,
                        "result": "mafia_win",
                        # Новые поля
                        "gameStatus": GAME_STATUSES["FINISHED_NO_SCORES"],
                        "gameSubstatus": None,
                        "isCriticalRound": False
                    }
                ]
            }
        ]
    },
    {
        "id": 1002,
        "name": "Турнир по мафии",
        "description": "Официальный городской турнир по спортивной мафии. Призовой фонд 50 000 руб.",
        "date": "2025-06-15",
        "language": "ru",
        "status": EVENT_STATUSES["PLANNED"],
        "category": EVENT_CATEGORIES["TOURNAMENT"],
        "tables": [
            {
                "id": 2003,
                "name": "Турнирный стол A",
                "capacity": 10,
                "seatingType": "fixed",
                "judge": "Михаил Судейкин",
                "games": []
            }
        ]
    },
    {
        "id": 1003,
        "name": "Mafia International",
        "description": "International mafia game event with players from different countries",
        "date": "2025-07-10",
        "language": "en",
        "status": EVENT_STATUSES["PLANNED"],
        "category": EVENT_CATEGORIES["MINICAP"],
        "tables": []
    },
    {
        "id": 1004,
        "name": "Մաֆիա Երևանում",
        "description": "Մաֆիա խաղի միջոցառում Երևանում",
        "date": "2025-06-01",
        "language": "am",
        "status": EVENT_STATUSES["COMPLETED"],
        "category": EVENT_CATEGORIES["CHARITY"],
        "tables": []
    }
]

# Обновленные состояния игр - убираем поле phase полностью
game_states = [
    {
        "gameId": 3005,  # Тестовая игра в статусе SEATING_READY
        "round": 0,
        "isGameStarted": False,
        # Новые поля - статус SEATING_READY для отладки
        "gameStatus": GAME_STATUSES["SEATING_READY"],
        "gameSubstatus": None,
        "isCriticalRound": False,
        "scores": {str(i): {"baseScore": 0, "additionalScore": 0} for i in range(1, 11)},
        
        "players": default_players(10),
        "nominatedPlayers": [],
        "votingResults": {},
        "shootoutPlayers": [],
        "deadPlayers": [],
        "eliminatedPlayers": [],
        "nightKill": None,
        "bestMoveUsed": False,
        "noCandidatesRounds": 0,
        "mafiaTarget": None,
        "donTarget": None,
        "sheriffTarget": None,
        "rolesVisible": False
    },
    {
        "gameId": 3002,  # Игра #2 со статусом "in_progress"
        "round": 3,
        "isGameStarted": True,
        # Новые поля
        "gameStatus": GAME_STATUSES["IN_PROGRESS"],
        "gameSubstatus": GAME_SUBSTATUS["DISCUSSION"],
        "isCriticalRound": False,
        "scores": {str(i): {"baseScore": 0, "additionalScore": 0} for i in range(1, 11)},
        
        "players": generate_players(10),
        "nominatedPlayers": [3, 7],
        "votingResults": {},
        "shootoutPlayers": [],
        "deadPlayers": [5],
        "eliminatedPlayers": [],
        "nightKill": 5,
        "bestMoveUsed": True,
        "noCandidatesRounds": 0,
        "mafiaTarget": None,
        "donTarget": None,
        "sheriffTarget": None,
        "rolesVisible": True
    },
    {
        "gameId": 3003,  # Финальная игра со статусом "finished"
        "round": 7,
        "isGameStarted": False,
        # Новые поля
        "gameStatus": GAME_STATUSES["FINISHED_WITH_SCORES"],
        "gameSubstatus": None,
        "isCriticalRound": False,
        
        "players": generate_players(10, True),
        "nominatedPlayers": [],
        "votingResults": {},
        "shootoutPlayers": [],
        "deadPlayers": [2, 5, 9],
        "eliminatedPlayers": [4, 8],
        "nightKill": None,
        "bestMoveUsed": True,
        "noCandidatesRounds": 0,
        "mafiaTarget": None,
        "donTarget": None,
        "sheriffTarget": None,
        "rolesVisible": True
    },
    {
        "gameId": 3004,  # Игра без баллов
        "round": 5,
        "isGameStarted": False,
        # Новые поля
        "gameStatus": GAME_STATUSES["FINISHED_NO_SCORES"],
        "gameSubstatus": None,
        "isCriticalRound": False,
        "scores": {str(i): {"baseScore": 0, "additionalScore": 0} for i in range(1, 11)},
        
        "players": generate_players(10, True),
        "nominatedPlayers": [],
        "votingResults": {},
        "shootoutPlayers": [],
        "deadPlayers": [1, 3, 6, 8],
        "eliminatedPlayers": [2, 7],
        "nightKill": None,
        "bestMoveUsed": True,
        "noCandidatesRounds": 0,
        "mafiaTarget": None,
        "donTarget": None,
        "sheriffTarget": None,
        "rolesVisible": True
    }
]

# Генерируем баллы для завершенной игры
finished_game_players = game_states[2]["players"]  # Игра 3003
game_states[2]["scores"] = generate_player_scores(finished_game_players, "city_win")

# Дефолтное состояние игры - убираем phase полностью
default_game_state = {
    "round": 0,
    "isGameStarted": False,
    # Новые поля - устанавливаем статус SEATING_READY для отладки
    "gameStatus": GAME_STATUSES["SEATING_READY"],
    "gameSubstatus": None,
    "isCriticalRound": False,
    "scores": {str(i): {"baseScore": 0, "additionalScore": 0} for i in range(1, 11)},
    
    "players": default_players(10),
    "nominatedPlayers": [],
    "votingResults": {},
    "shootoutPlayers": [],
    "deadPlayers": [],
    "eliminatedPlayers": [],
    "nightKill": None,
    "bestMoveUsed": False,
    "noCandidatesRounds": 0,
    "mafiaTarget": None,
    "donTarget": None,
    "sheriffTarget": None,
    "rolesVisible": False
}

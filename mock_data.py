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
            "fouls": random.randint(0, 2),  # Случайное количество фолов от 0 до 2
            "nominated": None,
            "isAlive": True if not revealed else random.random() > 0.3,  # Для завершенных игр некоторые игроки могут быть "мертвыми"
            "isEliminated": False,
            "isSilent": False,
            "silentNextRound": False
        })
        
    return players

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
            # существующие таблицы...
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
            # существующие таблицы...
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
        "tables": [
            # существующие таблицы...
        ]
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

# Состояния игр
game_states = [
    {
        "gameId": 3002,  # Игра #2 со статусом "in_progress"
        "round": 3,
        "phase": "day",
        "isGameStarted": True,
        "players": generate_players(10),  # Генерируем 10 игроков
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
        "phase": "end",
        "isGameStarted": False,
        "players": generate_players(10, True),  # Генерируем игроков с раскрытыми ролями
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
    }
]

# Дефолтное состояние игры (используется для новых игр)
default_game_state = {
    "round": 0,
    "phase": "distribution",
    "isGameStarted": False,
    "players": generate_players(10),
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

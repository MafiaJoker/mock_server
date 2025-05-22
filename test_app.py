# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app
import mock_data
from copy import deepcopy

# Создаем тестовый клиент
client = TestClient(app)

# Фикстура для сброса данных перед каждым тестом
@pytest.fixture(autouse=True)
def reset_data():
    # Сохраняем оригинальные данные
    original_events = deepcopy(mock_data.events)
    original_game_states = deepcopy(mock_data.game_states)
    
    yield
    
    # Восстанавливаем оригинальные данные после теста
    mock_data.events = original_events
    mock_data.game_states = original_game_states

# Тесты для корневого маршрута
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# Тесты для мероприятий (Events)
def test_get_events():
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()) == len(mock_data.events)

def test_get_event():
    event_id = mock_data.events[0]["id"]
    response = client.get(f"/api/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == event_id

def test_get_event_not_found():
    response = client.get("/api/events/9999")
    assert response.status_code == 404

def test_create_event():
    new_event = {
        "name": "Тестовое мероприятие",
        "description": "Описание для тестов",
        "date": "2025-08-01",
        "language": "ru"
    }
    response = client.post("/api/events", json=new_event)
    assert response.status_code == 201
    assert response.json()["name"] == new_event["name"]
    assert "id" in response.json()
    assert "tables" in response.json()

def test_update_event():
    event_id = mock_data.events[0]["id"]
    updated_data = {
        "name": "Обновленное название",
        "description": "Обновленное описание"
    }
    response = client.put(f"/api/events/{event_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["description"] == updated_data["description"]
    assert response.json()["id"] == event_id

# Тесты для столов (Tables)
def test_get_tables():
    event_id = mock_data.events[0]["id"]
    response = client.get(f"/api/events/{event_id}/tables")
    assert response.status_code == 200
    assert len(response.json()) == len(mock_data.events[0]["tables"])

def test_get_table():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    response = client.get(f"/api/events/{event_id}/tables/{table_id}")
    assert response.status_code == 200
    assert response.json()["id"] == table_id

def test_get_table_not_found():
    event_id = mock_data.events[0]["id"]
    response = client.get(f"/api/events/{event_id}/tables/9999")
    assert response.status_code == 404

def test_create_table():
    event_id = mock_data.events[0]["id"]
    new_table = {
        "name": "Тестовый стол",
        "capacity": 10,
        "seatingType": "free",
        "judge": "Тестовый судья"
    }
    response = client.post(f"/api/events/{event_id}/tables", json=new_table)
    assert response.status_code == 201
    assert response.json()["name"] == new_table["name"]
    assert "id" in response.json()
    assert "games" in response.json()

def test_update_table():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    updated_data = {
        "name": "Обновленный стол",
        "judge": "Новый судья"
    }
    response = client.put(f"/api/events/{event_id}/tables/{table_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["judge"] == updated_data["judge"]
    assert response.json()["id"] == table_id

# Тесты для игр (Games)
def test_get_games():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    response = client.get(f"/api/events/{event_id}/tables/{table_id}/games")
    assert response.status_code == 200
    assert len(response.json()) == len(mock_data.events[0]["tables"][0]["games"])

def test_get_game():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    game_id = mock_data.events[0]["tables"][0]["games"][0]["id"]
    response = client.get(f"/api/events/{event_id}/tables/{table_id}/games/{game_id}")
    assert response.status_code == 200
    assert response.json()["id"] == game_id

def test_get_game_not_found():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    response = client.get(f"/api/events/{event_id}/tables/{table_id}/games/9999")
    assert response.status_code == 404

def test_create_game():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    new_game = {
        "name": "Тестовая игра"
    }
    response = client.post(f"/api/events/{event_id}/tables/{table_id}/games", json=new_game)
    assert response.status_code == 201
    assert response.json()["name"] == new_game["name"]
    assert "id" in response.json()
    assert "status" in response.json()
    assert response.json()["status"] == "not_started"

def test_update_game():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    game_id = mock_data.events[0]["tables"][0]["games"][0]["id"]
    updated_data = {
        "name": "Обновленная игра",
        "status": "in_progress",
        "currentRound": 2
    }
    response = client.put(f"/api/events/{event_id}/tables/{table_id}/games/{game_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["status"] == updated_data["status"]
    assert response.json()["currentRound"] == updated_data["currentRound"]
    assert response.json()["id"] == game_id

# Тесты для состояний игр (Game States)
def test_get_game_state():
    game_id = mock_data.game_states[0]["gameId"]
    response = client.get(f"/api/games/{game_id}/state")
    assert response.status_code == 200
    assert response.json()["gameId"] == game_id
    assert "round" in response.json()
    assert "players" in response.json()

def test_get_game_state_default():
    # Запрашиваем состояние для несуществующей игры - должен вернуться дефолтный стейт
    response = client.get("/api/games/9999/state")
    assert response.status_code == 200
    assert "round" in response.json()
    assert "players" in response.json()
    assert response.json()["round"] == mock_data.default_game_state["round"]

def test_update_game_state():
    game_id = mock_data.game_states[0]["gameId"]
    updated_data = {
        "round": 5,
        "phase": "night",
        "deadPlayers": [1, 3]
    }
    response = client.put(f"/api/games/{game_id}/state", json=updated_data)
    assert response.status_code == 200
    assert response.json()["round"] == updated_data["round"]
    assert response.json()["phase"] == updated_data["phase"]
    assert response.json()["deadPlayers"] == updated_data["deadPlayers"]
    assert response.json()["gameId"] == game_id

def test_create_new_game_state():
    # Создание состояния для новой игры
    new_game_id = 9999
    new_state = {
        "round": 1,
        "phase": "day",
        "isGameStarted": True,
        "players": mock_data.generate_players(10)
    }
    response = client.put(f"/api/games/{new_game_id}/state", json=new_state)
    assert response.status_code == 200
    assert response.json()["round"] == new_state["round"]
    assert response.json()["phase"] == new_state["phase"]
    assert response.json()["gameId"] == new_game_id

# Тесты на обработку ошибок
def test_event_not_found_for_tables():
    response = client.get("/api/events/9999/tables")
    assert response.status_code == 404

def test_event_not_found_for_creating_table():
    new_table = {
        "name": "Стол, который не будет создан",
        "capacity": 10,
        "seatingType": "free"
    }
    response = client.post("/api/events/9999/tables", json=new_table)
    assert response.status_code == 404

def test_validation_game_result():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    game_id = mock_data.events[0]["tables"][0]["games"][0]["id"]
    
    # Проверяем, что можно установить корректный результат игры
    valid_results = ["city_win", "mafia_win", "draw", None]
    
    for result in valid_results:
        updated_data = {
            "result": result,
            "status": "finished" if result else "in_progress"
        }
        response = client.put(f"/api/events/{event_id}/tables/{table_id}/games/{game_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["result"] == result

# test_app.py (добавляем новые тесты)

def test_update_game_with_new_status():
    event_id = mock_data.events[0]["id"]
    table_id = mock_data.events[0]["tables"][0]["id"]
    game_id = mock_data.events[0]["tables"][0]["games"][0]["id"]
    
    updated_data = {
        "gameStatus": "in_progress",
        "gameSubstatus": "discussion",
        "isCriticalRound": False,
        "currentRound": 2
    }
    
    response = client.put(f"/api/events/{event_id}/tables/{table_id}/games/{game_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["gameStatus"] == "in_progress"
    assert response.json()["gameSubstatus"] == "discussion"
    assert response.json()["isCriticalRound"] == False

def test_get_game_scores():
    game_id = mock_data.game_states[0]["gameId"]
    response = client.get(f"/api/games/{game_id}/scores")
    assert response.status_code == 200
    assert "scores" in response.json() or isinstance(response.json(), dict)

def test_update_game_scores():
    game_id = mock_data.game_states[0]["gameId"]
    new_scores = {
        "1": {"baseScore": 1.0, "additionalScore": 0.5},
        "2": {"baseScore": 0.0, "additionalScore": -0.5}
    }
    
    response = client.put(f"/api/games/{game_id}/scores", json=new_scores)
    assert response.status_code == 200
    assert "scores" in response.json()

def test_get_game_statistics():
    game_id = mock_data.game_states[0]["gameId"]
    response = client.get(f"/api/games/{game_id}/statistics")
    assert response.status_code == 200
    
    stats = response.json()
    assert "gameId" in stats
    assert "round" in stats
    assert "gameStatus" in stats
    assert "roleStatistics" in stats
    assert "playersAlive" in stats

def test_game_state_with_new_fields():
    game_id = 9999
    new_state = {
        "round": 1,
        "phase": "day",
        "gameStatus": "in_progress",
        "gameSubstatus": "discussion",
        "isCriticalRound": False,
        "scores": {
            "1": {"baseScore": 0, "additionalScore": 0},
            "2": {"baseScore": 0, "additionalScore": 0}
        },
        "isGameStarted": True,
        "players": mock_data.generate_players(10)
    }
    
    response = client.put(f"/api/games/{game_id}/state", json=new_state)
    assert response.status_code == 200
    assert response.json()["gameStatus"] == "in_progress"
    assert response.json()["gameSubstatus"] == "discussion"
    assert "scores" in response.json()

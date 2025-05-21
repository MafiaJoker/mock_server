# test_mock_data.py
import pytest
import mock_data

def test_generate_players():
    # Проверка, что функция генерирует правильное количество игроков
    players = mock_data.generate_players(10)
    assert len(players) == 10
    
    # Проверка наличия всех ролей
    roles = [p["role"] for p in players]
    assert roles.count("Мирный") == 6
    assert roles.count("Мафия") == 2
    assert roles.count("Дон") == 1
    assert roles.count("Шериф") == 1
    
    # Проверка, что originalRole совпадает с role
    for player in players:
        assert player["role"] == player["originalRole"]

def test_generate_players_with_revealed():
    # Проверка, что с параметром revealed=True некоторые игроки могут быть "убиты"
    players = mock_data.generate_players(10, revealed=True)
    assert len(players) == 10
    
    # Проверяем, что есть хотя бы один живой игрок и один мертвый
    alive_count = sum(1 for p in players if p["isAlive"])
    assert 0 < alive_count < 10  # По крайней мере один, но не все

def test_default_game_state():
    # Проверка дефолтного состояния игры
    assert mock_data.default_game_state["round"] == 0
    assert mock_data.default_game_state["phase"] == "distribution"
    assert mock_data.default_game_state["isGameStarted"] == False
    assert len(mock_data.default_game_state["players"]) == 10
    assert mock_data.default_game_state["deadPlayers"] == []
    assert mock_data.default_game_state["eliminatedPlayers"] == []

def test_events_structure():
    # Проверка структуры тестовых мероприятий
    assert len(mock_data.events) > 0
    
    for event in mock_data.events:
        assert "id" in event
        assert "name" in event
        assert "description" in event
        assert "date" in event
        assert "language" in event
        assert "tables" in event
        
        # Проверка, что язык соответствует разрешенным
        assert event["language"] in ["ru", "en", "am"]
        
        # Проверка структуры столов
        for table in event["tables"]:
            assert "id" in table
            assert "name" in table
            assert "capacity" in table
            assert "seatingType" in table
            assert "games" in table
            
            # Проверка, что тип рассадки соответствует разрешенным
            assert table["seatingType"] in ["free", "fixed"]
            
            # Проверка структуры игр
            for game in table["games"]:
                assert "id" in game
                assert "name" in game
                assert "created" in game
                assert "status" in game
                assert "currentRound" in game
                
                # Проверка, что статус соответствует разрешенным
                assert game["status"] in ["not_started", "in_progress", "finished"]

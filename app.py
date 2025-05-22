# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uvicorn
import json
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import mock_data

app = FastAPI(title="Mafia Game Helper API", description="Заглушка API для приложения Mafia Game Helper")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загружаем тестовые данные
events = mock_data.events
game_states = mock_data.game_states
judges = mock_data.judges

# Добавим классы для перечислений
class EventStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"

class EventCategory(str, Enum):
    FUNKY = "funky"
    MINICAP = "minicap"
    TOURNAMENT = "tournament"
    CHARITY = "charity_tournament"
    
@app.get("/")
def read_root():
    return {"message": "Mafia Game Helper API - Заглушка работает!"}

# Получить все мероприятия
@app.get("/api/events")
def get_events():
    return events

# Получить мероприятие по ID
@app.get("/api/events/{event_id}")
def get_event(event_id: int):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    return event

# Создать новое мероприятие
@app.post("/api/events", status_code=201)
def create_event(event_data: Dict[str, Any]):
    # Проверка категории и статуса, если они предоставлены
    if "category" in event_data and event_data["category"] not in [cat.value for cat in EventCategory]:
        raise HTTPException(status_code=400, detail=f"Неверная категория. Допустимые значения: {[cat.value for cat in EventCategory]}")
    
    if "status" in event_data and event_data["status"] not in [status.value for status in EventStatus]:
        raise HTTPException(status_code=400, detail=f"Неверный статус. Допустимые значения: {[status.value for status in EventStatus]}")
    
    # Если статус не указан, устанавливаем его как "created"
    if "status" not in event_data:
        event_data["status"] = EventStatus.CREATED.value
        
    # Если категория не указана, устанавливаем её как "funky" по умолчанию
    if "category" not in event_data:
        event_data["category"] = EventCategory.FUNKY.value
        
    new_event = {
        "id": int(datetime.now().timestamp() * 1000),
        **event_data,
        "tables": []
    }
    events.append(new_event)
    return new_event

# Обновить мероприятие
@app.put("/api/events/{event_id}")
def update_event(event_id: int, event_data: Dict[str, Any]):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    # Обновляем данные, сохраняя ID и таблицы
    events[event_index].update({
        **event_data,
        "id": event_id
    })
    
    # Если таблицы не были переданы, сохраняем существующие
    if "tables" not in event_data:
        events[event_index]["tables"] = events[event_index].get("tables", [])
        
    return events[event_index]

# Получить столы для мероприятия
@app.get("/api/events/{event_id}/tables")
def get_tables(event_id: int):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    return event.get("tables", [])

# Получить стол по ID
@app.get("/api/events/{event_id}/tables/{table_id}")
def get_table(event_id: int, table_id: int):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    table = next((t for t in event.get("tables", []) if t["id"] == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    return table

# Создать новый стол
@app.post("/api/events/{event_id}/tables", status_code=201)
def create_table(event_id: int, table_data: Dict[str, Any]):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    # Проверка статуса мероприятия
    if events[event_index]["status"] == EventStatus.COMPLETED.value:
        raise HTTPException(status_code=403, detail="Невозможно добавить стол к завершенному мероприятию")
    
    new_table = {
        "id": int(datetime.now().timestamp() * 1000),
        **table_data,
        "games": []
    }
    
    if "tables" not in events[event_index]:
        events[event_index]["tables"] = []
        
    events[event_index]["tables"].append(new_table)
    return new_table

# Обновить стол
@app.put("/api/events/{event_id}/tables/{table_id}")
def update_table(event_id: int, table_id: int, table_data: Dict[str, Any]):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    table_index = next((i for i, t in enumerate(events[event_index].get("tables", [])) 
                        if t["id"] == table_id), -1)
    if table_index == -1:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    # Обновляем данные, сохраняя ID и игры
    events[event_index]["tables"][table_index].update({
        **table_data,
        "id": table_id
    })
    
    # Если игры не были переданы, сохраняем существующие
    if "games" not in table_data:
        games = events[event_index]["tables"][table_index].get("games", [])
        events[event_index]["tables"][table_index]["games"] = games
        
    return events[event_index]["tables"][table_index]

# Получить игры для стола
@app.get("/api/events/{event_id}/tables/{table_id}/games")
def get_games(event_id: int, table_id: int):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    table = next((t for t in event.get("tables", []) if t["id"] == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    return table.get("games", [])

# Получить игру по ID
@app.get("/api/events/{event_id}/tables/{table_id}/games/{game_id}")
def get_game(event_id: int, table_id: int, game_id: int):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    table = next((t for t in event.get("tables", []) if t["id"] == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    game = next((g for g in table.get("games", []) if g["id"] == game_id), None)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    return game

# Создать новую игру
@app.post("/api/events/{event_id}/tables/{table_id}/games", status_code=201)
def create_game(event_id: int, table_id: int, game_data: Dict[str, Any]):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")

    # Проверка статуса мероприятия
    if events[event_index]["status"] == EventStatus.COMPLETED.value:
        raise HTTPException(status_code=403, detail="Невозможно добавить игру к завершенному мероприятию")
    
    table_index = next((i for i, t in enumerate(events[event_index].get("tables", [])) 
                        if t["id"] == table_id), -1)
    if table_index == -1:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    new_game = {
        "id": int(datetime.now().timestamp() * 1000),
        "created": datetime.now().isoformat(),
        "status": "not_started",
        "currentRound": 0,
        "result": None,
        **game_data
    }
    
    if "games" not in events[event_index]["tables"][table_index]:
        events[event_index]["tables"][table_index]["games"] = []
        
    events[event_index]["tables"][table_index]["games"].append(new_game)
    return new_game

# Обновить игру
@app.put("/api/events/{event_id}/tables/{table_id}/games/{game_id}")
def update_game(event_id: int, table_id: int, game_id: int, game_data: Dict[str, Any]):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    table_index = next((i for i, t in enumerate(events[event_index].get("tables", [])) 
                        if t["id"] == table_id), -1)
    if table_index == -1:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    game_index = next((i for i, g in enumerate(events[event_index]["tables"][table_index].get("games", [])) 
                        if g["id"] == game_id), -1)
    if game_index == -1:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    # Обновляем данные, сохраняя ID
    events[event_index]["tables"][table_index]["games"][game_index].update({
        **game_data,
        "id": game_id
    })
    
    return events[event_index]["tables"][table_index]["games"][game_index]

# Получить состояние игры
@app.get("/api/games/{game_id}/state")
def get_game_state(game_id: int):
    game_state = next((gs for gs in game_states if gs["gameId"] == game_id), None)
    if not game_state:
        # Если состояние игры не найдено, возвращаем начальное состояние
        return mock_data.default_game_state
    return game_state

# Обновить состояние игры
@app.put("/api/games/{game_id}/state")
def update_game_state(game_id: int, state_data: Dict[str, Any]):
    print(f"=== ОБНОВЛЕНИЕ СОСТОЯНИЯ ИГРЫ {game_id} ===")
    print(f"Входящие данные: {state_data}")
    
    game_state_index = next((i for i, gs in enumerate(game_states) if gs["gameId"] == game_id), -1)
    
    if game_state_index == -1:
        # Если состояние игры не найдено, создаем новое
        print(f"Создание нового состояния для игры {game_id}")
        new_game_state = {
            "gameId": game_id,
            **state_data
        }
        game_states.append(new_game_state)
        game_state = new_game_state
    else:
        # Обновляем существующее состояние
        print(f"Обновление существующего состояния для игры {game_id}")
        game_states[game_state_index].update({
            **state_data,
            "gameId": game_id
        })
        game_state = game_states[game_state_index]
        
    # ВАЖНО: Синхронизируем статус игры в основной структуре событий
    if "isGameStarted" in state_data:
        print(f"Синхронизация статуса игры. isGameStarted: {state_data['isGameStarted']}")
        
        # Ищем игру в структуре событий
        game_found = False
        for event in events:
            for table in event.get("tables", []):
                for game in table.get("games", []):
                    if game["id"] == game_id:
                        print(f"Найдена игра в событии {event['id']}, столе {table['id']}")
                        old_status = game.get("status", "not_started")
                        
                        # Обновляем статус игры
                        if state_data["isGameStarted"]:
                            game["status"] = "in_progress"
                            if "round" in state_data:
                                game["currentRound"] = state_data["round"]
                                
                        print(f"Статус игры изменен с '{old_status}' на '{game['status']}'")
                        game_found = True
                        break
                if game_found:
                    break
            if game_found:
                break
            
        if not game_found:
            print(f"ВНИМАНИЕ: Игра с ID {game_id} не найдена в структуре событий!")
            
    print(f"Итоговое состояние игры: {game_state}")
    return game_state

# Удалить мероприятие
@app.delete("/api/events/{event_id}")
def delete_event(event_id: int):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    # Удаляем мероприятие из списка
    deleted_event = events.pop(event_index)
    
    return {"detail": "Мероприятие успешно удалено", "deleted": deleted_event["id"]}

@app.delete("/api/events/{event_id}/tables/{table_id}")
def delete_table(event_id: int, table_id: int):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    tables = events[event_index].get("tables", [])
    table_index = next((i for i, t in enumerate(tables) if t["id"] == table_id), -1)
    if table_index == -1:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    # Удаляем стол
    deleted_table = tables.pop(table_index)
    
    return {"detail": "Стол успешно удален", "deleted": deleted_table["id"]}

# Получить список ведущих
@app.get("/api/judges")
def get_judges():
    return judges

# Получить ведущего по ID
@app.get("/api/judges/{judge_id}")
def get_judge(judge_id: int):
    judge = next((j for j in judges if j["id"] == judge_id), None)
    if not judge:
        raise HTTPException(status_code=404, detail="Ведущий не найден")
    return judge

@app.delete("/api/events/{event_id}/tables/{table_id}/games/{game_id}")
def delete_game(event_id: int, table_id: int, game_id: int):
    event_index = next((i for i, e in enumerate(events) if e["id"] == event_id), -1)
    if event_index == -1:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    
    table_index = next((i for i, t in enumerate(events[event_index].get("tables", [])) 
                       if t["id"] == table_id), -1)
    if table_index == -1:
        raise HTTPException(status_code=404, detail="Стол не найден")
    
    games = events[event_index]["tables"][table_index].get("games", [])
    game_index = next((i for i, g in enumerate(games) if g["id"] == game_id), -1)
    if game_index == -1:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    # Удаляем игру
    deleted_game = games.pop(game_index)
    
    return {"detail": "Игра успешно удалена", "deleted": deleted_game["id"]}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)

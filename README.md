# Mafia Game Helper API

## Описание

Это заглушка API для приложения Mafia Game Helper, реализованная с использованием FastAPI. Сервер предоставляет REST API для работы с мероприятиями, столами, играми и их состояниями, заменяя localStorage на серверное хранилище.

Заглушка содержит предварительно заполненные данные и предоставляет полную функциональность CRUD для всех сущностей приложения.

## Требования

- Python 3.8+
- Зависимости из файла requirements.txt:
  - fastapi==0.104.1
  - pydantic==2.4.2
  - uvicorn==0.23.2

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <url-вашего-репозитория>
cd mafia-game-api
```

2. Создайте и активируйте виртуальное окружение (опционально, но рекомендуется):
```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите сервер:
```bash
python app.py
```

Сервер будет доступен по адресу: `http://localhost:3000`

## Структура проекта

```
mafia-game-api/
├── app.py              # Основной файл приложения с API эндпоинтами
├── mock_data.py        # Файл с тестовыми данными
├── requirements.txt    # Зависимости проекта
├── adapter.js          # JavaScript адаптер для клиентской части
└── README.md           # Документация проекта
```

## API эндпоинты

### Мероприятия (Events)

- **GET /api/events** - Получить список всех мероприятий
- **GET /api/events/{event_id}** - Получить мероприятие по ID
- **POST /api/events** - Создать новое мероприятие
- **PUT /api/events/{event_id}** - Обновить существующее мероприятие

### Столы (Tables)

- **GET /api/events/{event_id}/tables** - Получить все столы мероприятия
- **GET /api/events/{event_id}/tables/{table_id}** - Получить стол по ID
- **POST /api/events/{event_id}/tables** - Создать новый стол
- **PUT /api/events/{event_id}/tables/{table_id}** - Обновить существующий стол

### Игры (Games)

- **GET /api/events/{event_id}/tables/{table_id}/games** - Получить все игры стола
- **GET /api/events/{event_id}/tables/{table_id}/games/{game_id}** - Получить игру по ID
- **POST /api/events/{event_id}/tables/{table_id}/games** - Создать новую игру
- **PUT /api/events/{event_id}/tables/{table_id}/games/{game_id}** - Обновить существующую игру

### Состояния игр (Game States)

- **GET /api/games/{game_id}/state** - Получить состояние игры
- **PUT /api/games/{game_id}/state** - Обновить состояние игры

## Документация API

FastAPI автоматически генерирует интерактивную документацию API:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

## Интеграция с клиентом

Для взаимодействия с API из JavaScript-приложения используйте файл `adapter.js`. Он предоставляет класс `ApiAdapter` с методами для всех операций API.

### Пример использования адаптера:

```javascript
import apiAdapter from './adapter.js';

// Загрузить все мероприятия
async function loadEvents() {
  const events = await apiAdapter.loadEvents();
  console.log('Загружено мероприятий:', events.length);
  return events;
}

// Создать новое мероприятие
async function createEvent(eventData) {
  const newEvent = await apiAdapter.saveEvent(eventData);
  console.log('Создано новое мероприятие:', newEvent.name);
  return newEvent;
}
```

## Модификация моделей клиента

Для использования API вместо localStorage необходимо модифицировать модели `event-model.js` и `game-model.js` в клиентском приложении:

1. Добавьте файл `adapter.js` в корень проекта.
2. Обновите модель `event-model.js`:
   - Импортируйте адаптер: `import apiAdapter from '../adapter.js';`
   - Измените методы для использования адаптера вместо localStorage.

3. Обновите модель `game-model.js`:
   - Добавьте методы для загрузки и сохранения состояния игры через адаптер.

## Отладка и тестирование

1. **Мониторинг запросов**:
   - Все запросы логируются в консоли сервера
   - Используйте инструменты разработчика в браузере (Network tab)

2. **Тестирование API**:
   - Используйте Swagger UI (http://localhost:3000/docs) для интерактивного тестирования эндпоинтов
   - Или используйте инструменты вроде Postman, curl, или httpie

## Предзаполненные данные

API содержит предзаполненные тестовые данные:
- 4 мероприятия с разными языками
- Несколько столов с разными настройками
- Игры в разных состояниях (не начата, в процессе, завершена)

## Расширение функциональности

При необходимости вы можете:

1. Добавить более сложную логику обработки в эндпоинты
2. Расширить модель данных в `mock_data.py`
3. Добавить новые эндпоинты в `app.py`
4. Реализовать персистентность данных (сохранение в файл или базу данных)

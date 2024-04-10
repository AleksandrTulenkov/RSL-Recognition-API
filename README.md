# API для модели распознавания русского жестового языка
Это интерфейс-обёртка для открытой модели распознавания русского жестового языка 
[Easy_sign](https://github.com/ai-forever/easy_sign). С помощью данного проекта
вы сможете использовать её в своих проектах, отправляя запросы через WebSocket.

Модель распознает ~1600 жестов русского языка жестов и может обработать 3-3.5 жестов в секунду на процессоре 
Intel(R) Core(TM) i5-6600 с частотой 3,30 ГГц. Список распознаваемых жестов доступен в файле RSL_class_list.txt.

## Интерфейс модели
1. API принимает изображения 224x224px (Если соотношение сторон не равно 1 к 1 - дозаполнить `#727272` цветом) на 
эндпоинте **"data"**
2. Когда модель распознает жесты, сработает ивент **"send_not_normalize_text"** со строкой, в которой будет содержаться
объект вида `{"0": "*Первый предикт*", "1": "*Второй предикт*", "2": "*Третий предикт*"}` - слова в порядке убывания 
их возможности

[Пример использования интерфейса](https://github.com/CatDevelop/Teaching-RSL-Stand/blob/pin-code/frontend/src/features/training/components/RecognitionBlock/RecognitionBlock.tsx)

## Инструкция запуска
```bash
pip install -r requirements.txt
python SLT_API.py
```
Поднимется сервер по адресу `localhost:5000`, к которому и необходимо подключаться по WebSocket.

## Deploy
Конфигурация .service файла для развертывания на сервере
```
/etc/systemd/system/rsl-api.service

[Unit]
Description=rsl-api
After=multi-user.target

[Service]
User=akhidov
Type=simple
Restart=always
WorkingDirectory=/home/akhidov/RSL-Recognition-API
ExecStart=python3 /home/akhidov/RSL-Recognition-API/SLT_API.py

[Install]
WantedBy=multi-user.target
```

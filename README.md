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

## Фильтр для жестов в API
Можно использовать фильтр для отправки из API только нужных жестов.
Структура и пример файла для фильтра лежит в `list_filter.txt`. 

Из модели в python скрипт сервера будут возвращаться все жесты, но API будет отправлять по сокетам только те жесты, которые есть в файле.

## Инструкция ручного запуска
```bash
pip install -r requirements.txt
python SLT_API.py
```
Поднимется сервер по адресу `localhost:5000`, к которому и необходимо подключаться по WebSocket.

Либо так, для запуска API c фильтром:
```bash
pip install -r requirements.txt
python SLT_API_filter.py
```

## Как запустить с помощью docker
**Без фильтра:**
1. Сбилдить образ и запустить

```bash
docker build -f Dockerfile_rsl_api -t rsl-img . && docker run -d -p 5000:5000 --name rsl-api --restart=always rsl-img
```
2. Удалить контейнер и образ:
```bash
docker stop rsl-api && docker rm rsl-api && docker rmi rsl-img
```
**С фильтром:**
1. Сбилдить образ и запустить

```bash
docker build -f Dockerfile_rsl_api_filter -t rsl-filter-img . && docker run -d -p 5000:5000 --name rsl-api-filter --restart=always rsl-filter-img
```
2. Удалить контейнер и образ:
```bash
docker stop rsl-api-filter && docker rm rsl-api-filter && docker rmi rsl-filter-img
```

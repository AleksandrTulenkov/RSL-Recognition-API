import base64
import datetime
import json
import logging
import os

from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import cv2
import numpy as np
import socketio
from flask import Flask
from model import Predictor

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

sio = socketio.Server(cors_allowed_origins="*", async_mode="threading")
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

CONFIG_PATH = "config_filter.json"
SAMPLE_LENGTH = 32
ROTATE_180_FLAG = False

sign_res = []
room_id = 0
users = {}
model = None
filter_list = []

with open("list_filter.txt", 'r') as list_filter:
    for line in list_filter:
        clear_line = line.strip().replace('\n','')
        filter_list.append(clear_line)

def init_model(config_path):
    try:
        with open(config_path, "r") as read_content:
            config = json.load(read_content)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at path: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding the configuration file: {config_path}")
    try:
        model = Predictor(config)
        return model
    except KeyError as e:
        raise KeyError(f"Missing key in configuration file: {e}")
    except ValueError as e:
        raise ValueError(f"Error creating Predictor configuration: {e}")


def inference(model, frame_queue, sid):
    global users

    while True:
        if users[sid][2]:
            users.pop(sid, None)
            break

        if len(frame_queue) >= SAMPLE_LENGTH:
            cur_windows = list(frame_queue)
        else:
            continue

        results = model.predict(cur_windows)
        if results:
            print(datetime.datetime.now(), results)
            if results['labels'][0] != 'нет жеста':
                results['labels'] = {x: results['labels'][x] for x in results['labels'] if results['labels'][x] in filter_list}
                if len(results['labels']) > 0:
                    sio.emit("send_not_normalize_text", json.dumps(results['labels']), room=sid)

def main():
    global model
    model = init_model(CONFIG_PATH)
    cam_disp = {'cam': None}
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(create_server)

    while True:
        if cam_disp['cam'] is not None:
            cv2.imshow('cam', cam_disp['cam'])

        if cv2.waitKey(1) == ord('q'):
            break


@sio.event
def connect(sid, environ):
    global room_id, users, model
    print("Client connected:", sid)

    room_id = sid

    if sid not in users.keys():
        users[sid] = []
        users[sid].append(deque(maxlen=32))  # Frame queue
        users[sid].append(Thread(target=inference, args=(model, users[sid][0], sid), daemon=True))
        users[sid].append(False)
        users[sid][1].start()


@sio.event
def disconnect(sid):
    global room_id, users, model
    print("Client disconnected:", sid)
    users[sid][0].clear()
    users[sid][2] = True


# Socket.IO event handler: Received video frame data from the client
@sio.on("data")
def data(sid, data):
    global users, ROTATE_180_FLAG
    image_data = data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    frame = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(frame, -1)
    # if camera rotated to 180 degrees
    if ROTATE_180_FLAG:
        image = cv2.rotate(image, cv2.ROTATE_180)
    users[sid][0].append(np.array(image[:, :, ::-1]))


def create_server():
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
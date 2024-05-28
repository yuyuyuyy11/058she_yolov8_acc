import base64
import json
import time
import cv2
import requests

cap = cv2.VideoCapture(0)
frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("video fps={}, width={}, height={}".format(frame_fps, frame_width, frame_height))
last = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.putText(frame, f'FPS: {1 / (time.time() - last):.2f}', (0, 30), 1, 2, (0, 0, 255))
    # cv2.imshow('frame', frame)
    last = time.time()
    # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    _, buffer = cv2.imencode('.jpg', frame)
    byte_data = buffer.tobytes()

    # 将字节流编码为base64字符串
    base64_str = str(base64.b64encode(byte_data), encoding='utf-8')
    json_obj = {
        'file': base64_str
    }
    url = 'http://127.0.0.1:5000/upload'
    headers = {
        'content-type': 'application/json'
    }
    requests.post(url, data=json.dumps(json_obj), headers=headers)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

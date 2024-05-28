import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

parameters = {
    'weight': os.path.join(BASE_DIR, 'weights/best.pt'),
    'tracker': os.path.join(BASE_DIR, 'cfg/bytetrack.yaml')
}
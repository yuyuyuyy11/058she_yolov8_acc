import torch
from .ultralytics.utils import IterableSimpleNamespace, yaml_load
from .ultralytics.utils.checks import check_yaml
from .ultralytics.trackers.track import BYTETracker
from .utils import *

class BytetrackManager(object):
    def __init__(self):
        tracker = check_yaml(parameters['tracker'])
        cfg = IterableSimpleNamespace(**yaml_load(tracker))
        self.tracker = BYTETracker(args=cfg, frame_rate=30)

    def update(self, results):
        det = results[0].boxes.cpu().numpy()
        if len(det) == 0:
            return None
        tracks = self.tracker.update(det, results[0].orig_img)
        if len(tracks) == 0:
            return None
        idx = tracks[:, -1].astype(int)
        results[0] = results[0][idx]
        results[0].update(boxes=torch.as_tensor(tracks[:, :-1]))
        result = results[0]
        boxes = result.boxes
        names = result.names
        bbox = boxes.data
        cls = boxes.cls
        conf = boxes.conf
        result_list = []
        for idx, _ in enumerate(cls):
            class_index = int(cls[idx])
            confidence = round(float(conf[idx]), 2)
            xmin = int(bbox[idx][0])
            ymin = int(bbox[idx][1])
            xmax = int(bbox[idx][2])
            ymax = int(bbox[idx][3])
            tracker_id = int(bbox[idx][4])
            result_list.append([names[class_index], confidence, xmin, ymin, xmax, ymax, tracker_id])  # [label, conf, x1, y1, x2, y2, id]
        return result_list

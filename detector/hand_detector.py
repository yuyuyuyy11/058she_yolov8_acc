from typing import List
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                           max_num_hands=2,
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None
        
    def detect_thumb_tips(self, image_bgr) -> List[List[int]]:
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        # 初始化 Mediapipe 手势模块
        width, heigth = image_rgb.shape[1], image_rgb.shape[0]
        # 处理图像以获取手部关键点
        self.results = self.hands.process(image_rgb)
        # 初始化大拇指指尖坐标列表
        thumb_tips = []
        # 检查是否有手被检测到
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # 获取大拇指指尖的关键点
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                # 将归一化坐标转换为图像坐标
                thumb_x = int(thumb_tip.x * width)
                thumb_y = int(thumb_tip.y * heigth)
                # 将坐标添加到列表中
                thumb_tips.append([thumb_x, thumb_y])
                
        thumb_tips = sorted(thumb_tips, key=lambda x: x[0])
        # 返回大拇指指尖坐标列表
        return thumb_tips
    
    def draw_on_image(self, image_pil):
        # 绘制手部骨架
        if self.results and self.results.multi_hand_landmarks:
            image_np = np.array(image_pil)
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(image_np, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            image_pil = Image.fromarray(image_np)
        # 返回绘制了手部骨架的图像
        return image_pil

    def crop_image_from_tips_pos(self, image_bgr, pos):
        return image_bgr[:, pos[0][0]:pos[1][0]]
# This code is derived from an original work covered by the GNU General Public License (GPL-3.0).
# The original code can be found at https://github.com/Viral-Doshi/Gesture-Controlled-Virtual-Mouse.
#
# Modifications by BukSan-MAM team, 2024:
# - Adapted and modified `Gest` and `Controller` classes.

import cv2
import mediapipe as mp
import pyautogui
from enum import IntEnum
import time
import math

pyautogui.FAILSAFE = False


# One Euro Filter
class OneEuroFilter:
    def __init__(self, freq, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.freq = max(freq, 1e-6)  # 최소값 설정
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = None
        self.dx_prev = None
        self.t_prev = None

    def alpha(self, cutoff):
        tau = 1.0 / (2.0 * math.pi * cutoff)
        te = 1.0 / self.freq
        return 1.0 / (1.0 + tau / te)

    def apply(self, x, t):
        if self.t_prev is None:
            self.t_prev = t
            self.x_prev = x
            self.dx_prev = 0.0
            return x

        dt = t - self.t_prev
        if dt <= 0:
            dt = 1e-6  # 최소값 설정

        self.freq = 1.0 / dt

        dx = (x - self.x_prev) / dt
        edx = self.dx_prev + self.alpha(self.d_cutoff) * (dx - self.dx_prev)
        cutoff = self.min_cutoff + self.beta * abs(edx)
        x_hat = self.x_prev + self.alpha(cutoff) * (x - self.x_prev)

        self.t_prev = t
        self.x_prev = x_hat
        self.dx_prev = edx

        return x_hat 

# Gesture Codes
class Gest(IntEnum):
    # Binary Encoded
    """
    Enum for mapping all hand gesture to binary number.
    """
    PAUSE = -1
    FOCUS_RESET = 0
    CURSOR_MOVE = 1
    LEFT_CLICK = 2
    RIGHT_CLICK = 3
    SCROLL_VERTICAL = 5
    MOUSE_DOWN = 6
    MOUSE_UP = 7

# Controller
class Controller:
    # Locate Hand to get Cursor Position
    # Stabilize cursor by Dampening
    grabflag = False
    prev_hand = None
    movement_x = 0
    movement_y = 0
    scale_adj_range = 0.03 # 480 -> 0.03
    sensitivity = 1 # 0.5 ~ 1.5

    def set_adg_range(dist_palm_points):
        a = 0.000063286
        b = 0.0057
        Controller.scale_adj_range = a * dist_palm_points + b

    def get_position(hand_result, point = 9):
        """
        returns coordinates of current hand position.

        Locates hand to get cursor position also stabilize cursor by 
        dampening jerky motion of hand.

        Returns
        -------
        tuple(float, float)
        """
        position = [hand_result.landmark[point].x ,hand_result.landmark[point].y, hand_result.landmark[point].z]
        sx,sy = pyautogui.size()    # 화면 사이즈 출력 (ex. Size(width=1920, height=1080))
        x_old,y_old = pyautogui.position()  # 포인터 위치 출력 (ex. Point(x=677, y=481))
        x = int(position[0]*sx)
        y = int(position[1]*sy)

        if Controller.prev_hand is None:
            Controller.prev_hand = x,y
        delta_x = x - Controller.prev_hand[0]
        delta_y = y - Controller.prev_hand[1]

        distsq = delta_x**2 + delta_y**2
        ratio = 1
        if point == 9:
            Controller.prev_hand = [x,y]

        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** (1/2))
        else:
            ratio = 2.1

        sensitivity = Controller.sensitivity            
        x, y = x_old + delta_x*ratio*sensitivity , y_old + delta_y*ratio*sensitivity
        
        if point == 9:
            Controller.movement_x = delta_x*ratio
            Controller.movement_y = delta_y*ratio

        return (x,y)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
               min_detection_confidence=0.8,
               min_tracking_confidence=0.8)

# 1 Euro 필터 초기화 (각 랜드마크에 대해 별도의 필터 사용)
hand_filters = [[OneEuroFilter(freq=30, min_cutoff=2.0, beta=0.2, d_cutoff=1.0) for _ in range(3)] for _ in range(21)]

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)

prev_state = None   # -1: 손바닥 편 상태, 0: 주먹, 1: 커서 이동, 2: 좌클릭, 3: 우클릭
ADJ_RANGE = 0.03

def islower(x, y):
    return x >= y

def isNotZero(x):
    if x != 0 :
        return True
    return False

def is_two_point_adj(x0, x1):
    return abs(x0 - x1) <= Controller.scale_adj_range

def get_dist_two_points(p1, p2):
    return math.sqrt(abs(p1[0] - p2[0]) ** 2 + abs(p1[1] -p2[1]) ** 2)

def set_sensitivity(normalized_y):
    """
    Scales a value x from the range [1, 0] to the range [0.5, 1.5].

    Parameters:
    x (float): The value to be scaled. Should be between 1 and 0.

    Returns:
    float: The scaled value.
    """
    if 0 <= normalized_y and normalized_y <= 1:
        # Scale normalized_y from [1, 0] to [0.3, 2.0]
        scaled_y = 0.5 + (3.0 - 0.5) * (1 - normalized_y)
        Controller.sensitivity = scaled_y

while cap.isOpened():
    ret, frame = cap.read()

    # mirror image
    frame = cv2.flip(frame, 1)

    # Convert to rgb --bgr is cv ka default...convert to rgb bcs mediapipe rgb me operate krta hai
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)  # hand landmarks detect krne ko
    if results.multi_hand_landmarks:  # agar hands detect hue to
        for landmarks in results.multi_hand_landmarks:
            # 현재 시간
            t = time.time()

            # 각 랜드마크 좌표에 1 Euro 필터 적용
            for i, landmark in enumerate(landmarks.landmark):
                x = landmark.x
                y = landmark.y
                z = landmark.z

                filtered_x = hand_filters[i][0].apply(x, t)
                filtered_y = hand_filters[i][1].apply(y, t)
                filtered_z = hand_filters[i][2].apply(z, t)

                landmarks.landmark[i].x = filtered_x
                landmarks.landmark[i].y = filtered_y
                landmarks.landmark[i].z = filtered_z
            # hand check krne ko
            handedness = results.multi_handedness[results.multi_hand_landmarks.index(landmarks)].classification[0].label

            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            # draws hand landmarks and connections on the frame

            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
            thumb_mid = landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mid = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

            mid_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            mid_mid = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_mid = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]

            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            pinky_mid = landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

            if handedness == "Left":  # left mouse
                # stabilized cursor x, y point
                cursor_x, cursor_y = Controller.get_position(landmarks)
                thumb_mid_pos, pinky_tip_pos = Controller.get_position(landmarks, 2), Controller.get_position(landmarks, 17)
                Controller.set_adg_range(get_dist_two_points(thumb_mid_pos, pinky_tip_pos))

                # 우클릭
                if is_two_point_adj(index_tip.x, thumb_tip.x) and is_two_point_adj(index_tip.y, thumb_tip.y) \
                    and is_two_point_adj(mid_tip.x, thumb_tip.x) and is_two_point_adj(mid_tip.y, thumb_tip.y) \
                    and is_two_point_adj(mid_tip.x, index_tip.x) and is_two_point_adj(mid_tip.y, index_tip.y) \
                    and islower(ring_tip.y, ring_mid.y) and islower(pinky_tip.y, pinky_mid.y) and islower(thumb_tip.x, thumb_ip.x):
                    pyautogui.click(button='right', clicks=1)   # 한번만 클릭
                    print("중지 우클릭")
                    prev_state = Gest.RIGHT_CLICK
                    print(f'DEBUG) 손크기 {get_dist_two_points(thumb_mid_pos, pinky_tip_pos)} 검지거리 {index_tip.y- thumb_tip.y} 중지거리 {mid_tip.y- thumb_tip.y} ADG {Controller.scale_adj_range}')
                # 커서 이동
                elif islower(index_mid.y, index_tip.y) and islower(mid_tip.y, mid_mid.y) and islower(ring_tip.y, ring_mid.y) and islower(pinky_tip.y, pinky_mid.y):
                    # 검지랑 엄지만 편 상태
                    if islower(thumb_mid.x, thumb_tip.x):
                        pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)
                        prev_state = Gest.PAUSE
                    elif islower(thumb_ip.x, thumb_tip.x):
                        prev_state = Gest.CURSOR_MOVE
                # 스크롤
                elif islower(thumb_ip.x, thumb_tip.x) and islower(index_mid.y, index_tip.y) and islower(mid_mid.y, mid_tip.y) \
                    and islower(ring_tip.y, ring_mid.y) and islower(pinky_tip.y, pinky_mid.y):
                    print("스크롤")
                    if prev_state == Gest.SCROLL_VERTICAL and isNotZero(int(Controller.movement_x) + int(Controller.movement_y)):
                        if int(abs(Controller.movement_x)) > int(abs(Controller.movement_y) * 1.2): # 가로스크롤
                            pyautogui.keyDown('shift')
                            pyautogui.scroll(int(Controller.movement_x)) # + 위방향 - 아래방향
                            pyautogui.keyUp('shift')
                        else:   # 세로 스크롤
                            pyautogui.scroll(int(Controller.movement_y))
                    prev_state = Gest.SCROLL_VERTICAL
                # 좌클릭 & 드래그
                elif is_two_point_adj(index_tip.y, thumb_tip.y) and is_two_point_adj(index_tip.x, thumb_tip.x):
                    # 드래그
                    if islower(pinky_mid.y, pinky_tip.y) and islower(ring_mid.y, ring_tip.y) and islower(mid_mid.y, mid_tip.y):
                        if prev_state == Gest.MOUSE_DOWN:
                            pyautogui.moveTo(cursor_x + int(Controller.movement_x), cursor_y + int(Controller.movement_y))
                            print("drag: ", prev_state)
                        else:
                            prev_state = Gest.MOUSE_DOWN
                            Controller.grabflag = True
                            pyautogui.mouseDown(button = "left")
                            print("drag selected")
                    elif prev_state != Gest.MOUSE_DOWN and Controller.grabflag == True:
                        pyautogui.mouseUp(button = "left")
                        prev_state = Gest.MOUSE_UP
                        Controller.grabflag = False
                    elif prev_state != Gest.LEFT_CLICK:
                        prev_state = Gest.LEFT_CLICK
                        pyautogui.click(clicks=1)   # 한번만 클릭
                        print("검지 클릭")
                        print(f'DEBUG) 손크기 {get_dist_two_points(thumb_mid_pos, pinky_tip_pos)} 검지거리 {index_tip.y- thumb_tip.y} 중지거리 {mid_tip.y- thumb_tip.y} ADG {Controller.scale_adj_range}')    
                # 마우스 민감도 조절
                elif islower(pinky_mid.y, pinky_tip.y) and islower(ring_tip.y, ring_mid.y) and islower(mid_tip.y, mid_mid.y) and islower(index_tip.y, index_mid.y):
                    print(f'pinky_tip.y: {pinky_tip.y}')
                    set_sensitivity(pinky_tip.y)
                # 그 외 모든 동작은 Neutral 
                else:
                    # print('neutral: ', prev_state)
                    prev_state = Gest.PAUSE
                    Controller.prev_hand = None

                if Controller.grabflag == True and prev_state != Gest.MOUSE_DOWN:
                    pyautogui.mouseUp(button = "left")
                    prev_state = Gest.MOUSE_UP
                    Controller.grabflag = False

            # If right hand detected, do nothing
            elif handedness == "Right":  # right keyboard
                pass                

    # comment out the line below if you don't want to show the webcam image
    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

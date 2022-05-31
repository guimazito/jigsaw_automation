import sys
import cv2
import time
import imutils
import settings
import keyboard
import pyautogui

settings.init()

qx = {
    'qx0': 323,
    'qx1': 458,
    'qx2': 600,
    'qx3': 738,
    'qx4': 887,
    'qx5': 1027,
    'qx6': 1167,
    'qx7': 1303,
    'qx8': 1447,
    'qx9': 1587
}

qy = {
    'qy0': 82,
    'qy1': 225,
    'qy2': 366,
    'qy3': 492,
    'qy4': 636,
    'qy5': 767 
}

def check_black_rectangle(qx, qy):
    pyautogui.screenshot('qxqy.png', region=(qx, qy, 15, 15))
    original = cv2.imread('blackRectangle.png')
    new = cv2.imread('qxqy.png')
    diff = original.copy()
    cv2.absdiff(original, new, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0,3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i+1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x,y), (x+w,y+h), (0,255,0), 1)
    if len(cnts) == 0:
        return 0
    else:
        return 1

def check_mouse(qx, qy):
    pyautogui.screenshot('mouse.png', region=(qx, qy, 15, 15))
    original = cv2.imread('mouseAlone.png')
    new = cv2.imread('mouse.png')
    diff = original.copy()
    cv2.absdiff(original, new, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0,3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i+1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x,y), (x+w,y+h), (0,255,0), 1)
    if len(cnts) == 0:
        settings.control_reset += 1
        return 0
    else:
        settings.control_reset = 0
        return 1

def move_to_grid():
    print(' Inside grid...')
    for j in range(len(qy)):
        for i in range(len(qx)):
            if check_black_rectangle(qx['qx{}'.format(i)], qy['qy{}'.format(j)]) == 0:
                pyautogui.moveTo(qx['qx{}'.format(i)], qy['qy{}'.format(j)])
                pyautogui.mouseUp(qx['qx{}'.format(i)], qy['qy{}'.format(j)])
                time.sleep(0.5)
                pyautogui.mouseDown(qx['qx{}'.format(i)], qy['qy{}'.format(j)])
                if check_mouse(qx['qx{}'.format(i)], qy['qy{}'.format(j)]) == 0:
                    break
            else:
                continue
            if keyboard.is_pressed('F7'):
                sys.exit()
        else:
            continue
        break

def check_reset_pieces(side):
    if settings.control_reset > 5:
        if side == 0:
            print('\nMix Pieces!\n')
            pyautogui.moveTo(1870, 46)
            pyautogui.mouseUp(1870, 46)
            pyautogui.mouseDown(1870, 46)
            time.sleep(1)
            pyautogui.moveTo(1881, 263)
            pyautogui.mouseUp(1881, 263)
            pyautogui.mouseDown(1881, 263)
            time.sleep(1)
            settings.control_reset = 0
        elif side == 1:
            print('\nMix Pieces!\n')
            pyautogui.moveTo(1870, 46)
            pyautogui.mouseUp(1870, 46)
            pyautogui.mouseDown(1870, 46)
            time.sleep(1)
            pyautogui.moveTo(1881, 263)
            pyautogui.mouseUp(1881, 263)
            pyautogui.mouseDown(1881, 263)
            time.sleep(1)
            settings.control_reset = 0
            settings.repeat_left_side = 0
            while settings.repeat_left_side == 0:
                process_image_left_side()

def process_image_left_side():
    pyautogui.screenshot('img.png', region=(0, 0, 242, 1074))
    # Image processing
    original = cv2.imread('leftSide.png')    
    new = cv2.imread('img.png')
    diff = original.copy()
    cv2.absdiff(original, new, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0,3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i+1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) == 0:
        settings.repeat_left_side = 1
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x,y), (x+w,y+h), (0,255,0), 1)
        if (w > 50) and (h > 50):
            location = (x, y, w, h)
            print(location)
            xCenter, yCenter = pyautogui.center(location)
            print('Getting piece left side...')
            pyautogui.moveTo(xCenter, yCenter)
            pyautogui.mouseUp(xCenter, yCenter)
            pyautogui.mouseDown(xCenter, yCenter)
            move_to_grid()
            check_reset_pieces(0)

def process_image_right_side():
    pyautogui.screenshot('img.png', region=(1675, 0, 242, 1074))
    # Image processing
    original = cv2.imread('rightSide.png')
    new = cv2.imread('img.png')
    diff = original.copy()
    cv2.absdiff(original, new, diff)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    for i in range(0,3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i+1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) == 0:
        settings.repeat_right_side = 1
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(new, (x,y), (x+w,y+h), (0,255,0), 1)
        if (w > 50) and (h > 50):
            x = 1675 + x
            location = (x, y, w, h)           
            xCenter, yCenter = pyautogui.center(location)
            print('Getting piece right side...')
            pyautogui.moveTo(xCenter, yCenter)
            pyautogui.mouseUp(xCenter, yCenter)
            pyautogui.mouseDown(xCenter, yCenter)
            move_to_grid()
            check_reset_pieces(1)

while True:
    print('waiting F6...')
    if keyboard.is_pressed('F6'):
        tic = time.perf_counter()
        while settings.repeat_left_side == 0:
            process_image_left_side()
        while settings.repeat_right_side == 0:
            process_image_right_side()
        toc = time.perf_counter()
        print(f'Jigsaw completed in {(toc-tic)/60:0.3f} minutes!')
        settings.repeat_left_side = 0
        settings.repeat_right_side = 0
        keyboard.release('F6')
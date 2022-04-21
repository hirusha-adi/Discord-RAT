import pyautogui
import random
import string
import time
from datetime import datetime

time.sleep(2)
start_time = 0
end_time = 20

while True:
    if start_time <= end_time:
        randint = random.randint(0, 20)
        randomstring = (string.ascii_lowercase+string.ascii_uppercase +
                        string.ascii_letters+string.digits+string.punctuation)
        pyautogui.write(''.join(random.choice(randomstring)
                        for i in range(randint)))
        start_time = start_time+1
    else:
        break

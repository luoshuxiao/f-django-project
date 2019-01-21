import random
import time


def get_order_sn():
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQAZWSXEDCRFVTGBYHNUJMIKOLP'
    order_sn = ''
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    return order_sn
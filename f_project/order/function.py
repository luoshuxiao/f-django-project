# -*- coding: utf-8 -*-

"""Éú³ÉËæ»ú×Ö·û´®"""

import time
import random


def get_order_sn():
    """Ëæ»ú×Ö·û´®"""
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQAZWSXEDCRFVTGBYHNUJMIKOLP'
    order_sn = ''
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    return order_sn
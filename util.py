
import time


start_time = int(time.time()*1000)
def get_milliseconds():
    return int(time.time()*1000) - start_time
    
def lerp(x1, x2, interpolation):
    return x1 + (x2 - x1) * interpolation

def rectangles_overlap(x1, y1, w1, h1, x2, y2, w2, h2):

    return (x1 < x2+w2 and x1+w1 > x2 and y1 < y2+h2 and y1+h1 > y2)
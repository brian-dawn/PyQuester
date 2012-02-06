
import time


start_time = int(time.time()*1000)
def get_milliseconds():
    return int(time.time()*1000) - start_time
    
def lerp(x1, x2, interpolation):
    return x1 + (x2 - x1) * interpolation
from threading import Timer

def delay(function, time, *args, **kwargs):
    timer = Timer(time, function, *args, **kwargs);
    timer.start()
    return timer

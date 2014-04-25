_listeners = {}

def pub(event, *args, **kwargs):
    for listener in _listeners.get(event,set()):
        listener(*args, **kwargs)

def sub(event, listener):
    _listeners[event] = _listeners.get(event, set()) | {listener}

def unsub(event, listener):
    _listeners[event] =  _listeners.get(event, set()) - {listener}

def reset():
    _listeners.clear()

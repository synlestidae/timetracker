import collections

Event = collections.namedtuple('Event', ['timestamp', 'kind', 'description', 'isstopping'])

class Timelog:
    events = []

    def __init__(self):
        self.start()

    def start(self):
       self.__log__('start', 'User started logging time', False) 

    def stop(self):
       self.__log__('stop', 'User stopped logging time', False) 

    def lockscreen(self):
       self.__log__('stop', 'Screen was locked', False) 

    def wakeup(self):
       self.__log__('stop', 'User stopped logging time', False) 

    def wakeup(self):
        pass

    def __log__(self, kind, description, isstopping):
        self.events.append(Event(datetime.utcnow(), kind, description, isstopping))

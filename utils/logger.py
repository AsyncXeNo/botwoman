import json

class Logger():
    logs_open = False
    postlist = []
    subscribers = []

    @staticmethod
    def subscribe(subscriber):
        try:
            subscriber.logger_event(f"{subscriber} subscribed to logger posts!")
        except:
            Logger("utils/logger").log_error("You subscribed to logger posts from a class with no logger_event() function.")
            raise Exception("subscriber doesn't have logger_event() function")
        Logger.subscribers.append(subscriber)

    def __init__(self, path):

        self.path = path

        self.escape_code = '\033['
        self.end_escape = 'm'

        self.colors = {
            None: 37,
            'black': 30,
            'red': 31,
            'green': 32,
            'yellow': 33,
            'blue': 34,
            'purple': 35,
            'cyan': 36,
            'white': 37
        }

        self.styles = {
            None: 0,
            'bold': 1,
            'underline': 2,
            'negative1': 3,
            'negative2': 5
        }

        self.levels = {'neutral': 1, 'warning': 2, 'alert': 3, 'error': 4}

        self.log_functions = {
            1: self.log_neutral,
            2: self.log_warning,
            3: self.log_alert,
            4: self.log_error,
        }

        self.end = f'{self.escape_code}{self.styles[None]};{self.colors[None]}{self.end_escape}'


    def log(self, msg, level):
        self.log_functions[self.levels[level]](msg)


    def log_neutral(self, msg):
        msg_style = self.styles['underline']
        msg_color = self.colors['green']

        loginfo = 'NORMAL'

        self.display(loginfo, msg, msg_style, msg_color)

    def log_warning(self, msg):
        msg_style = self.styles['underline']
        msg_color = self.colors['yellow']
        
        loginfo = 'WARNING'

        self.display(loginfo, msg, msg_style, msg_color)

    def log_alert(self, msg):
        msg_style = self.styles[None]
        msg_color = self.colors['yellow']

        loginfo = 'ALERT'

        self.display(loginfo, msg, msg_style, msg_color)

    def log_error(self, msg):
        msg_style = self.styles['bold']
        msg_color = self.colors['red']

        loginfo = 'ERROR'

        self.display(loginfo, msg, msg_style, msg_color)


    # custom
    def custom_log(self, msg, style, color, loginfo = None):
        msg_style = self.styles[style]
        msg_color = self.colors[color]

        msg_loginfo = 'CUSTOM' if loginfo == None else loginfo

        self.display(msg_loginfo, msg, msg_style, msg_color)


    # display
    def display(self, loginfo, msg, msg_style, msg_color):
        log = f"[{self.convert_string(loginfo)}] [{self.convert_string(self.path)}]: {msg}"
        print(f'{self.escape_code}{msg_style};{msg_color}{self.end_escape}{log}{self.end}')
        self.post(log)

    
    # post
    def post(self, log):
        if Logger.logs_open:
            Logger.postlist.append(log)
        else:
            Logger.logs_open = True
            Logger.postlist.append(log)
            while not len(Logger.postlist) == 0:
                with open("data/logs.json", "r") as f:
                    logs = json.load(f)
                post = Logger.postlist.pop(0)
                logs.append(post)
                for subscriber in Logger.subscribers:
                    subscriber.logger_event(post) 
                with open("data/logs.json", "w") as f:
                    json.dump(logs, f, indent=4)
            Logger.logs_open = False


    #info
    def convert_string(self, string):

        string_to_return = ''

        for letter in string:
            string_to_return += letter

        return string_to_return
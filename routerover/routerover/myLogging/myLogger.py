import logging
import logging.config

logConfigDict = {
'version': 1,
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'level': 'INFO',
        'formatter': 'detailed',
        'stream': 'ext://sys.stdout',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'INFO',
        'formatter': 'detailed',
        'filename': 'rover.log',
        'mode': 'a',
        'maxBytes': 10485760,
        'backupCount': 5,
    },

},
'formatters': {
    'detailed': {
        'format': '%(asctime)-30s %(module)-30s line:%(lineno)-4d ' \
        '%(levelname)-8s %(message)s',
    },
    'email': {
        'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
        'Line: %(lineno)d\nMessage: %(message)s',
    },
},
'loggers': {
    'roverLogOnFile': {
        'level':'DEBUG',
        'handlers': ['file',]
        },
    'roverLogOnConsole': {
        'level':'DEBUG',
        'handlers': ['console',]
        },
    'roverLogOnBothConsoleAndFile': {
        'level':'DEBUG',
        'handlers': ['console','file',]
        },
}
}

logging.config.dictConfig(logConfigDict)
roverLogOnFile = logging.getLogger('roverLogOnFile')
roverLogOnConsole = logging.getLogger('roverLogOnConsole')
roverLogOnBothConsoleAndFile = logging.getLogger('roverLogOnBothConsoleAndFile')

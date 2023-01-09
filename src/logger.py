import argparse
import logging
import logging.config


_loggingSettings = {
    'version': 1,
    'formatters': {
        'default': {'format': '%(asctime)s %(levelname)s:%(name)s:%(message)s'}
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': './logs/appLogs.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30
        }
    },
    'loggers': {
        'app': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'app.composer': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'app.windows.main': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'app.windows.ctrlr': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'app.windows.ctrlr.model': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
    }
}


def _getAppCmptNames() -> list:
    """
    Get the supported application component names.

    Returns:
        The list of the supported application component names.
    """
    return [cmpt for cmpt in _loggingSettings['loggers'] if 'app' in cmpt]


def _parseArguments() -> argparse.Namespace:
    """
    Parse the logger arguments.
    """
    argParser = argparse.ArgumentParser(allow_abbrev=False)
    argParser.add_argument('-a', '--app', type=str, default=None,
                           help=f"Set debug level for application components."
                           f"\nUse the following component names : "
                           f"{_getAppCmptNames()}.")
    return argParser.parse_args()


def _setInDebugMode(loggerList: str) -> None:
    """
    Set loggers in debug mode.

    Params:
        loggerList:     The logger list to put in debug mode.
    """
    if loggerList:
        _loggingSettings['handlers']['console']['level'] = 'DEBUG'
        for logger in loggerList.split(','):
            if logger in _loggingSettings['loggers']:
                _loggingSettings['loggers'][logger]['level'] = 'DEBUG'
            else:
                _loggingSettings['loggers'][logger] = \
                    {'level': 'DEBUG', 'handlers': ['console', 'file']}


def _updateSettings(args: argparse.Namespace) -> None:
    """
    Update the logger configuration from the received arguments.

    Params:
        args:           The received arguments.
    """
    _setInDebugMode(args.app)


def initLogging():
    """
    Initialize the logger.
    """
    _updateSettings(_parseArguments())
    logging.config.dictConfig(_loggingSettings)

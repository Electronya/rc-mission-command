from logger import initLogger
import pkgs.mqttClient as client

from pkgs.ui import AppComposer

# App constants
_CLIENT_ID = 'commander'
_CLIENT_PASSWD = '12345'

# App data
_globalLogger: object = None
_logger: object = None
_ui: object = None
_units = {'active': None, 'list': []}


def main():
    """
    Application main.
    """
    logger = initLogger()
    client.init(logger, _CLIENT_ID, _CLIENT_PASSWD)
    app = AppComposer(logger)
    app.run()


if __name__ == '__main__':
    main()

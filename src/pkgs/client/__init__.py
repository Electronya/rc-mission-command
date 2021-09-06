import logging

import paho.mqtt.client as mqtt

from ..messages.unitCxnStateMsg import UnitCxnStateMsg


class Client(mqtt.Client):
    """
    The mission commander mqtt client class.
    """
    CLIENT_ID = 'commander'

    def __init__(self, root, password):
        """
        The mission commander mqtt client constructor.

        Params:
            root:           The application root.
            password:       The client password creds.
        """
        super().__init__(client_id=self.CLIENT_ID, transport='tcp')

        self._logger = logging.getLogger('MQTT')
        self._logger.debug('initializing mqtt client')
        self._root = root

        stateMsgPayload = {UnitCxnStateMsg.STATE_KEY:
                           UnitCxnStateMsg.OFFLINE_STATE}
        self._stateMsg = UnitCxnStateMsg(unit=self.CLIENT_ID,
                                             payload=stateMsgPayload)
        self.will_set(self._stateMsg.get_topic(), self._stateMsg.to_json(),
                      qos=self._stateMsg.get_qos(), retain=True)
        self.username_pw_set(self.CLIENT_ID, password)

        self._logger.info('trying to connect to mission broker')
        self.connect('127.0.0.1', 1883)
        self.loop_start()

    def on_connect(self, client, usrData, flags, rc):
        """
        On connect event callback.

        Params:
            client:         The mqtt client.
            usrData:        Private user data if set.
            flags:          The response flags from the broker.
            rc:             The connection results.
        """
        self._logger.info('connected to mission broker.')
        payload = {UnitCxnStateMsg.STATE_KEY:
                   UnitCxnStateMsg.ONLINE_STATE}
        self._stateMsg.set_payload(payload)
        self.publish(self._stateMsg.get_topic(), self._stateMsg.to_json(),
                     qos=self._stateMsg.get_qos(), retain=True)

        self.subscribe(f"{UnitCxnStateMsg.TOPIC_ROOT}/#", qos=1)

    def on_disconnect(self, client, usrData, rc):
        """
        On disconnect event callback.

        Params:
            client:         The mqtt client.
            usrData:        Private user data if set.
            rc:             The connection results.
        """
        self._logger.info('disconnected from mission broker.')
        self.loop_stop()

    def on_message(self, client, usrData, msg):
        """
        On message event callback.

        Params:
            client:         The mqtt client.
            usrData:        Private user data if set.
            msg:            The message recived.
        """
        topic = msg.topic
        receivedMsg = msg.payload.decode('utf-8')
        self._logger.info(f"received message topic: {topic}.")
        self._logger.debug(f"message payload: {receivedMsg}")

        if self._stateMsg.TOPIC_ROOT in topic:
            stateMsg = UnitCxnStateMsg(unit=None)
            stateMsg.set_from_json(receivedMsg)
            if stateMsg.get_unit() != self.CLIENT_ID and stateMsg.is_online():
                self._logger.debug(f"new unit: {stateMsg.get_unit()}")
                self._root.add_unit(stateMsg.get_unit())
            elif stateMsg.get_unit() != self.CLIENT_ID \
                    and stateMsg.is_offline():
                self._logger.debug(f"unit left: {stateMsg.get_unit()}")
                self._root.remove_unit(stateMsg.get_unit())

    def on_publish(self, client, usrData, mid):
        """
        On publish event callback.

        Params:
            client:         The mqtt client.
            usrData:        Private user data if set.
            mid:            The message ID.
        """
        self._logger.debug(f"message published: mid {mid}")

    def on_subscribe(self, client, usrData, mid, granted_qos):
        """
        On publish event callback.

        Params:
            client:         The mqtt client.
            usrData:        Private user data if set.
            mid:            The message ID.
            granted_qos:    The granted quality of service.
        """
        self._logger.debug(f"subscription done with mid: {mid}; "
                           f"and qos: {granted_qos}")

    def disconnect(self):
        """
        Disconnect the client from the broker.
        """
        self._logger.info('disconnecting from mission broker.')
        payload = {UnitCxnStateMsg.STATE_KEY:
                   UnitCxnStateMsg.OFFLINE_STATE}
        self._stateMsg.set_payload(payload)
        self.publish(self._stateMsg.get_topic(), self._stateMsg.to_json(),
                     self._stateMsg.get_qos(), retain=True)
        super().disconnect()

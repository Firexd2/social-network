import json

import tornado.websocket

from alerts.mixins import HandlerRedisMessages


class NewMessageHandler(HandlerRedisMessages, tornado.websocket.WebSocketHandler):

    channel = 'alert'

    def on_message(self, msg):

        if msg.kind == 'message':

            json_msg = msg.body
            message = json.loads(json_msg)
            # If the message contains the self.id_user, then send to client
            if self.id_user in message.keys():
                self.write_message(json.dumps(message[self.id_user]))

        if msg.kind == 'disconnect':
            self.close()


class ReadingMessagesHandler(HandlerRedisMessages, tornado.websocket.WebSocketHandler):

    channel = 'read'

    def on_message(self, msg):

        if msg.kind == 'message':

            json_msg = msg.body
            message = json.loads(json_msg)

            if self.id_user in message['users_ids']:
                self.write_message(message['rooms_id'])

        if msg.kind == 'disconnect':
            self.close()

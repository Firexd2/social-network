import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornadoredis

import json


class AlertsHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(AlertsHandler, self).__init__(*args, **kwargs)
        self.id_user = ''
        self.client = tornadoredis.Client()
        self.listen()

    def check_origin(self, origin):
        return True

    @tornado.gen.engine
    def listen(self):
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'alert')
        self.client.listen(self.on_message)

    def on_message(self, msg):

        if msg.kind == 'message':

            json_msg = msg.body
            message = json.loads(json_msg)

            # If in message is the self.id_user, then send to client
            if self.id_user in message.keys():
                self.write_message(json.dumps(message[self.id_user]))

        if msg.kind == 'disconnect':
            self.close()

    def open(self, id_user):
        self.id_user = id_user

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe('alert')
            self.client.disconnect()


class ReadingMessagesHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(ReadingMessagesHandler, self).__init__(*args, **kwargs)
        self.id_user = ''
        self.client = tornadoredis.Client()
        self.listen()

    def check_origin(self, origin):
        return True

    @tornado.gen.engine
    def listen(self):
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'read')
        self.client.listen(self.on_message)

    def on_message(self, msg):

        if msg.kind == 'message':

            json_msg = msg.body
            message = json.loads(json_msg)

            if self.id_user in message['users_ids']:
                self.write_message(message['rooms_id'])

        if msg.kind == 'disconnect':
            self.close()

    def open(self, id_user):
        print('OK')
        self.id_user = id_user

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe('read')
            self.client.disconnect()

import tornado.websocket

listen_users = dict()


class WSPagesAlerts(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    # сделать проверку на юзера (из куков)
    def open(self, id_user):
        print('Подписка на оповещения')
        listen_users[id_user] = self


class WSSendMessage(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print('Подписка на отправку сообщений')
        pass

    def on_message(self, message):

        o = listen_users[message]

        o.write_message('new')

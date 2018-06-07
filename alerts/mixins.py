import tornado.gen
import tornadoredis


class RedisConnectMixin:

    channel = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_user = ''
        self.client = tornadoredis.Client()
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, self.channel)
        self.client.listen(self.on_message)


class AccessMixin:

    def check_origin(self, origin):
        return True

    def open(self, id_user):
        self.id_user = id_user

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe(self.channel)
            self.client.disconnect()


class HandlerRedisMessages(AccessMixin, RedisConnectMixin):
    """
    Собирает все методы для приема сообщений от redis
    """

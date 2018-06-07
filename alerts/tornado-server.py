import tornado.web

from alerts.handlers import NewMessageHandler, ReadingMessagesHandler

app = tornado.web.Application(
    [
        (r'/pages_alerts/(?P<id_user>\w+)/', NewMessageHandler),
        (r'/reading_messages/(?P<id_user>\w+)/', ReadingMessagesHandler)
    ],
    debug=True
)

http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(8888)
tornado.ioloop.IOLoop.instance().start()

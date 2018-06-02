import tornado.web

from alerts.handlers import AlertsHandler, ReadingMessagesHandler

app = tornado.web.Application(
    [
        (r'/pages_alerts/(?P<id_user>\w+)/', AlertsHandler),
        (r'/reading_messages/(?P<id_user>\w+)/', ReadingMessagesHandler)
    ],
    debug=True
)

http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(8888)
print('Demo is runing at 0.0.0.0:8888\nQuit the demo with CONTROL-C')
tornado.ioloop.IOLoop.instance().start()

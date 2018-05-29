import asyncio

import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop

from websockets.handlers import WSPagesAlerts, WSSendMessage

app = tornado.web.Application(
    [
        (r'/pages_alerts/(?P<id_user>\w+)/', WSPagesAlerts),
        (r'/send_message/', WSSendMessage)
    ],
    debug=True
)

app.listen(8888)
AsyncIOMainLoop().install()
loop = asyncio.get_event_loop()
try:
    loop.run_forever()
except KeyboardInterrupt:
    print(" server stopped")

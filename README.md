## Social network

Social network, written in the likeness of http://vk.com, has all the necessary features. Page, user's settings, system friends, albums and messages, which work in real-time.

See http://social-network.beloglazov.me

The project work with the help of Django and Tornado + Redis. Tornado and Redis uses ideology of the Pub/Sub. 

### Why was to develop a social network?

In the development of particular interest were the real-time messages. For successful implementation, we used Tornado and Redis, which communicate with each other via pub/sub messages.
When the user sent the message, from his client we issue a PUBLISH operation:

```python

# in chat/views.py
...
self.client.publish('alert', json.dumps(notify))
...
```

Then the Tornado receives the message data:

```python

# in alerts/mixins.py

# listen to the channel

self.channel = 'alerts'
...
yield tornado.gen.Task(self.client.subscribe, self.channel)
...
```

We accept the message and sends it on websocket's:

```python

# alerts/handelrs.py

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
```

Browser receives data and js-code inserts message.

![social-network](https://github.com/Firexd2/social-network/blob/master/social-network.gif)

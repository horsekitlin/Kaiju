from tornado import ioloop, template, websocket, web

config = {
    'sockets' : list(),
    'users' : list(),
    'TEMPLATE_ROOT' : ''
}

class HomeHandler(web.RequestHandler):
    def get(self):
        loader = template.Loader(config['TEMPLATE_ROOT'])
        self.write(loader.load('login.html').generate())

class ChatHandler(web.RequestHandler):
    def get(self):
        pass
    def post(self):
        username = self.get_argument('username')
        loader = template.Loader(config['TEMPLATE_ROOT'])
        self.write(loader.load('chat.html').generate(username=username))

class ClientSocket(websocket.WebSocketHandler):
    def open(self):
        username = self.get_argument('username').replace("'", "")
        config['sockets'].append(self)
        config['users'].append(username)

        for socket in config['sockets']:
            socket.write_message('{} joined the room!'.format(username))

        print 'WebSocket opened for user {}'.format(username)

    def on_message(self, message):
        sender = config['users'][config['sockets'].index(self)]

        for i in range(len(config['sockets'])):
            username = config['users'][i]
            socket = config['sockets'][i]
            socket.write_message(' {} : {}'.format(sender, message))

    def on_close(self):
        index = config['sockets'].index(self)
        print config['users']
        username = config['users'][index]
        config['sockets'].remove(self)
        del config['users'][index]

        for socket in config['sockets']:
            socket.write_message('{} left the room!'.format(username))

class Announcer(web.RequestHandler):
    def get(self):
        data = self.get_argument('data')

        for socket in config['sockets']:
            socket.write_message(data)
        self.write('Posted')

if __name__ =='__main__':
    application = web.Application([(r'/', HomeHandler),
        (r'/chat', ChatHandler),
        (r'/socket', ClientSocket),
        (r'/push', Announcer)
        ], debug=True)

    application.listen(8080)
    ioloop.IOLoop.instance().start()

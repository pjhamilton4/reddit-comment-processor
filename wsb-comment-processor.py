import time

import stomp

# Add ability to pull this from configuration file
conn = stomp.Connection([('192.168.1.246', 61613)])


class MyListener(object):
    msg_list = []

    def __init__(self):
        self.msg_list = []

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)

    def on_message(self, headers, message):
        print(message)
        self.msg_list.append(message)


def execute_app():
    print("Starting listener!")
    listen = MyListener()
    conn.set_listener('', listen)
    conn.connect('admin', 'admin', wait=True)
    conn.subscribe(destination='reddit.comment.parser.raw', id='py-processor-1', ack='auto')

    while True:
        time.sleep(30)
        listen.msg_list = []


def handle_cleanup():
    conn.disconnect()


def main():
    try:
        execute_app()
    finally:
        handle_cleanup()


if __name__ == '__main__':
    main()

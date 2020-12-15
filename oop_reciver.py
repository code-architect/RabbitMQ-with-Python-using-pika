try:
    import pika
    import ast
except Exception as e:
    print("Some modules are missing {}".format_map(e))


class Metaclass(type):
    """ singleton design pattern """
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Metaclass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMQServerConfigure(metaclass=Metaclass):
    def __init__(self, queue='hello',
                 url="amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd"):
        self.host = url
        self.queue = queue


class RabbitMQServer():
    def __init__(self, server):
        """
        :param server: Object of RabbitMQServerConfigure class
        """
        self.server = server
        self._connection = pika.BlockingConnection(pika.URLParameters(self.server.host))
        self._channel = self._connection.channel()
        self._queue = self._channel.queue_declare(queue=self.server.queue)

    @staticmethod
    def callback(ch, method, properties, body):
        payload = body.decode("utf-8")
        payload = ast.literal_eval(payload)
        print(type(payload))
        print("Data Received: {}".format(payload))

    def start_server(self):
        self._channel.basic_consume(queue=self.server.queue, on_message_callback=RabbitMQServer.callback, auto_ack=True)
        self._channel.start_consuming()


if __name__ == "__main__":
    configuration = RabbitMQServerConfigure()
    consumer = RabbitMQServer(server=configuration)
    consumer.start_server()

# TODO: 1. Going to add a json converter
# TODO: 2. work on a auto-import mechanism for import
#

try:
    import pika
except Exception as e:
    print("Some modules are missing {}".format_map(e))


class Metaclass(type):
    """ singleton design pattern """
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Metaclass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


# ----------------------------------------------------------------------------------------------------------------------

class RabbitMQConfigure(metaclass=Metaclass):
    """ Configuration of the RabbitMQ server """

    def __init__(self, queue='hello',
                 url="amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd",
                 routingKey='hello', exchange=''):
        self.queue = queue
        self.host = url
        self.routingKey = routingKey
        self.exchange = exchange


# ----------------------------------------------------------------------------------------------------------------------

class RabbitMQ():
    __slots__ = ["server", "_channel", "_connection"]

    def __init__(self, server):
        """
        :param server: Object of RabbitMQConfigure class
        """
        self.server = server

        self._connection = pika.BlockingConnection(pika.URLParameters(self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def __enter__(self):
        print("Hi, I'm __enter__ method")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("I'm __exit__ method")
        self._connection.close()

    def publish(self, payload={}):
        """
        :param payload: JSON payload
        :return: None
        """
        self._channel.basic_publish(exchange=self.server.exchange, routing_key=self.server.routingKey,
                                    body=str(payload))
        print("Published Message: {}".format(payload))


# ----------------------------------------------------------------------------------------------------------------------


class Image(object):
    __slots__ = ["filename"]

    def __init__(self, filename):
        self.filename = filename

    @property
    def get(self):
        with open(self.filename, "rb") as f:
            data = f.read()
        return data


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    server = RabbitMQConfigure(queue='hello',
                               url="amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd",
                               routingKey='hello', exchange='')

    # we can use the os module to get the path also
    image = Image(filename="D:\/xampp\/htdocs\/sand_box\/RabbitMQ_python\/77588.jpg")
    data = image.get

    with RabbitMQ(server) as rabbitmq:
        rabbitmq.publish(payload=data)

# Got help from Soumil. Thank you brother for the wonderful idea.

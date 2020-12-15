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


class RabbitMQConfigure(metaclass=Metaclass):
    """ Configuration of the RabbitMQ server """

    def __init__(self, queue='hello',
                 url="amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd",
                 routingKey='hello', exchange=''):
        self.queue = queue
        self.host = url
        self.routingKey = routingKey
        self.exchange = exchange


class RabbitMQ():
    def __init__(self, server):
        """
        :param server: Object of RabbitMQConfigure class
        """
        self.server = server

        self._connection = pika.BlockingConnection(pika.URLParameters(self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def publish(self, payload={}):
        """
        :param payload: JSON payload
        :return: None
        """
        self._channel.basic_publish(exchange=self.server.exchange, routing_key=self.server.routingKey,
                                    body=str(payload))
        print("Published Message: {}".format(payload))
        self._connection.close()


if __name__ == "__main__":
    server = RabbitMQConfigure(queue='hello',
                               url="amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd",
                               routingKey='hello', exchange='')

    rabbitmq = RabbitMQ(server)
    rabbitmq.publish(payload={"data": 22})

# Got help from Soumil. Thank you brother for the wonderful idea.

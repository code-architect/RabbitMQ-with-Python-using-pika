try:
    import pika
except Exception as e:
    print("Some modules are missing {}".format_map(e))


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """ Singleton design pattern """
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMQ(metaclass=MetaClass):
    def __init__(self, queue='hello'):
        self._connection = pika.BlockingConnection(
            pika.URLParameters("amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd"))
        self._channel = self._connection.channel()
        self.queue = queue
        self._channel.queue_declare(queue=self.queue)

    def publish(self, payload={}):
        self._channel.basic_publish(exchange='',
                                    routing_key='hello',
                                    body=str(payload))
        print("published")

        self._connection.close()


if __name__ == "__main__":
    server = RabbitMQ(queue='hello')
    server.publish(payload={"data": "hello"})

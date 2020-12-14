try:
    import pika
except Exception as e:
    print("Some modules are missing {}".format_map(e))

url = "amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd"
params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World')
print("message published")

connection.close()
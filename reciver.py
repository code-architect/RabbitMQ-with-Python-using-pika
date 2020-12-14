try:
    import pika
except Exception as e:
    print("Some modules are missing {}".format_map(e))

url = "amqps://kdqxikdd:r3YcTfJjFXoN0f04K8MFLixfO08RrY8d@lionfish.rmq.cloudamqp.com/kdqxikdd"
params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print("Received %r" % body)

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print("waiting for message")
channel.start_consuming()
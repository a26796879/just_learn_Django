from celery import Celery
import time
app = Celery('tasks', 
                broker='amqp://niceguy:niceguy@35.227.175.4:5672',
                )
 
@app.task
def send_email(email, token):
    print ("sending email...")
    print ("you can saving a file or log a message here to verify it.")

@app.task
def add(x, y):
    return x + y


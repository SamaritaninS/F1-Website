from django.contrib import admin
from django.core.mail import EmailMessage
from jinja2 import Template
from multiprocessing.dummy import Process, Queue
from .models import Category, Racer, Team, TeamShots, Reviews, Feedback


class Function():
    def function(self):
        return




class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class QueueSinglenton(metaclass=Singleton):
    def __init__(self):
        self.message_queue = Queue()

    def get_queue(self):
        return self.message_queue


class EmailReply(admin.ModelAdmin):
    message_queue = QueueSinglenton().get_queue()

    dictionary={}


    def save_model(self, request, obj, form, change):

        if not obj.email_reply_tprmerext:
            return
        if not obj.email_adress:
            return

        recipients = obj.email_adress.split(',')

        def send_email_to_users(ModelAdmin, request, recipients):
            for emails in recipients:
                child_process = Process(target=send_email_to_user, args=(request, emails, self.message_queue))
                child_process.start()
                self.message_queue.get().send()
                child_process.join()

        def send_email_to_user(request, emails, message_queue):
            message = Template('Hello \n {{email_reply_text}}\n').render(text=obj.email_reply_text)
            email = EmailMessage('svalik01@gmail.com', obj.email_reply_text, to=[emails])
            message_queue.put(email)

        send_email_to_users(self, request, recipients)
        super().save_model(request, obj, form, change)


admin.site.register(Feedback, EmailReply)

admin.site.register(Category)
admin.site.register(Racer)
admin.site.register(Team)
admin.site.register(TeamShots)
admin.site.register(Reviews)

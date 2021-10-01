from multiprocessing.dummy import Pool
from multiprocessing import Process, Queue

from django.contrib import admin
from django.core.mail import send_mail, EmailMessage
from jinja2 import Template

from feedback.models import Feedback


class EmailReply(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.email_reply_text:
            return
        if not obj.email_adress:
            return

        recipients = obj.email_adress.split(',')

        if not obj.verified:
            recipients.append(obj.email_adress)

        def send_message(mail):
            message = Template('Hello \n {{email_reply_text}}\n').render(text=obj.email_reply_text)
            send_mail(obj.email_reply_capt, obj.email_reply_text, 'svalik01@gmail.com', [mail])

        if obj.verified:
            pool = Pool()
            pool.map(send_message, recipients)

        obj.email_reply = False
        obj.email_reply_capt = ''
        obj.email_reply_text = None
        super().save_model(request, obj, form, change)


admin.site.register(Feedback, EmailReply)

# class EmailReply(admin.ModelAdmin):
#
#     def save_model(self, request, obj, form, change):
#
#         if not obj.email_reply_text:
#             return
#         if not obj.email_adress:
#             return
#
#         recipients = obj.email_adress.split(',')
#
#         if not obj.verified:
#             recipients.append(obj.email_address)
#
#         def send_email_to_users(ModelAdmin, request, recipients):
#             message_queue = Queue()
#             for emails in recipients:
#                 child_process = Process(target=send_email_to_user, args=(request, emails, message_queue))
#                 child_process.start()
#                 message_queue.get().send()
#                 child_process.join()
#
#         def send_email_to_user(request, emails, message_queue):
#             message = Template('Hello \n {{email_reply_text}}\n').render(text=obj.email_reply_text)
#             email = EmailMessage('svalik01@gmail.com', obj.email_reply_text, to=[emails])
#             message_queue.put(email)
#
#         send_email_to_users(self, request, recipients)
#         super().save_model(request, obj, form, change)
#
#
# admin.site.register(Feedback, EmailReply)

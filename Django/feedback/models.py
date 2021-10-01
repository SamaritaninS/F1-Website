from django.db import models


class Feedback(models.Model):
    verified = models.BooleanField('Отправить ответ на e-mail')
    email_adress = models.CharField('e-mail адрес для ответа', blank=True, max_length=500)
    email_reply_capt = models.CharField('Заголовок ответа на e-mail', blank=True, max_length=500)
    email_reply_text = models.TextField('Текст ответа на e-mail', null=True, blank=True)
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Racer(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="racer/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Гонщики и руководители"
        verbose_name_plural = "Гонщики и руководители"


class Team(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Опмсание")
    logo = models.ImageField("Логотип", upload_to="teams/")
    year = models.PositiveSmallIntegerField("Год дебюта")
    country = models.CharField("Страна", max_length=30)
    base = models.CharField("База", max_length=50)
    directors = models.ManyToManyField(Racer, verbose_name="руководитель", related_name="team_director")
    racers = models.ManyToManyField(Racer, verbose_name="гонщики", related_name="team_racer")
    total_victories = models.PositiveSmallIntegerField("Всего побед", default=0)
    total_points = models.PositiveSmallIntegerField("Всего очков", default=0)
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name="team_category")
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("team_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class TeamShots(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="team_shots/")
    team = models.ForeignKey(Team, verbose_name="Команда", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фотография команды"
        verbose_name_plural = "Фотографии каманды"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey(Team, verbose_name="команда", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.team}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Feedback(models.Model):
    verified = models.BooleanField('Отправить ответ на e-mail')
    email_adress = models.CharField('e-mail адрес для ответа', blank=True, max_length=500)
    email_reply_capt = models.CharField('Заголовок ответа на e-mail', blank=True, max_length=500)
    email_reply_text = models.TextField('Текст ответа на e-mail', null=True, blank=True)
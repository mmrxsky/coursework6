from django.utils import timezone

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):

    email = models.EmailField()
    name = models.CharField(max_length=50, verbose_name='Имя')
    comment = models.TextField(verbose_name='Примечание', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:

        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):

    title = models.CharField(max_length=50, verbose_name='Тема сообщения', **NULLABLE)
    message = models.TextField(verbose_name='Сообщение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):

    PERIODS = (
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Выполнена'),
    )

    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время окончания')
    period = models.CharField(max_length=20, default='daily', choices=PERIODS, verbose_name='Период')
    status = models.CharField(max_length=20, default=STATUS_CREATED, choices=STATUSES, verbose_name='Статус')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.time_start} ({self.period})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):

    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    date_time = models.DateTimeField(auto_now_add=timezone.now, verbose_name='Дата и время', **NULLABLE)
    status = models.CharField(max_length=20, default=STATUS_OK, choices=STATUSES, verbose_name='Статус')
    answer_server = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    class Meta:

        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

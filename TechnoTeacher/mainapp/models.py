from django.core.validators import RegexValidator
from django.db import models, transaction, DatabaseError
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    desc = models.TextField()
    slug = models.SlugField(max_length=250)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f'{self.name}'

    def restore(self, using=None, keep_parents=False):
        self.is_active = True
        self.name = self.name[1:]
        self.course_set.all().update(is_active=True)
        self.save()

    def delete(self):
        self.is_active = False
        with transaction.atomic() as _:
            self.course_set.all().update(is_active=False)
            self.name = f'_{self.name}'
            self.save()
        return 1, {}


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='course')
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=250, default=name)
    cover = models.ImageField(verbose_name='Обложка', upload_to='images/course/')
    desc = models.TextField()
    price = models.DecimalField(verbose_name='Стоимость', max_digits=6, decimal_places=2, default=0)
    teachers = models.ManyToManyField("authapp.UserProfile", related_name='course_teachers')
    students = models.ManyToManyField('authapp.UserProfile', blank=True, related_name='course_students')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f'{self.name}'

    def restore(self):
        self.is_active = True
        self.name = self.name[1:]
        self.course_task.all().update(is_active=True)
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        with transaction.atomic() as _:
            self.course_order.all().delete()
            self.course_task.all().update(is_active=False)
            self.name = f'_{self.name}'
            self.save()
        return 1, {}


class Order(models.Model):
    user = models.ForeignKey("authapp.UserProfile", verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name="user_order")
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, related_name="course_order")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="content_task")
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["course"]
        verbose_name = "Содержание"
        verbose_name_plural = "Содержание"

    def __str__(self):
        return f'{self.course.name} - {self.name}'


class Task(models.Model):
    DIFFICULTY_HARD = 'h'
    DIFFICULTY_EASY = 'e'
    DIFFICULTY_MEDIUM = "m"
    DIFFICULTY = (
        (DIFFICULTY_HARD, _('Hard')),
        (DIFFICULTY_EASY, _('Easy')),
        (DIFFICULTY_MEDIUM, _('Medium')),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_task")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="content_task", blank=True)
    name = models.CharField(max_length=128)
    desc = models.TextField()
    status = models.BooleanField(default=False)
    difficulty = models.CharField(_('difficulty'), max_length=1, choices=DIFFICULTY, blank=True)
    test = models.FileField(upload_to='test/',
                            null=True)  # Как реализовать проверку с помощью тестов не знаю надо подумать над этим
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return f'{self.course.name} - {self.name}'

    def finish(self):
        self.status = True
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class Sollution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sollution')
    code = models.TextField()

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"


class Event(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField()
    images = models.ImageField(upload_to='images/events')
    date = models.DateTimeField()

    class Meta:
        ordering = ["date"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.name


class ContactEvent(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=('Необходимо ввести номер телефона в формате: +70123456789, '
                 'допускается до 15 знаков')
    )

    name = models.CharField(max_length=156, )
    email = models.EmailField()
    phone_number = models.CharField(validators=[phone_validator], max_length=17, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
        verbose_name = "Запись мероприятие"
        verbose_name_plural = "Запись мероприятие"

    def __str__(self):
        return self.email

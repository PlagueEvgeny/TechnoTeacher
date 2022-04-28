from django.db import models, transaction, DatabaseError


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
    slug = models.SlugField(max_length=250) 
    cover = models.ImageField(verbose_name='Обложка', upload_to='images/course/')
    desc = models.TextField()
    price = models.DecimalField(verbose_name='Стоимость', max_digits=6, decimal_places=2, default=0)
    teachers = models.ManyToManyField("authapp.UserProfile", related_name='course_teachers')
    students = models.ManyToManyField('authapp.UserProfile', related_name='course_students')
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
        self.task_set.all().update(is_active=True)
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        with transaction.atomic() as _:
            self.task_set.all().update(is_active=False)
            self.name = f'_{self.name}'
            self.save()
        return 1, {}


class Order(models.Model):
    user = models.ForeignKey("authapp.UserProfile", verbose_name='Пользователь', on_delete=models.CASCADE, related_name="user_order")
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, related_name="course_order")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Task(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="task")
    name = models.CharField(max_length=128)
    desc = models.TextField()
    solution = models.FileField(upload_to='solution/', null=True)
    test = models.FileField(upload_to='test/',
                            null=True)  # Как реализовать проверку с помощью тестов не знаю надо подумать над этим
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def restore(self):
        self.is_active = True
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()



from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=('Необходимо ввести номер телефона в формате: +70123456789, '
                 'допускается до 15 знаков')
    )

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
    )

    ROLE_STUDENT = 's'
    ROLE_TEACHER = 't'
    ROLE_CHOICES = (
        (ROLE_STUDENT, _('Student')),
        (ROLE_TEACHER, _('Teacher')),
    )

    date_birth = models.DateField(_('birth date'), null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, default='avatar/default.png')
    phone_number = models.CharField(validators=[phone_validator], max_length=17, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    role = models.CharField(_('role'), max_length=1, choices=ROLE_CHOICES, blank=False)
    balance = models.DecimalField(verbose_name="Баланс", max_digits=6, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'{self.username} | {self.balance}'

    def restore(self):
        self.is_active = True
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
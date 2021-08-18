from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class CompanyManager(models.Model):
    """Model representing a company contact person and own position in current company"""
    company = models.ForeignKey('Company', verbose_name='Контактное лицо', on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name='Имя', max_length=20)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    manager_position = models.CharField(verbose_name='Должность', max_length=100)

    def clean(self):
        self.name = self.name.title()
        self.surname = self.surname.title()
        return self.name, self.surname

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'


class CompanyEmail(models.Model):
    """Model representing an email for company"""
    company = models.ForeignKey('Company', verbose_name='Компания', on_delete=models.CASCADE, null=True)
    company_email = models.EmailField(verbose_name='email', max_length=100, null=True, blank=False)


class Phone(models.Model):
    """Model representing a phone for company"""
    company = models.ForeignKey('Company', verbose_name='Компания', on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=10, verbose_name='Телефон', null=True, blank=False, help_text='Введите номер телефона в формате "0XXXXXXXXX"')

    def __str__(self):
        return f'+38{self.phone}'

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'


class Company(models.Model):
    """Model representing a company"""
    name = models.CharField(verbose_name='Название компании', max_length=200)
    description = RichTextField(verbose_name='Описание', null=True, blank=True)
    date_create = models.DateField(verbose_name='Дата создания записи о компании', auto_now_add=True)
    date_edit = models.DateField(verbose_name='Дата последнего изменения записи', auto_now=True)
    address = models.TextField(verbose_name='Адрес компании', max_length=200)

    def __str__(self):
        return f'Компания {self.name}'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'pk': self.id})


class Project(models.Model):
    """Model representing a project of company"""
    project = models.CharField(verbose_name='Проект', max_length=250)
    company = models.ForeignKey('Company', verbose_name='Компания', on_delete=models.CASCADE, null=True)
    description = models.TextField(verbose_name='Описание проекта')
    start_date = models.DateField(verbose_name='Дата начала')
    final_date = models.DateField(verbose_name='Дата окончания')
    price = models.PositiveIntegerField(verbose_name='Стоимость проекта')

    def __str__(self):
        return self.project

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.id})

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from company.models import Company, Project


class User(AbstractUser):
    """Model representing default user with photo and biography"""
    photo = models.ImageField(verbose_name='Фото', upload_to='archives/', null=True, blank=True)
    bio = models.TextField(verbose_name='Биография', blank=True, null=True)

    def __str__(self):
        return self.username


class Keyword(models.Model):
    """Model representing keywords for interactions' filter"""
    keyword = models.CharField(verbose_name='Ключевое слово', max_length=250, unique=True)

    class Meta:
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'

    def get_absolute_url(self):
        """Get url after successful creating of keyword"""
        return reverse('interaction_list')


class Interaction(models.Model):
    """Model representing an interaction between company and manager of crm"""
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE)
    CHANNEL = (('Звонок', 'c'), ('Письмо', 'l'), ('Email', 'e'), ('Сайт', 's'))
    channel = models.CharField(verbose_name='Канал обращения', max_length=100, choices=CHANNEL)
    manager = models.ForeignKey(User, verbose_name='Менеджер', on_delete=models.SET_NULL, null=True)
    description = models.TextField(verbose_name='Описание')
    GRADE = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    grade = models.IntegerField(verbose_name='Оценка', choices=GRADE)

    class Meta:
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'
        default_related_name = 'interactions'

    def get_absolute_url(self):
        """Get url after successful creating or updating of current interaction"""
        return reverse('interaction_detail', kwargs={'pk': self.id})

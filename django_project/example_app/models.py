from django.db import models


class A(models.Model):
    name = models.CharField('name', max_length=64)
    nickname = models.CharField('nickname', max_length=64, default='unknown')

    def __str__(self) -> str:
        return f'{self.name} ({self.id})'

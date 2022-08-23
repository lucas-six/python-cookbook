import uuid

from django.db import models


class A(models.Model):
    SEXES = (
        ('M', 'Man'),
        ('F', 'Female'),
        ('-', '-'),
    )

    # id = models.BigAutoField(primary_key=True)

    # UUIDField
    # for PostgreSQL: uuid datatype
    # for others: char(32) datatype
    uuid = models.UUIDField('uuid', default=uuid.uuid4, unique=True, editable=False)

    # CharField
    # Avoid using `null=True`` on string-based fields such CharField, TextField
    SexType = models.TextChoices('SexType', 'Man Female -')
    name = models.CharField('name', max_length=64)
    nickname = models.CharField('nickname', max_length=64, default='[unknown]')
    sex = models.CharField('sex', max_length=8, choices=SEXES, blank=True)
    sex2 = models.CharField('sex2', max_length=8, choices=SexType.choices, blank=True)

    # IntegerField & DecimalField
    age = models.PositiveSmallIntegerField('age', null=True, blank=True)
    balance = models.DecimalField(
        'balance', max_digits=8, decimal_places=2, default=0.0
    )
    score = models.PositiveIntegerField('score', default=0)

    is_active = models.BooleanField('is active', default=True)
    created_time = models.DateTimeField('created time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.id})'

    class Meta:
        # abstract = True
        # ordering = ['name']
        verbose_name = 'A'
        verbose_name_plural = 'As'

    def save(self, *args, **kwargs) -> None:
        # do_something()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        # do_something_else()


class B(models.Model):
    a = models.ForeignKey(A, on_delete=models.CASCADE, verbose_name='A')

    def __str__(self) -> str:
        return f'{self.a.name} ({self.id})'

    class Meta:
        verbose_name = 'B'
        verbose_name_plural = 'Bs'

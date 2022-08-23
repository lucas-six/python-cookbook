# Django - Database: PostgreSQL

## Dependencies

- PostgreSQL *11+*.
See [PostgreSQL - Setup](https://leven-cn.github.io/python-cookbook/recipes/web/postgresql_setup)
and [PostgreSQL CLI - Usage](https://leven-cn.github.io/python-cookbook/recipes/web/postgresql_usage).

```toml
# pyproject.toml

dependencies = [
    "psycopg2 >= 2.8",
]
```

```bash
pipenv install 'psycopg2>=2.8'
pipenv install --dev types-psycopg2
```

## Settings

```python
# settings.py

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['<db_name>'],
        'USER': os.environ['<user_name>'],
        'PASSWORD': os.environ['<password>'],
        'HOST': '127.0.0.1',
        'PORT': '5432',

        # Enable persistent database connections.
        # `None` for unlimitied persistent database connections.
        # Use `0` (default) to close database connections at the end of each request.
        'CONN_MAX_AGE': 60,  # in seconds.

        # Setting `CONN_HEALTH_CHECKS` to `True` can be used to improve the robustness of
        # connection reuse and prevent errors when a connection has been closed by the
        # database server which is now ready to accept and serve new connections.
        # Since Django 4.1
        'CONN_HEALTH_CHECKS': True,
    },
}
```

## Models

```python
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
    sex2 = models.CharField('sex', max_length=8, choices=SexType.choices, blank=True)

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
```

See [Python source code](https://github.com/leven-cn/python-cookbook/blob/main/django_project/example_app/models.py).

## Run

```bash
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

pipenv run python manage.py createsuperuser

pipenv run python manage.py runserver [localhost:8000]
```

## SQLs

```sql
CREATE TABLE IF NOT EXISTS public.example_app_a
(
    id bigint NOT NULL DEFAULT nextval('example_app_a_id_seq'::regclass),

    uuid uuid NOT NULL,

    name character varying(64) COLLATE pg_catalog."default" NOT NULL,
    nickname character varying(64) COLLATE pg_catalog."default" NOT NULL,
    sex character varying(8) COLLATE pg_catalog."default" NOT NULL,
    sex2 character varying(8) COLLATE pg_catalog."default" NOT NULL,

    age smallint,
    balance numeric(8,2) NOT NULL,
    score integer NOT NULL,

    is_active boolean NOT NULL,
    created_time timestamp with time zone NOT NULL,
    updated_time timestamp with time zone NOT NULL,

    CONSTRAINT example_app_a_pkey PRIMARY KEY (id),
    CONSTRAINT example_app_a_uuid_key UNIQUE (uuid),
    CONSTRAINT example_app_a_age_check CHECK (age >= 0),
    CONSTRAINT example_app_a_score_check CHECK (score >= 0)
);


CREATE TABLE IF NOT EXISTS public.example_app_b
(
    id bigint NOT NULL DEFAULT nextval('example_app_b_id_seq'::regclass),
    a_id bigint NOT NULL,
    CONSTRAINT example_app_b_pkey PRIMARY KEY (id),
    CONSTRAINT example_app_b_a_id_9a9a6b60_fk_example_app_a_id FOREIGN KEY (a_id)
        REFERENCES public.example_app_a (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS example_app_b_a_id_9a9a6b60
    ON public.example_app_b USING btree
    (a_id ASC NULLS LAST)
    TABLESPACE pg_default;
```

See [SQL source code](https://github.com/leven-cn/python-cookbook/blob/main/data/django_postgresql.sql).

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Home](https://www.postgresql.org/)
- [`psycopg` Home](https://www.psycopg.org/)

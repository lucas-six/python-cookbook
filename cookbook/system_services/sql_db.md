# SQL Database: `SQLModel` + `Alembic`

## Recipes (PostgreSQL)

```bash
uv add psycopg[binary] sqlmodel alembic alembic-postgresql-enum
```

```bash
uv run alembic init --template pyproject alembic
```

```python
# alembic/env.py

from sqlmodel import SQLModel
import alembic_postgresql_enum
from app.db_models import XXXModel

target_metadata = SQLModel.metadata
```

```mako
# alembic/script.py.mako

import sqlmodel
```

```bash
uv run alembic revision --autogenerate -m "Initial migration."
uv run alembic upgrade head

# rollback to the previous migration
uv run alembic downgrade -1

# show migration history
uv run alembic history

# show the current revision
uv run alembic current
```

## References

- [**`SQLModel`** - SQL database ORM, powered by `Pydantic` and `SQLAlchemy`](https://sqlmodel.tiangolo.com/)
- [**`Alembic`** - SQL database migration tool](https://alembic.sqlalchemy.org/)
- [*`SQLAlchemy`* - SQL database ORM](https://www.sqlalchemy.org/)
- [**`Psycopg`** PostgreSQL database adapter](https://www.psycopg.org/)

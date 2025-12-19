# `pymongo` - Python Driver for MongoDB

## Start

See [MongoDB Overview - Linux Cookbook](https://lucas-six.github.io/linux-cookbook/cookbook/admin/mongodb/mongodb_overview)
and [MongoDB on Ubuntu - Linux Cookbook](https://lucas-six.github.io/linux-cookbook/cookbook/admin/mongodb/mongodb_ubuntu).

```bash
uv add pymongo
```

## Usage

```python
import logging

import pymongo
from pymongo import AsyncMongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult, UpdateResult


MONGO_URL = 'mongo://xxx'

mongo_client: AsyncMongoClient = AsyncMongoClient(MONGO_URL)
mongo_db = mongo_client['database-name']
tb_users = mongo_db['table-name']

# create index
await tb_users.create_index(
    [('login_name', pymongo.ASCENDING)], unique=True, name='unique_login_name'
)

# find one
user_doc = await tb_users.find_one({'login_name': 'xxx'})
if user_doc is None:
    logging.error('not exists')

# insert one
try:
    rsp1: InsertOneResult = await tb_users.insert_one({'login_name': 'xxx'})
except DuplicateKeyError:
    logging.error('duplicated key')
logging.info(f'id={rsp1.inserted_id}')

# update one
try:
    rsp2: UpdateResult = await tb_users.update_one(
        {'login_name': 'xxx', '$set': {'login_name': 'yyy'}})
except DuplicateKeyError:
    logging.error('duplicated key')
if rsp2.modified_count != 1:
    logging.error('update failed')


# transaction
try:
    async with await mongo_client.start_session() as session:
        async with session.start_transaction():
            await tb_users.insert_one(
                {'login_name': 'a'}, session=session
            )
            await tb_users.insert_one(
                {'login_name': 'b'}, session=session
            )
except DuplicateKeyError:
    logging.error('transaction failed')
```

## More

- [MongoDB Overview - Linux Cookbook](https://lucas-six.github.io/linux-cookbook/cookbook/admin/mongodb/mongodb_overview)
- [MongoDB on Ubuntu - Linux Cookbook](https://lucas-six.github.io/linux-cookbook/cookbook/admin/mongodb/mongodb_ubuntu)
- [MongoDB TLS - Linux Cookbook](https://lucas-six.github.io/linux-cookbook/cookbook/admin/mongodb/mongodb_tls)
- [CLI: **`mongosh`** Usage - Linux Cookbook](https://lucas-six.github.io/linux-cookbook/cookbook/admin/mongodb/mongodb_usage)

## References

- [MongoDB Python Driver](https://www.mongodb.com/docs/drivers/python/)
- [**`Beanie`** - Async Python ODM for MongoDB, based on `Pydantic`](https://beanie-odm.dev/)

# PostgreSQL Usage

## Basic

```bash
su - postgres

# connect
psql [-U <username>] <db_name>

# quit
> \q
```

## User

```bash
> \du

createuser -P <username>
> create user <username> password '<password>';

dropuser <username>
> drop user <username>;

> create role <username> password '<password>' LOGIN;

> alter user <username> password '<password>';
```

## Database

```bash
> \l

createdb -O<username> -Eutf8 <db_name>
> create database <db_name> owner <username>;

dropdb <db_name>
> drop database <db_name>;

> alter database <db_name> owner to <username>;

> revoke all on database <db_name> from public;
> grant all on database <db_name> to public;
```

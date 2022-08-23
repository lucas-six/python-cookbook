# PostgreSQL - Setup

## Basic Concepts

- Relational Database Management System, **RDBMS** (关系型数据库管理系统)
- Structured Query Language, **SQL** (结构化查询语言)
- **ACID**: Atomicity(原子性), Consistency(一致性), Isolation(隔离性), Durability(持久性)
- **Transaction** (事务)

## Installation

### Ubuntu

```bash
apt install apt apt-utils python-apt-common python3-apt systemd
apt install curl ca-certificates gnupg
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt update
apt install postgresql-12 libpq-dev
```

### CentOS

#### System Repo

```bash
# Client
dnf install -y postgresql12 postgresql12-devel

# Server
dnf install -y postgresql12-server systemd
/usr/pgsql-12/bin/postgresql-12-setup initdb
systemctl enable postgresql-12
```

#### Official Repo

```bash
dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf makecache

# 禁用不必要的源
dnf module list postgresql
dnf config-manager --disable pgdg11
dnf config-manager --disable pgdg10
dnf config-manager --disable pgdg96
dnf config-manager --disable pgdg95
dnf module disable postgresql  # 禁用系统自带的源

# Client
dnf install -y postgresql12 postgresql12-devel

# Server
dnf install -y postgresql12-server postgresql12-contrib systemd
/usr/pgsql-12/bin/postgresql-12-setup initdb
systemctl enable postgresql-12
```

```bash
# /etc/bashrc

export PATH="/usr/pgsql-12/bin:$PATH"
```

```bash
systemctl start postgresql-12
```

## Configuration

```conf
# /etc/postgresql/12/main/postgresql.conf

#listen_addresses = 'localhost'  # '*' for all
#port = 5432
max_connections = 4096
password_encryption = scram-sha-256  # md5 or scram-sha-256

shared_buffers = 256MB  # 128MB

client_encoding = 'UTF8'
```

```ini
# /etc/postgresql/12/main/pg_hba.conf

host all all 127.0.0.1/32 scram-sha-256

host all all all　　       scram-sha-256
```

```bash
systemctl enable|disable postgresql
systemctl start|stop|restart|status postgresql
```

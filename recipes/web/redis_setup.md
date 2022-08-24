# Redis - Setup

## Basic Concepts

- Key-Value Cache/DB (键值缓存/数据库)
- Use Case: Cache

## Installation

For both Ubuntu and CentOS:

```bash
apt install redis systemd
```

## Configuration

```conf
# /etc/sysctl.d/30-redis.conf

vm.swappiness = 0
vm.overcommit_memory = 1
net.core.somaxconn = 4096
net.core.netdev_max_backlog = 4096
net.ipv4.tcp_max_syn_backlog = 4096
```

```bash
systemctl restart procps.service
```

```conf
# /etc/security/limits.d/redis.conf

redis  soft  nofile  65535
redis  hard  nofile  65535
```

```conf
# /etc/redis/redis.conf

#bind 0.0.0.0
protected-mode yes
tcp-backlog <4096>
appendonly yes
```

```bash
echo never > /sys/kernel/mm/transparent_hugepage/enabled

systemctl start|stop|status|restart redis
```

```bash
# Ubuntu
systemctl enable|disable redis-server
systemctl start|stop|restart|status redis-server

# CentOS
systemctl enable|disable redis
systemctl start|stop|restart|status redis
```

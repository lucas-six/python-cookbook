# Uvicorn

## Recipes

```bash
pip install 'uvicorn[standard]'
```

```json
/* uvicorn_logging.json */

{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": null
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr"
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": [
                "default"
            ],
            "level": "INFO",
            "propagate": false
        },
        "uvicorn.error": {
            "level": "ERROR"
        },
        "uvicorn.debug": {
            "level": "DEBUG"
        },
        "uvicorn.access": {
            "handlers": [
                "access"
            ],
            "level": "INFO",
            "propagate": false
        }
    }
}
```

```bash
uvicorn --host 0.0.0.0 --port 8000 \
    --proxy-headers \
    --forwarded-allow-ips "*" \
    --workers 8 \
    --limit-concurrency 1024 \
    --backlog 4096 \
    --log-level info \
    --timeout-keep-alive 5 \
    --no-use-colors \
    --no-server-header \
    app.main:app --log-config uvicorn_logging.json
```

## References

- [`uvicorn` Home](https://www.uvicorn.org/)

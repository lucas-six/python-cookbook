# `aiomqtt` - Python Asyncio APIs for MQTT

## Set Up

```toml
# pyproject.toml

dependencies = [
    "aiomqtt",
]
```

```bash
pipenv install aiomqtt
```

## Usage

```python
"""MQTT `aiomqtt` Usage.
"""

import asyncio
import os
import sys

import aiomqtt

MQTT_HOST = 'localhost'
MQTT_TOPIC_PREFIX = 'python-cookbook'


async def main():
    async with aiomqtt.Client(MQTT_HOST, timeout=3.5) as client:

        # Subscribe
        await client.subscribe(f'{MQTT_TOPIC_PREFIX}/#')
        async for message in client.messages:
            if isinstance(message.payload, bytes):
                print(message.payload.decode('utf-8'))

        # Publish
        # await client.publish(f'{MQTT_TOPIC_PREFIX}/example', payload={'msg': 'hello'})


# Change to the "Selector" event loop if platform is Windows
if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import WindowsSelectorEventLoopPolicy  # type: ignore
    from asyncio import set_event_loop_policy

    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

asyncio.run(main())
```

## References

- [`aiomqtt` Documentation](https://sbtinstruments.github.io/aiomqtt/index.html)

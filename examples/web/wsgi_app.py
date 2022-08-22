"""WSGI (Web Server Gateway Interface) Application.

Copyright (c) 2015-2022 Li Yun <leven.cn@gmail.com>
All Rights Reserved.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import annotations

import json
import mimetypes
import sys
import time
from http import HTTPStatus
from pathlib import Path
from typing import Any, BinaryIO, Callable


def application(
    environ: dict[str, Any],
    start_response: Callable[[str, list[tuple[str, str]]], None],
) -> list[bytes]:
    assert environ['wsgi.version'] == (1, 0)
    assert environ['wsgi.url_scheme'] in ('https', 'http')
    assert environ['wsgi.input'] == sys.stdin.buffer
    assert environ['wsgi.errors'] == sys.stderr
    assert isinstance(environ['wsgi.multithread'], bool)
    assert isinstance(environ['wsgi.multiprocess'], bool)
    assert isinstance(environ['wsgi.run_once'], bool)
    assert environ['SERVER_PROTOCOL'] in ('HTTP/1.1', 'HTTP/2')
    assert environ['HTTPS'] in ('on', '1')
    assert isinstance(environ['CONTENT_LENGTH'], str)
    assert isinstance(environ['CONTENT_TYPE'], str)

    # req_uri = environ['REQUEST_URI']
    req_path: str = environ['PATH_INFO']
    req_method: str = environ['REQUEST_METHOD']

    root_path = Path('.')
    rsp = []
    rsp_status = HTTPStatus.OK
    rsp_content: str | bytes = ''
    rsp_content_type = 'text/plain; charset=utf-8'
    rsp_headers = []

    # Dispatcher (URL Routing)
    if req_path == '/':
        rsp = [b'Hello world']
    elif req_path.endswith('.html'):
        rsp_path = root_path / req_path[1:]
        rsp_content = rsp_path.read_text(encoding='utf-8')
        rsp = [rsp_content.encode('utf-8')]
    elif req_path.endswith(('.png', '.jpg')):
        rsp_path = root_path / req_path[1:]
        rsp_content = rsp_path.read_bytes()
        _type = mimetypes.guess_type(rsp_path)[0]
        rsp_content_type = (
            f'image/{rsp_path.suffix.removeprefix(".")}' if _type is None else _type
        )
        rsp = [rsp_content]
    elif req_path.endswith('.json'):  # json
        rsp_content = json.dumps(
            {'a': 1, 'b': '你好', 'time': time.time()}, ensure_ascii=False
        )
        rsp_content_type = 'application/json'
        rsp = [rsp_content.encode('utf-8')]
    elif req_method == 'POST':
        req_input: BinaryIO = environ['wsgi.input']
        req_content_len = int(environ['CONTENT_LENGTH'])
        req_content = req_input.read(req_content_len).decode('utf-8')
        req_content_type = environ['CONTENT_TYPE']
        print(req_content, req_content_type)
        rsp = [b'']
    # elif req_path.endswith('.ws'):  # websocket
    #   import uwsgi
    #   uwsgi.websocket_handshake()
    #   while True:
    #       uwsgi.websocket_send(
    #           json.dumps({'a': 1, 'b': '你好', 'time': time.time()}, ensure_ascii=False)
    #       )
    #       msg = uwsgi.websocket_recv()
    #   rsp = [msg]
    else:
        rsp_status = HTTPStatus.NOT_FOUND

    status = f'{rsp_status.value} {rsp_status.phrase}'
    rsp_headers = [('Content-Type', rsp_content_type)]
    start_response(status, rsp_headers)
    return rsp

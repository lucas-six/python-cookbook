# `curl` - Command Line URL Request for HTTP

## GET

```bash
curl --connect-timeout 3.5 <url>

# querystring: ?q=python&count=20&comment=hello%20world
curl -G -d 'q=python' -d 'count=20' --data-urlencode 'comment=hello world' <url>
```

## POST

### JSON

```bash
curl --json @<data.json> -X POST <url>
curl --json @- -X POST <url> < data.json
```

automatically set the following headers:

```http
Content-Type: application/json
```

### Form

```bash
-d 'param1=val1&param2=val2'
-d 'param1=val1' -d 'param2=val2'
--data-urlencode 'comment=hello world'
```

automatically set the following headers:

```http
Content-Type: application/x-www-form-urlencoded
```

## Header

```bash
-H 'Accept: application/json'
--header 'Accept: application/json'
```

## Upload

```bash
curl -X PUT --upload-file <file.png>
```

```bash
-F 'fileparam=@<file.png>;filename=<target.png>'
```

automatically set the following headers:

```http
Content-Type: multipart/form-data
```

```bash
-F 'fileparam=@<file.png>;type=image/png;filename=<target.png>'
```

automatically set the following headers:

```http
Content-Type: application/octet-stream
```

## User Agent

```bash
# = -H 'User-Agent: curl/7.1'
-A 'curl/7.1'
```

## Cookie

```bash
-b <cookie-file> or 'key=val;key2=val2'
--cookie <cookie-file> or 'key=val;key2=val2'

-c <cookie-file>
--cookie-jar <cookie-file>
```

## Range

```bash
-r 0-1024
```

## Referer

```bash
# = -H 'Referer: https://google.com?q=example'
-e 'https://google.com?q=example'
```

## Redirect (3XX)

```bash
-L
```

## Proxy

```bash
-x http://proxy
--proxy http://proxy
```

## Bypass Server TLS/SSL certificate verification

```bash
-k
```

## Transfer-Encoding: chunked

```bash
--chunked
```

```http
Transfer-Encoding: chunked
```

## Download

```bash
curl -C - -L --parallel --parallel-max 100 --max-time 30 --retry 3 -o <download-file> <url>
```

### Speed Limit

```bash
--limit-rate 10K
```

## HTTP Version

```bash
# Since 7.47.0, the curl tool enables HTTP/2 by default for HTTPS connections.
# `--http3`: experimental
--http1.1
--http2
--http3
```

## TCP Keep-Alive

```bash
--keepalive-time 15
```

## Multiple Transfers With A Single Command Line

```bash
-O <url1> -O <url2>
```

## Python Bindings

**`PycURL`** is a Python interface to *`libcurl`*.

```bash
pip install pycurl
```

## References

- [`curl` Home](https://curl.se)
- [cURL Cookbook](https://catonmat.net/cookbooks/curl)
- [`PycURL` Home](https://pycurl.io)

# `httpie` - Command-Line HTTP Client

## Compare to `curl`

- colorful
- user-friendly
- GUI App
- plugin support

## GET

```bash
http --timeout 3.5 <url>

# querystring: ?q=python&count=20&comment=hello%20world
http <url> q==python count==20 comment=='hello world'
http <url> q==@<path.txt>
```

## POST

### JSON

```bash
http POST <url> param1=val1 param2=val2

http POST <url> < <path.json>

http POST <url> \
    param1=val1 \                      # String (default)
    age:=29 \                          # Raw JSON — Number
    married:=false \                   # Raw JSON — Boolean
    hobbies:='["http", "pies"]' \      # Raw JSON — Array
    favorite:='{"tool": "HTTPie"}' \   # Raw JSON — Object
    bookmarks:=@<path.json> \          # Embed JSON file
    description=@<path.txt>            # Embed text file
```

automatically set the following headers:

```http
Content-Type: application/json
Accept: application/json, */*;q=0.5
```

### Form

```bash
http --form POST <url> param1=val1 param2=val2 comment='hello world'
```

```http
POST <url> HTTP/1.1
Content-Type: application/x-www-form-urlencoded; charset=utf-8

param1=val1&param2=val2&comment=hello+world
```

### Multipart

```bash
http --multipart --offline <url> hello=world
```

```http
POST / HTTP/1.1
Content-Length: 129
Content-Type: multipart/form-data; boundary=c31279ab254f40aeb06df32b433cbccb
Host: example.org

--c31279ab254f40aeb06df32b433cbccb
Content-Disposition: form-data; name="hello"

world
--c31279ab254f40aeb06df32b433cbccb--
```

## Header

### Default

```http
GET / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
User-Agent: HTTPie/<version>
Host: <taken-from-URL>
```

### Custom

```bash
https pie.dev/headers User-Agent:Bacon/1.0 'Cookie:valued-visitor=yes;foo=bar' \
    Referer:https://httpie.org/

http pie.dev/headers X-Data:@<path.txt>
```

```http
GET /headers HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Cookie: valued-visitor=yes;foo=bar
Host: pie.dev
Referer: https://httpie.org/
User-Agent: Bacon/1.0
```

## Upload

```bash
http -f POST <url> param=val fileparam@<path.png>

http -f POST <url> param=val fileparam@'<path.png>;type=image/png;filename=<target.png>'
```

automatically set the following headers:

```http
Content-Type: multipart/form-data
```

## Authentication

### Basic Auth

```bash
http -a <username> <url>
```

### Digest auth

```bash
http -A digest -a <username> <url>
```

### Bearer auth

```bash
http -A bearer -a <username> <url>
```

### `.netrc`

```bash
$ cat ~/.netrc
machine pie.dev
login httpie
password test
```

### Auth Plugins

- httpie-api-auth: ApiAuth
- httpie-aws-auth: AWS / Amazon S3
- httpie-edgegrid: EdgeGrid
- httpie-hmac-auth: HMAC
- httpie-jwt-auth: JWTAuth (JSON Web Tokens)
- httpie-negotiate: SPNEGO (GSS Negotiate)
- httpie-ntlm: NTLM (NT LAN Manager)
- httpie-oauth1: OAuth 1.0a
- requests-hawk: Hawk

## Redirect (3XX)

```bash
--follow

# show intermediary process
--follow --all

# default 30
--max-redirects=2
```

## Proxy

```bash
http --proxy=http:http://10.10.1.10:3128 --proxy=https:https://10.10.1.10:1080 example.org
```

## Bypass Server TLS/SSL certificate verification

```bash
--verify=no
```

## Download

```bash
http -dco <download-file> <url>
```

`-dco` = `--download` + `--continue` + `--output`

`--download` always implies `--follow`, and `--check-status`.

## Session

```bash
--session=<path.json>

# ~/.config/httpie/sessions/<host>/<name>.json
--session=<name>

--session-read-only=<path.json>
```

## Plugin

```bash
httpie cli check-updates

httpie cli plugins install httpie-plugin
httpie cli plugins list
httpie cli plugins upgrade httpie-plugin
httpie cli plugins uninstall httpie-plugin
```

## References

- [`httpie` Home](https://httpie.io)

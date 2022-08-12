# Cross-Site Request Forgery (CSRF) (跨站请求伪造)

**CSRF** (**Cross-Site Request Forgery**), also known as **one-click attack**, **XSRF**
or **session riding**,
is an attack that impersonates a trusted user and sends a website unwanted or unauthorized commands.

## Protection Solution

### 1. Cookie Hashing

```http
Set-Cookie: csrftoken=xxxxxx; Secure; HttpOnly; SameSite=Strict
```

### 2. One-Time CSRF Tokens

```html
<meta name="csrf-token" content="{{ csrf_token }}">
```

or

```html
<form method="POST" action="transfer.php">
  <input type="hidden" name="csrf-token" value="{{ csrf_token }}">
  <input type="text" name="toBankId">
  <input type="text" name="money">
  <input type="submit" name="submit" value="Submit">
</form>
```

### 3. XSS Prevention

## References

- [MDN - CSRF](https://developer.mozilla.org/en-US/docs/Glossary/CSRF)
- [Wikipedia - Cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery)

# 💬 BiteWire

BiteWire is a simple, secure chat application that allows users to connect to hosted servers, communicate in real-time, and manage their own server through a separate application.

---
<img width="2050" height="1166" alt="image" src="https://github.com/user-attachments/assets/739d7fd9-0331-481a-b9bb-69e7f64af4ca" />

## ⚙️Server Setup

To host a BiteWire server, you need SSL certificate for encrypted connections.
Here is an example of self generated certificate:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365
```

<img width="530" height="658" alt="image" src="https://github.com/user-attachments/assets/9bcda007-8efb-43c4-9da7-d4d6174b464d" />

⚠️Disclaimer
This project is in an early stage of developement.
Bugs and missing features may be present.

⭐ Support
If you like the project, consider giving it a star ⭐

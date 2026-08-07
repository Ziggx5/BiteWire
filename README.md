# 💬 BiteWire
![Client](https://img.shields.io/badge/component-client-blue)
![Version](https://img.shields.io/badge/version-2.2.0-blue)
![Server](https://img.shields.io/badge/component-server-green)
![Version](https://img.shields.io/badge/version-2.1.0-green)
![License](https://img.shields.io/badge/license-GPL--3.0-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![Downloads](https://img.shields.io/github/downloads/Ziggx5/BiteWire/total)

BiteWire is a simple, secure chat application that allows users to connect to hosted servers, communicate in real-time, and manage their own server through a dedicated server application.

---
<img width="1920" height="1154" alt="image" src="https://github.com/user-attachments/assets/c7461c37-9762-4612-b032-5eff1b46b360" />

## ⚙️ Server Setup

### 1. Generate TLS certificate

To host a BiteWire server, a TLS certificate is required for encrypted connections.
Example of a self signed certificate:

### Windows
Download and install <a href = https://git-scm.com/>Git</a>.
Then open **Git Bash** and run:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365 -nodes
```

### Linux
Most Linux distributions already have ```openssl``` installed.
Open terminal and generate self signed certificate:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365 -nodes
```
During setup you may be asked questions which can be skipped by pressing enter.
After certificate generation two files will be created:
```server.key```
```server.crt```

After that, open the server app, click the folder button and drag generated files into opened folder.

### 2. Port forward
Make sure port ```50505``` is open on your router.
- for local (LAN) usage, this step is not required
- for external connections, port forwarding is necessary

<img width="928" height="632" alt="image" src="https://github.com/user-attachments/assets/ea7aaf7f-eb14-439e-9b58-d8566c1b4915" />

## 📦 Downloads

<table>
  <tr>
    <th> / </th>
    <th>Windows (.exe)</th>
    <th>Debian (.deb)</th>
    <th>Red Hat (.rpm)</th>
  </tr>
  <tr>
    <td>BiteWire 2.2.0</td>
    <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/c2.2.0/BiteWire.exe">⬇️ Download</a></td>
    <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/c2.2.0/bitewire_2.2.0_amd64.deb">⬇️ Download</a></td>
      <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/c2.2.0/bitewire-2.2.0-1.x86_64.rpm">⬇️ Download</a></td>
  </tr>
  <tr>
  <td>BiteWire Server 2.1.0</td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s2.1.0/BiteWire.Server.exe">⬇️ Download</a></td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s2.1.0/bitewire-server_2.1.0_amd64.deb">⬇️ Download</a></td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s2.1.0/bitewire-server-2.1.0-1.x86_64.rpm">⬇️ Download</a></td>
  </tr>
</table>

## ⚠️ Disclaimer

This project is still in an early stage of development.

Bugs and missing features may be present.

## ⭐ Support

If you like the project, consider giving it a star ⭐

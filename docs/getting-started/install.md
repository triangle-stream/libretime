---
title: Installation
sidebar_position: 1
---

## Minimum system requirements

- One of the following Linux distributions
  - Ubuntu [current LTS](https://wiki.ubuntu.com/Releases)
  - Debian [current stable](https://www.debian.org/releases/)
- 1 Ghz Processor
- 2 GB RAM recommended (1 GB required)
- A static IP address for your server

## Preparing the server

Configure the server to have a static IP address by modifying the Netplan configuration.

```bash
cd /etc/netplan && ls  # find the netplan filename
sudo nano ##-network-manager-all.yaml
```

If the Netplan configuration is empty, fill in the file with the example below. Otherwise,
input the IP address reserved for the server in `xxx.xxx.xxx.xxx/yy` format, the gateway (the IP address
of your router), and your DNS server's address.

:::tip

Don't have a DNS server of your own? You can use a public DNS server like Google (`8.8.8.8`) or Cloudflare (`1.1.1.1`), or input your router's address in most cases.

:::

:::caution

Do not use tabs in YAML files. Use two spaces to indent instead.

:::

```yaml title="Netplan configuration on Ubuntu"
network:
  version: 2
  renderer: networkd
  ethernets:
    enp3s0:
      addresses: [192.168.88.8/24]
      gateway4: 192.168.88.1
      nameservers:
        addresses: [192.168.88.1]
```

After the netplan file has been saved, run `sudo netplan apply` to apply changes.

Next, configure Ubuntu's firewall by running:

```bash
sudo ufw enable
sudo ufw allow 22,80,8000/tcp
```

:::info

Unblock ports 8001 and 8002 if you plan to use LibreTime's Icecast server to broadcast livestreams without an external Icecast server acting as a repeater.

```bash
sudo ufw allow 8001,8002/tcp
```

:::

## Installing LibreTime

<iframe width="560" height="315" src="https://www.youtube.com/embed/Djo_55LgjXE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Installing LibreTime consists of running the following commands in the terminal:

```bash
git clone https://github.com/LibreTime/libretime.git
cd libretime

sudo bash install -fiap
```

After the install is completed, head to the IP address of the server LibreTime was just installed on
to complete the welcome wizard. While not strictly necessary, it is recommended that you change the passwords prompted in the welcome wizard if you intend on accessing the server from the Internet. The welcome wizard will
walk you through the rest of the installation process.

## Services

Once all of the services needed to run LibreTime are installed and configured,
it is important that the server starts them during the boot process, to cut down on downtime, especially in live environments.
Ubuntu 18.04 uses the `systemctl` command to manage services, so run the following commands to enable all
LibreTime-needed services to run at boot:

```bash
sudo systemctl enable libretime-liquidsoap
sudo systemctl enable libretime-playout
sudo systemctl enable libretime-celery
sudo systemctl enable libretime-analyzer
sudo systemctl enable apache2
sudo systemctl enable rabbitmq-server
```

:::tip

If an error is returned, try adding `.service` to the end of each command.

:::

## User permissions

If you plan to have LibreTime output analog audio directly to a mixing console or transmitter,
the `www-data` user needs to be added to the `audio` user group using the command below:

```
sudo adduser www-data audio
```

---
title: Local development
---

## Vagrant

To use Vagrant, you need to install a virtualization engine: [VirtualBox](https://www.virtualbox.org) or Libvirt. The [vagrant-vbguest] package on Github can help maintain guest extensions on host systems using VirtualBox.

:::tip

If you try run a libvirt provided box after using a VirtualBox one, you will receive an
error:

```
Error while activating network:
Call to virNetworkCreate failed: internal error: Network is already in use by interface vboxnet0.
```

This is fixed by stopping virtualbox and re-creating the vagrant box:

```bash
sudo systemctl stop virtualbox
vagrant destroy ubuntu-bionic
vagrant up ubuntu-bionic --provider=libvirt
```

:::

### Installing Libvirt

On Debian and Ubuntu:

1. Install Vagrant

```bash
sudo apt install vagrant vagrant-libvirt libvirt-daemon-system vagrant-mutate libvirt-dev
sudo usermod -aG libvirt $USER
```

2. Reboot your computer, and then run

```bash
vagrant box add bento/ubuntu-18.04 --provider=virtualbox
vagrant mutate bento/ubuntu-18.04 libvirt
vagrant up ubuntu-bionic --provider=libvirt
```

On other distributions, you will need to install [libvirt](https://libvirt.org/) and `vagrant-mutate` and then run

```bash
vagrant plugin install vagrant-libvirt
sudo usermod -a -G libvirt $USER

# Reboot

vagrant plugin install vagrant-mutate
vagrant box fetch bento/ubuntu-18.04
vagrant mutate bento/ubuntu-18.04 libvirt
vagrant up ubuntu-bionic --provider=libvirt
```

### Starting LibreTime Vagrant

To get started you clone the repo and run `vagrant up`. The command accepts a parameter to
change the default provider if you have multiple installed. This can be done by appending
`--provider=virtualbox` or `--provider=libvirt` as applicable.

```bash
git clone https://github.com/libretime/libretime.git
cd libretime
vagrant up ubuntu-bionic
```

If everything works out, you will find LibreTime on [port 8080](http://localhost:8080)
and Icecast on [port 8000](http://localhost:8000).

Once you reach the web setup GUI you can click through it using the default values. To
connect to the vagrant machine you can run `vagrant ssh ubuntu-bionic` in the libretime
directory.

### Alternative OS installations

With the above instructions LibreTime is installed on Ubuntu Bionic. The Vagrant setup
offers the option to choose a different operation system according to you needs.

| OS           | Command                      | Comment                                                     |
| ------------ | ---------------------------- | ----------------------------------------------------------- |
| Debian 10    | `vagrant up debian-buster`   | Install on Debian Buster.                                   |
| Debian 11    | `vagrant up debian-bullseye` | Install on Debian Bullseye.                                 |
| Ubuntu 18.04 | `vagrant up ubuntu-bionic`   | Install on Ubuntu Bionic Beaver.                            |
| Ubuntu 20.04 | `vagrant up ubuntu-focal`    | Install on Ubuntu Focal Fossa.                              |
| CentOS       | `vagrant up centos`          | CentOS 8 with native systemd support and activated SELinux. |

### Troubleshooting

If anything fails during the initial provisioning step you can try running `vagrant provision`
to re-run the installer.

If you only want to re-run parts of the installer, use `--provision-with $step`. The
supported steps are `prepare` and `install`.

## Multipass

[Multipass](https://multipass.run) is a tool for easily setting up Ubuntu VMs on Windows, Mac, and Linux.
Similar to Docker, Multipass works through a CLI. To use, clone this repo and then create a new Multipass VM.

```
git clone https://github.com/libretime/libretime.git
cd libretime
multipass launch bionic -n ltTEST --cloud-init cloud-init.yaml
multipass shell ltTEST
```

Multipass isn't currently able to do an automated install from the cloud-init script.
After you enter the shell for the first time, you will still need to [run the LibreTime installer](/docs/getting-started/install).

The IP address of your new VM can be found by running `multipass list`. Copy and paste it into your web browser to access the LibreTime interface and complete the setup wizard.

You can stop the VM with `multipass stop ltTEST` and restart with `multipass start ltTEST`.
If you want to delete the image and start again, run `multipass delete ltTEST && multipass purge`.

### Cloud-init options in cloud-init.yaml

You may wish to change the below fields as per your location.

```yaml
timezone: America/New York # change as needed
ntp:
  pools: ["north-america.pool.ntp.org"]
  servers: ["0.north-america.pool.ntp.org", "0.pool.ntp.org"]
```

# Password Strength Calculator

Script calculate password strength based on multiple criteria.

# Quickstart

The script requires the installed Python interpreter version 3.x.
You have to run the script with the `-p`, `--password` argument with the password.
To call the help, run the script with the `-h` or `--help` option.

```bash
$ python3 password_strength.py -h
usage: password_strength.py [-h] -p PASSWORD

optional arguments:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        set password
```
Example of script launch on Linux, Python 3.6:

```bash
$ python3 password_strength.py -p BeN34Fe#^X
Password strength is: 7/10
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

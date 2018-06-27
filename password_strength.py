import re
import base64
import argparse
import requests

MIN, OK, GOOD = (5, 8, 11)


def load_passwords_blacklist(blacklist_url):
    response = requests.get(blacklist_url)
    if response.ok:
        encoded_content = response.json().get('content')
        decoded_content = base64.decodebytes(bytes(encoded_content, 'utf-8')).decode("utf-8")
        blacklist_passwords = decoded_content.split('\n')
        return blacklist_passwords
    else:
        print('Content was not found.')
        return None


def get_password_strength(password, blacklist_passwords):
    return sum([
        has_both_cases(password),
        has_digit(password),
        is_not_in_blacklist(password, blacklist_passwords),
        has_special_characters(password),
        check_length(password),
        is_not_contain_email(password),
        is_not_contain_phone_number(password),
        is_not_contain_date(password),
    ])


def is_not_contain_date(password):
    date_regex = \
        r'([12]\d{3}[-/\s\.](0[1-9]|1[0-2])[-/\s\.](0[1-9]|[12]\d|3[01]))|' \
        r'((0[1-9]|[12]\d|3[01])[-/\s\.](0[1-9]|1[0-2])[-/\s\.][12]\d{3})'
    return False if re.match(date_regex, password) else True


def is_not_contain_phone_number(password):
    phone_regex = \
        r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$'
    return False if re.match(phone_regex, password) else True


def is_not_contain_email(password):
    email_regex = \
        r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return False if re.match(email_regex, password) else True


def check_length(password):
    if len(password) < MIN:
        return 0
    elif MIN <= len(password) < OK:
        return 1
    elif OK <= len(password) < GOOD:
        return 2
    else:
        return 3


def is_not_in_blacklist(password, blacklist_passwords):
    return password not in blacklist_passwords


def has_special_characters(password):
    special_characters = r"[_`~!@#$%\^&*()\-+=/{\}\[\]\\|;':\",.<>?]"
    return True if re.match(special_characters, password) else False


def has_both_cases(password):
    if re.match('[A-Z]', password) and re.match('[a-z]', password):
        return True
    else:
        return False


def has_digit(password):
    return any(char.isdigit() for char in password)


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help='set password',
        required=True,
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_command_line_args()
    blacklist_url = 'https://api.github.com/repos/{}/{}/contents/{}'.format(
        'danielmiessler',
        'SecLists',
        '/Passwords/darkweb2017-top10000.txt',
    )
    blacklist_passwords = load_passwords_blacklist(blacklist_url)
    password_strength = get_password_strength(
        args.password,
        blacklist_passwords,
    )
    print('Password strength is: {}/10'.format(password_strength))

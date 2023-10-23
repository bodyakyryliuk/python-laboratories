import argparse
import datetime
import json
import smtplib
import requests
import bs4


def send_mail(message):
    sender1 = 'Bohdan Kyryliuk'
    smtpSrv = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtpSrv.starttls()

    sender = read_json()[0]
    password = read_json()[1]
    receiver = 'wojciech.thomas@pwr.edu.pl'
    recipients = [receiver]
    time = datetime.datetime.now()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    subject = 'Lab message sent on <' + formatted_time + '>'
    try:
        smtpSrv.login(sender, password)
        smtpSrv.sendmail(sender, recipients, f"From: {sender1}\nSubject: {subject}\n{message}")
        smtpSrv.close()
        print('The message has been sent successfully!')
    except Exception as e:
        print(e)


def read_json():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config['email'], config['password']


def get_cat_facts(amount):
    url = f"https://cat-fact.herokuapp.com/facts/"
    params = {"amount": f"{amount}"}

    response = requests.get(url, params)

    if response.status_code == 200:
        data = response.json()
        i = 0
        for text in data:
            print(text["text"])
            i += 1
            if i == amount:
                break
    else:
        print("Error: Could not retrieve facts")


def get_researchers(letter):
    url = f"https://wit.pwr.edu.pl/wydzial/struktura-organizacyjna/pracownicy?letter={letter}"
    response = requests.get(url)
    html_content = response.text

    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    researchers = soup.find_all('div', {'news-box'})
    if len(researchers) == 0:
        print("There are no researchers starting with letter", letter)
    else:
        for researcher in researchers:
            title = researcher.find('a', {'class': 'title'})
            if title:
                print(title.get_text())
            email = researcher.find('p')
            if email:
                print(email.get_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mail', help='send an email with the message')
    parser.add_argument('--cat-facts', type=int, help='get facts about cats')
    parser.add_argument('--teachers', type=str, help='get list of researchers')

    args = parser.parse_args()

    if args.mail:
        send_mail(args.mail)

    if args.cat_facts:
        get_cat_facts(args.cat_facts)

    if args.teachers:
        get_researchers(args.teachers)


if __name__ == '__main__':
    main()



#python lab9.py --mail "hello"
#python lab9.py --cat-facts 5
#python lab9.py --teachers b

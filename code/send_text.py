__author__ = 'notme'

#from twilio.rest import TwilioRestClient
from twilio import rest
import csv

def read_auth():
    with open("..\\auth.txt") as auth:
        auth_reader = csv.DictReader(auth)
        for row in auth_reader:
            if row['Variable'] == 'account_sid':
                account_sid = row['Value']
            else:
                auth_token = row['Value']
        #print account_sid, auth_token
    return account_sid, auth_token


def get_numbers(to):
    #with open("..\\test_numbers.txt") as auth:
    with open("..\\numbers.txt") as auth:
        number_reader = csv.DictReader(auth)
        for row in number_reader:
            print "to = ", to
            print row
            if row['Client'] == 'from':
                from_number = row['Phone Number']
            elif row['Client'] == to:
                print row
                to_number = row['Phone Number']

    #print to_number, from_number
    return to_number, from_number

def send_text(body, to_number, from_number, auth):
    # Your Account Sid and Auth Token from twilio.com/user/account

    account_sid = auth[0]
    auth_token = auth[1]

    '''
    print account_sid
    print auth_token
    print "auth[0] = ", auth[0]
    print "auth[1] = ", auth[1]
    '''

    client = rest.TwilioRestClient(account_sid, auth_token)

    body = client.messages.create(body=body,
                                     to=to_number,
                                     from_=from_number)
    print body.sid
    print "Sent Text To:"
    print to_number
    print "Message Text Follows:"
    print body



def build_message_body(party_name, case_number, date_time, location):
    global message_body
    message_body = party_name + '\n\n' + \
                   'Your Hearing for:\n' + \
                   '   Case Number: ' + case_number + '\n\n' + \
                   'Will be held: ' + date_time + '\n\n' + \
                   'In: ' + location + '\n'
    #print message_body
    return message_body


if __name__ == "__main__":
    # read_auth gets the sid and token
    auth = read_auth()

    defendant = 'AAGAARD, KATHIE J'

    # Odyssey has the court dates.
    filename = "Odyssey-JobOutput-June 01, 2016 06-32-43-1609654-3.TXT"
    with open("..\\data\\Odyssey" + '\\' + filename) as ody:
        reader = csv.DictReader(ody)

        for row in reader:
            if row['Party Name'] == defendant:
                party_name = row['Party Name']
                location = row['Hearing Location']
                date_time = row['Hearing Date/Time']
                case_number = row['Case Number']

    message_body = build_message_body(party_name, case_number,
                                      date_time, location)

    #to = 'Me'
    #clients = ['Tracey Cell', 'Jo', 'Me', 'Eric', 'Phil', 'Jessica', 'Chris', 'Al', 'Antonio']
    #clients = ['Me']
    clients = ['Antonio']
    for client in clients:
        to_number, from_number = get_numbers(client)
        print to_number, from_number
        send_text(message_body, to_number, from_number, auth)

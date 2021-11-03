from PyInquirer import prompt
import csv

user_questions = [
    {
        "type":"input",
        "name":"username",
        "message":"New User - Name: ",
    },
    {
        "type":"input",
        "name":"age",
        "message":"New User - Age: ",
    },
    {
        "type":"input",
        "name":"balance",
        "message":"New User - Balance: ",
    },
]

def add_user():
    # This function should create a new user, asking for its name
    # What a nice idea !
    infos = prompt(user_questions)
    
    with open('user_list.csv', 'a', newline='') as csvfile:
        fieldnames = ['username', 'age', 'balance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writer.writeheader()
        writer.writerow(infos)

    print("User Added !")
    return

def get_users():
    user_list = []
    with open('user_list.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_list.append(row)

    return user_list
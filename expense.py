from PyInquirer import prompt
from user import get_users
import csv

expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount: ",
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label: ",
    },
    {
        "type":"list",
        "name":"spender",
        "message":"New Expense - Spender: ",
        "choices": []
    },
    {
        "type":"checkbox",
        "name":"involved",
        "message":"New Expense - Involved People (spender will be automatically added): ",
        "choices": []
    },
]

status_question = [
    {
        "type":"checkbox",
        "name":"payed",
        "message": "Current debt status - Select a line to mark it as payed: ",
        "choices": []
    }
]



def new_expense(*args):
    # Get users
    expense_questions[2]['choices'] = []
    for row in get_users():
        obj = {"name": row['username']}
        expense_questions[2]['choices'].append(obj)
        expense_questions[3]['choices'].append(obj)

    infos = prompt(expense_questions)
    # Writing the informations on external file might be a good idea ¯\_(ツ)_/¯
    # That's right !
    if (infos == {}):
        return

    if (not infos['spender'] in infos['involved']):
        infos['involved'].append(infos['spender'])
    with open('expense_report.csv', 'a', newline='') as csvfile:
        fieldnames = ['amount', 'label', 'spender', 'involved', 'payed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writer.writeheader()
        writer.writerow(infos)

    print("Expense Added !")
    return True

def get_expense():
    expense_list = []
    import csv
    with open('expense_report.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            expense_list.append(row)
    return expense_list

def overwrite_expense(expenses):
    with open('expense_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['amount', 'label', 'spender', 'involved', 'payed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in expenses:
            writer.writerow(row)

def parse_involved_list(x):
    if x == '':
        return
    while x[0] == ' ':
        x = x[1:]
    return x[1:][:-1]

# Taken from https://stackoverflow.com/questions/2793324/is-there-a-simple-way-to-delete-a-list-element-by-value (jfs' answer)
def remove_all(seq, value):
    pos = 0
    for item in seq:
        if item != value:
           seq[pos] = item
           pos += 1
    del seq[pos:]


def pay_debt(in_debt, spender):
    expense_list = get_expense()
    for row in expense_list:
        payed_list = [] if row['payed'] == None else row['payed'][1:][:-1].split(',')
        payed_list = list(map(parse_involved_list, payed_list))
        payed_list.append(in_debt)
        row['payed'] = payed_list
        
        involved_list = row['involved'][1:][:-1].split(',')
        involved_list = list(map(parse_involved_list, involved_list))
        row['involved'] = remove_all(involved_list, in_debt)
    overwrite_expense(expense_list)

def status_report():
    while True:
        expense_list = get_expense()
        user_reimbursements = []
        for row in expense_list:
            involved_list = row['involved'][1:][:-1].split(',')
            debt = float(row['amount']) / len(involved_list)
            for involved in involved_list:
                if involved == '':
                    continue
                # Remove spaces at the begining
                while involved[0] == ' ':
                    involved = involved[1:]
                # Remove quotes
                involved = involved[1:][:-1]
                if involved == row['spender']:
                    continue
                obj = {
                    "in_debt": involved,
                    "spender": row['spender'],
                    "debt": debt
                }
                user_reimbursements.append(obj)
        
        # Print status
        status_question[0]['choices'] = []
        for in_debt in get_users():
            for spender in get_users():
                if in_debt == spender:
                    continue
                debt_list = [x for x in user_reimbursements if x['in_debt'] == in_debt['username'] and x['spender'] == spender['username']]
                amount = sum(x['debt'] for x in debt_list)
                amount_str = str(amount) + '€' if amount != 0 else 'nothing'
                status_row = in_debt['username'] + ' owes ' + amount_str + ' to ' + spender['username']
                status_question[0]['choices'].append({'name': status_row})

        status_question[0]['choices'].append({'name': 'Exit'})
        infos = prompt(status_question)

        if 'Exit' in infos['payed']:
            return
        
        for selected in infos['payed']:
            selected_splitted = selected.split(' ')
            if 'nothing' in selected_splitted:
                continue
            pay_debt(selected_splitted[0], selected_splitted[-1])

from PyInquirer import prompt
from examples import custom_style_2
from expense import expense_questions,new_expense, status_report
from user import add_user

def ask_option():
    main_option = {
        "type":"list",
        "name":"main_options",
        "message":"Expense Tracker v1",
        "choices": ["New Expense","Show Status","New User","Exit"]
    }
    option = prompt(main_option)
    if (option['main_options']) == "New Expense":
        new_expense()
        ask_option()
    if (option['main_options']) == "Show Status":
        status_report()
        ask_option()
    if (option['main_options']) == 'New User':
        add_user()
        ask_option()
    if (option['main_options']) == 'Exit':
        print("Goodbye!")
        return

def main():
    ask_option()

main()
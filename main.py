import os,csv,pandas as pd
from Login import login
from signUp import sign_up
from ForgotPassword import forgot_pass
from Query import query

user_database='/Users/bhoomi/Documents/GitHub/DBMS/user_database.csv'

print('Hello...')
def greet():
    choice=int(input(f'\nEnter your choice: \n 1. Login\n 2. Sign Up\n 3. Forgot Passsword\n 0. Exit\nYour choice: '))
    return choice

if __name__=='__main__':
    while True:
        choice=greet()
        match choice:
            case 1:
                # is_valid,username=login()
                # while not is_valid:
                #     is_valid,username=login()
                # query(username)
                query('bhoomi')
            case 2:
                sign_up()
                print('\nLogin:\n')
                is_valid=login()
                while not is_valid:
                    is_valid=login()
                query()
            case 3:
                forgot_pass()
            case _:
                print('_')

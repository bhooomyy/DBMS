import os,pandas as pd,csv
import hashlib
user_database='/Users/bhoomi/Documents/GitHub/DBMS/user_database.csv'

def validate_username(username):
    if os.path.exists(user_database):
        df=pd.read_csv(user_database)
        if username in df['username'].values:
            print('user already exists...')
            return False
    return True
    
            
def validate_password(password):
    special_char='@#$%^&*+=-~`'
    has_capital_char=any(char.isupper() for char in password)
    cnt=0
    for index in range(0,len(password)):
        if not password[index].isdigit():
            cnt+=1
    has_8char=(cnt>=8)
    has_digit=any(digit.isdigit() for digit in password)
    has_special_char=(char in special_char for char in password)
    if(has_capital_char and has_digit and has_8char and has_special_char):
        return True
    else:
        print(' 1. Password must contain atleast 1 capital letter.\n 2. password must contains atleast 1 digit.\n 3. password must has 8 characters.\n 4. password has atleast 1 special character.')
        return False

def validate_re_entered_password(password,re_entered_password):
    if validate_password(password) and password==re_entered_password:
        return True
    else:
        if(not validate_password(password)):
            print('Unmatched password criteria\n')
            print(' 1. Password must contain atleast 1 capital letter.\n 2. password must contains atleast 1 digit.\n 3. password must has 8 characters.\n 4. password has atleast 1 special character.')
        elif password!=re_entered_password:
            print('password mis match error!')
        return False

def validate_email(email):
    if email=="":
        return True
    if (' ' in email) or ('@' not in email and email.count('@')>1) or ('.' not in email):
        print('Invalid password type! Must be in username@domain.extension format...')
        return False
    else:
        return True

def sign_up():
    username=input('Enter username: ')
    if validate_username(username):
        password=input('Enter password: ')
        if validate_password(password):
            re_enterpassword=input('Re enter password: ')
            if validate_re_entered_password(password,re_enterpassword):
                email=input('Enter email: ')
                if validate_email(email):
                    if not os.path.exists(user_database):
                        with open(user_database,mode='w',newline='') as file:
                            writer=csv.writer(file)
                            writer.writerow(['username','password','email'])
                            password=hashlib.sha256(password.encode()).hexdigest()
                            writer.writerow([username,password,email])
                            print(f'{username} added successfully!')
                    else:
                        with open(user_database,mode='a',newline='') as file:
                            writer=csv.writer(file)
                            password=hashlib.sha256(password.encode()).hexdigest()
                            writer.writerow([username,password,email])  
                            print(f'{username} added successfully!')
    else:
        print('\n')
        sign_up()
    

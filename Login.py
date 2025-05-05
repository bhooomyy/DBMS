import pandas as pd
import hashlib
user_database='/Users/bhoomi/Documents/GitHub/DBMS/user_database.csv'

def login():
    username=input('Enter username: ')
    password=input('Enter password: ')
    password=hashlib.sha256(password.encode()).hexdigest()
    df=pd.read_csv(user_database)
    if username in df['username'].values:
        row=df[df['username']==username]
        if password==row.iloc[0]['password']:
            print(f'Welcome back {username}')
            return True,username
    else:
        print('Invalid username or password')
        return False,None


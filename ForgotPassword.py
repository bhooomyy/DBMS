from signUp import validate_password
import pandas as pd,os,csv,hashlib
user_database='/Users/bhoomi/Documents/GitHub/DBMS/user_database.csv'

def forgot_pass():
    username=input('Enter username: ')
    df=pd.read_csv(user_database)
    if os.path.exists(user_database):
        if username in df['username'].values:
            new_password=input('Enter new password: ')
            while not validate_password(new_password):
                new_password=input('Enter new password: ')
            new_password=hashlib.sha256(new_password.encode()).hexdigest()
            df.loc[df['username']==username,'password']=new_password
            df.to_csv(user_database,index=False)
        else:
            print('No such user exists...')
import os,pandas as pd,csv
#table_path='/Users/bhoomi/Documents/GitHub/DBMS/'
def select_query(query,username):
    if '*' in query:
        chunk=query.strip().split(' ')
        if chunk[2].lower()=='from':
            table_path=os.path.join(os.getcwd(), username, f"{chunk[3]}.csv")
            #os.path.join(os.path.join(os.getcwd(),username),chunk[3]+'.csv')
            print(pd.read_csv(table_path))
    elif ',' in query:
        chunk=query.strip().split(',')
    else:
        chunk=query.strip().split(' ')
        table_path=os.path.join(os.getcwd(), username, f"{chunk[3]}.csv")
        df=pd.read_csv(table_path)
        print(df[chunk[1]].values)
        
def create_query(query,username):
    if '(' in query and ')' in query:
        temp=query.split('(')
        table_name=temp[0].strip().split(' ')[-1]
        table_path=os.path.join(os.getcwd(), username, table_name+".csv")
        if os.path.exists(table_path):
            print('Table already exists...')
        else:
            table_defination=temp[1].strip(')').strip().split(',')
            column_name=[]
            column_type=[]
            for column_def in table_defination:
                parts=column_def.strip().split()
                if len(parts)!=2:
                    print('Invalid query. Please check syntax...Expected "CREATE TABLE <table_name>(column_name1 column_type1,column_name2 columns_type2,...)"')
                    return
                column_name.append(parts[0])
                column_type.append(parts[1])
            with open(table_path,mode='w',newline='') as file:
                writer=csv.writer(file)
                header=[]
                for name,type in zip(column_name,column_type):
                    header.append(f"{name}.{type}")
                writer.writerow(header)
        
    elif ((')' in query) and ('(' not in query)) or ((')' not in query) and ('(' in query)):
        print('Invalid query. Please check syntax...Expected "CREATE TABLE <table_name>(column_name1 column_type1,column_name2 columns_type2,...)"')
    else:
        chunk=query.strip().split(' ')
        table_path=os.path.join(os.getcwd(), username, f"{chunk[2]}.csv")
        if os.path.exists(table_path):
            print('Table already exists...')
        else:
            with open(table_path,mode='w',newline='') as file:
                writer=csv.writer(file)
                print('Empty table created!')


def query(username):
    while True:
        query=input('\nPress enter to End the session...\nEnter query: ')
        if not query:
            return False
        command=query.strip().split(' ')
        if command[0].lower()=='select':
            select_query(query,username)
        elif command[0].lower()=='create':
            create_query(query,username)
        # elif command[0].lower=='insert':
        #     insert_query(query,username)
        # elif command[0].lower=='delete':
        #     delete_query(query,username)
        # else:
        #     print('Not a valid query format')
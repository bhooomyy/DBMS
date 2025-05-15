import os,pandas as pd,csv
#table_path='/Users/bhoomi/Documents/GitHub/DBMS/'
        
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

def insert_query(query,username):
    table_name=query.strip().split('(')[0].split(' ')[2].strip(' ')
    if (query.strip().split(' ')[1]!='into') or ((query.count('(')!=2) and (query.count(')')!=2)) or ('values' not in query.lower()):
        print('Error: Invalid query format... Expected "INSERT INTO <table_name>(column_name1,column_name2,...) VALUES (column_value1, columns_value2,...)')
        return False
    temp=query.strip().split('(')[1].split(')')[0]
    requested_columns=temp.strip().split(',')
    temp=query.strip().split('(')[2].split(')')[0]
    requested_col_values=temp.strip().split(',')
    if len(requested_columns)!=len(requested_col_values):
        print('Number of requested columns are not same as number of requested values')
        return
    table_path=os.path.join(os.getcwd(),username,table_name+'.csv')
    result=[]
    if os.path.exists(table_path):
        df=pd.read_csv(table_path)
        df_columns=[col.split('.')[0] for col in df.columns]
        df_col_type=[col.split('.')[1] for col in df.columns]
        for col in requested_columns:
            if col not in df_columns:
                print(f'Error {col} doesn\'t exist in table...')
                return
        isValid=True
        for index in range(len(df_columns)):
            csv_columns=df_columns[index]
            csv_col_type=df_col_type[index]
            if(csv_columns in requested_columns):
                value=requested_col_values[requested_columns.index(csv_columns)]
                try:
                    if(csv_col_type.lower()=='integer'):
                        if '.' in value:
                            print(f"{csv_columns} only accept integer type. You are passing float value. type mismatch error...")
                            isValid=False
                            break
                        if "'" in value:
                            print(f"{csv_columns} only accept integer type. You are passing string or varchar. type mismatch error...")
                            isValid=False
                            break
                        if '-' in value:
                            print(f"{csv_columns} only accept integer type. You are passing Negative value which is not acceptable. type mismatch error...")
                            isValid=False
                            break
                        if value.isdigit():
                            result.append(int(value))
                    elif csv_col_type.lower()=='float':
                        if "'" in value:
                            print(f"{csv_columns} only accept float type. You are passing string or varchar. type mismatch error...")
                            isValid=False
                            break
                        if '.' not in value and value.isdigit():
                            print(f"{csv_columns} only accept float value. You are passing integer value. type mismatch error...")
                            isValid=False
                            break
                        if value.replace('.', '', 1).isdigit():
                            result.append(float(value))
                    elif(csv_col_type.lower()=='string' or csv_col_type.lower()=='varchar'):
                        if '.' in value and value.replace('.', '', 1).isdigit():
                            print(f"{csv_columns} only accept string type. You are passing float value. type mismatch error...")
                            isValid=False
                            break
                        if value.isdigit():
                            print(f"{csv_columns} only accept string. You are passing integer type. type mismatch error...")
                            isValid=False
                            break
                        if (value.startswith("'") and value.endswith("'")):
                            result.append(value)
                        else:
                            print(f"{csv_columns} only accept string or varchar type. ' is missing. type mismatch error...")
                            isValid=False
                            break
                except ValueError:
                    return False
            else:
                if csv_col_type.lower()=='string' or csv_col_type.lower()=='varchar':
                    result.append('NONE')
                else:
                    result.append('NULL')
                
        if isValid:
            with open(table_path,mode='a',newline='') as file:
                writer=csv.writer(file)
                writer.writerow(result)
                print('Row inserted!')
    else:
        print('No such table exists...')

def select_query(query,username):
    chunk=query.strip().split(' ')
    if len(chunk) < 4 or chunk[0] != 'select' or chunk[2] != 'from':
            print("Error: Invalid query format. Expected: SELECT <columns> FROM <table> [WHERE <conditions> (optional)]")
            return False
    if 'where' in query.lower():
        table_name=query.strip().split('from')[1].split('where')[0].strip(' ')
    else:
        table_name=query.strip().split('from')[1].strip(' ')

    table_path=os.path.join(os.getcwd(), username, table_name+".csv")
    df=pd.read_csv(table_path)
    col_name=[col.split('.')[0] for col in df.columns]
    df.columns=col_name
    if 'where' not in query:
        if '*' in query:
            print(df)
        elif ',' in query:
            columns=query.split('select')[1].split('from')[0]
            columns=columns.strip().split(',')
            print(columns)
            print(df[columns])
        else:
            requested_col=query.split('select')[1].split('from')[0].strip(' ')
            print(f"Index {requested_col}")
            print(df[requested_col])
    else:
        condition=query.split('where')[1].strip(' ')
        if '<>'in query or '!=' in query:
            if '<>' in query:
                condition=condition.split('<>')
            else:
                condition=condition.split('!=')
            condition_col=condition[0].strip()
            condition_col_value=condition[1].strip()
            print(f"{condition_col} {condition_col_value}")
            if condition_col not in df.columns:
                print(f"No such column exists named {condition_col} ok?")
                return
            filtered_df=df[df[condition_col].astype(str)!=condition_col_value]
            result=[]
            if '*' in query:
                print(filtered_df)
            elif ',' in query:
                columns=query.split('select')[1].split('from')[0]
                columns=columns.strip().split(',')
                print(filtered_df[columns])
            else:
                requested_col=query.split('select')[1].split('from')[0].strip(' ')
                print(f"Index {requested_col}")
                print(filtered_df[requested_col])
        elif '=' in query:
            condition=condition.strip(' ').split('=')
            condition_col=condition[0]
            condition_col_value=condition[1]
            if condition_col not in df.columns:
                print(f"No such column exists named {condition_col}")
                return
            filtered_df=df[df[condition_col].astype(str)==condition_col_value]
            if '*' in query:
                print(filtered_df)
            elif ',' in query:
                columns=query.split('select')[1].split('from')[0]
                columns=columns.strip().split(',')
                print(filtered_df[columns])
            else:
                requested_col=query.split('select')[1].split('from')[0].strip(' ')
                print(f"Index {requested_col}")
                print(filtered_df[requested_col])
        elif '<' in query:
            condition=condition.strip(' ').split('<')
            condition_col=condition[0]
            condition_col_value=condition[1]
            if condition_col not in df.columns:
                print(f"No such column exists named {condition_col}")
                return
            filtered_df=df[df[condition_col].astype(str)<condition_col_value]
            if '*' in query:
                print(filtered_df)
            elif ',' in query:
                columns=query.split('select')[1].split('from')[0]
                columns=columns.strip().split(',')
                print(filtered_df[columns])
            else:
                requested_col=query.split('select')[1].split('from')[0].strip(' ')
                print(f"Index {requested_col}")
                print(filtered_df[requested_col])
        elif '>' in query:
            condition=condition.strip(' ').split('>')
            condition_col=condition[0]
            condition_col_value=condition[1]
            if condition_col not in df.columns:
                print(f"No such column exists named {condition_col}")
                return
            filtered_df=df[df[condition_col].astype(str)>condition_col_value]
            if '*' in query:
                print(filtered_df)
            elif ',' in query:
                columns=query.split('select')[1].split('from')[0]
                columns=columns.strip().split(',')
                print(filtered_df[columns])
            else:
                requested_col=query.split('select')[1].split('from')[0].strip(' ')
                print(f"Index {requested_col}")
                print(filtered_df[requested_col])
        elif 'not in' in query.lower():
            condition_col=condition.split('not in')[0].strip(' ')
            condition=condition.split('(')[1].strip(')')
            if ',' in condition.lower():
                condition_col_val=condition.split(',')
            else:
                condition_col_val=condition
            filtered_df=df[~df[condition_col].astype(str).isin(condition_col_val)]
            if '*' in query:
                print(filtered_df)
            elif ',' in query:
                columns=query.split('select')[1].split('from')[0]
                columns=columns.strip().split(',')
                print(filtered_df[columns])
            else:
                requested_col=query.split('select')[1].split('from')[0].strip(' ')
                print(f"Index {requested_col}")
                print(filtered_df[requested_col])
        elif 'in' in query.lower():
            condition_col=condition.split('in')[0].strip(' ')
            condition=condition.split('(')[1].strip(')')
            if ',' in condition.lower():
                condition_col_val=condition.split(',')
            else:
                condition_col_val=condition
            filtered_df=df[df[condition_col].astype(str).isin(condition_col_val)]
            if '*' in query:
                print(filtered_df)
            elif ',' in query:
                columns=query.split('select')[1].split('from')[0]
                columns=columns.strip().split(',')
                print(filtered_df[columns])
            else:
                requested_col=query.split('select')[1].split('from')[0].strip(' ')
                print(f"Index {requested_col}")
                print(filtered_df[requested_col])
        

def update_query(query,username):
    print()

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
        elif command[0].lower()=='insert':
            insert_query(query,username)
        elif command[0].lower()=='update':
            update_query(query,username)
        # elif command[0].lower=='delete':
        #     delete_query(query,username)
        # else:
        #     print('Not a valid query format')
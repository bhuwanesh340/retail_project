from __future__ import print_function
import sqlite3
from sqlite3 import Error

def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file, timeout=10)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    print('CURRENT USER table created successfully')


def insert_current_user_detail(conn,input_user_id,dept_name):
    sql = ''' INSERT INTO curr_user_table (user_id,department)
		VALUES (?,?) '''
   
    cur = conn.cursor()
    
    try:
        cur.execute(sql,(input_user_id,dept_name))
        conn.commit()
        
    except sqlite3.IntegrityError:
        print('An user of same name is already logged in !!')

    except sqlite3.OperationalError:
        print('Database is locked, cant login now :( Please try later.')
        user_exit(conn)

    return cur.lastrowid


def user_exit(conn):
    cur = conn.cursor()
    sql = '''DROP TABLE curr_user_table'''
    sql_create_curr_user_table = """ CREATE TABLE IF NOT EXISTS curr_user_table ( 
					user_id text PRIMARY KEY,
					department text
		                        ); """
    try:
        cur.execute(sql)
        cur.execute(sql_create_curr_user_table)
        print('You have been logged out successfully !!')
    except sqlite3.OperationalError:
        print('Table not dropped')
    
    return cur.lastrowid

#********************************************
#main function
#********************************************

def curr_user_login_main():
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"

    sql_create_curr_user_table = """ CREATE TABLE IF NOT EXISTS curr_user_table ( 
					user_id text PRIMARY KEY,
					department text
		                        ); """
  
    conn = create_connection(database)
    if conn is not None:
        
        create_table(conn, sql_create_curr_user_table)
    else:
        print("Error! cannot create the database connection.")

#********************************************************************

if __name__ == '__main__':
    curr_user_login_main()

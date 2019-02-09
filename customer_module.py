from __future__ import print_function
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, timeout=10)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    print('CUSTOMER table created successfully')

#*******************************************
#insert data function
#*******************************************

def insert_cust_data(conn,customer_id,total_amount,purchase_dt,discount_offer):
#ip_ct_id,ttl_amt,cr_dt,ip_dsc_ofr
#metadata- customer_id,total_amount,purchase_dt,discount_offer

#CHANGED
    sql = ''' INSERT INTO cust_details (customer_id,total_amount,purchase_dt,discount_offer)
		VALUES (?,?,?,?) '''
   
    cur = conn.cursor()

    #cur.execute(sql,(customer_id,total_amount,purchase_dt,discount_offer)) changed for python 2 below
    cur.execute(sql,(str(customer_id),total_amount,purchase_dt,discount_offer))
    conn.commit()
    return cur.lastrowid


def select_all_cust_data(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM cust_details ")
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

#*************************************************
#**** SELECT CUST DATA IN A FORMAT ********************

def select_all_cust_data_query2(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM cust_details ")
    rows = cur.fetchall()
    
    print("*"*45)
    print("| CUSTOMER_ID | TOTAL_AMOUNT | PURCHASE_DATE | DISCOUNT_OFFER |")
    for row in rows:
        print("| {} | {} | {} | {} |".format(row[0],row[1],row[2],row[3]))

    print("*"*45)
    


#*************************************************


#***************************************************************************************************
#***************************************************************************************************

def cust_details_main():
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"

    sql_create_customer_table = """ CREATE TABLE IF NOT EXISTS cust_details (
                                        customer_id text NOT NULL,
					total_amount float NOT NULL,
					purchase_dt date,
					discount_offer integer
		                        ); """
  
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create grocery billing table
        create_table(conn, sql_create_customer_table)
    else:
        print("Error! cannot create the database connection.")

    print('All customer data present in database')

    def check_name_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
        rows = cur.fetchall()
        return rows

    try:
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]
        print('{} !! is already logged in :) '.format(curr_logged_user_name))

        conn = create_connection(database)
        select_all_cust_data(conn)
        select_all_cust_data_query2(conn)

        import time
        print("Redirecting to Login Page ...")
        time.sleep(3)

        import home_page
        home_page.home_page(conn)

    except IndexError:
        print('No one is logged in, please login first !!')

        import time
        print("Redirecting to Login Page ...")
        time.sleep(3)

        import login_module
        login_module.login_page_main()
'''
#INSERTING TEST DATA FOR CUSTOMER RECOGNITION
    #insert_cust_data(conn,'BHUW_TEST_2017_10_08','0','',12.5)
    
    select_all_cust_data(conn)
    #import home_page
    #home_page.home_page(conn)
'''    

#********************************************************************

if __name__ == '__main__':
    cust_details_main()

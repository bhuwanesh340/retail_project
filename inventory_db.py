from __future__ import print_function
import sqlite3
from sqlite3 import Error
 
 
#**************************************************************************************
#CREATE TABLE QUERY

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


#*******************************************
#insert data function
#*******************************************

def insert_inventory_data(conn, inventory):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO inventory (prod_categ,prod_code, prod_name, prod_desc, prod_brand, quantity, unit_price)
		VALUES (?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    conn.commit()

    try:
        cur.execute(sql, inventory)

    except sqlite3.IntegrityError:
        print('ERROR: PROD_CATEG already exists in PRIMARY KEY column ')

    print('Insert query executed successfully')
    return cur.lastrowid

#*******************************************
#retrieve data function
#*******************************************


def select_all_data(conn):
    """
    Query all rows in the inventory table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory WHERE prod_code NOT IN (SELECT prod_code FROM inventory WHERE QUANTITY = '') ")

 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

#***********************************************************************
#fetch all inventory data query 2
#***********************************************************************


def select_all_inventory_data_query2(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory WHERE prod_code NOT IN (SELECT prod_code FROM inventory WHERE QUANTITY = '') ")
    rows = cur.fetchall()
    
    print("*"*120)
    print("| PRODUCT CATEGORY | PRODUCT CODE | PRODUCT NAME | PRODUCT DESCRIPTION | PRODUCT BRAND | QUANTITY | UNIT PRICE |")

    for row in rows:
        print("| {} | {} | {} | {} | {} | {} | {} |".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

    print("*"*120)


#********************************************
#main function
#********************************************

def inventory_main():
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    
    sql_create_inventory_table = """ CREATE TABLE IF NOT EXISTS inventory (
                                        prod_categ text NOT NULL,
                                        prod_code text PRIMARY KEY NOT NULL,
					prod_name text NOT NULL,
					prod_desc text NOT NULL,
					prod_brand text NOT NULL,
					quantity integer NOT NULL,
					unit_price integer
		                        ); """
  
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create inventory table
        create_table(conn, sql_create_inventory_table)
    else:
        print("Error! cannot create the database connection.")

    #********************** inserting data 

    def check_name_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
        rows = cur.fetchall()
        return rows

    try:
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]
        conn = create_connection(database)
        select_all_inventory_data_query2(conn)

        import home_page
        import time
        print("******************************************************************")
        print("Redirecting to Nu Grocery Store Home Page ...")
        time.sleep(5)
        home_page.home_page(conn)

    except IndexError:

        import login_module_tushar_methods_added as login_module
        login_module.login_page_main()

#*************************************************************************************************
#*************************************************************************************************

if __name__ == '__main__':
    inventory_main()


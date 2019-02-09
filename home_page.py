from __future__ import print_function
import sqlite3
from sqlite3 import Error
import datetime

def recognised_customers(names):
    for name in names:
        print('Identified customers are: ',name)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def user_logged_in(conn):
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
    rows = cur.fetchall()
    return rows

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
    except sqlite3.OperationalError:
        print('Table not dropped')
    
    print('You have been logged out successfully !!')
    return cur.lastrowid


#database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
conn = create_connection(database)
curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

def home_page(conn):
    print("********************************************************************")
    print("********************************************************************")
    print("****** WELCOME TO NIIT UNIVERSITY RETAIL STORE MANAGEMENT APP ******")
    print()
            
    try:
        if user_logged_in(conn) != '':
            print("Today is: {}                   Welcome {} !!      ".format(curr_date,user_logged_in(conn)[0][0]))

    except IndexError:
        print("Today is: {}                                        ".format(curr_date))
    
    print()        
    print('We have below options on the home page:')
    print('1. USER LOGIN')
    print('2. BILLING PAGE')
    print('3. INVENTORY DETAILS')
    print('4. STAFF DETAILS')
    print('5. SALES TRACKER')
    print('6. CUSTOMER DETAILS PAGE')
    print('7. LOG OUT')
    print('8. EXIT')
    print()
    print("********************************************************************")
    print('************************** HAVE A NICE DAY *************************')
    print("********************************************************************")

# ALWAYS CALLING FUNCTIONALITY

    x = int(input('Enter your response to go-to a page: '))
    
    if x == 1:
        conn.close()
        conn = create_connection(database)
        import login_module_tushar_methods_added as login_module
        login_module.login_menu(conn)
        
    if x == 2:
        conn.close()
        conn = create_connection(database)
        import billing_details_testing_face as billing_module
        billing_module.bill_detail_main()
        
    if x == 3:
        conn.close()
        conn = create_connection(database)
        import inventory_db as inventory_module
        inventory_module.inventory_main()

    if x == 4:
        conn.close()
        conn = create_connection(database)
        import staff_details_updated as staff_module
        staff_module.staff_details_main()
        
    if x == 5:
        conn.close()
        conn = create_connection(database)
        import sales_modules_updated_vidushi as sales_module
        sales_module.sales_data_main()

    if x == 6:
        conn.close()
        conn = create_connection(database)
        import customer_module
        customer_module.cust_details_main()
    
    if x == 7:
        conn.close()
        import current_user_db
        conn = create_connection(database)
        current_user_db.user_exit(conn)
        
        print("Logging out ...")
        import time
        time.sleep(3)
        home_page(conn)

    if x == 8:
        print("Have a nice day :)")


# ****************************************************************************

if __name__ == '__main__':
    home_page(conn)

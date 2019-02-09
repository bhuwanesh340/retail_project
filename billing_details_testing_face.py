from __future__ import print_function
import sqlite3
from sqlite3 import Error
import inventory_db as inventory_module
import datetime
from builtins import input
 

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



def search_prod_name(conn,input_prod_code):

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(prod_name) FROM inventory WHERE prod_code = ?", (input_prod_code,))
    rows = cur.fetchall()
    return rows


def search_prod_categ(conn,ip_prd_cat):

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(prod_categ) FROM inventory WHERE prod_categ = ?", (ip_prd_cat,))
    rows = cur.fetchall()
    return rows


def fetch_unit_price(conn,input_prod_code):

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(unit_price) FROM inventory WHERE prod_code = ?", (input_prod_code,))
    rows = cur.fetchall()
    return rows  


#*****************************************************************************************

def insert_aggregate_billing_table_data(conn,inv_no,ip_cust_id,disc_amt,cur_dat,bil_agnt,ttl_bil_amt):
    sql = '''INSERT INTO groc_billing_aggregate(invoice_number,customer_id,discount_offer,sys_date,bill_agent,total_bill_amt)
		VALUES (?,?,?,?,?,?) '''
  
    cur = conn.cursor()
    cur.execute(sql,(inv_no,ip_cust_id,disc_amt,cur_dat,bil_agnt,ttl_bil_amt))
    conn.commit()
    return cur.lastrowid


def insrt_grc_bil_indv_data(conn,inv_no,ip_prd_cat,ip_prd_cd,prd_nm_ftch,ip_cust_id,cur_dat,bil_agnt,ip_qt_prch,unt_prc,indv_amt,pymnt_md): 
    sql = '''INSERT INTO groc_billing_individual       	(invoice_number,prod_categ,prod_code,prod_name,customer_id,sys_date,bill_agent,quantity_purchased,unit_price,total_amt,pymnt_mode)
		VALUES (?,?,?,?,?,?,?,?,?,?,?) '''
  
    cur = conn.cursor()

    cur.execute(sql,(inv_no,ip_prd_cat,ip_prd_cd,prd_nm_ftch,ip_cust_id,cur_dat,bil_agnt,ip_qt_prch,unt_prc,indv_amt,pymnt_md))
    conn.commit()
    return cur.lastrowid

#*****************************************************************************************


def fetch_groc_table_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM groc_billing_aggregate")
    rows = cur.fetchall()
    for row in rows:
        print(row)
#********************************************

#main function
#********************************************

#******** face recognition for customer *********************************************
#FIND UNIQUE CUSTOMERS FROM THE TABLE

def list_of_all_customers(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(customer_id) FROM cust_details ")
    rows = cur.fetchall()
    #for row in rows:
        #print(row[0])
    
    return(rows)

#FETCH CUSTOMER ID

def recognised_customers(recognised_names):
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    conn = create_connection(database)
    existing_customers = list_of_all_customers(conn)
    #print("Existing customers are: ")
    #for row in range(0,len(existing_customers)):
    #    print(existing_customers[row][0])

    final_name = []
    for name in range(0,len(recognised_names)):
        #print("Identified customers are: ",recognised_names[name])
        #print("Existing customers are: ",existing_customers[name][0])
        for cust_name in range(0,len(existing_customers)):
            if recognised_names[name] == existing_customers[cust_name][0]:
                final_name.append(recognised_names[name])
                #print("Appended name is: ",final_name[0])
            else:
                continue
    
    return(final_name)

##########################################################################################



def bill_detail_main():
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    # create a database connection
    conn = create_connection(database)

#security feature

    def check_name_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
        rows = cur.fetchall()
        return rows

    try:
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]
        #print('{} !! is already logged in :) '.format(curr_logged_user_name))

        conn = create_connection(database)

        import bash_face_recog_module #call face recognition module
        bash_face_recog_module.call_face_reco_script()        

    except IndexError:
        print('No one is logged in, please login first and then come back here !!')   
        import time
        print("Redirecting to Login Utility Page ...")
        time.sleep(3)
        import login_module_tushar_methods_added as login_module
        login_module.login_page_main()



#*************************************************************************************
def bill_detail_main2(cust_id):
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    
    sql_create_aggregate_billing_table = """ CREATE TABLE IF NOT EXISTS groc_billing_aggregate (
                                        invoice_number text PRIMARY KEY,
					customer_id text NOT NULL,
					discount_offer integer,
					sys_date date,
                                        bill_agent text,
                                        total_bill_amt float
		                        ); """

    sql_create_individual_billing_table = """ CREATE TABLE IF NOT EXISTS groc_billing_individual (
                                        invoice_number text,
                                        prod_categ text NOT NULL,                       
                                        prod_code text NOT NULL,
					prod_name text NOT NULL,
					customer_id text NOT NULL,
					sys_date date,
                                        bill_agent text,
					quantity_purchased integer,
                                        unit_price float,
                                        total_amt float,
                                        pymnt_mode text
		                        ); """
    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        # create grocery billing table
        create_table(conn,sql_create_aggregate_billing_table)
        create_table(conn,sql_create_individual_billing_table)

    else:
        print("Error! cannot create the database connection.")

    #print('GROCERY BILLING table created successfully')

    #*****************************************************************

    if len(cust_id) == 0:
        ip_cust_id = input("Enter customer id for new user: ")

    else:    
        ip_cust_id = cust_id
        print("Recognised customer_id is: ",ip_cust_id)

    # generate invoice number
    import random
    inv_no = random.randint(100000,900000)
    
    #fetch billing agent detail

    def fetch_current_user_detail(conn):
        #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
        database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT(user_id) FROM curr_user_table")
        rows = cur.fetchall()
        #print('Current user is: ',rows)
        return rows

    bil_agnt = fetch_current_user_detail(conn)[0][0]
    print("Billing agent id: ",bil_agnt)

    cur_dat = datetime.datetime.now().strftime("%Y-%m-%d") #current date

    bill_exit = 0
    sub_total_bil_amt = 0
    
    while bill_exit != 1:
    
        ip_prd_cat = input('Enter Product category: ')
        #fetch product category from inventory
        #prod_cat_fetch = str(search_prod_categ(conn,ip_prd_cat)[0][0]) # create function to fetch product category
        while len(search_prod_categ(conn,ip_prd_cat)) == 0:
            ip_prd_cat = input('Enter Product category: ')

        #print('Product category is: ',prod_cat_fetch)

        ip_prd_cd = input('Enter Product code: ')
        #fetch prod_name from inventory module
        #return product name from inventory table
        while len(search_prod_name(conn,ip_prd_cd)) == 0:
            ip_prd_cd = input('Enter Product code: ')

        prd_nm_ftch = str(search_prod_name(conn,ip_prd_cd)[0][0])
        print('Product name is: ',prd_nm_ftch)
    
        ip_qt_prch = int(input('Enter quantity purchased: '))
    
        #fetch unit price of the product     
        unit_prc = int(fetch_unit_price(conn,ip_prd_cd)[0][0])
        print('Unit price of the product is: ',unit_prc)
    
        #calculate individual amount
        indv_amt = ip_qt_prch * unit_prc
        print('Price of current purchase is: ',indv_amt )

        #calculate sum price for each product 
        sub_total_bil_amt += indv_amt

        #ask for payment mode
        pymnt_md = input("Enter Payment mode (M- Cash ; C- Card): ")
        while pymnt_md not in ("M","C"):
            pymnt_md = input("Enter Payment mode (M- Cash ; C- Card): ")
    
	#enter the purchase details in a separate sales table
        insrt_grc_bil_indv_data(conn,inv_no,ip_prd_cat,ip_prd_cd,prd_nm_ftch,ip_cust_id,cur_dat,bil_agnt,ip_qt_prch,unit_prc,indv_amt,pymnt_md)
        
        bill_exit = int(input('If you want to stop billing ? Press 1: '))
        
    
    # billing counter ends here * check customer identification
    # call to customer identification module
    # import bash_face_recog_module
    # fetch customer id from the table
    # call face recognition module in the starting of the billing module
    
#    input_cust_id = input('Enter customer id:')                        commenting it now,as taking face as input
    
# write a logic for discount to new users and existing users
#discount option to be fetched from customer table


#calculate total amount

#calculate discount amount based on percentage   

    #inp_disc_per = int(input('Enter discount percentage:'))
 
    def evaluate_offer(conn,ip_cust_id):
        cur = conn.cursor()
        sql_query = '''SELECT DISTINCT(customer_id), SUM(total_bill_amt) FROM groc_billing_aggregate WHERE customer_id = ? GROUP BY customer_id
                    '''
        cur.execute(sql_query,(ip_cust_id,))
        rows = cur.fetchall()
        return rows

    try:
        sales_till_date = evaluate_offer(conn,ip_cust_id)[0][1] 
        print("Sales till date is: ",sales_till_date)   

    except:
        sales_till_date = 0

    if 0 <= sales_till_date < 1000: 
        inp_disc_per = 5
    elif 1000 <= sales_till_date < 5000:
        inp_disc_per = 7.5
    elif 5000 <= sales_till_date < 10000:
        inp_disc_per = 10
    else:
        inp_disc_per = 12.5

    print("Discount percent offered is: ",inp_disc_per)

    disc_amt = (((sub_total_bil_amt)*(float(inp_disc_per)))/100)
    ttl_bil_amt = (sub_total_bil_amt - disc_amt)

    print('Discount amount offered: %.2f' % disc_amt)
    print('                     **********')
    print('Total billable amount:', ttl_bil_amt)
    print('                     **********')
    
    #********************** insert bill data in customer table

    import customer_module as cust_module
    cust_module.insert_cust_data(conn,ip_cust_id,ttl_bil_amt,cur_dat,inp_disc_per)
    #cust_module.select_all_cust_data(conn) #prit data of customer module
#************** need to pass invoice numer here
    #calling function to isert grocery data
    insert_aggregate_billing_table_data(conn,inv_no,ip_cust_id,disc_amt,cur_dat,bil_agnt,ttl_bil_amt)

    #fetch_groc_table_data(conn)
    print()
    choice = int(input('Do you want to continue billing, enter 0 to continue 1 to go back to home page: '))
    print()
    while choice not in (0,1):
        choice = int(input('Do you want to continue billing, enter 0 to continue 1 to go back to home page: '))    
    
    else:
        if choice == 0:
            print()
            bill_detail_main()
            
        else:

            import home_page
            import time
            print("******************************************************************")
            print("Redirecting to Nu Grocery Store Home Page ...")
            time.sleep(5)
            home_page.home_page(conn)


#************************************************************

if __name__ == '__main__':
        bill_detail_main()
        


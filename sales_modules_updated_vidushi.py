from __future__ import print_function
import sqlite3
from sqlite3 import Error
from matplotlib import pyplot as plt
from matplotlib import interactive
interactive(True)
import datetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

    
def print_template():
    
    print("********************************************************")
    print()
    print('Options for the Sales Analysis:')
    print('1. Daily Sales')
    print('2. Monthly Sales')
    print('3. Top Customers In a Month')
    print('4. Product category graph')
    print('5. Return to Home Page')
    print()
    print("********************************************************")

# GENERIC ONES *********************************************************************************


def price(flag):
#database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    
    #database = "D:\\Study Material NIIT\\Programming Analytics\\Project\\database test-20180926T155412Z-001\\database test\\retail_app.db"
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if(flag == 'D'):
        sql_fetch_billing_data = """SELECT prod_categ, sum(total_amt) FROM groc_billing_individual WHERE sys_date = ? GROUP by prod_categ"""
    elif (flag == 'M'):
        sql_fetch_billing_data = """SELECT prod_categ,sum(total_amt) FROM groc_billing_individual WHERE sys_date > ? - 30 GROUP by prod_categ"""

    # create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # fetch data from billing table
        c = conn.cursor()
        c.execute(sql_fetch_billing_data,(curr_date,))
    else:
        print("Error! cannot create the database connection.")
    
    all_data = c.fetchall()
    
    #for row in all_data:
    print(all_data)

    prod_cat = []
    sum_price = []
    for i in range(0,len(all_data)):
        prod_cat.append(all_data[i][0])

    for i in range(0,len(all_data)):
        sum_price.append(all_data[i][1])

    print(prod_cat)
    print(sum_price)

    daily_graph(prod_cat,sum_price)



def category_sales(flag,product_cat):
#database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    
    #database = "D:\\Study Material NIIT\\Programming Analytics\\Project\\database test-20180926T155412Z-001\\database test\\retail_app.db"
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if(flag == 'D'):
        sql_fetch_billing_data = """SELECT prod_categ,sum(quantity_purchased) FROM groc_billing_individual WHERE sys_date = ? AND prod_categ = ? GROUP by prod_categ"""
#'" + product_cat + "'
    elif (flag == 'M'):
        sql_fetch_billing_data = """SELECT prod_categ,sum(quantity_purchased) FROM groc_billing_individual WHERE sys_date > ? - 30 AND prod_categ = ?  GROUP by prod_categ"""
#'" + product_cat + "'
    
    # create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # fetch data from billing table
        c = conn.cursor()
        c.execute(sql_fetch_billing_data,(curr_date,product_cat))
    else:
        print("Error! cannot create the database connection.")
    

    all_data = c.fetchall()
    
    #for row in all_data:
    print(all_data)

    prod_name = []
    sum_qty = []
    for i in range(0,len(all_data)):
        prod_name.append(all_data[i][0])

    for i in range(0,len(all_data)):
        sum_qty.append(all_data[i][1])

    print(prod_name)
    print(sum_qty)

    category_graph(prod_name,sum_qty,product_cat)




def payment(flag):
#database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    
    #database = "D:\\Study Material NIIT\\Programming Analytics\\Project\\database test-20180926T155412Z-001\\database test\\retail_app.db"
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if(flag == 'D'):
        sql_fetch_billing_data = """SELECT pymnt_mode, count(*) FROM groc_billing_individual WHERE sys_date = ? GROUP by pymnt_mode"""
    elif (flag == 'M'):
        sql_fetch_billing_data = """SELECT pymnt_mode, count(*) FROM groc_billing_individual WHERE sys_date > ? - 30 GROUP by pymnt_mode"""

    # create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # fetch data from billing table
        c = conn.cursor()
        c.execute(sql_fetch_billing_data,(curr_date,))
    else:
        print("Error! cannot create the database connection.")
    

    all_data = c.fetchall()
    
    #for row in all_data:
    print(all_data)

    payment_mode = []
    count = []
    for i in range(0,len(all_data)):
        payment_mode.append(all_data[i][0])

    for i in range(0,len(all_data)):
        count.append(all_data[i][1])

    print(payment_mode)
    print(count)

    daily_graph(payment_mode,count)


###############################################################################################################
# DAILY TEMPLATES
    
def daily_template():

    print("********************************************************")
    print()
    print('Options for the Daily Sales:')
    print('1. Based on Price')
    print('2. Based on Product Category')
    print('3. Based on Payment Mode')
    print()
    print("********************************************************")


def daily_sales():

    daily_template()

    x = int(input('Enter your response: '))

    flag = 'D'

    if x==1:
        price(flag)
    elif x==2:
        category(flag)
    elif x==3:
        payment(flag)
    else:
        print('Invalid input. Enter your response again')
        x = int(input('Enter your response: '))


# MONTHLY TEMPLATES

def monthly_template():

    print("********************************************************")
    print()
    print('Options for the Monthly Sales:')
    print('1. Based on Price')
    print('2. Based on Product Category')
    print('3. Based on Payment Mode')
    print()
    print("********************************************************")


def monthly_sales():

    monthly_template()

    x = int(input('Enter your response: '))

    flag = 'M'

    if x==1:
        price(flag)
    elif x==2:
        category(flag)
    elif x==3:
        payment(flag)
    else:
        print('Invalid input. Enter your response again')
        x = int(input('Enter your response: '))


# CATEGORY TEMPLATES

def category_template():

    print("********************************************************")
    print()
    print('Product Options:')
    print('1. GROCERIES')
    print('2. BABY_FOODS')
    print('3. BEVERAGES')
    print('4. FAST_FOODS')
    print('5. COSUMER_GOODS')
    print('6. STATIONERY')
    print()
    print("********************************************************")


def category(flag):

    category_template()

    x = int(input('Enter your response: '))

    product = ['GROCERIES','BABY_FOODS','BEVERAGES','FAST_FOODS','COSUMER_GOODS','STATIONERY']

    if x in range(0,6):
        category_sales(flag,product[x-1])
    else:
        print('Invalid input. Enter your response again')
        x = int(input('Enter your response: '))

# ***********************************************************************************************

def top_customer():
#database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"

    #database = "D:\\Study Material NIIT\\Programming Analytics\\Project\\database test-20180926T155412Z-001\\database test\\retail_app.db"
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

    sql_fetch_billing_data = """SELECT customer_id, sum(total_amount) FROM cust_details WHERE purchase_dt > ? - 30 AND rowid <=5 GROUP by customer_id ORDER by 2 DESC"""

    
    # create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # fetch data from billing table
        c = conn.cursor()
        c.execute(sql_fetch_billing_data,(curr_date,))
    else:
        print("Error! cannot create the database connection.")
    

    all_data = c.fetchall()
    
    #for row in all_data:
    print(all_data)

    cust_code = []
    #cust_name = []
    amount = []
    for i in range(0,len(all_data)):
        cust_code.append(all_data[i][0])

    #for i in range(0,len(all_data)):
        #cust_name.append(all_data[i][1])

    for i in range(0,len(all_data)):
        amount.append(all_data[i][1])
        

    print(cust_code)
    #print(cust_name)
    print(amount)

    customer_graph(cust_code,amount)




################################################################################################

#PRODUCT CATEGORY GRAPH

def product_categ_graph():
#database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"

    #database = "D:\\Study Material NIIT\\Programming Analytics\\Project\\database test-20180926T155412Z-001\\database test\\retail_app.db"
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")

    sql_fetch_billing_data = """SELECT DISTINCT(prod_categ), SUM(total_amt) FROM groc_billing_individual WHERE sys_date > ? - 30 GROUP  BY  prod_categ """

    
    # create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # fetch data from billing table
        c = conn.cursor()
        c.execute(sql_fetch_billing_data,(curr_date,))
    else:
        print("Error! cannot create the database connection.")
    
    all_data = c.fetchall()
    
    #for row in all_data:
    print(all_data)

    prod_category = []
    amount = []
    for i in range(0,len(all_data)):
        prod_category.append(all_data[i][0])

    for i in range(0,len(all_data)):
        amount.append(all_data[i][1])
        

    print(prod_category)
    print(amount)

    prod_category_graph(prod_category,amount)



######################################################################################################################################################
    

def daily_graph(labels,sizes):


    # Data to plot
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    # explode = (0, 0, 0, 0)
 
    # Plot
    plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=45)

    # function to show the plot
    plt.axis('on')
    plt.show(block = True)

    sales_data_main()


def customer_graph(labels,sizes):

      
    # plotting a bar chart 
    plt.bar(labels, sizes, width = 0.6, color = ['red', 'green']) 
      
    # naming the x-axis 
    plt.xlabel('Customer Name') 
    # naming the y-axis 
    plt.ylabel('Amount Spent') 
    # plot title 
    plt.title('Top Customers in a Month') 
      
    # function to show the plot
    plt.axis('on')
    plt.show(block = True)

    sales_data_main()

def prod_category_graph(labels,sizes):      

    # plotting a bar chart 

    plt.bar(labels, sizes, width = 0.6, color = ['red', 'green', 'blue']) 
    # naming the x-axis 

    plt.xlabel('Category Name') 

    # naming the y-axis 
    plt.ylabel('Amount Spent') 
    # plot title 
    plt.title('Top Categories in a Month') 
      
    # function to show the plot
    plt.axis('on')
    plt.show(block = True)

    sales_data_main()



def category_graph(labels,sizes,category):

      
    # plotting a bar chart 
    plt.bar(labels, sizes, width = 0.6, color = ['red', 'green']) 
      
    # naming the x-axis 
    plt.xlabel('Product Name') 
    # naming the y-axis 
    plt.ylabel('Quantity Sold') 
    # plot title
    t_title = "Sales of " + category
    plt.title(t_title) 
      
    # function to show the plot
    plt.axis('on')
    plt.show(block = True)

    sales_data_main()

#***********************************************************************************
#***********************************************************************************

def sales_data_main():

    print_template()

    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    conn = create_connection(database)

    def check_name_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
        rows = cur.fetchall()
        return rows

    try:
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]
        print('{} !! is already logged in :) '.format(curr_logged_user_name))

        x = int(input('Enter your response: '))

        if x==1:
            daily_sales()
        elif x==2:
            monthly_sales()
        elif x==3:
            top_customer()
        elif x==4:
            product_categ_graph()
        elif x==5:

            import time
            print("Redirecting to Login Page ...")
            time.sleep(3)

            import home_page
            home_page.home_page(conn)

        else:
            print('Invalid input. Enter your response again')
            x = int(input('Enter your response: '))        

    except IndexError:
        print('No one is logged in, please login first and then come back here !!')
        import login_module
        login_module.login_page_main()    

#***********************************************************************************
#***********************************************************************************

if __name__ == '__main__':
    sales_data_main()






#***********************************************************************************
#***********************************************************************************

def sales_data_main():

    print_template()

    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    conn = create_connection(database)

    def check_name_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
        rows = cur.fetchall()
        return rows

    try:
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]
        #print('{} !! is already logged in :) '.format(curr_logged_user_name))

        x = int(input('Enter your response: '))

        if x==1:
            daily_sales()
        elif x==2:
            monthly_sales()
        elif x==3:
            top_customer()
        elif x==4:
            product_categ_graph()
        elif x==5:
            import home_page

            home_page.home_page(conn)

        else:
            print('Invalid input. Enter your response again')
            x = int(input('Enter your response: '))        

    except IndexError:
        print('No one is logged in, please login first and then come back here !!')   
        import time
        print("Redirecting to Login Utility Page ...")
        time.sleep(3)
        import login_module_tushar_methods_added as login_module
        login_module.login_menu(conn)   

#***********************************************************************************
#***********************************************************************************

if __name__ == '__main__':
    sales_data_main()


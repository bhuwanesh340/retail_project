from __future__ import print_function
import sqlite3
from sqlite3 import Error
import string,random,sys,smtplib,re

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

    print('STAFF DETAILS table created successfully')

#*******************************************************
#insert staff data query
#*******************************************************

def insert_data_query_2(conn, staff_data):

    sql = ''' INSERT INTO staff_details (user_id,user_name,email,gender,age,department,base_salary,password)
		VALUES (?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    
    try:
        cur.execute(sql, staff_data)
        conn.commit()
        print('Insert query executed successfully')

    except sqlite3.IntegrityError:
        print('ERROR: USER_ID already exists in PRIMARY KEY column')

    return cur.lastrowid

#*******************************************************

def select_all_staff_data_query2(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM staff_details ")
    rows = cur.fetchall()
    
    print("*"*120)
    print("| USER_ID | USER_NAME | EMAIL | GENDER | AGE | DEPARTMENT | BASE_SALARY | PASSWORD |")

    for row in rows:
        print("| {} | {} | {} | {} | {} | {} | {} | {} |".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))

    print("*"*120)

#*********************************QUERY TO FETCH USERNAME AND PASSWORD

def fetch_user_id(conn,input_user_id):

    cur = conn.cursor()
    cur.execute("SELECT user_id FROM staff_details WHERE user_id = ?", (input_user_id,))
    rows = cur.fetchall()
    return rows

def fetch_user_name(conn,input_user_id):

    cur = conn.cursor()
    cur.execute("SELECT user_name FROM staff_details WHERE user_id = ?", (input_user_id,))
    rows = cur.fetchall()
    return rows

#************************************ FUNCTION TO ENTER DATA FOR NEW USER

def newUser(conn):
    found = 0
    while found == 0:
        Userid = input("Please enter a Userid: ")
        c = conn.cursor()
        findUser = ('''SELECT * FROM staff_details WHERE user_id = ?''')                 #*check invalid user
        
        c.execute(findUser, (Userid,))
        
        if c.fetchall():
            print("Userid already taken, please try again !!")
            found = 1
            return newUser(conn)
        else:
            password = input("Please enter password of employee: ")
            password1 = input("Please re-enter password of employee: ")

            #check if passwrds are same
            while password != password1:
                print("Employee passwords did not match, please try again")
                password = input("Please enter password of employee: ")
                password1 = input("Please re-enter password of employee: ")
                

            Email = input("Please enter email ID of employee: ")
            mo = re.match('[a-z][a-z0-9\.\-_\+]*@[a-z]+\.[a-z]+',Email)
		
            if mo:
                pass
            else:
                Email = input("Please re-enter email ID of employee: ")
                if mo:
                    break
                else:
                    print("Maximum Attempt reached !!")

                    import time
                    print("Redirecting to Login Utility Page ...")
                    time.sleep(3)
                    import login_module_tushar_methods_added as login_module
                    login_module.login_page_main()

                            
            Firstname = input("Please enter first name of employee: ")
            Lastname = input("Please enter last name of employee: ")
            Full_name = (Firstname + " " + Lastname)

            Department = input("Please enter Department of employee: ")

		#Designation = input("Please enter your Designation") not required

            Gender = input("Please enter Gender of employee: ")
            Age = input("Please enter Age of employee: ")
            Basic_salary = float(input("Please enter basic salary of the employee: "))

		#send email 
            server = smtplib.SMTP( "smtp.gmail.com", 587 )
            server.starttls()
            server.login( 'grocerystore.niit@gmail.com','Grocery@123' )
            text1 = 'Your account has been registered successfully'
            text2 = 'Your user id is: '
            text3 = 'Password is: '
            message = 'Subject: Greetings {} from NU Grocey Store\n\n{}\n{}{}\n{}{}'.format(Full_name,text1,text2,Userid,text3,password)
            server.sendmail("grocerystore.niit@gmail.com", Email, message)
            print("Please check your email for registartion confirmation")

		#using insert query2 function to insert staff data of new user

            staff_data = (Userid,Full_name,Email,Gender,Age,Department,Basic_salary,password)
            staff_id = insert_data_query_2(conn, staff_data)
            print("User successfully created")

            import time
            print("Redirecting to Login Utility Page ...")
            time.sleep(3)
            import login_module_tushar_methods_added as login_module
            login_module.login_page_main()

#***************************************************************************************************
# main function
#***************************************************************************************************

def staff_details_main():
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    
    sql_create_staff_table = """ CREATE TABLE IF NOT EXISTS staff_details ( 
					user_id text PRIMARY KEY,
					user_name text,
                                        email text,
					gender text,
					age integer,
					department text,
					base_salary float,
					password text
		                        ); """

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_staff_table)
    else:
        print("Error! cannot create the database connection.")

    def check_name_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
        rows = cur.fetchall()
        return rows

    try:
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]

        conn = create_connection(database)

        #select_all_staff_data(conn)
        select_all_staff_data_query2(conn)

        import home_page
        import time
        print("******************************************************************")
        print("Redirecting to Nu Grocery Store Home Page ...")
        time.sleep(5)
        home_page.home_page(conn)

    except IndexError:
        print('No one is logged in, please login first and then come back here !!')   
        import time
        print("Redirecting to Login Utility Page ...")
        time.sleep(3)
        import login_module_tushar_methods_added as login_module
        login_module.login_page_main()


#*************************************************************************************************
#*************************************************************************************************
    
if __name__ == '__main__':
    staff_details_main()


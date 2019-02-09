from __future__ import print_function
import sqlite3
from sqlite3 import Error
import string,random,sys,smtplib,re,time

def create_connection(db_file):

	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None


def check_valid_user(conn,input_user_id):
	cur = conn.cursor()
	cur.execute("SELECT user_id FROM staff_details WHERE user_id = ?", (input_user_id,))
	rows = cur.fetchall()
	return rows

def fetch_user_name(conn,input_user_id):    
	cur = conn.cursor()
	cur.execute("SELECT DISTINCT(user_name) FROM staff_details WHERE user_id = ?", (input_user_id,))
	rows = cur.fetchall()
	return rows

def fetch_user_dept(conn,input_user_id):
	cur = conn.cursor()
	cur.execute("SELECT DISTINCT(department) FROM staff_details WHERE user_id = ?", (input_user_id,))
	rows = cur.fetchall()
	return rows

def fetch_user_password(conn,input_user_id):
	cur = conn.cursor()
	cur.execute("SELECT DISTINCT(password) FROM staff_details WHERE user_id = ?", (input_user_id,))
	rows = cur.fetchall()
	return rows


def fetch_current_user_detail(conn):
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(user_id) FROM curr_user_table")
    rows = cur.fetchall()
    #print('Current user is: ',rows)
    return rows

def check_current_logged_user(conn):
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT(user_id) FROM curr_user_table")
        rows = cur.fetchall()
        return rows

#----------------------- Random Password generator with emailing functionality ----------------------- 

def randompassword():
    chars= string.ascii_uppercase + string.ascii_lowercase + string.digits
    a = ''.join(random.choice(chars) for x in range(8))
    return a


def passreset(conn):
    Userid = input("Please enter a Userid: ")
    Email = input("Please enter a registered Email ID: ")
    c = conn.cursor()
    findUser = ("SELECT * FROM staff_details WHERE user_id = ? AND email = ?")
    c.execute(findUser, (Userid,Email))
        
    if c.fetchall():

        Password = randompassword()
        updatedata = """UPDATE staff_details SET password = ? WHERE user_id = ? AND email = ?"""
        c.execute(updatedata,(Password,Userid,Email))
        conn.commit()

        #send email

        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login( 'grocerystore.niit@gmail.com','Grocery@123' )

        text1 = 'Greetings !!'
        text2 = 'Your new password is:'

        message = 'Subject: Password reset \n\n{} {}\n{} {}'.format(text1,Userid,text2,Password)

        server.sendmail("grocerystore.niit@gmail.com",Email, message) #"bhuwanesh340@gmail.com" previously
        print("Password changed successfully !!") 

    else:
        print("User not found. Please enter correct Userid and Email ID")
        return passreset()
  
    print("Please check your email for new password")

    print("Redirecting to Login Utility Page ...")
    import time
    time.sleep(3)
    login_menu(conn)

#-------------------------------------------------------------------
#----------------------- Login Menu function -----------------------
#-------------------------------------------------------------------
    
def login_menu(conn):
    
    print("********************************************************************")
    print("********************************************************************")
    print("Welcome to NU Grocery Store Login Utility")
    print("********************************************************************")
    print("********************************************************************")
    print()
    menu =("""
    1 - Create New User
    2 - Login to system
    3 - Password Reset
    4 - Exit system
********************************************************************\n""")
    

    Userinput = input(menu)

    if Userinput == "1":
        import staff_details_updated
        staff_details_updated.newUser(conn)

    elif Userinput == "2":

        def check_name_current_logged_user(conn):
            cur = conn.cursor()
            cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
            rows = cur.fetchall()
            return rows
        
        if(len(check_name_current_logged_user(conn))==0):
            user_login(conn)
        else:
            login_page_main()

    elif Userinput == "3":
        passreset(conn) 

    elif Userinput == "4":

        import time
        print("************************************************************************")
        print("Redirecting to Nu Grocery Store Home Page ...")
        time.sleep(3)
        import home_page
        home_page.home_page(conn)

    else:
        print("Please enter valid menu choice")
    
#**********************************************************************************
#main function 
#**********************************************************************************

def user_login(conn):
		#import staff module 
                    import staff_details_updated as staff_details

		#take inputs from user
                    input_user_id = input('Enter your user id: ')

                    #print('Fetched user id is: ',staff_details.fetch_user_id(conn,input_user_id)[0][0])          #****************
		#Check valid user id

                    #while (input_user_id != staff_details.fetch_user_id(conn,input_user_id)[0][0]):
                    while (staff_details.fetch_user_id(conn,input_user_id)==[]):
                            input_user_id = input('Enter your user id: ')
        	# counter can be taken **

                    else:
                            input_user_id = staff_details.fetch_user_id(conn,input_user_id)[0][0]  #check and return same value from table
                            user_flag = 1   #setting user flag 1
                            
		#if user name is correct then set valid flag = 1
		#check department of user
    
                    dept_name = fetch_user_dept(conn,input_user_id)[0][0]
                    #print('Department of user is: ',dept_name)                                                  #******************

                #********************************************************************************************************
		# defining function for looping over password

                    def password_counter(conn,input_user_id):
                            for password in range(3):
	        #Userid = input("Please enter your Userid: ")
                                    input_passwrd = input("Please enter your Password: ")
	    	#check if password is correct
	    	
                                    x = fetch_user_password(conn,input_user_id)[0][0]
	        #need to remove
                                    #print('Password of user is: ',x)                                            ********************
	        #search user_id in table
                                    cur = conn.cursor()
                                    find_user = ("SELECT * FROM staff_details WHERE user_id = ? AND password = ?")
                                    cur.execute(find_user,[(input_user_id),(input_passwrd)])
                                    results = cur.fetchall()
                                    if results:
                                            return(1)
                                    else:
                                            print("Username and password not recognized")
                                            again = input("Do you want to try again?(y/n): ")
                                            if again.lower() in ("n"):
                                                    #import home_page
                                                    #home_page.home_page(conn)
                                                    import time
                                                    print("Redirecting to Login Utility Page ...")
                                                    time.sleep(3)
                                                    login_menu(conn)

                                            else:
                                                    if password == 0:
                                                            print("You have lost your 1st attempt, 2 more left !!")

                                                    elif password == 1:
                                                            print("You have lost your 2nd attempt, 1 more left !!")

#********************************************************************************************************

                    #call function
                    password_flag = password_counter(conn,input_user_id)
                    while password_flag != 1:
                            print('Invalid credentials, re-directing to home page !!')
                            #import home_page
                            #home_page.home_page(conn)
                            import time
                            print("Redirecting to Login Utility Page ...")
                            time.sleep(3)
                            login_menu(conn)

                    #print('Value of password flag is: ',password_flag) 					********************

                    #***************************************

                    if (user_flag == 1) and  (password_flag == 1):
                            import current_user_db as current_user_module
                            current_user_module.curr_user_login_main()
                            
		    #function call to isert current user detail in curent user table
                            current_user_module.insert_current_user_detail(conn,input_user_id,dept_name)
             
                
                    #curr_logged_user = fetch_user_name(conn,input_user_id)[0][0]
                    #print('Current user logged in is: ',curr_logged_user)                                      **********************

                    #calling login main function again after sleep

                    import time
                    print("******************************************************************")
                    print("Redirecting to Login Page ...")
                    time.sleep(3)

                    #import home_page
                    #home_page.home_page(conn)
                    login_menu(conn)

#*********************************************************************************
#*********************************************************************************

def login_page_main():
    #database = "G:\\NU MATERIAL\\NU-TERM1\\Prog for Ana\\PROJECT\\RETAIL PROJECT APP\\database test\\retail_app.db"
    database = "/media/bhuwanesh-ug1-3317/NIIT/NU MATERIAL/NU-TERM1/Prog for Ana/PROJECT/RETAIL PROJECT APP/database test/retail_app.db"
    conn = create_connection(database)
    if conn is not None:
        #print("Login page connection successfull.")
        print()
    else:
        print("Error! cannot create the database connection.")
        

    # TRY TO CHECK IF USER IS LOGGED IN OR NOT
    
    try:
        def check_name_current_logged_user(conn):
            cur = conn.cursor()
            cur.execute("SELECT user_name FROM staff_details WHERE user_id IN (SELECT DISTINCT(user_id) FROM curr_user_table)")
            rows = cur.fetchall()
            return rows
        
        curr_logged_user_name = check_name_current_logged_user(conn)[0][0]
        print('{} !! is already logged in :) '.format(curr_logged_user_name))
    
        import time
        print("******************************************************************")
        print("Redirecting to Nu Grocery Store Home Page ...")
        time.sleep(3)

        import home_page
        home_page.home_page(conn)

    except IndexError:
        print('No one is logged in, please login first and then come back here !!')   
        import time
        print("Redirecting to Login Utility Page ...")
        time.sleep(3)
        login_menu(conn)
                    
                            

#*****************************************************************************************************

if __name__ == '__main__':
        login_page_main()
    

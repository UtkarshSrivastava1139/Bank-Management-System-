gi # Bank Management System
import time
from datetime import datetime
import csv
#MySQL integration
import mysql.connector as ms
sqlpass = input("Enter SQL password of your system: ")
mydb=ms.connect(host="localhost",user="root",passwd=sqlpass)
if mydb.is_connected():
        print("SQL is Connected")
myc=mydb.cursor()

def header():
    # Header
    print("================================================================================")
    print("\t\t\t PROJECT: BANK MANAGEMENT SYSTEM \n")
    print("\t MADE BY: UTKARSH SRIVASTAVA\n")
    print("\t Features: \n")
    print("\t 1. Administrator Login System(for branch manager)- \n\t\ta. Create User (Cashier) \n\t\tb. Update user details(name/username/password)\n\t\tc. Generate lists of all users\n\t\td. Delete user \n\t\te. Reset Software\n")
    print("\t 2. User Login System(for cashier)- \n\t\ta. Open Accounts\n\t\tb. Close A/c\n\t\tc. Update A/c(Customer name or a/c type)\n\t\td. Withdraw Amount\n\t\te. Deposit amount\n\t\tf. show list of all accounts\n\t\tg. generate bank statement\n\t\th. Balance enquiry \n\t\ti. Logout\n\t\tj. Quit")
    print("\t 3. Database stored in MySQL server.")
    print("\t 4. One Time Registration system for first use.")
    print("\t 5. Intital amount/Account Opening balance is required.")
    print("\t 6. Always gives a new and unique account number.")
    print("\t 7. Every bank transcation has a unique reciept number.")
    print("\t 8. Security password system used for forgot username/password.")
    print("\t 9. User-freindly Interface")
    print("================================================================================\n\n")
    

    myc.execute("Create database IF NOT EXISTS mybms;")
    myc.execute("USE mybms;")
    table_create = '''create table IF NOT EXISTS bdata(
        Ac_No INT(6) auto_increment Primary key not null,
        Name varchar(30) not null,
        Ac_t varchar(10) not null,
        O_bal int(30),
        o_date varchar(17),
        bal int(30))
        auto_increment= 1001'''
    myc.execute(table_create)
    table_create_2 = '''create table IF NOT EXISTS admin(
        Admin_name varchar(40),
        B_name varchar(50),
        A_user varchar(20),
        A_pass varchar(30),
        Ad_security varchar(30));
        '''
    myc.execute(table_create_2)
    table_create_3 = '''create table IF NOT EXISTS user(
        user_name varchar(40),
        u_user varchar(20),
        u_pass varchar(30));
        '''
    myc.execute(table_create_3)
    table_create_4 = '''create table IF NOT EXISTS statement(
        Sr_no int(10) auto_increment primary key,
        date varchar(17),
        Ac_no varchar(6),
        deposit int(60),
        withdraw int(60));
        '''
    myc.execute(table_create_4)
header()

def mpanel():
    print("\n================================================================================\n")
    print("\t\t\tWelcome to Main Panel \t")
    print("\n================================================================================\n")
    print("\tMain-Menu")
    print("-------------------------------------")
    print("\t 1. New Account")
    print("\t 2. Deposit Amount")
    print("\t 3. Withdraw Amount")
    print("\t 4. Balance Enquiry")
    print("\t 5. All Accounts List")
    print("\t 6. Close An Account")
    print("\t 7. Modify An Account")
    print("\t 8. Get Account Statement")
    print("\t 9. Logout")
    print("\t 10. Quit")
    print("-------------------------------------")   

    def newac():
        acname = input("Enter Account Holder's Name: ")
        global inamt2
        global actype
        def actypevalid():
            global actype
            actype = input("S for Saving Account\nC for Current Account\n Choose Account Type: ")
            if actype in ['s','S']:
                def intialamountvalid():
                    print("\nIntial Amount Must be Greater Than Rs. 499/-")
                    inamt= (input("Enter Intial Amount: "))
                    try:
                        global inamt2
                        inamt2 = int(inamt)
                        if inamt2<500:
                            intialamountvalid()
                        else: 
                            pass
                    except ValueError:
                        print("Wrong Value! It Must be a Number")
                        intialamountvalid()        
                intialamountvalid()
                
            elif actype in ['c','C']:            
                def intialamountvalid2():
                    print("\nIntial Amount Must be Greater Than Rs. 999/-")
                    inamt= (input("Enter Intial Amount: "))
                    try:
                        global inamt2
                        inamt2 = int(inamt)
                        if inamt2<1000:
                            intialamountvalid2()
                        else: 
                            pass
                    except ValueError:
                        print("Wrong Value! It Must be a Number")
                        intialamountvalid2()         
                intialamountvalid2()
                
            else:
                print("\nWrong Input!\n")
                actypevalid()
        actypevalid()
        intialamount = inamt2
        if actype in ["S","s"]:
            actype2 = "Saving"
        else:
            actype2 = "Current"
        
        now = datetime.now()
        acdate = now.strftime("%d/%m/%Y %H:%M")
        acbalance = intialamount
        acdata = (acname,actype2,intialamount,acdate,acbalance)
        myc.execute('insert into bdata(Name,Ac_t,O_bal,o_date,bal) Values("{}","{}",{},"{}",{});'.format(acname,actype2,intialamount,acdate,acbalance))
        mydb.commit()
        myc.execute('select Ac_no from bdata;')
        allacdata = myc.fetchall()
        acnumber = allacdata[-1][0]
        myc.execute("insert into statement(date, Ac_no,deposit,withdraw) values('{}','{}',{},{});".format(acdate,acnumber,intialamount,0))
        mydb.commit()
        print('\n-----------------------------------')
        print("Account Created Succesfully!")
        print("Account No.: ",acnumber)
        print("Account Holder's Name: ",acname)
        print("Account Type: ",actype2)
        print("Account Intial Amount: ",intialamount)
        print("Account Balance: ",acbalance)
        print('\n-----------------------------------\n')
        
        choice9 = input("Press any button to go back to main panel......")
        if choice9 == "":
            mpanel()
        else:
            mpanel()
    def depamt():
        print("\n-------------------------------------")
        acno = int(input("Enter Account No. : "))
        now = datetime.now()
        acdate = now.strftime("%d/%m/%Y %H:%M")
        myc.execute("Select Ac_no from bdata;")
        acc_list_temp = myc.fetchall()
        acc_list = []
        for i in acc_list_temp:
            acc_list.append(i[0])
        myc.execute("Select * from bdata;")
        aclist = myc.fetchall()
        if (acno) in acc_list:
            acno2 = acc_list.index(acno)
            userdata = (aclist[acno2])
            acbalance = (userdata[5]) 
            print("\n-------------------------------------")
            print("Account Holder's Name: ",(userdata[1]))
            print("Account Type: ",(userdata[2]))
            print("Current Account Balance: ",acbalance)
            print("-------------------------------------\n")
            def depamount2():
                global depamount
                global acbalance2
                depamount = input("Enter Amount to deposit: ")
                try:
                    ida = int(depamount)
                    acbalance2 = int(acbalance)
                    acbalance2 += ida
                    bal_upd = '''update bdata 
                    set bal = {}
                    where Ac_no = {}
                   '''.format(acbalance2,acno)
                    myc.execute(bal_upd)
                    mydb.commit()
                    myc.execute("insert into statement(date, Ac_no,deposit,withdraw) values('{}','{}',{},{});".format(acdate,acno,depamount,0))
                    mydb.commit()
                except ValueError:
                    print("Wrong Input! It can be only a number")
                    depamount2()
            depamount2()
            print(depamount," has been deposited to A/C No.: ",acno)
            print("Current A/c Balance is: ",acbalance2)
            print("-------------------------------------\n")
            choice9 = input("Press any button to go back to main panel......")
            if choice9 == "":
                mpanel()
            else:
                mpanel()
        else:
           print("Account No.: ",acno,'is not present.\nEnter A valid account No.')
           depamt()        
    def withamt():
        print("\n-------------------------------------")
        acno = int(input("Enter Account No. : "))
        now = datetime.now()
        acdate = now.strftime("%d/%m/%Y %H:%M")
        myc.execute("Select Ac_no from bdata;")
        acc_list_temp = myc.fetchall()
        acc_list = []
        for i in acc_list_temp:
            acc_list.append(i[0])
        myc.execute("Select * from bdata;")
        aclist = myc.fetchall()
        if (acno) in acc_list:
            acno2 = acc_list.index(acno)
            userdata = (aclist[acno2])
            acbalance = (userdata[5]) 
            print("\n-------------------------------------")
            print("Account Holder's Name: ",(userdata[1]))
            print("Account Type: ",(userdata[2]))
            print("Current Account Balance: ",acbalance)
            print("-------------------------------------\n")
            def withamount2():
                global withamount
                global acbalance3
                withamount = input("Enter Amount to withdraw: ")
                
                try:
                        ida = int(withamount)
                        if ida < int(acbalance):
                            acbalance3 = int(acbalance)
                            acbalance3 -= ida
                            bal_upd = '''update bdata 
                                set bal = {}
                                where Ac_no = {}
                                '''.format(acbalance3,acno)
                            myc.execute(bal_upd)
                            mydb.commit()
                            myc.execute("insert into statement(date, Ac_no,deposit,withdraw) values('{}','{}',{},{});".format(acdate,acno,0,withamount))
                            mydb.commit()
                            print(withamount," has been withdrawl from A/C No.: ",acno)
                            print("Current A/c Balance is: ",acbalance3)
                            print("-------------------------------------\n")
                            choice9 = input("Press any button to go back to main panel......")
                            if choice9 == "":
                                mpanel()
                            else:
                                mpanel()
                        else:
                            print("Sorry! Your Current Account Balance is Less i.e. Rs.",acbalance,' only\n')
                            withamount2()
                            
                except ValueError:
                        print("Wrong Input! It can be only a number")
                        withamount2()                    
                
            withamount2()
        else:
           print("Account No.: ",acno,'is not present.\nEnter A valid account No.')
           withamt()
    def blcheck():
        print("\n-------------------------------------")
        acno = int(input("Enter Account No. : "))
        myc.execute("Select Ac_no from bdata;")
        acc_list_temp = myc.fetchall()
        acc_list = []
        for i in acc_list_temp:
            acc_list.append(i[0])
        myc.execute("Select * from bdata;")
        aclist = myc.fetchall()

        if (acno) in acc_list:
            acno2 = acc_list.index(acno)
            userdata = (aclist[acno2])
            acbalance = (userdata[5]) 
            print("\n-------------------------------------")
            print("Account Holder's Name: ",(userdata[1]))
            print("Account Type: ",(userdata[2]))
            print("Current Account Balance: ",acbalance)
            print("-------------------------------------\n")
            choice9 = input("Press any button to go back to main panel......")
            if choice9 == "":
                mpanel()
            else:
                mpanel()
        else:
           print("Account No.: ",acno,'is not present.\nEnter A valid account No.')
           blcheck()
    def allac():
        myc.execute("Select * from bdata;")
        acread = myc.fetchall()
        aclist = []
        print('\n-----------------------------------------------------------------------------------------------------------')
        print("{:<8} {:<13} {:<20} {:<10} {:<15} {:<20} {:10}"
        .format("SNo.","Account No.","A/c Holder\'s Name","Type","Intial Amount","Opening Date","A/c Balance"))
        print("-----------------------------------------------------------------------------------------------------")
        for r in acread:
            aclist.append(r)
            i = aclist.index(r)
            print("{:<8} {:<13} {:<20} {:<10} {:<15} {:<20} {:10}".format(i+1,r[0],r[1],r[2],r[3],r[4],r[5]))
            
        print("-----------------------------------------------------------------------------------------------------------")
        print("Total No. of Accounts: ",len(aclist))
        print("-----------------------------------------------------------------------------------------------------------")
        choice9 = input("\nPress any button to go back to main panel......")
        if choice9 == "":
            mpanel()
        else:
            mpanel()
    def closeac():
        acno = int(input("Enter Account No. : "))
        now = datetime.now()
        acdate = now.strftime("%d/%m/%Y %H:%M")
        myc.execute("Select Ac_no from bdata;")
        acc_list_temp = myc.fetchall()
        acc_list = []
        for i in acc_list_temp:
            acc_list.append(i[0])
        myc.execute("Select * from bdata;")
        aclist = myc.fetchall()
        if (acno) in acc_list:
            acno2 = acc_list.index(acno)
            data = aclist[acno2]
            name = data[1]
            atype = data[2]
            balance = data[-1]
            myc.execute("Delete from bdata where Ac_no = {}".format(acno))
            mydb.commit()
            myc.execute("insert into statement(date, Ac_no,deposit,withdraw) values('{}','{}',{},{});".format(acdate,acno,0,balance))
            mydb.commit()
            print("\n-------------------------------------")
            print("Name: ",name)
            print("A/c Type: ", atype)
            print("A/c Balance: ",balance)
            print("\n-------------------------------------")
            print("Account No.: ", acno, "has been succesfully closed!")
            choice9 = input("\nPress any button to go back to main panel......")
            if choice9 == "":
                mpanel()
            else:
                mpanel()
        else:
           print("Account No.: ",acno,'is not present.\nEnter A valid account No.')
           closeac()
    def modifyac():
        print("\n-------------------------------------")
        acno = int(input("Enter Account No. : "))
        myc.execute("Select Ac_no from bdata;")
        acc_list_temp = myc.fetchall()
        acc_list = []
        for i in acc_list_temp:
            acc_list.append(i[0])
        myc.execute("Select * from bdata;")
        aclist = myc.fetchall() 
        if (acno) in acc_list:
            acno2 = acc_list.index(acno)
            data = aclist[acno2]
            print("\n--------------------------")
            print("A/c Holder's Name: ",data[1])
            print("A/c Type: ",data[2])
            print("A/c Balance: ",data[-1])
            print("\n--------------------------")
            print("1. Update A/c Holder's Name")
            print("2. Change A/c Type:")

            def choiice10():
                choice10 = input("Enter Your Choice: ")
                if choice10 == '1':
                    oldname = data[1]
                    print("Current Name: ",oldname)
                    nname = input("\nEnter New Name: ")
                    myc.execute("update bdata set Name = '{}' where Ac_no= {}".format(nname,acno))
                    print(oldname," changed to ",nname,' for A/c no.: ',acno)
                    choice9 = input("\nPress any button to go back to main panel......")
                    if choice9 == "":
                        mpanel()
                    else:
                        mpanel()
                elif choice10 == '2':
                    oldtype = data[2]
                    print("Current A/c Type: ",oldtype)
                    ntype = input("\nS for Saving Account\nC for Current Account\n Choose Account Type: ")
                    if ntype in ["S","s"]:
                        ntype2 = "Saving"
                    else:
                        ntype2 = "Current"
                        
                    myc.execute("update bdata set Ac_t = '{}' where Ac_no= {}".format(ntype,acno))
                    print(oldtype," changed to ",ntype2,' for A/c no.: ',acno)
                    choice9 = input("\nPress any button to go back to main panel......")
                    if choice9 == "":
                        mpanel()
                    else:
                        mpanel()
                else:
                    print("Wrong Choice!")
                    choiice10()
            choiice10()
        else:
           print("Account No.: ",acno,'is not present.\nEnter A valid account No.')
           modifyac()
    
    def acstatement():
        print("\n-------------------------------------")
        acno = int(input("Enter Account No. : "))
        myc.execute("Select Ac_no from bdata;")
        acc_list_temp = myc.fetchall()
        acc_list = []
        for i in acc_list_temp:
            acc_list.append(i[0])
        myc.execute("Select * from bdata;")
        aclist = myc.fetchall()

        if (acno) in acc_list:
            acno2 = acc_list.index(acno)
            userdata = (aclist[acno2])
            acbalance = (userdata[5]) 
            print("\n-------------------------------------")
            print("Account Holder's Name: ",(userdata[1]))
            print("Account Type: ",(userdata[2]))
            myc.execute("select * from statement where ac_no = '{}';".format(acno))
            acstat = myc.fetchall()
            aclist = []
            print('\n-----------------------------------------------------------------------------------------------------------')
            print("{:<8} {:<10} {:<20} {:<20} {:<20} "
            .format("SNo.","Receipt No.","Date.","Deposit","Withdraw"))
            print("-----------------------------------------------------------------------------------------------------")
            for r in acstat:
                i = acstat.index(r)
                print("{:<8} {:<10} {:<20} {:<20} {:<20}".format(i+1,r[0],r[1],r[3],r[4]))

            print("Current Account Balance: ",acbalance)
            print("-------------------------------------\n")
            choice9 = input("Press any button to go back to main panel......")
            if choice9 == "":
                mpanel()
            else:
                mpanel()
        else:
           print("Account No.: ",acno,'is not present.\nEnter A valid account No.')
           blcheck()
    def choiice9():
        choice9 = input("Enter Your Choice: ")
        if choice9 == '1':
            newac()
        elif choice9 == "2":
            depamt()
        elif choice9 == '3':
            withamt()
        elif choice9 == '4':
            blcheck()
        elif choice9 == '5':
            allac()
        elif choice9 == "6":
            closeac()
        elif choice9 == "7":
            modifyac()
        elif choice9 == "8":
            acstatement()
        elif choice9 == '9':
            print("Thank You!")
            print("-------------------------------------\n")   
            header2()
            loginask()
        elif choice9 == '10':
            print("Thank You, Bye!")
            print("It will be quit in 3 seconds!")
            time.sleep(3)
            quit()
        else:
            print("Wrong Choice!")
            choiice9()
    choiice9()

def admin(): 
    def reguser():
        name1 = input("Enter Name: ")
        uname= input("Enter Username: ")
        npas= input("Enter Password: ")
        myc.execute("Insert into user Values('{}','{}','{}');".format(name1,uname,npas))
        mydb.commit()
        
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Name: ",name1)
        print("Username: ",uname)
        print("Password: ",npas)
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Following User has been registered!")
        time.sleep(2)
        admin()
    def deluser():
        user3 = input("Enter the username: ")
        myc.execute("Select * from user where u_user = '{}';".format(user3))
        udata = myc.fetchall()
        print(udata)
        if len(udata) == 0:
            print("Not a valid username!")
            choice7 = input("\n Press T to Try-again or \n Press any button to Back to main menu ")
            if choice7 in ['t',"T"]:
                deluser()
            else:
                header2()
        else:
            print("\n----------------------")
            print("Name:",udata[0][0])
            print("Username:",udata[0][1])
            myc.execute("delete from user where u_user = '{}';".format(user3))
            mydb.commit()
            print("----------------------")
            print("Following user has been deleted!")
            admin()
    def chgdeta():
        user3 = input("Enter the username: ")
        myc.execute("select * from user where u_user = '{}';".format(user3))
        udata = myc.fetchall()
        if len(udata) == 0:
            print("wrong username")
            chgdeta()
        else:
            def chpas():
               name12 = udata[0][0]
               user12 = udata[0][1]
               pas12 = udata[0][2]
               print("\t 1. Update Name")
               print("\t 2. Update Username")
               print("\t 3. Update Password")
               choice8 = input("Enter Choice: ")
               if choice8 == '1':
                   print("Old name: ", name12)
                   nname = input("Enter new name: ")
                   myc.execute("update user set user_name = '{}' where u_user = '{}';".format(nname,user3))
                   mydb.commit()
                   print("Name is update from",name12,'to',nname)
               elif choice8 == '2':
                    print("Old username: ", user12)
                    nuname = input("Enter new username: ")
                    myc.execute("update user set u_user = '{}' where u_user = '{}';".format(nuname,user3))
                    mydb.commit()
                    print("Username is update from",user12,'to',nuname)

               elif choice8 == '3':
                    print("Old Password: ", pas12)
                    newpas = input("Enter new password: ")
                    myc.execute("update user set u_pass = '{}' where u_user = '{}';".format(newpas,user3))
                    mydb.commit()
                    print("Password is update from",pas12,'to',newpas)
                    

               else:
                    print("Wrong Input!")
                    chpas()
    
               print("\n----------------------")
               admin()
            chpas()
    def showall():
        myc.execute("select * from user;")
        ulist5 = myc.fetchall()
        totalno = len(ulist5)
        print('\n----------------------------------------------------------')
        print("Total users: ",totalno)
        print('----------------------------------------------------------')
        print(("{:<8} {:<15} {:<15} {:<15}").format("S No.","Name","Username","Password\n"))
        for i in range(totalno):
            print(("{:<8} {:<15} {:<15} {:<15}").format((i+1),ulist5[i][0],ulist5[i][1],ulist5[i][2]))
            print('--------------------------------------------------------')
        time.sleep(2)
        choice9 = input("Press any button to go back to admin panel......")
        if choice9 == "":
            admin()
        else:
            admin()
    
    def reset_soft():
        print("WARNING - Do you really want to reset this software? - Recovery not possible")
        choice11 = (input("Press 1 for yes else press any other button:-  "))
        if choice11 == '1':
            myc.execute("Drop Database mybms;")
            print("This software is completely reseted. It will quit in 3 seconds.\n Restart it for new system. ")
            time.sleep(3)
            quit()
        else:
            print("This is software is not reseted.")
            admin()
            
    
    print("\n---------------------------------------------!")  
    print("Welcome To Admin Panel!")  
    print("\t 1. Register New User")    
    print("\t 2. Delete Any User")  
    print("\t 3. Update Details of Any User")   
    print("\t 4. Show all Users Details")   
    print("\t 5. Back to Login Panel")
    print("\t 6. Reset Software")
    print("\t 7. Quit")
    def choiice6():
        choice6 = input("\nEnter Your Choice:")
        if choice6 == "1":
            reguser()
        elif choice6 == "2":
            deluser()
        elif choice6 == '3':
            chgdeta()
        elif choice6 == '4':
            showall()
        elif choice6 == '5':
            header2()
        elif choice6 == '6':
            reset_soft()
        elif choice6 == '7':
            quit()
        else:
            print("Wrong Input!")
            choiice6()
    choiice6()

def login():

    user= input("\n\tUSERNAME: ")
    myc.execute("select * from user where u_user = '{}';".format(user))
    udata = myc.fetchall()

    if len(udata) == 0:
        print("Not a valid user, Contact Admin")
        choice2 = input("\n Press T to Try-again or \n Press any button to back to main menu: ")
        if choice2 in ['t',"T"]:
            login()
        else:
            header2()
        
    else:
        def pascheck1():
            pas= input("\n\tEnter password: ")
            spas = udata[0][2]
            if pas== spas:
                print("\tWelcome ",udata[0][0])
                mpanel()
            else:
                print("Wrong Password \n Enter again or quit")
                choice3 = input("\n Press T to Try-again or \n Press any button to Back to main menu ")
                if choice3 in ['t',"T"]:
                    pascheck1()
                else:
                    header2()
                    
        pascheck1()  

def adminlogin():
    
    myc.execute("Select * from admin;")
    ad_data = myc.fetchall()
    ad_user = ad_data[0][2]
    ad_pass = ad_data[0][3]
    ad_name = ad_data[0][0]
    ad_bank = ad_data[0][1]
    global wrong_user 
    wrong_user = 0
    global wrong_pass
    wrong_pass = 0
    def chg_auser_pass():
        print("\n-----Now you can recover your username or password")
        sec_pass_check = input("Enter your security password: ")
        myc.execute('Select * from admin;')
        addata = myc.fetchall()
        ad_sec = addata[0][-1]
        if sec_pass_check == ad_sec:
            print("Enter current username or password, if not to change.")
            ad_user = input("Enter New Username: ")
            ad_pass = input("Enter New Password: ")
            myc.execute("update admin set A_user = '{}', A_pass = '{}' where ad_security = '{}';".format(ad_user,ad_pass,ad_sec))
            mydb.commit()
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            adminlogin()
        else:
            print("Wrong Security Password")
            chg_auser_pass()

    def adminlogin3():
        usercheck2= input("Enter Admin Username: ")
        global wrong_user
           
        if wrong_user< 4:
                if usercheck2 == ad_user:
                    def pascheck2():
                        pas2= input("Enter Password: ")
                        global wrong_pass
                        if wrong_pass<4:
                            if pas2 == ad_pass:
                                admin()
                            else:
                                print("Wrong Password\n Enter again or quit")
                                print(4-wrong_pass," more tries left.\n after this you can reset it using recovery password")
                                choice4 = input("\n Press T to Try-again or \n Press any button to Back to main menu ")
                                if choice4 in ['t',"T"]:
                                    wrong_pass += 1
                                    pascheck2()
                                else:
                                    header2()
                        else:
                            chg_auser_pass()
                    pascheck2()
                else:  
                    print("Not a valid username!")
                    print(4-wrong_user," more tries left.\n after this you can reset it using recovery password")
                    choice5 = input("\n Press T to Try-again or \n Press any button to Back to main menu ")
                        
                    if choice5 in ['t',"T"]:
                        wrong_user += 1
                        adminlogin3()
                    else:
                        header2()
        else:
            chg_auser_pass()

    adminlogin3()
               
def loginask():

        choice1 = input("\n\n\n------------------\n\tEnter Login Type: ")
        if choice1 == "1":
            login()
        elif choice1== "2":
            adminlogin()
        elif choice1 == "3":
            print("Thank You....")
            time.sleep(2)
            quit()
        else:
            print("Wrong Input!")
            loginask()


def header2():
    print("\t 1. User Login")
    print("\t 2. Admin Login")
    print("\t 3. Quit")
    loginask()
def f_reg():
    print("~~~~~~~~~~~One Time Registration~~~~~~~~~~~~")
    admin_name = input("Enter Administrator Name: ")
    bank_name = input("Enter your bank name: ")
    admin_user = input("Enter new Username: ")
    admin_pass = input("Enter new password: ")
    print("\n This will help u when you forgot your password or username: ")
    global sqlpass


    ad_security = input("Enter your recovery password: ")
    myc.execute("insert into admin values('{}','{}','{}','{}','{}');".format(admin_name,bank_name,admin_user,admin_pass,ad_security))
    mydb.commit()
    print("----- Registration done---------")
    print("Administrator Name: ",admin_name)
    print("Bank Name: ",bank_name)
    print("Admin username: ",admin_user)
    print("Admin password: ",admin_pass)
    
    print("--------- IMPORTANT ------------")
    print("Please note this recovery password somewhere:",ad_security,"\n")
    print("beacause It will help You\n to recover your username or password once forgot.\n\n")
    print("---------------------------------------------------------------------")
    adminlogin()
def check_first_reg():
    myc.execute("Select * from admin;")
    addata = myc.fetchall()
    if len(addata) == 0 :
        f_reg()
    else:
        header2()
check_first_reg()







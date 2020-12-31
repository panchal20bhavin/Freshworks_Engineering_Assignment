import json,time
from threading import *
temp_data={}

def fileop(op,data):
    if op=="read":
        f=open("file.json","r")
        var1=f.read()
        if len(var1)==0:
            return "Oops! There is not data in json file"
        else:
            parsed=json.loads(var1)
       
        f.close()
        return parsed
    elif op=="write":
        f=open("file.json","w")
        parsed=json.dumps(data)
        f.write(parsed)
        f.close()
        

def Create(key,value,timeout=0):
    if key in temp_data:
        print("error: this key already exists") #Error
    else:
        if(key.isalpha()):
            if len(temp_data)<(1024*1020*1024) and len(value)<=(16*1024*1024): #This Constraints for file size less than 1GB and Json-object value less than 16KB 
                if timeout==0:
                    list1=[value,timeout]
                else:
                    list1=[value,time.time()+timeout]
                if len(key)<=32:                     #This Constraints for input key capped at 32chars only
                    temp_data[key]=list1
                    fileop("write",temp_data)
                    temp_data.clear()
            else:
                print("Oops! The key length is high.") #Error
        else:
            print("Oops! The key must contain only alphabets and no special characters or numbers......") #Error

def Read(key):
    rtn_statament=fileop("read",None)
    if rtn_statament=="Oops! There is not data in json file":
        # return "Oops! There is not data in json file"
        print("Oops! There is not data in json file")
    else:
        if key not in rtn_statament:
            print("Oops! THIS key dosen't exist in Database.Please Enter a valid key!!!") #Error
        else:
            temp_var=rtn_statament[key]
            if temp_var[1]!=0:
                if time.time()<temp_var[1]:   #This Comparing the present time with expiry time
                    var_str=str(key)+":"+str(temp_var[0]) 
                    # return var_str
                    print(var_str)
                else:
                    print(f"Error for time-to-live of '{key}' has expired") #Error 
            else:
                var_str=str(key)+":"+str(temp_var[0])
                # return var_str
                print(var_str)

def Delete(key):
    rtn_statament=fileop("read",None)
    if rtn_statament=="Oops! There is not data in json file":
        print("Oops! There is not data in json file")
    else:
        if key not in rtn_statament:
            print("Oops! THIS key dosen't exist in Database.Please Enter a valid key!!!") #Error 
        else:
            temp_var=rtn_statament[key]
            if temp_var[1]!=0:
                if time.time()<temp_var[1]:   #This Comparing the present time with expiry time
                    del rtn_statament[key]
                    fileop("write",rtn_statament)
                    print("Finally! This key is successfully deleted in json file.") #Success
                else:
                    print(f"Error for time-to-live of '{key}' has expired....") #Error 
            else:
                del rtn_statament[key]
                print("Finally! This key is successfully deleted in json file.") #Success

# while True:
#     print("1 create")
#     print("2 read")
#     print("3 delete")
#     print("4 exit")
#     choice = int(input("Enter :"))
#     if choice == 1:
#         key = input("Enter key :")
#         val = input("Enter value :")
#         sec = int(input("Enter seconds :"))
#         Create(key,val,sec)
#     if choice == 2:
#         key = input("Enter key :")
#         msg = Read(key)
#         print(msg)
#         # print(d)
#     if choice == 3:
#         key = input("Enter key :")
#         Delete(key)
#     if choice == 4:
#         break


t1=Thread(target=Create,args=("Harsh","java",120))    
t2=Thread(target=Create,args=("Bhavin","Python",120))  
# t3=Thread(target=Create,args=('Sneh',"Php",120)) 


t4=Thread(target=Read,args=("Harsh",))
t5=Thread(target=Read,args=("Bhavin",))
# t6=Thread(target=Read,args=('Sneh'))       
t6=Thread(target=Delete,args=("Bhavin",))

t1.start()
t2.start()
# t1.sleep()
t4.start()
t5.start()
t6.start()
# t4.sleep()
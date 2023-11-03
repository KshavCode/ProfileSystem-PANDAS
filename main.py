from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import pandas as pd
import requests
import time 
import numpy as np

loc = "companydata/data.csv"
pd.options.mode.chained_assignment = None

class Employee : 
    def __init__(self):
        global loc
        if os.path.exists("companydata")==False :
                os.mkdir("companydata")
        if os.path.isfile(loc)==False : 
            columnlist = ["Name", "Age", "Gender", "Title", "Wallpaper", "DP"]
            datafile = pd.DataFrame(columns=columnlist)
            datafile.to_csv(loc, index=False)

    def savedata(self, name, age, gender, jobtitle) -> None:
        """'Saves data of a person inside the CSV file, won't if person already exists in data"""
        global loc
        time.sleep(0.5)
        genderslis = ["male", "female", "other"]
        if type(name) != str: 
            return "What's that name?"
        elif type(age) != int : 
            return "Wrong age given" 
        elif type(gender) != str : 
            return "Invalid gender -_-"
        elif type(jobtitle) != str : 
            return "Really, this is a jobtitle?"
        elif gender.lower() not in genderslis : 
            return "Invalid gender -_-"
        else : 
            reg = False
            data = pd.read_csv(loc) 

            if name.lower() in data["Name"].values and int(age) in data["Age"].values and jobtitle.lower() in data["Title"].values and gender.lower() in data["Gender"].values : 
                reg = True

            if reg == False : 
                newdata = pd.DataFrame({"Name":[name.lower()], "Age":[int(age)], "Gender":[gender.lower()], "Title":[jobtitle.lower()], "Wallpaper":["notset"], "DP":["nopic"]})
                data = pd.concat([data, newdata], ignore_index=True)
                data.to_csv(loc, index=False)
                return "Data Saved Successfully!"
            elif reg == True : 
                return "User already registered!"
                

    def viewdata(self, name, age, jobtitle) -> None : 
        """Shows a person's data in a form of an image, won't if the person is not registered in the data file"""
        global loc
        reg = False
        name = name.lower()
        jobtitle = jobtitle.lower()
        if type(name) != str: 
            return "What's that name?"
        elif type(age) != int : 
            return "Wrong age given" 
        data = pd.read_csv(loc)
        if name in data["Name"].values and age in data["Age"].values and jobtitle in data["Title"].values: 
            reg = True

        if reg == False : 
            return "User not in the data"
        elif reg == True : 
            for u in range(0, data.shape[0]) : 
                if data["Name"][u] == name and data["Age"][u] == int(age) and data["Title"][u]==jobtitle : 
                    wall = data["Wallpaper"][u]
                    gen = data["Gender"][u]
                    dp = data["DP"][u]
                    break
            with Image.open(f"wallpapers/{wall}.jpg") as img : 
                img2 = Image.open(f"profilepic/{dp}.jpg")
                img2 = img2.resize((300, 300))
                image_resized = img.resize((900, 500))
                imgmain = image_resized.filter(ImageFilter.GaussianBlur(radius=5))
                imgmain.paste(img2, (560, 90))
                draw = ImageDraw.Draw(imgmain)
                font1 = ImageFont.truetype("arial.ttf", 40)
                draw.rectangle((30, 100, 480, 150), fill="black", outline="white", width=2)
                draw.text((50, 100), text="Name : ", font=font1, fill="lightpink")
                draw.text((190, 102), text=name.title(), font=font1, fill="white")
                draw.rectangle((30, 180, 480, 230), fill="black", outline="white", width=2)
                draw.text((50, 180), text="Age: ", font=font1,fill="lightpink")
                draw.text((140, 182), text=str(age), font=font1, fill="white")
                draw.rectangle((30, 260, 480, 310), fill="black", outline="white", width=2)
                draw.text((50, 260), text="Gender: ", font=font1,fill="lightpink")
                draw.text((210, 262), text=gen.title(), font=font1, fill="white")
                draw.rectangle((30, 340, 480, 390), fill="black", outline="white", width=2)
                draw.text((50, 340), text="Job Title: ", font=font1, fill="lightpink")
                draw.text((230, 342), text=jobtitle.title(), font=font1, fill="white")
                imgmain.show()


    def editdata(self, name, age, gender, jobtitle) : 
        """'Change various details of a person in the data file, won't if the person doesn't exist in the data file"""
        time.sleep(0.5)
        global loc
        reg = False
        name = name.lower()
        jobtitle = jobtitle.lower()
        if type(name) != str: 
            return "What's that name?"
        elif type(age) != int : 
            return "Wrong age given" 
        data = pd.read_csv(loc)
        if name in data["Name"].values and age in data["Age"].values and jobtitle in data["Title"].values and gender in data["Gender"].values : 
            reg = True
        if reg == False : 
            return f"{name} is not registered in the database :("
        elif reg == True : 
            for u in range(0, data.shape[0]) : 
                if data["Name"][u] == name and data["Age"][u] == int(age) and data["Title"][u]==jobtitle : 
                    break
            genders = ["male", "female", "other"]
            choice = int(input("What do you want to change : \n1. Name\n2. Age\n3. Gender\n4. Jobtitle\n5. Wallpaper\n6. Profile Picture\n"))
            time.sleep(0.5)
            if choice == 1 : 
                val = input("Enter new value : ")
                val = val.lower()
                data["Name"][u] = val
                data.to_csv(loc, index=False)
                time.sleep(0.5)
                return "Data changed successfully!"
            elif choice == 2 : 
                val = int(input("Enter new value : "))
                data["Age"][u] = val
                data.to_csv(loc, index=False)
                time.sleep(0.5)
                return "Data changed successfully!"
            elif choice == 3 : 
                val = input("Enter new value : ")
                if val.lower() not in genders : 
                    return "Invalid gender input"
                else : 
                    data["Gender"][u] = val
                    data.to_csv(loc, index=False)
                    time.sleep(0.5)
                    return "Data changed successfully!"
            elif choice == 4 : 
                val = input("Enter new value : ")
                data["Title"] = val
                data.to_csv(loc, index=False)
                time.sleep(0.5)
                return "Data changed successfully!"
            elif choice == 5 : 
                try : 
                    val = input("Enter link for wallpaper (JPG only) : ")
                    linkd = requests.get(val).content
                    currentdate = time.strftime("%d%m%y%H%M%S")
                    with open(f"wallpapers/{currentdate}.jpg", "wb") as newwall: 
                        newwall.write(linkd)
                    data["Wallpaper"][u] = currentdate
                    data.to_csv(loc, index=False)
                    time.sleep(0.5)
                    return "Data changed successfully!"
                except : 
                    return "Maybe you have provided invalid or a broken link......"
            elif choice == 6 : 
                val = input("Enter profile picture link (JPG) : ")
                try : 
                    linkd = requests.get(val).content
                    currentdate = time.strftime("%d%m%y%H%M%S")
                    with open(f"profilepic/{currentdate}.jpg", "wb") as newwall: 
                        newwall.write(linkd)
                    data["DP"][u] = currentdate
                    data.to_csv(loc, index=False)
                    time.sleep(0.5)
                    return "Data changed successfully!"
                except : 
                    return "Maybe you have provided invalid or a broken link......"
            else : 
                return "Invalid input!"

    def deldata(self, name, age, gender, jobtitle) : 
        """Deletes employee data from the file. USE WITH CAUTION"""
        
        global loc
        time.sleep(0.5)
        reg = False
        data = pd.read_csv(loc) 

        if name.lower() in data["Name"].values and int(age) in data["Age"].values and jobtitle.lower() in data["Title"].values and gender.lower() in data["Gender"].values : 
            reg = True

        if reg == False : 
            return "User is not in the database!"

        elif reg == True : 
            for u in range(0, data.shape[0]) : 
                if data["Name"][u] == name and data["Age"][u] == int(age) and data["Title"][u]==jobtitle : 
                    break
            data.drop(u, axis="index", inplace=True )
            data.to_csv(loc, index=False)
            return "Data Deleted Successfully!"
            

emplo = Employee()
time.sleep(0.5)
while True : 
    print("What do you want to do?\n1. View Data\n2. Save Data\n3. Edit Data\n4. Delete Data\n5. Exit")
    time.sleep(0.5)
    choice = int(input("Enter the number of your choice : "))
    time.sleep(0.5)
    if choice == 1 :    
        n = input("Enter the name of the person : ")
        a = int(input("Enter the age of the person : "))
        jt = input(f"Enter the job title of {n} : ")
        time.sleep(0.5)
        print(emplo.viewdata(n, a, jt))

        
    elif choice == 2 : 
        n2 = input("Enter the name of the person : ")
        a2 = int(input("Enter the age of the person : "))
        g2 = input("Enter the gender of the person : ")
        jt2 = input(f"Enter the job title of {n2} : ")
        time.sleep(0.5)
        print(emplo.savedata(n2, a2, g2, jt2))
        
    elif choice == 3 : 
        n3 = input("Enter the name of the person : ")
        a3 = int(input("Enter the age of the person : "))
        g3 = input("Enter the gender of the person : ")
        jt3 = input(f"Enter the job title of {n3} : ")
        time.sleep(0.5)
        print(emplo.editdata(n3, a3, g3, jt3))
        
    elif choice == 4 : 
        n4 = input("Enter the name of the person : ")
        a4 = int(input("Enter the age of the person : "))
        g4 = input("Enter the gender of the person : ")
        jt4 = input(f"Enter the job title of {n4} : ")
        time.sleep(0.5)
        while True : 
            confirmation = input("Type CONFIRM in order to conform deletion or type CANCEL to abort the process : ")
            time.sleep(0.5)
            if confirmation == "CONFIRM" : 
                print(emplo.deldata(n4.lower(), a4, g4.lower(), jt4.lower()))
                break
            elif confirmation == "CANCEL" : 
                print("Process aborted!")
                break
            else : 
                continue
    elif choice == 5 : 
        print("Exiting the app...................")
        time.sleep(2)
        break
    else : 
        print("Wrong input, try again!")
        time.sleep(0.5)

    

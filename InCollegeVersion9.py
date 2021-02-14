###############################################################################
#
# Author: Team Utah
# Version 9 - 11/16/2020
#
# This application is designed to allow college students to create personal
# accounts, upload profile information, search for and apply for jobs, and 
# connect with other students both at their college and at other colleges. 
#
# EXECUTION COMMAND: Python InCollegeVersion9.py
#
###############################################################################

import csv
import sys
from os import system, name 
import os.path
import collections
import datetime
#=========================== Global Variables ================================
MAXACCOUNT = 10
MAXJOB= 10
MAXEXPERIMENT = 3
MAXEDUCATION = 10

studentList = {} #updated to a DIRECTIONARY, where username is the key. i.e studentList.get("qizheng"), this returns a StudentAccount class
jobList = [] #Khalani new object list for job listings (Khalani)

studentAccountfile="dataFiles/student_accounts.csv"
studentFriendships="dataFiles/account_friendships.csv"
studentProfilefile = "dataFiles/student_profiles.csv"
studentProfileEducations = "dataFiles/student_profile_educations.csv"
studentProfileExperiences = "dataFiles/student_profile_experiences.csv"
jobDataFile="dataFiles/job_list.csv" #Khalani, new file to store job listings
jobAppFile="dataFiles/job_apps.csv"
studentfriendrequests="dataFiles/friend_requests.csv"
studentfriendrequestsSENT="friend_request_sent.csv"
savedJobsFile="dataFiles/saved_jobs.csv"
inboxFile = "dataFiles/inbox.csv"
courseFile = "dataFiles/student_courses_took.csv"

loggedIn=False      #login states
loggedInUsername = ""    #current login username - key to the studentList
lastLoginTime=None

#================================= Student Class ===============================
class StudentAccount:  #student account class: (Khalani)
    #Student profile information (Qi). To access "title", studentList.get("qizheng").StudentProfile.title
    class StudentProfile:
        def __init__(self, created=False,title="", major="", university="", aboutMe="", experience=[], education=[]):
            self.created = created   #detemine if the profile is created or not
            self.title = title
            self.major = major
            self.university = university
            self.aboutMe = aboutMe
            self.experience = experience
            self.education = education
    
    #Student Account contructor
    def __init__(self, fName, lName, password, language = "ENGLISH", email = "ON", sms = "ON", targetedAdv = "ON", type = "STANDARD", friendship=[], requestFrom=[], requestTo=[], appliedJobs=[], applications=[], savedJobs=[], inbox = [],createdOn=None, lastLogin=None, courseTook=[]):
        self.fName = fName
        self.lName = lName
        self.password = password
        self.language = language
        self.email = email
        self.sms = sms
        self.targetedAdv = targetedAdv
        self.type = type #Added by JaNae (Epic 7)
        self.friendship = friendship
        self.requestFrom = requestFrom
        self.requestTo=requestTo
        self.StudentProfile = self.StudentProfile(False,"", "", "", "",[], [])
        self.appliedJobs = appliedJobs
        self.applications = applications
        self.savedJobs = savedJobs
        self.inbox = inbox
        self.createdOn=createdOn
        self.lastLogin=lastLogin
        self.courseTook=courseTook
    
#================================= Job Class ===============================
#job listing class (Khalani)
class JobApplication:
    def __init__(self,user, jobId,graduationDate,startByDate,paragraph, appliedDate, marked):
        self.user = user
        self.jobId = jobId
        self.graduationDate = graduationDate
        self.startByDate = startByDate
        self.paragraph = paragraph
        self.appliedDate=appliedDate
        self.marked=marked

class JobListing:
    def __init__(self,jobId,title, description, employer, location, salary, createdBy, postedOn, marked,deleteOn):
        self.jobId=jobId
        self.title = title
        self.description = description
        self.employer = employer
        self.location = location
        self.salary = salary
        self.createdBy = createdBy
        self.postedOn=postedOn
        self.marked=marked
        self.deleteOn=deleteOn

#=============================== Helper Functions =============================================
#Make sure this system only support for up to 5 unique student accounts and jobs. Used in createAccount function (Monica/Khalani)
def maxListCheck(listName, maxNum): 
    if len(listName) >= maxNum:
        return False
    else:
        return True

def maxJobCheck():
    count=0
    for job in jobList:
        if job.marked =="IN":
            count+=1
    if count >=MAXJOB:
        return False
    else:
        return True


#This function return true is it a valid password, else return false. Used in CreateAccount function (Qi)
def checkPW(password):
    if (len(password) >= 8 and len(password) <= 12 and any(x.isupper() for x in password) and any(x.isalpha() for x in password) and
            any(x.isdigit() for x in password) and any(not x.isalnum() for x in password)):
        return True
    else: False

#This function make sure the input values is either y or n and returns the corresponding value (Qi)
def yORnCheck(inputValue, question):
    returnValue = inputValue
    while((returnValue.lower() != 'y') and (returnValue.lower() != 'n')):
        returnValue = input("\nERROR: Invalid input. {} ".format(question))
    if(returnValue.lower() == 'y'):
        clear()
    return returnValue

#Convert first character of all the words to uppercase and rest to lowercase (Jack)
def ToUpperWord(st):
    i = 0
    newstr = ""
    while i < len(st):
        newstr = newstr + st[i].upper()
        i = i + 1
        while i < len(st):
            if st[i] == " ":
                break
            newstr = newstr + st[i].lower()
            i = i + 1
        if i == len(st):
            break
        newstr = newstr + st[i]
        i = i + 1
    return newstr

#Add a new line character after "every" characters to avoid long text (Qi)
def insert_newlines(string, part='\n',every=60):
    return part.join(string[i:i+every] for i in range(0, len(string), every))

#Clear concole (Qi)
def clear(): 
    if name == 'nt':    # for windows 
        _ = system('cls') 
    else:  # for mac and linux(here, os.name is 'posix') 
        _ = system('clear')

#Valid string in timestamp
def checkDate(date_string):
    try:
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        return True
    except ValueError:
        return False

#convert string to date and check future time
def convertDate(timeStr, string):
    while True:
        if(checkDate(timeStr)):
            date_obj = datetime.datetime.strptime(timeStr, '%m/%d/%Y')
            if date_obj>datetime.datetime.now():
                timeStr=input("\tERROR: No Future date allow. "+string)
            else:
                break
        else:
            timeStr=input("\tERROR: Invalid format. "+string)

    return timeStr

    
def ApplicationDate(timeStr, string): #Khalani same as the convertDate(), just without a restriction.
    while True:
        if(checkDate(timeStr)):
            date_obj = datetime.datetime.strptime(timeStr, '%m/%d/%Y')
            break
        else:
            timeStr=input("\tERROR: Invalid format. "+string)

    return timeStr

#========================================== Read/write to data file ===================================
#read student data from data files. Invalid password will be will skip. (Khalani/Updated by Qi)
def readFromCSV():
    if os.path.isfile(studentAccountfile): #read from student account data file
        with open(studentAccountfile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if(checkPW(row[3])):
                    student = StudentAccount(row[0], row[1], row[3], row[4],row[5],row[6],row[7], row[8], [], [],[],[],[],[],[], row[9],row[10],[])
                    studentList.update({row[2].lower():student})

    if os.path.isfile(jobDataFile): #read from job list
        with open(jobDataFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                job = JobListing(row[0],row[1],row[2],row[3],row[4],row[5],row[6], row[7], row[8], row[9])
                jobList.append(job)

    if os.path.isfile(jobAppFile):
        with open(jobAppFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                App = JobApplication(row[0],row[1],row[2],row[3],row[4],row[5], row[6])
                studentList.get(App.user).applications.append(App)
                username = row[0]
                jobID = row[1]
                for job in jobList:
                    if jobID == job.jobId:
                        studentList.get(username).appliedJobs.append(job)

    if os.path.isfile(savedJobsFile):  # read saved jobs file
        with open(savedJobsFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if row[0].lower() in studentList:
                    for i in range(1, len(row)):
                        for job in jobList:
                            if job.jobId == row[i]:
                                studentList.get(row[0].lower()).savedJobs.append(job)

    if os.path.isfile(studentProfilefile): #read from student profile file
        with open(studentProfilefile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if row[0].lower() in studentList:
                    studentList.get(row[0].lower()).StudentProfile.created=True
                    studentList.get(row[0].lower()).StudentProfile.title=row[1]
                    studentList.get(row[0].lower()).StudentProfile.major=ToUpperWord(row[2])
                    studentList.get(row[0].lower()).StudentProfile.university=ToUpperWord(row[3])
                    studentList.get(row[0].lower()).StudentProfile.aboutMe=row[4]
    
    if os.path.isfile(studentProfileExperiences): #read from student experiences file
        with open(studentProfileExperiences) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                studentExp=[row[1], row[2], row[3],row[4], row[5], row[6]]
                if row[0].lower() in studentList:
                    studentList.get(row[0].lower()).StudentProfile.experience.append(studentExp)

    if os.path.isfile(studentProfileEducations): #read from student education history file
        with open(studentProfileEducations) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                studentEdu=[ToUpperWord(row[1]), ToUpperWord(row[2]), row[3]]
                if row[0].lower() in studentList:
                    studentList.get(row[0].lower()).StudentProfile.education.append(studentEdu)

    if os.path.isfile(studentFriendships): #read from student friendship file
        with open(studentFriendships) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if row[0].lower() in studentList:
                    for i in range (1, len(row)):
                        if row[i] != "":
                            studentList.get(row[0].lower()).friendship.append(row[i])

    if os.path.isfile(studentfriendrequests): #read from student request file
        with open(studentfriendrequests) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if(row[0]=="from"):
                    if row[1].lower() in studentList:
                        for i in range (2, len(row)):
                            if row[i] != "":
                                studentList.get(row[1].lower()).requestFrom.append(row[i])
                elif(row[0]=="to"):
                    if row[1].lower() in studentList:
                        for i in range (2, len(row)):
                            if row[i] != "":
                                studentList.get(row[1].lower()).requestTo.append(row[i])

    if os.path.isfile(inboxFile): #read from student experiences file
        with open(inboxFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                message = (row[1],row[2],row[3]) #sender, message and marked read/unread
                studentList.get(row[0]).inbox.append(message)

    if os.path.isfile(courseFile): #read from student course file
        with open(courseFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)
            for row in readCSV:
                if row[0].lower() in studentList:
                    for i in range (1, len(row)):
                        if row[i] != "":
                            studentList.get(row[0].lower()).courseTook.append(row[i])

#================================== write files functions ================================================
#write/update information to data files (Khalani)
def writeToStudent(): #write to student account file
    with open(studentAccountfile, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["first name", "last name", "username","password", "language option", "control email", "control SMS", "control targeted advertise", "type", "createdOn","lastLogin"]) #Edited by JaNae (Epic 7)
        for key in studentList:
            writeCSV.writerow([studentList.get(key).fName, studentList.get(key).lName, key, studentList.get(key).password, studentList.get(key).language, studentList.get(key).email, studentList.get(key).sms, studentList.get(key).targetedAdv, studentList.get(key).type, studentList.get(key).createdOn, studentList.get(key).lastLogin]) #Edited by JaNae (Epic 7)
    
def writeToJob():   #write to job file
    with open(jobDataFile, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["jobID","title","description","employer","location","salary","createdBy", "postedOn", "marked", "deleteOn"])
        for job in jobList:
            writeCSV.writerow([job.jobId,job.title,job.description,job.employer,job.location,job.salary,job.createdBy, job.postedOn, job.marked, job.deleteOn])

def writeToProfile():   #write to profile file (QI)
    with open(studentProfilefile, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username","title","major","univsersity name","about me"])
        for key in studentList:
            if(studentList.get(key).StudentProfile.created):
                writeCSV.writerow([key,studentList.get(key).StudentProfile.title,studentList.get(key).StudentProfile.major,studentList.get(key).StudentProfile.university,studentList.get(key).StudentProfile.aboutMe])

def writeToExp():   #write to experience file (QI)
    with open(studentProfileExperiences, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username","title","employer","date started", "data ended", "location", "description"])
        for key in studentList:
            for job in studentList.get(key).StudentProfile.experience:
                writeCSV.writerow([key, job[0], job[1], job[2], job[3], job[4], job[5]])

def writeToEdu():   #write to education file (QI)
    with open(studentProfileEducations, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username","school name","degree","years attended"])
        for key in studentList:
            for edu in studentList.get(key).StudentProfile.education:
                writeCSV.writerow([key, edu[0], edu[1], edu[2]])

def writeToFriend():   #write to friend file (QI)
    with open(studentFriendships, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username","friend with","friend with","friend with", "friend with", "friend with","friend with","friend with","friend with","friend with","friend with"])
        for key in studentList:
            if (len(studentList.get(key).friendship) > 0):
                friendList=[key]
                for friend in studentList.get(key).friendship:
                    friendList.append(friend)
                writeCSV.writerow(friendList)

def writeToFriendRequests():    #write to friend request file (QI)
    with open(studentfriendrequests, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["from/to","username","other","other","other","other","other","other","other","other", "other"])
        for key in studentList:
            if (len(studentList.get(key).requestFrom) > 0):
                friendfrom=["from",key]
                for friend in studentList.get(key).requestFrom:
                    friendfrom.append(friend)
                writeCSV.writerow(friendfrom)
            if (len(studentList.get(key).requestTo) > 0):
                friendto=["to",key]
                for friend in studentList.get(key).requestTo:
                    friendto.append(friend)
                writeCSV.writerow(friendto)


def writeToJobApp():   #write to job file
    with open(jobAppFile, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username","jobID","graduationDate","startByDate","paragraph","appliedDate", "marked"])
        for student in studentList:
            username = student
            for app in studentList.get(username).applications:
                writeCSV.writerow([app.user,app.jobId,app.graduationDate,app.startByDate,app.paragraph,app.appliedDate, app.marked])


def writeToSavedJobs():
    with open(savedJobsFile, 'w', newline ='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username", "jobId", "jobId", "jobId", "jobId", "jobId", "jobId", "jobId", "jobId", "jobId", "jobId"])
        for key in studentList:
            if (len(studentList.get(key).savedJobs) > 0):
                #print("user: " + key + " num saved " + str(len(studentList.get(key).savedJobs)))
                jobs = []
                jobs.append(key)
                for job in studentList.get(key).savedJobs:
                    jobs.append(job.jobId)
                writeCSV.writerow(jobs)


def writeToInbox():
    with open(inboxFile, 'w', newline='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["reciever", "sender", "message", "marked"])
        for key in studentList:
            for message in studentList.get(key).inbox:
                writeCSV.writerow([key, message[0], message[1], message[2]])


def writeToCourseTook():
    with open(courseFile, 'w', newline='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        writeCSV.writerow(["username", "took", "took", "took","took","took"])
        for key in studentList:
            if (len(studentList.get(key).courseTook) > 0):
                courses = []
                courses.append(key)
                for course in studentList.get(key).courseTook:
                    courses.append(course)
                writeCSV.writerow(courses)

#======================================= Main Menus switch cases =========================================
#main menu function - switch cases statements in python (Khalani)
def mainMenuSelection(selection):
    switcher = {
        1: login,
        2: createAccount,
        3: searchForJob,
        4: findSomeone,
        5: viewSkills,
        6: videoMessage,
        7: trainingmenu,
        0: quitOut
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

#main function that perform all the tasks (Khalani)
def mainMenu():
    while True: #Changed by JaNae
        if not loggedIn:
            print("\n\n******************************* Welcome To Community College *******************************"
                    "\n\n                        *******ANASTASIA'S STORY*******" #(JaNae)
                    "\nWhen Anastasia graduated, she found that her college had shoved her into the real" 
                    "\nworld without a leg to stand on. They lacked the support and networking needed for" 
                    "\nAnastasia to find a job. Then she found InCollege. With its vast network of diverse"
                    "\nindividuals, InCollege connected Anastasia to a job in no time. And it can do the"
                    "\nsame with you. Enter '6' to watch an video on why to join InCollege.\n\n"
                    "\n\t[1] Log in using an existing account"
                    "\n\t[2] Create a new InCollege account")
        else:
            if(studentList.get(loggedInUsername).language.lower()=="english"):
                print("\n************************* Welcome "+studentList.get(loggedInUsername).fName.upper()+" "+studentList.get(loggedInUsername).lName.upper()+ " "+ "To Community College *************************")      #Enlish
            elif (studentList.get(loggedInUsername).language.lower()=="spanish"):
                print("\n\n******************** Bienvenido "+studentList.get(loggedInUsername).fName.upper()+" "+studentList.get(loggedInUsername).lName.upper()+ " "+ "A La Universidad Comunitaria ********************")     #spanish
            if(not studentList.get(loggedInUsername).StudentProfile.created):
                print("\n  [V] View My Profile    [C] Create My Profile    [N] View My Inbox   [S] Send message\n")
            elif(studentList.get(loggedInUsername).StudentProfile.created):
                print("\n  [V] View My Profile    [N] View My Inbox   [S] Send message\n")
            pastSevenDayJobNotifi()
            if(not studentList.get(loggedInUsername).StudentProfile.created):
                print("\n\t~~ Don't forget to create a profile")
            newJoinNotifi()
            if(checkfriendrequest()):
                print("\n\t~~ NOTIFICATION: You Have A Pending Friend Request(s). Enter 7 to accept or reject")
            if (checkInbox()):
                print("\n\t~~ NOTIFICATION: You have message(s) waiting for you")
            print("\n\t[1] Login out\n\t[2] Post a new job")

        print("\t[3] Search for a job/internship"
                "\n\t[4] Find/Search someone you know"
                "\n\t[5] Learn a new skill")
        
        if not loggedIn: #Added by JaNae for the 'play video' option
            print("\t[6] Why to join InCollege")
            print("\t[7] Training")
        else:
            print("\t[6] Show my network")
            print("\t[7] Pending friend request")
            print("\t[8] In College Learning")
        print("\t[0] Quit\n\n")
        print("   [Enter L1] Useful Links\t\t       [Enter L2] InCollege Important Links")
        print("\n\n*******************************************************************************************")
        
        selection = input("Enter your selection: ")
        if loggedIn and selection.lower() =="v":
            clear()
            check='n'
            while check.lower()=='n':
                printProfile(loggedInUsername)
                check = yORnCheck(input("Back to main menu? [Y/N]: "),"Back to main menu? [Y/N]: ")
            clear()
        elif loggedIn and selection.lower()=="c":
            clear()
            createProfile()
        elif selection.lower() == 'l1':
            clear()
            usefulLinkMenu()
        elif selection.lower() == 'l2':
            clear()
            importantLinkMenu()
        elif selection.lower() == "n":
            clear()
            inbox()
        elif selection.lower() == "s":
            clear()
            if studentList.get(loggedInUsername).type.lower() == "standard":
                sendMessageStandard()
            elif studentList.get(loggedInUsername).type.lower() == "plus":
                sendMessagePlus()
        else:
            try:
                selection=int(selection)
            except:
                clear()
                print("ERROR: Integer Selection Only OR L1 OR L2")
                continue

            if selection==0:
                clear()
                quitOut()
            elif loggedIn and (selection <1 or selection>8):
                clear()
                print("ERROR: Invalid Main Menu Selection")
                continue
            elif (not loggedIn) and (selection <0 or selection> 7):
                clear()
                print("ERROR: Invalid Main Menu Selection")
                continue
            
            if loggedIn and selection == 1:
                logOut()
                clear()
                print("INFO: Logged Out")
            elif loggedIn and selection==2:
                clear()
                createNewJob()
            elif loggedIn and selection ==4:
                searchStudent()
            elif loggedIn and selection == 7:
                clear()
                friendrequestaccept()
            elif loggedIn and selection ==6:
                clear()
                printFriends(loggedInUsername)
            elif loggedIn and selection == 8:
                clear()
                inCollegeLearning()
            else:
                clear() 
                mainMenuSelection(selection)

#============================== Epic # 3: Two groups of Links Menus (Qi) =======================================================
def helpCenter():
    print("\n\n=========== Help Center ============="
        "\nWe're here to help.\n"
        "=====================================\n")

def about():
    print ("\n\n================================= About ================================"
            "\nIn College: Welcome to In College, the world's largest college student"
           "\nnetwork with many users in many countries and territories worldwide."
           "\nIt is designed to allow college students to create personal accounts,"
           "\nupload profile information, search for and apply for jobs, and connect"
           "\nwith other students both at their college and at other colleges.\n"
           "========================================================================\n")

def press():
    print("\n\n================================= Press ======================================"
        "\nIn College Pressroom: Stay on top of the latest news, updates, and reports.\n"
        "=============================================================================\n")

def blog():
    print("\n\n*** BLOG UNDER CONSTRUCTION ***")

def careers():
    print("\n\n*** CAREERS UNDER CONSTRUCTION ***")

def developers():
    print("\n\n*** DEVELOPERS UNDER CONSTRUCTION ***")

def browse():
    print("\n\n*** BROWSE UNDER CONSTRUCTION ***")

def businessSolution():
    print("\n\n*** BUSINESS SOLUTION UNDER CONSTRUCTION ***")

def directories():
    print("\n\n*** DIRECTORIES UNDER CONSTRUCTION ***")

def copyrightNotice():
    print("\n\n============================== Copyright Notice ================================"
        "\nInCollege respects the intellectual property rights of others."
        "\nYou retain your rights to any content you post or display on this platform." 
        "\nBy posting or displaying information, you are submitting to our right to "
        "\nremove content and/or accounts that infringe upon others’ copyrights or"
        "\ncontain unlawful content."
        "\n\t        © InCollege 2020 All rights reserved.\n"
        "=================================================================================\n")

def accessibility():
    print("\n\n============================== Accessibility ================================"
        "\nTo account for all users’ accessibilities as it pertains to social media,"
        "\nInCollege adheres to the Accessibility Guidelines outlined in the WCAG 2.1.\n"
        "===============================================================================\n")

def userAgreement():
    print("\n\n============================== User Agreement ================================"
        "\nBy signing up or registering an account with InCollege, you are agreeing" 
        "\nto enter into a legally binding contract with InCollege. If you wish to"
        "\nterminate this contract, you may delete your account. This applies to all"
        "\nplatforms of InCollege (website, applications, etc.).\n"
        "===============================================================================\n")

#If user logged and selected this option will allow them to view/update their control feature
def privacyPolicy():
    print("\n\n============================== Privacy Policy ================================"
        "\nThis Privacy Policy applies when you use our platform. You do not have"
          "\nto post or upload personal data, but if you choose to it will be used"
          "\nto enhance your user experience.\n"
          "===============================================================================\n")
    if (loggedIn):
        userInput=input("Do you want to view/update your control feature status? [Y/N]: ")
        userInput = yORnCheck(userInput, "Do you want to view/update your control feature status? [Y/N]: ")
        
        if userInput.lower() == "y":
            guestControls()
        else:
            clear()
        
def cookiePolicy():
    print("\n\n============================== Cookie Policy ================================"
        "\nWe use session cookies which only last as long as the session, the"
          "\ncurrent visit to the platform. These are used to recognize you as a"
          "\nuser and to enhance your user experience.\n"
          "=============================================================================\n")

def copyrightPolicy():
        print("\n\n============================== Copyright Policy ================================"
            "\nInCollege respects the intellectual property rights of others."
        "\nYou retain your rights to any content you post or display on this platform." 
        "\nBy posting or displaying information, you are submitting to our right to "
        "\nremove content and/or accounts that infringe upon others’ copyrights or"
        "\ncontain unlawful content."
        "\n\t        © InCollege 2020 All rights reserved.\n"
        "=================================================================================\n")

def brandPolicy():
    print("\n\n============================== Brand Policy ================================"
        "\nA product branded with the InCollege name or logo is part of InCollege."
            "\nInCollege doesn't allow others to make, sell, or give away anything with"
            "\nour name or logo on it.\n"
            "============================================================================\n")

# The Guest Controls option will provide a signed in user with the ability to individually turn 
# off the InCollege Email, SMS, and Targeted Advertising features (Qi)
def guestControls():
    while True:
        print("\n\n----------- Your Current Control Feature Status -----------------")
        print("\tInCollege Email: {:23}".format(studentList.get(loggedInUsername).email))
        print("\tSMS: {:23}".format(studentList.get(loggedInUsername).sms))
        print("\tTartgeted Advertising: {:23}".format(studentList.get(loggedInUsername).targetedAdv))
        print("-----------------------------------------------------------------")
    
        option = input("Which option do you want to update? [email/sms/targeted advertising/no update]: ")
        if option.lower()=="email" or option.lower()=="sms" or option.lower()=="targeted advertising":
            pass
        elif option.lower()=="no update":
            clear()
            print("INFO: No Update Made")
            return
        else: 
            clear()
            print("ERROR: Invalid Feature Input.") 
            continue

        onOff =""
        #Current status of the features
        if ((option.lower()=="email" and studentList.get(loggedInUsername).email.upper()=="ON") or
            (option.lower()=="sms" and studentList.get(loggedInUsername).sms.upper()=="ON") or
            (option.lower()=="targeted advertising" and studentList.get(loggedInUsername).targetedAdv.upper()=="ON")):
            onOff="OFF"
        elif ((option.lower()=="email" and studentList.get(loggedInUsername).email.upper()=="OFF")or
            (option.lower()=="sms" and studentList.get(loggedInUsername).sms.upper()=="OFF") or
            (option.lower()=="targeted advertising" and studentList.get(loggedInUsername).targetedAdv.upper()=="OFF")):
            onOff="ON"
        #ask if user want to update the feature option or not
        respond = input("Do you want to turn "+ onOff+" InCollege "+option.upper()+" option? [Y/N]: ") 
        respond = yORnCheck(respond, "Do you want to turn "+ onOff+" InCollege "+option.upper()+" option? [Y/N]: ")
        if respond.lower() == 'n':
            clear()
            print("INFO: No Update Made")
            continue
        print("UPDATED: " + option.upper()+" is turned "+onOff)

        #make update if input 'Y'
        if option.lower()=="email" and studentList.get(loggedInUsername).email.upper()=="ON":
            studentList.get(loggedInUsername).email="OFF"
        elif option.lower()=="email" and studentList.get(loggedInUsername).email.upper()=="OFF":
            studentList.get(loggedInUsername).email="ON"
        elif option.lower()=="sms" and studentList.get(loggedInUsername).sms.upper()=="ON":
            studentList.get(loggedInUsername).sms="OFF"
        elif option.lower()=="sms" and studentList.get(loggedInUsername).sms.upper()=="OFF": 
            studentList.get(loggedInUsername).sms="ON"
        elif option.lower()=="targeted advertising" and studentList.get(loggedInUsername).targetedAdv.upper()=="ON":
            studentList.get(loggedInUsername).targetedAdv="OFF"
        elif option.lower()=="targeted advertising" and studentList.get(loggedInUsername).targetedAdv.upper()=="OFF":
            studentList.get(loggedInUsername).targetedAdv="ON"
        
        writeToStudent() #Write to the data file

    return studentList.get(loggedInUsername)  #return student object    

#Selecting the Languages option will allow a user to select between English and Spanish. (Qi)
def languages():
    print("\n============================ Language setting ============================")
    print("\nINFO: Your current application wording is "+studentList.get(loggedInUsername).language.upper() + " \n")
    option = ""
    if(studentList.get(loggedInUsername).language.lower()=="spanish"):
        option = "ENGLISH"
    elif (studentList.get(loggedInUsername).language.lower()=="english"):
        option = "SPANISH"
    
    userInput = input("Do you want to change the application wording to "+ option.upper() +"? [Y/N]: ")
    userInput = yORnCheck(userInput, "Do you want to the application wording to "+ option.upper() +"? [Y/N]: ")
    
    #update language option in the data file
    if ((userInput.lower() == "y") and (option=="ENGLISH")):
        studentList.get(loggedInUsername).language = option
        print("INFO: Changed Language To", option)
        writeToStudent()
    elif ((userInput.lower() == "y") and (option=="SPANISH")):
        studentList.get(loggedInUsername).language = option
        print("INFO: Changed Language To", option)
        writeToStudent()
    elif userInput.lower() == "n":
        clear()
        print("INFO: No Update Made")
     
    return studentList.get(loggedInUsername).language  #return "English" or "Spanish"

# Useful link menu switch statement (Qi)
def usefulLinkSelection(selection):
    switcher = {
        1: usefulGeneralMenu,
        2: browse,
        3: businessSolution,
        4: directories,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

# Useful link -> general switch statement (Qi)
def usefulGeneral(selection):
    switcher = {
        1: createAccount,
        2: helpCenter,
        3: about,
        4: press,
        5: blog,
        6: careers,
        7: developers,
        0: usefulLinkMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

# Useful important link menu switch statement(Qi)
def importantLinkSelection(selection):
    switcher = {
        1: copyrightNotice,
        2: about,
        3: accessibility,
        4: userAgreement,
        5: privacyPolicy,
        6: cookiePolicy,
        7: copyrightPolicy,
        8: brandPolicy,
        9: guestControls,
        10: languages,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

# Useful link -> general navigation(Qi)
def usefulGeneralMenu():
    while True:
        print("\n\n ============ General Info =============\n\n"
            "\t[1] Sign Up\n"
            "\t[2] Help Center\n"
            "\t[3] About\n"
            "\t[4] Press\n"
            "\t[5] Blog\n"
            "\t[6] Careers\n"
            "\t[7] Developers\n"
            "\t[0] Back to Useful Link Menu\n"
            "\n=========================================")
        selection = input("Enter your selection: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection <0 or selection>7:
            clear()
            print("ERROR: Invalid General Menu Selection\n")
            continue
        else:
            clear()
            usefulGeneral(selection)

# Useful link menu navigation (Qi)
def usefulLinkMenu():
    while True:
        print("\n\n============ Useful Link Menu ==============\n\n"
            "\t[1] General\n"
            "\t[2] Browse InCollege\n"
            "\t[3] Business Solutions\n"
            "\t[4] Directories\n"
            "\t[0] Back to Main Menu\n\n"
            "============================================")
        selection = input("Enter your selection [0 to 4]: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection < 0 or selection > 4:
            clear()
            print("ERROR: Invalid Useful Link Menu Selection [0 to 4]")
            continue
        
        clear()
        usefulLinkSelection(selection)

# important menu navigation (Qi)
def importantLinkMenu():
    while True:
        print("\n\n========== InCollege Important Links ==========\n"
            "\n\t[1]  Copyright Notice\n"
            "\t[2]  About\n"
            "\t[3]  Accessibility\n"
            "\t[4]  User Agreement\n"
            "\t[5]  Privacy Policy\n"
            "\t[6]  Cookie Policy\n"
            "\t[7]  Copyright Policy\n"
            "\t[8]  Brand Policy")
        if(loggedIn):
            print("\t[9]  Guest Controls\n"
            "\t[10] Languages") 
        print("\t[0]  Back to Main Menu\n\n==================================================")
        selection = input("Enter your selection: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if (not loggedIn) and (selection <0 or selection>8):
            clear()
            print("ERROR: Invalid Important Links Menu Selection [0 to 8]")
            continue
        elif(loggedIn) and (selection <0 or selection>10):
            clear()
            print("ERROR: Invalid Important Links Menu Selection [0 to 10]")
            continue
        
        clear()
        importantLinkSelection(selection)

#===================================== Main menu options ===========================================
#Main menu option 1: login to an exist account (Monica)
def login():
    while True:
        print("\n\n================= InCollege Account Login =================\n")
        username = input("\tEnter username:       ")
        password = input("\tEnter password:       ")
        print("\n===========================================================")
        if username.lower() in studentList:
            if studentList.get(username.lower()).password == password:
                global loggedIn, loggedInUsername, lastLoginTime
                loggedIn=True
                loggedInUsername = username.lower()
                clear()
                print("INFO: You have successfully logged in\n")
                lastLoginTime=studentList.get(loggedInUsername).lastLogin
                studentList.get(loggedInUsername).lastLogin=datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                writeToStudent()
        if loggedIn == True: break
        tryAgainUser = input("ERROR: Incorrect username / password. Try again? [Y/N]: ")
        tryAgainUser = yORnCheck(tryAgainUser, "Try again? [Y/N]: ")

        if tryAgainUser.lower()== 'n':
            clear()
            break
    return loggedIn

# logout (Qi)
def logOut():
    global loggedIn,loggedInUsername, lastLoginTime
    loggedIn=False
    loggedInUsername=""
    lastLoginTime=None
    studentList.clear()
    jobList.clear()
    readFromCSV()
    return loggedIn

# Main menu option 2: Create a new InCollege account (Monica)
def createAccount():
    studentCreated = False
    valid = ""
    if(maxListCheck(studentList,MAXACCOUNT) == False):
        print("INFO: All Permitted Accounts Have Been Created, Please Come Back Later.")
    else:
        #unique username, pasword: minimum of 8 characters, maximum of 12 characters, at least one capital letter, one digit, one non-alpha character)
        while True:
            validUsername = True
            uniqueName = True
            studentCreated = False
            print("\n\n============== Creating A New InCollege Account ===============\n")
            fName = input("\tEnter your first name:      ") #Added by JaNae
            lName = input("\tEnter your last name:       ") #Added by JaNae
            username = input("\tCreate an username:         ")
            password = input("\tCreate a password:          ")
            print("\n   Notice: PLUS accounts will be billed a monstly fee of $10.")
            accountType = input("\tSTANDARD(S) or PLUS(P) account? [S/P]: ") #Added by JaNae (Epic 7)
            print("\n===============================================================")
            for key in studentList: 
                if studentList.get(key).fName.casefold() == fName.casefold() and studentList.get(key).lName.casefold() == lName.casefold(): #Added by JaNae, first and last name validation
                    uniqueName = False
                    userTryAgain = input("ERROR: Name already associated with an account. Try again? [Y/N]: ")
                    break

            if(uniqueName and (studentList.get(username.lower())!=None)):
                    validUsername=False
                    userTryAgain = input("ERROR: Username Already Exists. Try again? [Y/N]: ")
                    break

            if (not uniqueName) or (not validUsername): 
                print()
                userTryAgain = yORnCheck(userTryAgain,"Try again? [Y/N]: ")
                if userTryAgain.lower() == "y":
                    continue
                elif userTryAgain.lower() == "n":
                    clear()
                    print("INFO: No Account Created")
                    break

            #if the username is not in the system, then check password
            if (checkPW(password)):
                studentCreated = True
            else:
                userTryAgain = input("ERROR: Password must be 8-12 characters, at least one capital letter, one digit, one non-alpha character. Try again? [Y/N]: ")
                userTryAgain = yORnCheck(userTryAgain, "Try again? [Y/N]: ")
                if userTryAgain.lower()=="n":
                    clear()
                    print("INFO: No Account Created")
                    break
                elif userTryAgain.lower()=="y":
                    clear()
                    continue

            if((accountType.lower() != 's') and (accountType.lower() != 'p')):
                userTryAgain = input("ERROR: Account type selection must be 'p' or 's'. Try again? [Y/N]: ")
                userTryAgain = yORnCheck(userTryAgain, "Try again? [Y/N]: ")
                if userTryAgain.lower() == "n":
                    clear()
                    print("INFO: No Account Created")
                    break
                elif userTryAgain.lower() == "y":
                    clear()
                    continue

            #confirm information
            print("\n------------ Comfirm Your Account Info --------------\n"
                  "\tYour Name: {} {}".format(fName, lName))
            print("\tYour Username: ", username)
            print("\tYour Password: ", password)
            if accountType.lower() == 's':
                print("\tSelected account type: STANDARD") #Added by JaNae (Epic 7)
            elif accountType.lower() == 'p':
                print("\tSelected account type: PLUS")
            print("-----------------------------------------------------")
            valid = input("Is Above Information Correct? [Y/N]: ")
            valid = yORnCheck(valid, "Is Above Information Correct? [Y/N]: ")
            if valid.lower() == 'n':
                studentCreated = False
                userTryAgain = input("INFO: No Account Created. Try again? [Y/N]: ")
                userTryAgain = yORnCheck(userTryAgain, "Try again? [Y/N]: ")
                if userTryAgain.lower()=='n':
                    clear()
                    print("INFO: No Account Created")
                    break
                elif userTryAgain.lower()=="y":
                    clear()
                    continue
            elif valid.lower() =='y':
                break
        #update the list and data file
        if studentCreated and valid.lower() == 'y':
            if accountType.lower() == 'p':
                student = StudentAccount(fName, lName, password, type="PLUS", createdOn=datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S') ) #Edited by JaNae to add the first and last name
                studentList.update({username.lower():student})
                writeToStudent()
                clear()
                print("INFO: Congrats Account Created For "+ fName.upper() +" "+lName.upper())
                print("Thank you for choosing PLUS. Your monthly bill will be $10.") #Added by JaNae (Epic 7)
            if accountType.lower() == 's':
                student = StudentAccount(fName, lName, password, type="STANDARD", createdOn=datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'), lastLogin=datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'))  # Edited by JaNae to add the first and last name
                studentList.update({username.lower(): student})
                writeToStudent()
                clear()
                print("INFO: Congrats Account Created For " + fName.upper() + " " + lName.upper())
    return studentCreated


# Logged in menu option 2: User must login. creates a jobListing object that takes in its parameters (Khalani)
def createNewJob():
    if(maxJobCheck() == False):
        print("\nINFO: Maximum Amount of Jobs Allowed Currently Have Been Created, Please Come Back Later.")
        return False
    print("\n\n==================== Post An New Job: Gather Information ======================\n")
    title = input("\tEnter the title for the Job: ")
    description = input("\tEnter a brief description of the Job: ")
    employer = input("\tEnter the employer name: ")
    location = input("\tLocation for this job: ")
    while True: #input validation check for salary
        salary = input("\tSalary for this listing: ")
        try:
            salary=float(salary)
            if (salary>0): break
        except:
            print("\t\tERROR: Must Be A Positive Numeric Value")

    print("===============================================================================")
    #update data file and job list 
    jobIDList=[]
    for job in jobList:
        jobIDList.append(int(job.jobId))
    newJobID = str(max(jobIDList)+1)

    Job = JobListing(newJobID,title,description, employer, location, str(salary), studentList.get(loggedInUsername).fName + " "+studentList.get(loggedInUsername).lName, datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'), "IN", None)
    jobList.append(Job)
    writeToJob()
    clear()
    print("\nINFO: Job "+newJobID+" Successfully Created.")
    return Job


def jobSearchSelection(selection):
    switcher = {
        1: displayAllJobs,
        2: displaySavedJobs,
        3: displayAppliedJobs,
        4: displayNonAppliedJobs,
        5: deleteJob,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()



#Main Menu option 3: search for job/internship #Khalani
def searchForJob():
    if(loggedIn == False):
        print("*** Must be logged in to access this feature! ***")
        return

    while True:
        print("\n================================= Search for a job =================================")
        numJobNotifi()
        newPostedNotifi()
        newDeleteNotifi()
        print("\n\t[1] Explore Job Catalogue! Apply, Save and More!"
              "\n\t[2] Display saved jobs [read-only]"
              "\n\t[3] Display Jobs you've applied [read-only]"
              "\n\t[4] Display all jobs not applied [read-only]"
              "\n\t[5] Delete jobs you have posted"
              "\n\t[0] Back to main menu"
              "\n\n====================================================================================")

        selection = input("Select from the menu: ")
        try:
            selection = int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection < 0 or selection > 5:
            clear()
            print("ERROR: Invalid Job Menu Selection [0 to 5]\n")
            continue
        
        if selection ==0:
            clear()
            return 

        clear()
        jobSearchSelection(selection)




#Main menu option 5: skill sub-menu selection - switch cases (Qi/Monica)
def skillMenuSelection(selection):
    switcher = {
        1: woodworking,
        2: microsoftWord,
        3: microsoftExcel,
        4: microsoftTeam,
        5: ArtificIntelligence,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

def viewSkills():
    while True:
        print("\n============= Learn New Skill ============="
            "\n\t[1] Woodworking"
            "\n\t[2] Microsoft Word"
            "\n\t[3] Microsoft Excel"
            "\n\t[4] Microsoft Team"
            "\n\t[5] Artificial Intelligence"
            "\n\t[0] Back to main menu"
            "\n===========================================")

        selection = input("Which skill would you like to learn: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection <0 or selection>5:
            clear()
            print("ERROR: Invalid Skill Menu Selection [0 to 5]\n")
            continue

        clear()
        skillMenuSelection(selection)

#Main Menu option 6: display video (JaNae)
def videoMessage():
    print("\nINFO: Video Is Now Playing.\n")
    while True:
        userInput = input("Back to main menu? [Y/N]: ")
        userInput = yORnCheck(userInput, "Back to main menu? [Y/N]: ")
        if userInput.lower() == 'y':
            break

    return "Video is now playing" #For testing


#Main Menu option 7: connect to help (JaNae)
def connectHelpSelection(selection):
    switcher = {
        1: login,
        2: createAccount,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

# Find someone already joined InCollege, if yes, provide option to join, else back to main menu(Janae/Qi)
def findSomeone():
    global loggedIn
    found=False
    print("============================= Connect For Help =============================")
    name = input("\nEnter connection's name [firstname lastname]: ")
    for key in studentList:
        if (studentList.get(key).fName +" " +studentList.get(key).lName).casefold() == name.casefold():
            found=True
            break
    #if found, then user select to login, signup or back to main
    if found:
        print("INFO: They are a part of the InCollege system.\n")
        if loggedIn is False:
            join_choice = input("Would you like to join InCollege? [Y/N]: ")
            join_choice = yORnCheck(join_choice, "Would you like to join InCollege? [Y/N]:")
            if join_choice.lower() == 'y':
                while True:
                    print("============================= Connect For Help =============================")
                    print("\n\n\t\t========= How Would You Like To Join ========="
                        "\n\t\t\t[1] Log in"
                        "\n\t\t\t[2] Sign Up"
                        "\n\t\t\t[0] Back to main menu"
                        "\n\t\t===========================================\n")
                    selection= input("Enter your selection: ")
                    try:
                        selection=int(selection)
                        if selection <0 or selection>2:
                            clear()
                            print("ERROR: Invalid Selection\n")
                    except:
                        clear()
                        print("ERROR: Integer Selection Only")
                        continue
                    result=False
                    if selection == 0:
                        return found
                    result = connectHelpSelection(selection)
                    if(result==True):
                        break
    else:
        clear()
        print("INFO: They are not yet a part of the InCollege system yet.")

    return found #For testing: return friend found or not

#Main Menu option 0: Program exit (Khalani)
def quitOut():
    sys.exit("\nGoodbye...\n\n")


#===================== Main Menu Option 5:  Skill Sub Menu Options ======================
#Skill menu option 1
def woodworking():
    print("*** WOODWORKING UNDER CONSTRUCTION ***")

#Skill menu option 2
def microsoftWord():
    print("*** MICROSOFTWORD UNDER CONSTRUCTION ***")

#Skill menu option 3
def microsoftExcel():
    print("*** MICROSOFTEXCEL UNDER CONSTRUCTION ***")

#Skill menu option 4
def microsoftTeam():
    print("*** MICROSOFTTEAM UNDER CONSTRUCTION ***")

#Skill menu option 5
def ArtificIntelligence():
    print("*** AI UNDER CONSTRUCTION ***")


#================================ Epic #4 Profile (Qi) ===============================
#Allow logged user to create their profile
def createProfile():
    print("\n\n================================ CREATING THE PROFILE ================================ \n\n"
          "NOTE: press ENTER to skip certain field(s)\n")
    title = input("\tEnter a title for the profile: ")
    major = ToUpperWord(input("\tEnter your major: "))
    university = ToUpperWord(input("\tEnter your university name: "))
    aboutMe = input("\tEnter a paragraph with information about you: ")

    studentList.get(loggedInUsername.lower()).StudentProfile.created=True
    studentList.get(loggedInUsername.lower()).StudentProfile.title=title
    studentList.get(loggedInUsername.lower()).StudentProfile.major=major
    studentList.get(loggedInUsername.lower()).StudentProfile.university=university
    studentList.get(loggedInUsername.lower()).StudentProfile.aboutMe=aboutMe


    print("\n\n\n     -------------------------- Experience Section --------------------------\n")
    numJob = input("\tHow many previous job experiences do you want to enter [0 to 3]: ")
    
    while True:
        if(numJob.isdigit()):
            if not (0<=int(numJob)<=3):
                numJob = input("\n\tERROR: Invalid Range [0 to 3]. Please re-enter: ")
                continue
            else:
                numJob=int(numJob)
                break
        else:
            numJob = input("\n\tERROR: Invalid Range [0 to 3]. Please re-enter: ")

    for count in range(numJob):
        print("\n\n     Job # "+ str(count+1))
        jobTitle = input("\tEnter job title: ")
        employer = input("\tEnter employer: ")
        startDate = convertDate(input("\tEnter date started [mm/dd/yyyy]: "),"Enter date started [mm/dd/yyyy]: " )
        endDate = convertDate(input("\tEnter date ended [mm/dd/yyyy]: "), "Enter date ended [mm/dd/yyyy]: ")
        location = input("\tEnter job location: ")
        description = input("\tDescription of what you did: ")
        studentList.get(loggedInUsername.lower()).StudentProfile.experience.append([jobTitle,employer,startDate,endDate,location, description])
    print("\n     -------------------------------------------------------------------------\n")

    print("\n\n\n     -------------------------- Education Section --------------------------\n")
    numEducation = input("\tHow many education information do you want to enter [0 to 10]: ")
    
    while True:
        if(numEducation.isdigit()):
            if not (0<=int(numEducation)<=10):
                numEducation = input("\n\tERROR: Invalid Range [0 to 10]. Please re-enter: ")
                continue
            else:
                numEducation=int(numEducation)
                break
        else:
            numEducation = input("\n\tERROR: Invalid Range [0 to 10]. Please re-enter: ")

    for count in range(numEducation):
        print("\n\n     Education # "+ str(count+1))
        school =  input("\tEnter school name: ")
        degree = input("\tEnter degree: ")
        yearAttend = input("\tEnter years attended [start-end]: ")
        studentList.get(loggedInUsername.lower()).StudentProfile.education.append([school,degree,yearAttend])
    print("\n     -------------------------------------------------------------------------\n")

    writeToProfile()
    writeToExp()
    writeToEdu()
    clear()
    print("INFO: Profile Created")

    return studentList.get(loggedInUsername.lower()).StudentProfile #return the logged user's StudentProfile class (who created the profile)
    

# Print out an user's profile information by pass in the username. Return a message if no profile data
def printProfile(username):
    clear()
    if(studentList.get(username.lower()).StudentProfile.created):   #profile created by this user
        print("\n\n================================ Profile for " +
              studentList.get(username.lower()).fName.upper() + " " +
              studentList.get(username.lower()).lName.upper() + " ================================\n")
        print ("\n    " + insert_newlines(studentList.get(username.lower()).StudentProfile.title, "-\n   ", 80)+"\n\n")
        print ("    MAJOR:          "+ studentList.get(username.lower()).StudentProfile.major+"\n")
        print ("    UNIVERSITY:     "+insert_newlines(studentList.get(username.lower()).StudentProfile.university, '-\n\t\t    ', 70)+"\n")
        print ("    About Me:       "+insert_newlines(studentList.get(username.lower()).StudentProfile.aboutMe,'-\n\t\t    ', 60)+"\n")
        print ("\n\n\t--------------------------- Experience Section ---------------------------\n")
        count=1
        for exps in studentList.get(username.lower()).StudentProfile.experience:
            print("\tJob #" + str(count))
            print("\t\t{:<20}".format("Job Title: ")+exps[0])
            print("\t\t{:<20}".format("Employer: ")+exps[1])
            print("\t\t{:<20}".format("Date Started: ")+exps[2])
            print("\t\t{:<20}".format("Date Ended: ")+exps[3])
            print("\t\t{:<20}".format("Location: ")+exps[4])
            print("\t\t{:<20}".format("Description: ")+insert_newlines(exps[5],'-\n\t\t\t\t    ',45)+"\n\n")
            count+=1
        print ("\t--------------------------------------------------------------------------\n\n")

        print ("\n\t--------------------------- Education Section --------------------------\n")
        count=1
        for exps in studentList.get(username.lower()).StudentProfile.education:
            print("\tEducation #" + str(count))
            print("\t\t{:<20}".format("School Name: ")+ ToUpperWord(exps[0]))
            print("\t\t{:<20}".format("Degree: ")+ exps[1])
            print("\t\t{:<20}".format("Years attended: ")+ exps[2]+"\n\n")
            count+=1
        print("\t--------------------------------------------------------------------------\n\n")
        print ("====================================================================================\n")
    else:   #profile has not been created by this user
        print("\n========================================================================")
        print("\nINFO: No Profile Information For "+ studentList.get(username.lower()).fName+" "+studentList.get(username).lName+"\n")
        print("========================================================================\n")

#print a list of username friend with
def printFriends(username):
    while True:
        notPrint=[]
        count = 1
        print("\n========================== "+studentList.get(username.lower()).fName.upper()+" "+studentList.get(username).lName.upper() +"'s Network ==========================\n\n")
        print("\tDisconnect With\t\tView Profile\t\tName")
        print("\t---------------\t\t------------\t\t-----\n")
        for friend in studentList.get(username.lower()).friendship:
            print("\t[DISCONNECT "+str(count)+"]",end="")
            if(studentList.get(friend.lower()).StudentProfile.created):
                print("\t\t[PROFILE "+str(count) + "]", end="")
            else:
                print("\t\t\t", end="")
                notPrint.append(count)
            print("\t\t"+ studentList.get(friend.lower()).fName +" "+ studentList.get(friend.lower()).lName+"\n")
            count+=1
        print("\n\n                                                [0] Back to main menu\n")
        print("===============================================================================")
        
        DorP = ""
        numList = -1

        ans = input("Enter \"DISCONNECT #\" or \"PROFILE #\" or 0: ")
        words=ans.split()
        
        if len(words) ==1:
            if(words[0].isdigit()):
                if not (0==int(words[0])):
                    clear()
                    print("\nERROR: Invalid Input [DISCONNECT/PROFILE #] or 0.\n")
                    continue
                else:
                    clear()
                    return
            else:
                clear()
                print("\nERROR: Invalid Input [DISCONNECT/PROFILE #] or 0.\n")
                continue
        elif len(words)==2:
            if (words[0].lower() == "disconnect" or words[0].lower()=="profile"):
                pass
            else:
                clear()
                print("\nERROR: Invalid Input [DISCONNECT/PROFILE #] or 0.\n")
                continue
            if(words[1].isdigit()):
                if (not (1<=int(words[1])<=len(studentList.get(loggedInUsername.lower()).friendship)) and (int(words[1]) in notPrint)):
                    clear()
                    print("\nERROR: Invalid Input [DISCONNECT/PROFILE #] or 0.\n")
                    continue
                else:
                    DorP=words[0].lower()
                    numList=int(words[1])
            else:
                clear()
                print("\nERROR: Invalid Input [DISCONNECT/PROFILE #] or 0.\n")
                continue
        else:
            clear()
            print("\nERROR: Invalid Input [DISCONNECT/PROFILE #] or 0.\n")
            continue

        if DorP == "disconnect":
            clear()
            disconnectFriend(studentList.get(username.lower()).friendship[numList-1])
        elif DorP == "profile":
            while True:
                clear()
                printProfile(studentList.get(username.lower()).friendship[numList-1])
                userInput = input("Back to your network list? [Y/N]: ")
                userInput = yORnCheck(userInput, "Back to your nextwork list? [Y/N]: ")
                if(userInput.lower()=='y'):
                    break


    return studentList.get(username).friendship  #return a list of friend for that user


def searchStudent():#Function that searches a student by their last name or university or major
    clear()
    while True:
        studentlistfind = []
        while True:
            print("\n\n================================ Search New Friend ================================\n")
            print("\t[1] Last name\n\t[2] University\n\t[3] Major\n\t[0] Back to main menu")
            print("\n=======================================================================================\n")
            option = input("How would you like to search?: ")

            clear()
            if option == "1":#search by lastname
                print("\n======================== Search By Last Name ========================\n")
                lastname = input("\tEnter last name: ")
                for key in studentList:
                    if (studentList.get(key).lName.lower() == lastname.lower() and key != loggedInUsername):
                        studentlistfind.append(key)
            elif option == "2":#search by university
                print("\n======================== Search By University ========================\n")
                univ = input("\tEnter university: ")
                for key in studentList:
                    if (studentList.get(key).StudentProfile.university.lower() == univ.lower() and key != loggedInUsername):
                        studentlistfind.append(key)
            elif option == "3":#Search by major
                print("\n========================= Search By Major =========================\n")
                major = input("\tEnter the major: ")
                for key in studentList:
                    if (studentList.get(key).StudentProfile.major.lower() == major.lower() and key != loggedInUsername):
                        studentlistfind.append(key)
            elif option == "0":
                return
            else:
                clear()
                print("ERROR: Invalid Selection\n")
                continue
            break

        if len(studentlistfind) == 0:#If no student was found
            print("\nINFO: No student was found") 

        else:
            count = 1
            newlist = []
            friended=[]
            requestfrom=[]
            requestto=[]
            print("\n      --------------------- Search Results --------------------\n")
            for key in studentlistfind:         #if already friend
                if key in studentList.get(loggedInUsername).requestFrom:
                    requestfrom.append(key)
                elif key in studentList.get(loggedInUsername).requestTo:
                    requestto.append(key)
                elif key in studentList.get(loggedInUsername).friendship:
                    friended.append(key)
                else:
                    newlist.append(key)
                    
            studentlistfind = []
            for key in newlist:
                studentlistfind.append(key)
            print("\tStatus\t\t\tName")
            print("\t------\t\t\t----")
            for key in friended:
                fname = studentList.get(key).fName
                lname = studentList.get(key).lName
                print("\n\t<connected>\t\t" + fname + " " + lname )

            for key in requestfrom:
                fname = studentList.get(key).fName
                lname = studentList.get(key).lName
                print("\n\t<pending>\t\t" + fname + " " + lname )

            for key in requestto:
                fname = studentList.get(key).fName
                lname = studentList.get(key).lName
                print("\n\t<pending>\t\t" + fname + " " + lname )

            if(len(studentlistfind)==0):
                print("\n\tINFO: No Additional New Search Result")
                print("\n      --------------------------------------------------------\n")
                print("\n===================================================================\n")
            else:
                for key in studentlistfind:#Printing all student who did match with the search
                    fname = studentList.get(key).fName
                    lname = studentList.get(key).lName
                    print("\n\t[" + str(count) + "]\t\t\t" + fname + " " + lname)
                    count = count + 1
                print("      --------------------------------------------------------\n")
                print("\n\t\t\t\t\t\t\t[0] Return")
                print("\n===================================================================\n")

                while True:
                    selection = input("Select the student for send a friend request or 0: ")#Getting the student to send friend request
                    if selection == "0":
                        clear()
                        return
                    elif selection.isdigit():
                        if (int(selection) < 0) and (int(selection) > len(studentList.get(loggedInUsername).studentlistfind)):
                            print("INFO: No Student Found")
                            break
                        else:
                            studentList.get(studentlistfind[int(selection)-1]).requestFrom.append(loggedInUsername)
                            studentList.get(loggedInUsername).requestTo.append(studentlistfind[int(selection)-1])
                            print("INFO: Friend Request Sent To " + studentList.get(studentlistfind[int(selection)-1]).fName +" "+studentList.get(studentlistfind[int(selection)-1]).lName)
                            writeToFriendRequests()#Updating file with friend requests
                            break
                    else:
                        print("ERROR: Invalid Selection.")


        userInput = yORnCheck(input("\nDo another search? [Y/N]: "), "Do another search? [Y/N]: ")
        if (userInput.lower() == 'y'):
            clear()
            continue
        else:
            clear()
            break
    return studentList.get(loggedInUsername)  #return user

#check if logged in user have any pending friend request or not
def checkfriendrequest():
    if not loggedIn:
        return False
    if len(studentList.get(loggedInUsername).requestFrom) != 0:
        return True
    return False

#accept or reject friend request
def friendrequestaccept():
    while True:
        if((len(studentList.get(loggedInUsername).requestFrom) ==0) and (len(studentList.get(loggedInUsername).requestTo)==0)):
            while True:
                print("\n\n================================ Pending Friend Requests ================================\n")
                print(" YOU HAVE NO PENDING FRIEND REQUESTS")
                print("\n======================================================================================\n")
                userInput = yORnCheck(input("\nBack to main menu? [Y/N]: "), "Back to main menu? [Y/N]: ")
                if (userInput.lower() == 'y'):
                    clear()
                    return
                else:
                    clear()
                    continue

        print("\n\n================================ Pending Friend Requests ================================\n")
        for users in studentList.get(loggedInUsername).requestTo:
            print("\t<WAITING>      "+studentList.get(users).fName + " " + studentList.get(users).lName+"\n")
        count=1
        print("-----------------------------------------------------------------------------------------\n")
        for users in studentList.get(loggedInUsername).requestFrom:
            print("\t[ACCEPT/REJECT "+ str(count)+"]      "+studentList.get(users).fName + " " + studentList.get(users).lName+"\n")
            count+=1
        print("\n                                                             [0] Back to main menu")
        print("\n======================================================================================\n")

        AorR = ""
        numList=-1
        while True:
            ans = input("Enter ACCEPT or REJECT follow by the request number [ACCEPT/REJECT #] or 0: ")
            words=ans.split()
            
            if len(words) ==1:
                if(words[0].isdigit()):
                    if not (0==int(words[0])):
                        print("\nERROR: Invalid Input [ACCEPT/REJECT #] or 0.\n")
                    else:
                        clear()
                        return
                else:
                    print("\nERROR: Invalid Input [ACCEPT/REJECT #] or 0.\n")
            elif len(words)==2:
                if (words[0].lower() == "accept" or words[0].lower()=="reject"):
                    pass
                else:
                    print("\nERROR: Invalid Input [ACCEPT/REJECT #] or 0.\n")
                if(words[1].isdigit()):
                    if not (1<=int(words[1])<=len(studentList.get(loggedInUsername.lower()).requestFrom)):
                        print("\nERROR: Invalid Input [ACCEPT/REJECT #] or 0.\n")
                    else:
                        AorR=words[0].lower()
                        numList=int(words[1])
                        break                
                else:
                    print("\nERROR: Invalid Input [ACCEPT/REJECT #] or 0.\n")
            else:
                print("\nERROR: Invalid Input [ACCEPT/REJECT #] or 0.\n")

        if AorR == "reject":
            friendName=studentList.get(loggedInUsername).requestFrom[numList-1]
            studentList.get(loggedInUsername).requestFrom.remove(friendName)
            studentList.get(friendName).requestTo.remove(loggedInUsername)
            clear()
            print("INFO: You rejected "+studentList.get(friendName).fName.upper()+ " "+studentList.get(friendName).lName.upper() +" To Be Your Friend.")
        elif AorR == "accept":
            friendName = studentList.get(loggedInUsername).requestFrom[numList-1]
            studentList.get(loggedInUsername).friendship.append(friendName)
            studentList.get(friendName).friendship.append(loggedInUsername)
            studentList.get(loggedInUsername).requestFrom.remove(friendName)
            studentList.get(friendName).requestTo.remove(loggedInUsername)
            clear()
            print("INFO: Congrats "+studentList.get(friendName).fName.upper()+ " "+studentList.get(friendName).lName.upper() +" And You Are Friend Now!")

        writeToFriend()
        writeToFriendRequests()
    
def disconnectFriend(username): #Qi
    print("\n\n=============================== Comfirm To Disconnect =================================\n")
    firstName = studentList.get(username).fName.upper()
    lastName = studentList.get(username).lName.upper()

    userInput = yORnCheck(input("Are you should you want to disconnect with "+ firstName + "" + lastName + " from InCollege System? [Y/N]: "),"Are you should you want to disconnect with "+ firstName + "" + lastName + " from InCollege System? [Y/N]: ")
    if userInput.lower() == "y":
        studentList.get(username).friendship.remove(loggedInUsername)
        studentList.get(loggedInUsername).friendship.remove(username)
        print("INFO: "+ firstName + " " + lastName +" And You Are Disconnect From InCollege System.")
    else:
        clear()
        print("\nINFO: No One Got Disconnected.\n")

    writeToFriend()
    return

def displayIndividualJob(job): #Qi
    print("\n================================== Job ID: "+job.jobId + " ============================================\n")
    print("\n\t{:30}{:50}".format("TITLE: ", job.title))
    print("\t{:30}".format("DESCRIPTION: ")+insert_newlines(job.description,'-\n\t\t\t\t      ',45))
    print("\t{:30}{:50}".format("EMPLOYER: ", job.employer))
    print("\t{:30}{:50}".format("LOCATION: ", job.location))
    print("\t{:30}{:50}".format("SALARY: ", job.salary))
    print("\t{:30}{:50}".format("CREATED BY: ", job.createdBy))

    if job in studentList.get(loggedInUsername).appliedJobs: #prints applied to jobs with an X
        print("\t{:30}{:50}".format("APPLICATION STATUS: ", "Applied"))
    else: #marks jobs not applied to with O
        print("\t{:30}{:50}".format("APPLICATION STATUS: ", "Not Applied Yet"))

    if job in studentList.get(loggedInUsername).savedJobs:
        print("\t{:30}{:50}\n".format("SAVE STATUS: ", "Saved"))
    else:
        print("\t{:30}{:50}\n".format("SAVE STATUS: ", "Unsave"))

    print("\n==========================================================================================\n")

def displayAllJobs(): #Khalani Displays all listed jobs in the system, Jobs already applied to are marked
    while True:
        print("\n\n========================= All Jobs that are currently in the System ============================\n")
        idList=[]
        for job in jobList:
            if job.marked =="IN":
                if job in studentList.get(loggedInUsername).appliedJobs: #prints applied to jobs with an X
                    print("\t<Applied>\t",end="")
                else:
                    print("\t{:10}\t".format("           "),end="")
                print("{:10}{:15}".format("JOB ID: ",job.jobId)+"{:10}{:30}\n".format("TITLE: ", job.title))
                idList.append(int(job.jobId))
        print("                                                                    [0] Back to Job menu\n")
        print("==================================================================================================")


        selection = input("Enter the job ID you would like to select or 0: ")
        try:
            selection = int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if (selection != 0) and ( selection not in idList):
            clear()
            print("ERROR: Invalid Job ID")
            continue

        if (selection == 0):
            clear()
            return
        clear()

        for jobInList in jobList:
            if int(jobInList.jobId) == selection and jobInList.marked=="IN":
                job = jobInList
                break
        while True:
            displayIndividualJob(job)
            
            print("\t[1] Apply to this Job"
                "\n\t[2] Save this job"
                "\n\t[3] Unsave this job"
                "\n\t[0] Select a different job\n")

            nextChoice = input("What would you like to do with this Job?: ")
            try:
                nextChoice = int(nextChoice)
            except:
                clear()
                print("ERROR: Integer Selection Only")
                continue

            if nextChoice < 0 or nextChoice > 3:
                clear()
                print("ERROR: choose integer from [0 to 3]\n")
                continue
            
            clear()

            if nextChoice == 0:
                clear()
                break
            elif (nextChoice == 1):
                ApplyToJob(job)
            elif (nextChoice == 2):
                saveJob(job)
            elif (nextChoice == 3):
                unSaveJob(job)
            




def saveJob(job): #Monica saves a job, adds job object to savedJobs list of studentAccount
    alreadySaved = False
    for savedJob in studentList.get(loggedInUsername).savedJobs:
        if job.jobId == savedJob.jobId:
            alreadySaved = True

    if not alreadySaved:
        studentList.get(loggedInUsername).savedJobs.append(job)
        print("INFO: Job ID "+job.jobId+" saved Successfully\n\n")
    else:
        print("INFO: Job ID "+job.jobId+" Is Already Saved\n\n")
    writeToSavedJobs()

def unSaveJob(job): #Monica removes job from savedJobs list
    save=False
    for savedJob in studentList.get(loggedInUsername).savedJobs:
        if job.jobId == savedJob.jobId:
            save=True

    if save:
        studentList.get(loggedInUsername).savedJobs.remove(job)
        print("INFO: Successfully Unsaved Job ID "+job.jobId+"\n\n")
    else:
        print("INFO: Job ID "+job.jobId+" Is Not Currently Saved\n\n")
    writeToSavedJobs()
    



def ApplyToJob(job): #Khalani Creates an application object and saved it in list of applications list of studentAccount
    if job in studentList.get(loggedInUsername).appliedJobs:
        print("INFO: You have already applied for the job with Job ID "+job.jobId+" \n\n")
        return
    print("========================== Apply For Job "+job.jobId+" "+job.title+" ===================================")
    studentList.get(loggedInUsername).appliedJobs.append(job)
    gradDate = ApplicationDate(input("\nEnter your expected graduation date [mm/dd/yyyy]: "), "Enter date ended [mm/dd/yyyy]: ")
    startDate = ApplicationDate(input("\nEnter the day you can begin working [mm/dd/yyyy]: "), "Enter date ended [mm/dd/yyyy]: ")
    description = input("\nPlease give a paragraph of text explaining why you are a good fit for the job: ")
    print("==========================================================================================================")
    
    Application = JobApplication(loggedInUsername, job.jobId, gradDate, startDate, description,datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'), "IN")

    studentList.get(loggedInUsername).applications.append(Application)
    clear()
    print("INFO: Job Application Sent For Job ID "+job.jobId+"\n\n")
    writeToJobApp()


def displayAppliedJobs(): #Khalani displays i na read only form all jobs loggedinuser has appleid to
    check='n'
    while check.lower()=='n':
        print("\n\n========================== Job(s) "+studentList.get(loggedInUsername).fName.upper()+" "+studentList.get(loggedInUsername).lName.upper()+ " Applied ========================\n")
        empty = True
        for job in jobList:
            if job in studentList.get(loggedInUsername).appliedJobs and job.marked=="IN":
                print("\nJOB ID: "+job.jobId)
                print("\n\t{:20}{:50}".format("TITLE: ", job.title))
                print("\t{:20}".format("DESCRIPTION: ")+insert_newlines(job.description,'-\n\t\t\t    ',45))
                print("\t{:20}{:50}".format("EMPLOYER: ", job.employer))
                print("\t{:20}{:50}".format("LOCATION: ", job.location))
                print("\t{:20}{:50}".format("SALARY: ", job.salary))
                print("\t{:20}{:50}".format("CREATED BY: ", job.createdBy))
                print("")
                empty = False

        if(empty == True):
            print("*** You have not applied to any jobs! ***")
        print("\n\n=========================================================================================================\n")
        check = yORnCheck(input("Back to Job Menu? [Y/N]: "),"Back to Job Menu? [Y/N]: ")
        clear()


def displaySavedJobs(): #Khalani Read-only, dispalys all saved jobs of logged in user
    check='n'
    while check.lower()=='n':
        print("\n\n=============================== Job(s) Saved By "+studentList.get(loggedInUsername).fName.upper()+" "+studentList.get(loggedInUsername).lName.upper()+ " ========================================\n")
        empty = True
        for job in jobList:
            if job in studentList.get(loggedInUsername).savedJobs and job.marked=="IN":
                print("\nJOB ID: "+job.jobId)
                print("\n\t{:20}{:50}".format("TITLE: ", job.title))
                print("\t{:20}".format("DESCRIPTION: ")+insert_newlines(job.description,'-\n\t\t\t    ',45))
                print("\t{:20}{:50}".format("EMPLOYER: ", job.employer))
                print("\t{:20}{:50}".format("LOCATION: ", job.location))
                print("\t{:20}{:50}".format("SALARY: ", job.salary))
                print("\t{:20}{:50}".format("CREATED BY: ", job.createdBy))
                print("")
                empty = False

        if empty == True:
            print("\tINFO: You Have Not Saved Any Jobs! ***")
        print("\n\n=========================================================================================================\n")
        
        check = yORnCheck(input("Back to Job Menu? [Y/N]: "),"Back to Job Menu? [Y/N]: ")
        clear()


def displayNonAppliedJobs(): #Khalani Read-only displays all jobs not applied to by logged in user
    check='n'
    while check.lower()=='n':
        print("\n\n=============================== Job(s) "+studentList.get(loggedInUsername).fName.upper()+" "+studentList.get(loggedInUsername).lName.upper()+ " Did Not Applied ========================================\n")
        empty = True
        for job in jobList:
            if job.marked =="IN":
                if job in studentList.get(loggedInUsername).appliedJobs:
                    pass
                else:
                    print("\nJOB ID: "+job.jobId)   
                    print("\n\t{:20}{:50}".format("TITLE: ", job.title))
                    print("\t{:20}".format("DESCRIPTION: ")+insert_newlines(job.description,'-\n\t\t\t    ',45))
                    print("\t{:20}{:50}".format("EMPLOYER: ", job.employer))
                    print("\t{:20}{:50}".format("LOCATION: ", job.location))
                    print("\t{:20}{:50}".format("SALARY: ", job.salary))
                    print("\t{:20}{:50}".format("CREATED BY: ", job.createdBy))
                    print("")
                    empty = False
        if empty == True:
                print("\tINFO: You Have Applied To All Jobs In The InCollege System!")
        print("\n\n=========================================================================================================\n")

        check = yORnCheck(input("Back to Job Menu? [Y/N]: "),"Back to Job Menu? [Y/N]: ")
        clear()

def deleteJob(): #Removes job from system and any, saved, applied to, and job listing associations or datafiles
    while True:
        fullname = studentList.get(loggedInUsername).fName + " " + studentList.get(loggedInUsername).lName
        print("\n\n=========================== Job(s) Posted By "+fullname.upper()+ " =============================\n")
        jobIDList=[]
        for job in jobList:
            if job.createdBy.lower() == fullname.lower() and job.marked == "IN":
                print("\nJOB ID: "+job.jobId)
                print("\n\t{:20}{:50}".format("TITLE: ", job.title))
                print("\t{:20}".format("DESCRIPTION: ")+insert_newlines(job.description,'-\n\t\t\t    ',45))
                print("\t{:20}{:50}".format("EMPLOYER: ", job.employer))
                print("\t{:20}{:50}".format("LOCATION: ", job.location))
                print("\t{:20}{:50}\n".format("SALARY: ", job.salary))
                jobIDList.append(int(job.jobId))
        if len(jobIDList) ==0:
            print("\tINFO: You Have No Posted Job")
        print("\n                                                            [0] Back to Job Menu")
        print("\n=====================================================================================\n")

        while True:
            selection = input("Enter Job ID for the job you would like to delete or 0: ")
            try:
                selection = int(selection)
            except:
                print("ERROR: Integer Selection Only")
                continue

            if selection != 0 and (selection not in jobIDList):
                print("ERROR: Invalid Job ID\n")
                continue
            else:
                break
        
        if selection == 0:
            clear()
            return

        found = False
        for job in jobList:
            if int(job.jobId) == selection and job.marked=="IN":
                found = True
                job.marked='DELETED'
                job.deleteOn=datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                writeToJob()
                break
                #jobList.remove(job)

        if found == False:
            clear()
            print("ERROR: No such Job Exists")
            deleteJob()

        for student in studentList:
            username = student
            for job in studentList.get(username).appliedJobs:
                if int(job.jobId) == selection:
                    job.marked="DELETED"
            for app in studentList.get(username).applications:
                if int(app.jobId) == selection:
                    app.marked="DELETED"
            for savedJob in studentList.get(username).savedJobs:
                if int(savedJob.jobId) == selection:
                    savedJob.marked="DELETED"

        writeToSavedJobs()
        writeToJob()
        writeToJobApp()
        clear()
        print("INFO: Job ID "+str(selection)+" Successfully Deleted")

def inbox():
    print("\n\n============================== INBOX ===================================\n")
    i = 1
    print("\t    SENDER\t\tMARKS")
    print("\t    ------\t\t-----\n")
    for message in studentList.get(loggedInUsername).inbox:
            index = str(i)
            print("\t["+index + "] " + message[0] + "\t\t" + message[2] + "\n")
            i = i + 1
    print("=========================================================================")
    selection = input("\nEnter the index of the message you would like to read OR enter 0 to return to main menu: ")

    if selection.lower() == '0':
        clear()
        pass
    elif int(selection) < 0 or int(selection) > len(studentList.get(loggedInUsername).inbox):
        clear()
        print("\nERROR: Invalid Input")
        inbox()
    else:
        selection = int(selection)-1
        displayMessage(selection)


def displayMessage(index): #Added by Khalani (Epic 7)
    clear()
    print("\n\n=================== MESSAGE FROM "+studentList.get(studentList.get(loggedInUsername).inbox[index][0]).fName.upper()+" "+studentList.get(studentList.get(loggedInUsername).inbox[index][0]).lName.upper()+" =========================\n")
    print("\n\t"+insert_newlines(studentList.get(loggedInUsername).inbox[index][1],"\n\t"))
    markAsRead = (studentList.get(loggedInUsername).inbox[index][0], studentList.get(loggedInUsername).inbox[index][1], "READ")
    print("\n===========================================================================\n")
    selection = input("Enter 'D' to delete this message, 'R' to respond, or 0 to return to the previous page: ")
    if selection.lower() == "d":
        studentList.get(loggedInUsername).inbox.pop(index)
        clear()
        print("INFO: MESSAGE DELETED\n")
    elif selection == "0":
        studentList.get(loggedInUsername).inbox.pop(index)
        studentList.get(loggedInUsername).inbox.append(markAsRead)
        clear()
    elif selection.lower() == "r":
        reciever = studentList.get(loggedInUsername).inbox[index][0]
        studentList.get(loggedInUsername).inbox.pop(index)
        studentList.get(loggedInUsername).inbox.append(markAsRead)
        sendMessage(reciever)
    else:
        print("*** Invalid Input ***\n")
        displayMessage(index)

    writeToInbox()
    inbox()

def sendMessagePlus(): #Added by Khalani (Epic 7)
    print(" *** All users you can send messages to ***")
    print("---USERS---\n")
    for student in studentList :
        print("\n{:10}{:20}".format("USERNAME: ", student))
        print("\t{:5}{:20}".format("Name: ", studentList.get(student).fName + " " + studentList.get(student).lName))
    selection = input("Enter the username of the user you would like to message or Enter '0' to return: ")
    if selection == "0":
        pass
    elif selection not in studentList:
        print("***No such user exists in the inCollege system***\n")
    else:
        for student in studentList:
            if selection == student:
                sendMessage(selection)

def sendMessageStandard(): #Added by Khalani (Epic 7)
    print("*** Friends you can send messages to ****")
    print("---FRIENDS---\n")
    for friend in studentList.get(loggedInUsername).friendship:
        print("\n{:10}{:20}".format("USERNAME: ", friend))
        print("\t{:5}{:20}".format("Name: ", studentList.get(friend).fName + " " + studentList.get(friend).lName ))
    selection = input("Enter the username of the user you would like to message or Enter '0' to return: ")
    if selection == "0":
        pass
    elif selection not in studentList:
        print("***No such user exists in the inCollege system***\n")
    elif selection not in studentList.get(loggedInUsername).friendship:
        print("***I'm sorry you are not friends with that person***\n")
    else:
        for friend in studentList.get(loggedInUsername).friendship:
            if selection == friend:
                sendMessage(selection)

def sendMessage(reciever): #Added by Khalani (Epic 7)
    selection = input("Please enter the message you want to send to this user: ")
    message = (loggedInUsername, selection, "UNREAD")
    studentList.get(reciever).inbox.append(message)
    writeToInbox()
    clear()
    print("\nINFO: MESSAGE to "+ reciever + " SUCCESSFULLY SENT")
    inbox()

def checkInbox(): #Added by Khalani (Epic 7)
    if not loggedIn:
        return False
    for message in studentList.get(loggedInUsername).inbox:
        if message[2] == "UNREAD":
            return True
    return False

def pastSevenDayJobNotifi():    #Qi (epic8)
    moreThan7days=False
    if(len(studentList.get(loggedInUsername).applications) == 0):
        moreThan7days = True
    for applied in studentList.get(loggedInUsername).applications:
        submittedDate=datetime.datetime.strptime(applied.appliedDate, ('%m/%d/%Y %H:%M:%S'))
        timeDifference = str(datetime.datetime.now()-submittedDate).split(",")
        if len(timeDifference)==1:
            moreThan7days =False
            continue
        else:
            numDays = timeDifference[0].split(" ")[0]
            if (numDays)>"7":
                moreThan7days = True
                break
            else:
                moreThan7days = False
                continue
    if(moreThan7days):
        print("\t"+insert_newlines("\n\t~~ Remember - You're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!~","-\n\t  ",70))
        return True     #True if pass 7 days
    return False

def newJoinNotifi():#QI (epic 8)
    newJoin=[]
    for key in studentList:
        if key!=loggedInUsername:
            createDate=datetime.datetime.strptime(studentList.get(key).createdOn, ('%m/%d/%Y %H:%M:%S'))
            loginTime=datetime.datetime.strptime(lastLoginTime, ('%m/%d/%Y %H:%M:%S'))
            if(createDate>loginTime):
                print("\n\t~~ NEW JOIN: "+studentList.get(key).fName.upper()+" "+studentList.get(key).lName.upper()+" has joined InCollege")   
                newJoin.append(studentList.get(key).fName+" "+studentList.get(key).lName)             
    return newJoin

def numJobNotifi():#QI (epic 8)
    count=0
    for job in studentList.get(loggedInUsername).applications:
        if job.marked=="IN":
            count+=1
    print("\n\n\t~~ You have currently applied for "+str(count)+ " jobs")

def newPostedNotifi():#QI (epic 8)
    newPost=[]
    for job in jobList:
        if job.marked =="IN":
            createDate=datetime.datetime.strptime(job.postedOn, ('%m/%d/%Y %H:%M:%S'))
            loginTime=datetime.datetime.strptime(lastLoginTime, ('%m/%d/%Y %H:%M:%S'))
            if(createDate>=loginTime):
                print("\t~~ NOTIFICATION: A new job "+job.title.upper() +" has been posted.")   
                newPost.append(job.title)             
    return newPost

def newDeleteNotifi(): #QI (epic 8)
    newDelete=[]
    for job in jobList:
        for applied in studentList.get(loggedInUsername).applications:
            if job.jobId==applied.jobId and job.deleteOn !='' and job.marked=="DELETED":
                deleteDate=datetime.datetime.strptime(job.deleteOn , ('%m/%d/%Y %H:%M:%S'))
                loginTime=datetime.datetime.strptime(lastLoginTime, ('%m/%d/%Y %H:%M:%S'))
                if(deleteDate>=loginTime):
                    print("\t~~ NOTIFICATION: A job that you applied for has been deleted - "+job.title.upper())   
                    newDelete.append(job.title)  
                break           
    return newDelete

#==================Jack (Epic 9)
def online_practice():
    print("*** ONLINE PRACTICE UNDER CONSTRUCTION ***")

def free_course():
    print("*** FREE COURSE UNDER CONSTRUCTION ***")

def test_sample():
    print("*** TEST SAMPLE UNDER CONSTRUCTION ***")

def questions_and_answers():
    print("*** QUESTIONS AND ANSWERS UNDER CONSTRUCTION ***")

def training_and_education_selection(selection):
    switcher = {
        1: online_practice,
        2: free_course,
        3: test_sample,
        4: questions_and_answers,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

def training_and_education_menu():
    while True:             
        print("\n\n======= Training and Education Menu ========\n\n"
                "\t[1] Online practices\n"
                "\t[2] Free courses\n"
                "\t[3] Test samples\n"
                "\t[4] Questions and answers\n"
                "\t[0] Back to Main Menu\n\n"
                "============================================")
        selection = input("Enter your selection [0 to 4]: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection < 0 or selection > 4:
            clear()
            print("ERROR: Invalid Training Menu Selection [0 to 4]")
            continue
            
        clear()
        if selection==0:
            break
        training_and_education_selection(selection)

def IT_help_desk_menu():
    print("*** Coming Soon! ***")

def business_analysis_and_strategy_menu():
    while True:         
        print("\n\n============================ Business Analysis and Strategy Menu ============================\n\n"
                "\t[1] How to use In College learning\n"
                "\t[2] Train the trainer\n"
                "\t[3] Gamification of learning\n"
                "\t[4] Not seeing what you’re looking for? Sign in to see all 7,609 results\n"
                "\t[0] Back to Main Menu\n\n"
                "============================================================================================")
        selection = input("Enter your selection [0 to 4]: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection < 0 or selection > 4:
            clear()
            print("ERROR: Invalid Training Menu Selection [0 to 4]")
            continue
            
        clear()
        if selection == 0:
            mainMenu()
        else:
            login()
            if loggedIn:
                break


def security_menu():
    print("*** Coming Soon! ***")

def trainingselection(selection):
    switcher = {
        1: training_and_education_menu,
        2: IT_help_desk_menu,
        3: business_analysis_and_strategy_menu,
        4: security_menu,
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

def trainingmenu():
    while True:
        print("\n\n================= Training Menu ===================\n\n"
                "\t[1] Training and Education\n"
                "\t[2] IT Help Desk\n"
                "\t[3] Business Analysis and Strategy\n"
                "\t[4] Security\n"
                "\t[0] Back to Main Menu\n\n"
                "===================================================")
        selection = input("Enter your selection [0 to 4]: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection < 0 or selection > 4:
            clear()
            print("ERROR: Invalid Training Menu Selection [0 to 4]")
            continue
            
        clear()
        if selection==0:
            break
        trainingselection(selection)
        
        if(selection == 3) and loggedIn:
            break

#=========== Qi (epic 9)
def learningSelection(selection):
    switcher = {
        1: addCourseTook("In College Learning"),
        2: addCourseTook("Train the Trainer"),
        3: addCourseTook("Gamification of learning"),
        4: addCourseTook("Architectural Design Process"),
        5: addCourseTook("Project Management Simplified"),
        0: mainMenu
    }
    func = switcher.get(selection, lambda: "invalid input")
    return func()

def inCollegeLearning():
    while True:
        print("\n\n============================= In College Learning Menu ==============================\n\n")
        if "In College Learning" in studentList.get(loggedInUsername).courseTook:
            print("{:55}{:15}".format("\t[1] How to use In College Learning","<ALREADY TAKEN>"))
        else:
            print("\t[1] How to use In College Learning")
        if "Train the Trainer" in studentList.get(loggedInUsername).courseTook:
            print("{:55}{:15}".format("\t[2] Train the trainer","<ALREADY TAKEN>"))
        else:
            print("\t[2] Train the trainer")
        if "Gamification of learning" in studentList.get(loggedInUsername).courseTook:
                print("{:55}{:15}".format("\t[3] Gamification of learning","<ALREADY TAKEN>"))
        else:
            print("\t[3] Gamification of learning")
        if "Architectural Design Process" in studentList.get(loggedInUsername).courseTook:
            print("{:55}{:15}".format("\t[4] Understanding the Architectural Design Process","<ALREADY TAKEN>"))
        else:
            print("\t[4] Understanding the Architectural Design Process")
        if "Project Management Simplified" in studentList.get(loggedInUsername).courseTook:
            print("{:55}{:15}".format("\t[5] Project Management Simplified","<ALREADY TAKEN>"))
        else:
            print("\t[5] Project Management Simplified")
        print("\t[0] Back to Main Menu\n\n"
                "=====================================================================================")
        selection = input("Enter your selection [0 to 5]: ")
        try:
            selection=int(selection)
        except:
            clear()
            print("ERROR: Integer Selection Only")
            continue

        if selection < 0 or selection > 5:
            clear()
            print("ERROR: Invalid In College Learning Menu Selection [0 to 5]")
            continue
            
        #clear()
        if selection == 0:
            clear()
            #mainMenu()
        elif selection == 1:
            addCourseTook("In College Learning")
        elif selection ==2:
            addCourseTook("Train the Trainer")
        elif selection ==3:
            addCourseTook("Gamification of learning")
        elif selection ==4:
            addCourseTook("Architectural Design Process")
        elif selection ==5:
            addCourseTook("Project Management Simplified")
        return #JaNae added for testing
        

# Add new took course to the data file
def addCourseTook(courseTitle):
    if courseTitle in studentList.get(loggedInUsername).courseTook:
        check = yORnCheck(input("\nYou have already taken this course, "+ courseTitle.upper()+", do you want to take it again?  [Y/N]: "),"You have already taken this course, "+ courseTitle.upper()+", do you want to take it again?  [Y/N]: ")
        if check.lower() == 'y':
            studentList.get(loggedInUsername).courseTook.remove(courseTitle) 
            addCourseTook(courseTitle)
        else:
            clear()
            print("INFO: Course Cancelled")
    else:
        clear()
        studentList.get(loggedInUsername).courseTook.append(courseTitle)
        print("INFO: You have now completed this training - "+courseTitle.upper())
    writeToCourseTook()
    return #JaNae added for testing




#========================================== Main ====================================
#========================= DO NOT CHANGE IT(Qi) ====================================
if __name__ == "__main__":
    readFromCSV()
    mainMenu()

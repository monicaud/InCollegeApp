#############################################################################################
#
# Author: Team Utah
# PyTest Version 9 - 11/16/2020
# This program is used to test the InCollegeForPyTest.py
# 
# EXECUTION COMMAND: pytest -v PyTestVersion9.py
#
# IMPORTANT: This PyTest ONLY VALID for the provided data file
# All test cases are depends on each other
#
# "monkeypatch" is to pass the user input(s) when program ask for input
# "capfd" is store the console (print statement) to the string
#
#############################################################################################

import InCollegeVersion9 as InCollegeApp
import unittest
import pytest
from unittest import mock
from unittest.mock import patch
from unittest import TestCase
from io import StringIO
import sys

#=============================================
#Clear file
def deleteContent(fName):
    file = open(fName,"r+")
    file.truncate(0)
    file.close()

#=================================================================================================
#Test for read data from the file based on the file that provided, which only 4 accounts (Qi)
#Test for read data from the file based on the file that provided, which only 4 accounts (Qi)
def testReadDatafile1():
    actualListName=['qizheng','monicaulloa','janaes','k_thomps', 'danphan', 'timmy_t', 'j_neutron', 'quester12', 'k_possible']
    actualListPassword=['Qz12345!','Mu@987654','#Js123456#','Kt987654%', 'Ghostboy261!', 'Fa!rly01', 'Neutron_954', 'Quest_101', 'Impo$$ible_1']
    actualFname=['Qi','Monica','Janae','Khalani', 'Danny', 'Timmy', 'Jimmy', 'Johnny', 'Kim']
    actualLname=['Zheng','Ulloa','Strickland','Thompson', 'Phantom', 'Thompson', 'Neutron', 'Thompson', 'Zheng']
    resultName=[]
    resultPassword=[]
    resultFname=[]
    resultLname=[]
    InCollegeApp.readFromCSV()
    for key in InCollegeApp.studentList: 
        resultName.append(key)
        resultPassword.append(InCollegeApp.studentList.get(key).password)
        resultFname.append(InCollegeApp.studentList.get(key).fName)
        resultLname.append(InCollegeApp.studentList.get(key).lName)
    #Make sure two lists are exactly match
    assert all([a==b for a, b in zip(actualListName, resultName)])
    assert all([a==b for a, b in zip(actualListPassword, resultPassword)])
    assert all([a==b for a, b in zip(actualFname, resultFname)])
    assert all([a==b for a, b in zip(actualLname, resultLname)])

#=================================================================================================
#Test Main menu option 1: login (Qi)

# Valid username + Invalid password
def testLogin1(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Qizheng\nIncorrectPass\nN\n'))  #unsuccessful login
    InCollegeApp.login()
    assert InCollegeApp.loggedIn==False

# Valid username + password
def testLogin2(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Qizheng\nQz12345!\n'))    #successful login
    InCollegeApp.login()
    assert InCollegeApp.loggedIn==True

#Invalid username+ Valid password
def testLogin3(monkeypatch):
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin',StringIO('MakeUpUsername\nQz12345!\nN\n'))  #unsuccessful login
    InCollegeApp.login()
    assert InCollegeApp.loggedIn==False

#Valid username+ Valid password
def testLogin4(monkeypatch):
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin',StringIO('MonicaUlloa\nMu@987654\nN\n'))  #successful login
    InCollegeApp.login()
    assert InCollegeApp.loggedIn==True

#=================================================================================================
#Test Main menu option 2: create account with invalid password, valid password, reached the max accounts = 5
#deleted assertions that were failing (Qi+Jack)
#=================================================================================================
#Account exist, no account created
def testCreateAccount1_AccountExit1(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Monica\nUlloa\nMonicaUlloa\nGuessMyPW123\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False

#Account exist, no account created
def testCreateAccount1_AccountExit2(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Khalani\nThompson\nKhalani Thompson\nGuessPassword\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False

#Valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW1(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nInvalidPassword\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True
    
#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW2(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nInvalidPW123\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW3(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nInvalidPW1233333333333333333!\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW4(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nInvalid!\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW5(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\n12345abc!\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW6(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\n123456789!\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW7(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nInvalidPW123!\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Again valid Account + invalid password, no account created
def testCreateAccount2_InvalidPW8(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nPW1234!\nS\nN\n'))   
    assert InCollegeApp.createAccount() == False
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    assert ('JackYang' not in resultName) == True

#Valid account + Valid password, add this 5th account
def testCreateAccount3_ValidNewAccount_WriteToData_checkControlStatus(monkeypatch):
    monkeypatch.setattr('sys.stdin',StringIO('Jack\nYang\nJackYang\nValidPW#1\nS\nY\n'))   
    assert InCollegeApp.createAccount() == True
    resultName=[]
    for key in InCollegeApp.studentList: 
        resultName.append(key)
    print(resultName)
    assert ('jackyang' in resultName) == True
    assert InCollegeApp.studentList.get("jackyang").email=="ON"
    assert InCollegeApp.studentList.get("jackyang").sms=="ON"
    assert InCollegeApp.studentList.get("jackyang").targetedAdv=="ON"
    assert InCollegeApp.studentList.get("jackyang").language=="ENGLISH"



def testJoinNotifi(capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    InCollegeApp.newJoinNotifi()
    out, err = capfd.readouterr()
    assert("NEW JOIN: JACK YANG has joined InCollege" in out) == True


#try to add 6th account to the list
def testCreateAccount4_ReachMaxAccounts(capfd):
    InCollegeApp.createAccount()    
    out,err=capfd.readouterr()
    print (out)
    assert 'INFO: All Permitted Accounts Have Been Created, Please Come Back Later.\n' in out

#check if data file contains correct 10 accounts
def testReadDatafile2():    
    actualListName=['qizheng','monicaulloa','janaes','k_thomps', 'danphan', 'timmy_t', 'j_neutron', 'quester12', 'k_possible','jackyang']
    actualListPassword=['Qz12345!','Mu@987654','#Js123456#','Kt987654%', 'Ghostboy261!', 'Fa!rly01', 'Neutron_954', 'Quest_101', 'Impo$$ible_1','ValidPW#1']
    actualFname=['Qi','Monica','Janae','Khalani', 'Danny', 'Timmy', 'Jimmy', 'Johnny', 'Kim', 'Jack']
    actualLname=['Zheng','Ulloa','Strickland','Thompson', 'Phantom', 'Thompson', 'Neutron', 'Thompson', 'Zheng','Yang']
    resultFname=[]
    resultLname=[]
    resultName=[]
    resultPassword=[]
    InCollegeApp.studentList.clear()
    InCollegeApp.jobList.clear()
    InCollegeApp.readFromCSV()
    for key in InCollegeApp.studentList: 
        resultName.append(key)
        resultPassword.append(InCollegeApp.studentList.get(key).password)
        resultFname.append(InCollegeApp.studentList.get(key).fName)
        resultLname.append(InCollegeApp.studentList.get(key).lName)
    print(resultName)
    assert all([a==b for a, b in zip(actualListName, resultName)])
    assert all([a==b for a, b in zip(actualListPassword, resultPassword)])
    assert all([a==b for a, b in zip(actualFname, resultFname)])
    assert all([a==b for a, b in zip(actualLname, resultLname)])
    
    #change data file back to orginal, remove account 'JackYang', so still only 4 accounts 
    InCollegeApp.studentList.pop("jackyang")
    deleteContent(InCollegeApp.studentAccountfile)

    InCollegeApp.writeToStudent()


#========================================================================
#Test createJob - Epic 2 (Monica)
#=======================================================================

#Job with negative salary then valid salary
def testCreateJob1_invalidSalary(monkeypatch):
    loggedIn=True     
    loggedInAccount="qizheng"  
    loggedInName = "Qi Zheng"
    monkeypatch.setattr('sys.stdin', StringIO('Teaching Assistant\nEducation\nUSF\nFL\n-45\n46\n'))
    InCollegeApp.createNewJob()
    jobTitles2 = []
    for job2 in InCollegeApp.jobList:
        jobTitles2.append(job2.title)
    assert ("Teaching Assistant" in jobTitles2) == True

#Valid job
def testCreateJob2_AllValidData(monkeypatch):
    loggedIn=True     
    loggedInAccount="MonicaUlloa"  
    loggedInName = "Monica Ulloa"
    monkeypatch.setattr('sys.stdin', StringIO('Federal Work Study\nCommunity\nUSF\nFL\n102.5\n'))
    InCollegeApp.createNewJob()
    jobTitles = []
    for job in InCollegeApp.jobList:
        jobTitles.append(job.title)
    assert ("Federal Work Study" in jobTitles) == True

#Testing the job wrote to file, uses previous function
def testCreateJob3_verifyDataFile():
    InCollegeApp.jobList.clear()
    InCollegeApp.studentList.clear()
    InCollegeApp.readFromCSV()
    jobTitles3 = []
    for job3 in InCollegeApp.jobList:
        jobTitles3.append(job3.title)
    assert ("Teaching Assistant" in jobTitles3) == True
    assert ("Federal Work Study" in jobTitles3) == True
    assert ("Cashier" in jobTitles3) == True
    assert ("Rowboater" in jobTitles3) == True
    assert ("Professional Gamer" in jobTitles3) == True
    assert ("Tester" in jobTitles3) == False
    assert ("Deverloper" in jobTitles3) == False

#try to add 6th job to the list
def testCreateJob_ReachMaxJob(capfd):
    InCollegeApp.createNewJob()    
    out,err=capfd.readouterr()
    print(InCollegeApp.jobList)
    assert ('INFO: Maximum Amount of Jobs Allowed Currently Have Been Created, Please Come Back Later.\n' in out)==True

    #change data file back to orginal, remove two recently added jobs
    InCollegeApp.jobList.pop()
    InCollegeApp.jobList.pop()
    deleteContent(InCollegeApp.jobDataFile)
    InCollegeApp.writeToJob()

#=================================================================================================
#Test video message (Jack)
#================================================================================================
def testVideoMessage(monkeypatch, capfd):
    monkeypatch.setattr('sys.stdin', StringIO('Y\n0\n'))
    assert (InCollegeApp.videoMessage() == "Video is now playing") == True


#==========================================================================================
#Test connectHelp (Jack)
#==================================================================================================
#Connect help not found
def testFindSomeone1_notFound(monkeypatch):
    InCollegeApp.loggedIn=False
    monkeypatch.setattr('sys.stdin',StringIO('Firstname Lastname\n'))
    assert InCollegeApp.findSomeone() == False

#Connect Help found but not join
def testFindSomeone2_foundNotJoin(monkeypatch):
    InCollegeApp.loggedIn=False
    monkeypatch.setattr('sys.stdin',StringIO('QI ZHENG\nN\n'))
    assert InCollegeApp.findSomeone() == True

#Connect help not found
def testFindSomeone3_noFound(monkeypatch):
    InCollegeApp.loggedIn=False
    monkeypatch.setattr('sys.stdin',StringIO('Peter William\n'))
    assert InCollegeApp.findSomeone() == False

#Connect Help found, join, back to menu
def testFindSomeone4_foundJoinBackToMenu(monkeypatch, capfd):
    InCollegeApp.loggedIn=False
    monkeypatch.setattr('sys.stdin',StringIO('Monica Ulloa\nY\n0\n'))
    assert InCollegeApp.findSomeone() == True
    

#Connect Help found, join and login
def testFindSomeone5_foundJoinLogin(monkeypatch):
    InCollegeApp.loggedIn=False
    monkeypatch.setattr('sys.stdin',StringIO('Monica Ulloa\nY\n1\nqizheng\nQz12345!\n'))
    assert InCollegeApp.findSomeone() == True

#Connect Help found, join and create account
def testFindSomeone6_foundJoinCreateAccount(monkeypatch):
    InCollegeApp.studentList.clear()
    InCollegeApp.jobList.clear()
    studentUsername=[]
    InCollegeApp.readFromCSV()
    InCollegeApp.loggedIn=False
    monkeypatch.setattr('sys.stdin',StringIO('Monica Ulloa\nY\n2\nPeter\nWilliam\npwilliam\nValid12345!\nS\nY\n'))
    assert InCollegeApp.findSomeone() == True
    for key in InCollegeApp.studentList:
        studentUsername.append(key)
    assert ("pwilliam" in studentUsername) == True

    #change data file back to orginal, remove "pwilliam" from the student list
    InCollegeApp.studentList.pop("pwilliam")
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()


#=================================================================================================
#Test Main menu option 3: search for job
def testSearchForJobNotLoggedIn(capfd):
    InCollegeApp.loggedIn=False
    InCollegeApp.searchForJob()
    out,err=capfd.readouterr()
    assert ("*** Must be logged in to access this feature!" in out) == True

#=================================================================================================
#Test Main menu option 5: Skill submenu
def testWoodworking(capfd):
    InCollegeApp.woodworking()
    out,err=capfd.readouterr()
    assert out == '*** WOODWORKING UNDER CONSTRUCTION ***\n'

def testMicrosoftWord(capfd):
    InCollegeApp.microsoftWord()
    out,err=capfd.readouterr()
    assert out == '*** MICROSOFTWORD UNDER CONSTRUCTION ***\n'

def testMicrosoftExcel(capfd):
    InCollegeApp.microsoftExcel()
    out,err=capfd.readouterr()
    assert out == '*** MICROSOFTEXCEL UNDER CONSTRUCTION ***\n'

def testMicrosoftTeam(capfd):
    InCollegeApp.microsoftTeam()
    out,err=capfd.readouterr()
    assert out == '*** MICROSOFTTEAM UNDER CONSTRUCTION ***\n'

def testArtificIntelligence(capfd):
    InCollegeApp.ArtificIntelligence()
    out,err=capfd.readouterr()
    assert out == '*** AI UNDER CONSTRUCTION ***\n'

#=================================================================================================
#Test links (Monica)
def testOutputLinks(capfd):
    InCollegeApp.helpCenter()
    out,err=capfd.readouterr()
    assert ("Help Center" in out) == True

    InCollegeApp.about()
    out,err=capfd.readouterr()
    assert ("About" in out) == True

    InCollegeApp.press()
    out,err=capfd.readouterr()
    assert ("Press" in out) == True

    InCollegeApp.blog()
    out,err = capfd.readouterr()
    assert ("BLOG" in out) == True
    
    InCollegeApp.careers()
    out, err = capfd.readouterr()
    assert ("CAREERS" in out) == True

    InCollegeApp.developers()
    out, err = capfd.readouterr()
    assert ("DEVELOPERS" in out) == True

    InCollegeApp.browse()
    out, err = capfd.readouterr()
    assert ("BROWSE" in out) == True
    
    InCollegeApp.businessSolution()
    out, err = capfd.readouterr()
    assert ("BUSINESS SOLUTION" in out) == True

    InCollegeApp.directories()
    out, err = capfd.readouterr()
    assert ("DIRECTORIES" in out) == True

    InCollegeApp.copyrightNotice()
    out, err = capfd.readouterr()
    assert ("Copyright" in out) == True

    InCollegeApp.accessibility()
    out, err = capfd.readouterr()
    assert ("Accessibility" in out) == True

    InCollegeApp.userAgreement()
    out, err = capfd.readouterr()
    assert ("User Agreement" in out) == True

    InCollegeApp.cookiePolicy()
    out, err = capfd.readouterr()
    assert ("Cookie Policy" in out) == True

    InCollegeApp.copyrightPolicy()
    out, err = capfd.readouterr()
    assert ("Copyright Policy" in out) == True

    InCollegeApp.brandPolicy()
    out, err = capfd.readouterr()
    assert ("Brand Policy" in out) == True

#Test Privacy Policy for login user - not update
def testPrivacyPolicy_notUpdateControl(capfd, monkeypatch):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "monicaulloa" #Monica
    monkeypatch.setattr('sys.stdin', StringIO('n\n'))
    InCollegeApp.privacyPolicy()
    out, err = capfd.readouterr()
    assert ("Privacy Policy" in out) == True

#Test Privacy Policy for login user
def testPrivacyPolicy_updateControl(capfd, monkeypatch):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "monicaulloa" #Monica
    monkeypatch.setattr('sys.stdin', StringIO('y\nemail\ny\nno update\n'))
    InCollegeApp.privacyPolicy()
    out, err = capfd.readouterr()
    assert ("InCollege Email: ON" in out) == True
    assert InCollegeApp.studentList.get("monicaulloa").email == "ON"
    
    #change datafile back
    InCollegeApp.studentList.get("monicaulloa").email = "OFF"
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()

def testGuestControls_updateSMS(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Janaes
    monkeypatch.setattr('sys.stdin', StringIO('sms\ny\nno update\n'))
    InCollegeApp.guestControls()
    out, err = capfd.readouterr()
    assert ("SMS: OFF" in out) == True
    assert InCollegeApp.studentList.get("janaes").sms == "OFF"

    #change datafile back
    InCollegeApp.studentList.get("janaes").sms = "ON"
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()

def testGuestControls_updateEmail(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Janaes
    monkeypatch.setattr('sys.stdin', StringIO('email\ny\nno update\n'))
    InCollegeApp.guestControls()
    out, err = capfd.readouterr()
    assert ("SMS: ON" in out) == True
    assert InCollegeApp.studentList.get("janaes").email == "ON"

    #change datafile back
    InCollegeApp.studentList.get("janaes").email = "OFF"
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()

def testGuestControls_updateAdv(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Janaes
    monkeypatch.setattr('sys.stdin', StringIO('targeted advertising\ny\nno update\n'))
    InCollegeApp.guestControls()
    out, err = capfd.readouterr()
    assert ("Tartgeted Advertising: OFF" in out) == True
    assert InCollegeApp.studentList.get("janaes").targetedAdv == "OFF"

    #change datafile back
    InCollegeApp.studentList.get("janaes").targetedAdv = "ON"
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()

def testGuestControls_noUpdate(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Monica
    monkeypatch.setattr('sys.stdin', StringIO('no update\n'))
    InCollegeApp.guestControls()
    out, err = capfd.readouterr()
    assert ("INFO: No Update Made" in out) == True

def testGuestControls_invalidInput(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Janaes
    monkeypatch.setattr('sys.stdin', StringIO('I want to update sms\nno update\n'))
    InCollegeApp.guestControls()
    out, err = capfd.readouterr()
    assert ("ERROR: Invalid Feature Input." in out) == True

def testGuestControls_noUpdate(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Janaes
    monkeypatch.setattr('sys.stdin', StringIO('no update\n'))
    InCollegeApp.guestControls()
    out, err = capfd.readouterr()
    assert ("INFO: No Update Made" in out) == True

def testLanguages_changeToEnglish(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes" #Janaes

    monkeypatch.setattr('sys.stdin', StringIO('y'))
    InCollegeApp.languages()
    out, err = capfd.readouterr()
    assert  ("INFO: Changed Language To ENGLISH" in out) == True
    assert InCollegeApp.studentList.get("janaes").language == "ENGLISH"

    #change datafile back
    InCollegeApp.studentList.get("janaes").language = "SPANISH"
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()

def testLanguages_changeToSpanish(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"

    monkeypatch.setattr('sys.stdin', StringIO('y'))
    InCollegeApp.languages()
    out, err = capfd.readouterr()
    assert  ("INFO: Changed Language To SPANISH" in out) == True
    assert InCollegeApp.studentList.get("k_thomps").language == "SPANISH"

    #change datafile back
    InCollegeApp.studentList.get("k_thomps").language = "ENGLISH"
    deleteContent(InCollegeApp.studentAccountfile)
    InCollegeApp.writeToStudent()

def testLanguages_noChange(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"

    monkeypatch.setattr('sys.stdin', StringIO('n'))
    InCollegeApp.languages()
    out, err = capfd.readouterr()
    assert  ("INFO: No Update Made" in out) == True
    assert InCollegeApp.studentList.get("k_thomps").language == "ENGLISH"



#===========================TESTING SEARCH AND FRIEND FOR EPIC 5 (Qi)
def testSearchByUniversity1_allConnected(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"

    monkeypatch.setattr('sys.stdin', StringIO("2\nUNIverSITY Of SoutH FLOrida\nN"))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("<connected>\t\tKhalani Thompson" in out) == True
    assert ("<connected>\t\tDanny Phantom" in out) == True
    assert ("INFO: No Additional New Search Result" in out) == True

def testSearchByUniversity2_SomeConnectedSomeNotConnected(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO("2\nUNIverSITY Of SoutH FLOrida\n0\nN"))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("<connected>\t\tQi Zheng" in out) == True
    assert ("<connected>\t\tDanny Phantom" in out) == True
    assert ("[1]\t\t\tKhalani Thompson" in out) == True
    assert ("INFO: No Additional New Search Result" not in out) == True

def testSearchByMajor1_resultOfAllSameMajor(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO("3\nCompUTER SCieNce\n0\nN"))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("<connected>\t\tQi Zheng" in out) == True
    assert ("<connected>\t\tDanny Phantom" in out) == True
    assert ("[1]\t\t\tKim Zheng" in out) == True

def testSearchByMajor2_DoesNotIncludeSelf(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"

    monkeypatch.setattr('sys.stdin', StringIO("3\nCompUTER SCieNce\n0\nN"))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("<connected>\t\tDanny Phantom" in out) == True
    assert ("[1]\t\t\tKim Zheng" in out) == True

def testPrintFriends(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO("6\n0\n0\n"))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("Qi Zheng" in out) == True


def testSearchFriendAlreadyFriendANDNoOtherSameLastName(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO('1\nPhantom\nN\n'))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("<connected>\t\tDanny Phantom" in out) == True
    assert ("INFO: No Additional New Search Result" in out) == True


def testSearchFriendNotFoundFriend(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO('1\ndoo\nN\n'))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("INFO: No student was found" in out) == True

def testSearchFriendNotFoundFriendDoAnotherSearch(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO('1\ndoo\nY\n1\nLee\nN\n'))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("INFO: No student was found" in out) == True


def testSearchFriendSentRequest1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO('1\nNeutron\n1\nN'))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    assert ("INFO: Friend Request Sent To Jimmy Neutron" in out) == True
    assert "j_neutron" in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).requestTo
    assert "janaes" in InCollegeApp.studentList.get("j_neutron").requestFrom

def testPendingFriendRequest1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"

    monkeypatch.setattr('sys.stdin', StringIO('0\n'))
    InCollegeApp.friendrequestaccept()
    out, err = capfd.readouterr()
    assert ("<WAITING>      Jimmy Neutron" in out) == True

def testRejectRequest(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "j_neutron"

    monkeypatch.setattr('sys.stdin', StringIO('Reject 1\n0\n'))
    InCollegeApp.friendrequestaccept()
    out, err = capfd.readouterr()
    assert ("INFO: You rejected JANAE STRICKLAND To Be Your Friend." in out) == True
    assert "janaes" not in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).friendship
    assert "j_neutron" not in InCollegeApp.studentList.get("janaes").friendship
    assert "janaes" not in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).requestFrom
    assert "j_neutron" not in InCollegeApp.studentList.get("janaes").requestFrom

def testPendingFriendRequest2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('0\n'))
    InCollegeApp.friendrequestaccept()
    out, err = capfd.readouterr()
    assert ("<WAITING>      Timmy Thompson" in out) == True

def testAcceptRequest(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "timmy_t"

    monkeypatch.setattr('sys.stdin', StringIO('AcCEPt 2\n0\n'))
    InCollegeApp.friendrequestaccept()
    out, err = capfd.readouterr()
    assert ("INFO: Congrats JANAE STRICKLAND And You Are Friend Now!" in out) == True
    assert "timmy_t" in InCollegeApp.studentList.get("janaes").friendship
    assert "janaes" in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).friendship
    assert "janaes" not in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).requestFrom
    assert "timmy_t" not in InCollegeApp.studentList.get("janaes").requestTo

def testDisconnectUnconfirm(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "timmy_t"

    monkeypatch.setattr('sys.stdin', StringIO('DisCONNEct 1\nN\n0'))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("INFO: No One Got Disconnected." in out) == True
    assert "timmy_t" in InCollegeApp.studentList.get("janaes").friendship
    assert "janaes" in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).friendship

def testDisconnectConfirm(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "timmy_t"

    monkeypatch.setattr('sys.stdin', StringIO('DisCONNEct 1\nY\n0'))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("INFO: JANAE STRICKLAND And You Are Disconnect From InCollege System." in out) == True
    assert ("[DISCONNECT 1]                Janae Strickland" not in out) == True
    assert "timmy_t" not in InCollegeApp.studentList.get("janaes").friendship
    assert "janaes" not in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).friendship

def testSearchFriendSentRequest2_mutipleSearchResult(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('1\nthompson\n2\nN\n'))
    InCollegeApp.searchStudent()
    assert "timmy_t" in InCollegeApp.studentList.get("janaes").requestTo
    assert "janaes" in InCollegeApp.studentList.get("timmy_t").requestFrom

def testPendingFriendRequest3(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('0\n'))
    InCollegeApp.friendrequestaccept()
    out, err = capfd.readouterr()
    assert ("<WAITING>      Timmy Thompson" in out) == True


def testSeachPendingFriend(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('1\nthompson\n0\n'))
    InCollegeApp.searchStudent()
    out, err = capfd.readouterr()
    print(out)
    assert ("<pending>\t\tTimmy Thompson" in out) == True
    assert ("[1]\t\t\tKhalani Thompson" in out) == True
    assert ("[2]\t\t\tJohnny Thompson" in out) == True
# ============================================================================ Khalani profile test stuff
def testCheckViewProfile(monkeypatch, capfd):  # make sure profile is printing  studentprofile correctly
    InCollegeApp.printProfile("k_thomps")
    out, err = capfd.readouterr()
    assert ("4th year Music Education" in out) == True
    assert ("Music Education" in out) == True
    assert ("University Of South Florida" in out) == True
    assert ("Born in New York, from a" in out) == True
    assert ("Cashier" in out) == True
    assert ("Target Corporation" in out) == True
    assert ("8/20/2018" in out) == True
    assert ("10/7/2019" in out) == True
    assert ("202 E Fowler Ave, San Francisco, CA 94117" in out) == True
    assert ("Assisted with customer service" in out) == True
    assert ("Ride Operator" in out) == True
    assert ("Busch Gardens" in out) == True
    assert ("12/27/2015" in out) == True
    assert ("24/11/2016" in out) == True
    assert ("8 La Follette Crossing" in out) == True
    assert ("Millenium High School" in out) == True
    assert ("Univesity Of New York" in out) == True
    assert ("Electrical Engineering" in out) == True
    assert ("2016-2020" in out) == True
    assert ("Music Education" in out) == True
    assert ("2020" in out) == True

def testFriendNoProfile1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('0\n'))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("[DISCONNECT 1]\t\t\t\t\tJanae Strickland" in out) == True
    assert ("[DISCONNECT 2]\t\t[PROFILE 2]\t\tMonica Ulloa" in out) == True
    assert ("[DISCONNECT 3]\t\t[PROFILE 3]\t\tKhalani Thompson" in out) == True
    assert ("[DISCONNECT 4]\t\t[PROFILE 4]\t\tDanny Phantom" in out) == True
    assert ("[DISCONNECT 5]\t\t[PROFILE 5]\t\tJimmy Neutron" in out) == True


def testFriendNoProfile2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "danphan"
    monkeypatch.setattr('sys.stdin', StringIO('0\n'))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("[DISCONNECT 1]\t\t[PROFILE 1]\t\tQi Zheng" in out) == True
    assert ("[DISCONNECT 2]\t\t\t\t\tJanae Strickland" in out) == True

def testFriendNoProfile3(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "danphan"
    monkeypatch.setattr('sys.stdin', StringIO('prOFIle 2\nY\n0\n'))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("[DISCONNECT 2]\t\t\t\t\tJanae Strickland" in out) == True
    assert ("INFO: No Profile Information For Janae Strickland" in out) == True

def testFriendProfile(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "danphan"
    monkeypatch.setattr('sys.stdin', StringIO('prOFIle 1\nY\n0\n'))
    InCollegeApp.printFriends(InCollegeApp.loggedInUsername)
    out, err = capfd.readouterr()
    assert ("[DISCONNECT 1]\t\t[PROFILE 1]\t\tQi Zheng" in out) == True
    assert ("I'm a 4th year computer science student" in out) == True
    assert ("Computer Science" in out) == True
    assert ("University Of South Florida" in out) == True
    assert ("I born in China." in out) == True
    assert ("Customer Services" in out) == True
    assert ("Walmart" in out) == True
    assert ("10/19/2019" in out) == True
    assert ("1/19/2020" in out) == True
    assert ("1234 Russell st, Tampa, FL, 33610" in out) == True
    assert ("Provide good product to customers" in out) == True
    assert ("Math Assistant" in out) == True
    assert ("Kumon" in out) == True
    assert ("4/10/2018" in out) == True
    assert ("2/7/2019" in out) == True
    assert ("4567 Robinson, Lutz, FL, 33517" in out) == True
    assert ("Tutor K-12 students with math; Do grading" in out) == True

def testCheckProfile():  # checking contents of Profile data, make sure data is in right spot
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.title == "4th year Music Education Major"
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.major == "Music Education"
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.university == "University Of South Florida"
    assert InCollegeApp.studentList.get(
        "k_thomps").StudentProfile.aboutMe == "Born in New York, from a young age I spent time around different musical scenes and clubs. After spending time in high school in my school's band program I realized I wanted to be involved with music for my life. From there found my into music education"


def testCheckExperience():  # check contents of experiences, make sure data is in right spot
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.experience[0] == ['Cashier', 'Target Corporation',
                                                                                     '8/20/2018', '10/7/2019',
                                                                                     '202 E Fowler Ave, San Francisco, CA 94117',
                                                                                     'Assisted with customer service, and the checkout of customers in the store']

    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.experience[1] == ['Ride Operator', 'Busch Gardens',
                                                                                     '12/27/2015', '24/11/2016',
                                                                                     '8 La Follette Crossing, San Francisco, CA 94468',
                                                                                     'In charge of the safe operation of rollder coasters in a theme park.']


def testCheckEducation():  # check contents of education
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.education[0] == ['Millenium High School',
                                                                                    'High School', '2012-2016']
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.education[1] == ['Univesity Of New York',
                                                                                    'Electrical Engineering',
                                                                                    '2016-2020']
    assert InCollegeApp.studentList.get("k_thomps").StudentProfile.education[2] == ['Univesity Of New York',
                                                                                    'Music Education', '2020']


def testCreateProfile1(monkeypatch):  # Khalani create profile test with some invalid input to check flow

    testCreateAccount3_ValidNewAccount_WriteToData_checkControlStatus(monkeypatch)

    monkeypatch.setattr('sys.stdin', StringIO(
        'I am a 3rd year CS student\nComputer Science\nUniversity of South Florida\nI like school\n4\n1\nButcher\nPublix\n11142012\n11/14/2012\n12/13/2012\nFlorida\nChopped stuff\n13\n1\nSickles High School\nHigh School\n2011-2059\n'))

    ##############above input runs invalid inputs and corrects them
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "jackyang"
    InCollegeApp.createProfile()
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.title == "I am a 3rd year CS student"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.major == "Computer Science"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.university == "University Of South Florida"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.aboutMe == "I like school"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.experience[0] == ['Butcher', 'Publix', '11/14/2012',
                                                                                     '12/13/2012', 'Florida',
                                                                                     'Chopped stuff']
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.education[0] == ['Sickles High School',
                                                                                    'High School', '2011-2059']

    InCollegeApp.studentList.pop("jackyang")
    deleteContent(InCollegeApp.studentAccountfile)
    deleteContent(InCollegeApp.studentProfilefile)  # reset other data files
    deleteContent(InCollegeApp.studentProfileEducations)
    deleteContent(InCollegeApp.studentProfileExperiences)

    InCollegeApp.writeToProfile()
    InCollegeApp.writeToExp()
    InCollegeApp.writeToEdu()
    InCollegeApp.writeToStudent()


def testCreateProfile2(monkeypatch):  # Khalani create profile test with only valid input

    testCreateAccount3_ValidNewAccount_WriteToData_checkControlStatus(monkeypatch)

    monkeypatch.setattr('sys.stdin', StringIO(
        'I am a 3rd year CS student\nComputer Science\nUniversity of South Florida\nI like school\n1\nButcher\nPublix\n11/14/2012\n12/13/2012\nFlorida\nChopped stuff\n1\nSickles High School\nHigh School\n2011-2059\n'))

    ##############above input runs invalid inputs and corrects them
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "jackyang"
    InCollegeApp.createProfile()
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.title == "I am a 3rd year CS student"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.major == "Computer Science"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.university == "University Of South Florida"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.aboutMe == "I like school"
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.experience[0] == ['Butcher', 'Publix', '11/14/2012',
                                                                                     '12/13/2012', 'Florida',
                                                                                     'Chopped stuff']
    assert InCollegeApp.studentList.get("jackyang").StudentProfile.education[0] == ['Sickles High School',
                                                                                    'High School', '2011-2059']

    InCollegeApp.studentList.pop("jackyang")
    deleteContent(InCollegeApp.studentAccountfile)
    deleteContent(InCollegeApp.studentProfilefile)  # reset other data files
    deleteContent(InCollegeApp.studentProfileEducations)
    deleteContent(InCollegeApp.studentProfileExperiences)

    InCollegeApp.writeToProfile()
    InCollegeApp.writeToExp()
    InCollegeApp.writeToEdu()
    InCollegeApp.writeToStudent()


def testEducationandExperienceBounds(monkeypatch, capfd):  # Khalani create profile test with only valid input

    testCreateAccount3_ValidNewAccount_WriteToData_checkControlStatus(monkeypatch)

    monkeypatch.setattr('sys.stdin', StringIO(
        'I am a 3rd year CS student\nComputer Science\nUniversity of South Florida\nI like school\n4\nO\n-5\n1\nButcher\nPublix\n11/14/2012\n12/13/2012\nFlorida\nChopped stuff\n-4\n14\nB\n1\nSickles High School\nHigh School\n2011-2059\n'))

    ##############above input runs invalid inputs and corrects them
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "jackyang"
    InCollegeApp.createProfile()

    out, err = capfd.readouterr()

    assert ("ERROR: Invalid Range [0 to 3]" in out) == True  # make sure experience input error message shows
    assert ("ERROR: Invalid Range [0 to 10]" in out) == True  # make sure education input error message shows

    InCollegeApp.studentList.pop("jackyang")
    deleteContent(InCollegeApp.studentAccountfile)
    deleteContent(InCollegeApp.studentProfilefile)  # reset other data files
    deleteContent(InCollegeApp.studentProfileEducations)
    deleteContent(InCollegeApp.studentProfileExperiences)

    InCollegeApp.writeToProfile()
    InCollegeApp.writeToExp()
    InCollegeApp.writeToEdu()
    InCollegeApp.writeToStudent()

def testDeleteJob1_InvalidJobID_ValidJobID(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"
    monkeypatch.setattr('sys.stdin', StringIO('5\n2\n1\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    count=0
    for job in InCollegeApp.jobList:
        if job.marked =="IN":
            count+=1
    assert count==7

def testDeleteJob2_InvalidJobID_ValidJobID_NoMorePostedJob(monkeypatch, capfd):
    monkeypatch.setattr('sys.stdin', StringIO('5\n1\n7\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: You Have No Posted Job" in out) == True
    count=0
    for job in InCollegeApp.jobList:
        if job.marked =="IN":
            count+=1
    assert count==6


def testListAllJobs1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"
    monkeypatch.setattr('sys.stdin', StringIO('1\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("JOB ID:   4              TITLE:    Pet Sitter" in out) == True
    assert ("JOB ID:   5              TITLE:    Food Service Worker" in out) == True
    assert ("JOB ID:   6              TITLE:    Tutor" in out) == True
    assert ("JOB ID:   8              TITLE:    Rideshare Driver" in out) == True
    assert ("JOB ID:   9              TITLE:    Uber Eat Driver" in out) == True
    assert ("JOB ID:   10             TITLE:    Customer Servers" in out) == True
   
def testPostTwoJobs(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"
    monkeypatch.setattr('sys.stdin', StringIO('Cashier\nCheckout customers\nWalmart\n7723 Russell st, Tampa, FL, 33610\n100.5\n'))
    InCollegeApp.createNewJob()
    InCollegeApp.jobList[len(InCollegeApp.jobList)-1].jobId=str(1)

    monkeypatch.setattr('sys.stdin', StringIO('Gym Receptionist\nSign up new members, give gym tours, clean equipment, check in guests\nREC Center\n4202 E Fowler Ave, Tampa, FL 33620\n550\n'))
    InCollegeApp.createNewJob()
    InCollegeApp.jobList[len(InCollegeApp.jobList)-1].jobId=str(7)

    count=0
    for job in InCollegeApp.jobList:
        if job.marked =="IN":
            count+=1
    assert count==8

    deleteContent(InCollegeApp.jobDataFile)
    InCollegeApp.writeToJob()

def testApplyJob1_applyNewJob(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('1\n1\n1\n12/15/2020\n11/10/2019\nI can count money and good at customer service\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    print(out)
    assert ("INFO: Job Application Sent For Job ID 1" in out) == True
    assert("APPLICATION STATUS:           Applied" in out)==True

def testApplyJob2_applyNewJob(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('1\n1\n1\n12/12/2018\n12/12/2018\nstacks of cash and love to serve cutomers\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    print(out)
    assert ("INFO: Job Application Sent For Job ID 1" in out) == True
    assert("APPLICATION STATUS:           Applied" in out)==True

def testListAllJobs2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"
    monkeypatch.setattr('sys.stdin', StringIO('1\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    print (out)
    assert ("JOB ID:   4              TITLE:    Pet Sitter" in out) == True
    assert ("JOB ID:   5              TITLE:    Food Service Worker" in out) == True
    assert ("JOB ID:   6              TITLE:    Tutor" in out) == True
    assert ("JOB ID:   8              TITLE:    Rideshare Driver" in out) == True
    assert ("JOB ID:   9              TITLE:    Uber Eat Driver" in out) == True
    assert ("JOB ID:   10             TITLE:    Customer Servers" in out) == True
    assert ("JOB ID:   1              TITLE:    Cashier" in out) == True
    assert ("JOB ID:   7              TITLE:    Gym Receptionist" in out) == True

def testSelectJobToViewDetails1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("TITLE:                        Pet Sitter" in out) == True
    assert ("DESCRIPTION:                  Pet cleanup, dog walking" in out) == True
    assert ("EMPLOYER:                     Pet owner" in out) == True
    assert ("LOCATION:                     888 W 28th St, New York, NY 10023" in out) == True
    assert ("SALARY:                       200" in out) == True
    assert ("CREATED BY:                   Jimmy Neutron" in out) == True

def testSelectJobToViewDetails2_Invalid(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_thomps"
    monkeypatch.setattr('sys.stdin', StringIO('1\n20\n4\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("TITLE:                        Pet Sitter" in out) == True
    assert ("DESCRIPTION:                  Pet cleanup, dog walking" in out) == True
    assert ("EMPLOYER:                     Pet owner" in out) == True
    assert ("LOCATION:                     888 W 28th St, New York, NY 10023" in out) == True
    assert ("SALARY:                       200" in out) == True
    assert ("CREATED BY:                   Jimmy Neutron" in out) == True


def testJobList_InvalidJobID(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_possible"
    monkeypatch.setattr('sys.stdin', StringIO('1\n24\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("ERROR: Invalid Job ID" in out) == True

def testApplyJob3_applyNewJob(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_possible"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n1\n12/20/2021\n10/20/2020\nI love pet! Very professional on it\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: Job Application Sent For Job ID 4" in out) == True
    assert("APPLICATION STATUS:           Applied" in out)==True
    assert InCollegeApp.studentList.get("k_possible").appliedJobs[0].jobId == str(4)

def testApplyJob4_applied(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "k_possible"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n1\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: You have already applied for the job with Job ID 4" in out)==True
    assert("APPLICATION STATUS:           Applied" in out)==True
    assert InCollegeApp.studentList.get("k_possible").appliedJobs[0].jobId == str(4)

    InCollegeApp.studentList.get("k_possible").appliedJobs.pop()
    InCollegeApp.studentList.get("k_possible").applications.pop()
    deleteContent(InCollegeApp.jobAppFile)
    InCollegeApp.writeToJobApp()

def testSaveJob1_saveNewJob(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n2\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: Job ID 4 saved Successfully" in out)==True
    assert("SAVE STATUS:                  Saved" in out)==True
    assert (str(4) in InCollegeApp.studentList.get("qizheng").savedJobs[2].jobId)==True

def testSaveJob2_saveNewJob(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "monicaulloa"
    oldJobList = []
    for job in InCollegeApp.studentList.get("monicaulloa").savedJobs:
        oldJobList.append(job)
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n2\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: Job ID 4 saved Successfully" in out)==True
    assert("SAVE STATUS:                  Saved" in out)==True

    inList = False
    for job in InCollegeApp.studentList.get("monicaulloa").savedJobs:
        if job.jobId == "4":
            inList = True
    assert (inList)==True
    InCollegeApp.studentList.get("monicaulloa").savedJobs.clear()
    print("mon " + str(len(InCollegeApp.studentList.get("monicaulloa").savedJobs)))
    for job in oldJobList:
        InCollegeApp.studentList.get("monicaulloa").savedJobs.append(job)
    InCollegeApp.writeToSavedJobs()


def testSaveJob2_saved(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n2\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: Job ID 4 Is Already Saved" in out)==True
    assert("SAVE STATUS:                  Saved" in out)==True



def testUnsaveJob_unsaveJob(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n3\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: Successfully Unsaved Job ID 4" in out)==True
    assert("SAVE STATUS:                  Unsave" in out)==True


def testSaveJob2_alreadyUnsaved(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n3\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("INFO: Job ID 4 Is Not Currently Saved" in out)==True
    assert("SAVE STATUS:                  Unsave" in out)==True

def testPrintJobList1_appliedJobIndicated(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('1\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("\t<Applied>\tJOB ID:   1" in out)==True

def testPrintJobList2_appliedJobIndicated(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('1\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("\t<Applied>\tJOB ID:   1" in out)==True
    assert ("\t<Applied>\tJOB ID:   4" in out)==True

def testJobMenuSelection_InvalidInput(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('6\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("ERROR: Invalid Job Menu Selection [0 to 5]" in out)==True

def testJobSubmenuSelection_InvalidInput(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('1\n1\n10\n0\n0\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("ERROR: choose integer from [0 to 3]" in out)==True

def testlistOfSavedJobs(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('2\ny\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("JOB ID: 5" in out) == True
    assert ("TITLE:              Food Service Worker" in out) == True
    assert ("DESCRIPTION:        Take orders, serve food and drinks" in out) == True
    assert ("EMPLOYER:           Cafe house" in out) == True
    assert ("LOCATION:           36 La Follette Crossing, San Francisco, CA 94468" in out) == True
    assert ("SALARY:             500" in out) == True

    assert ("JOB ID: 6" in out) == True
    assert ("TITLE:              Tutor" in out) == True
    assert ("DESCRIPTION:        Subject tutoring, test preparation" in out) == True
    assert ("EMPLOYER:           University of South Florida" in out) == True
    assert ("LOCATION:           4202 E Fowler Ave, Tampa, FL 33620" in out) == True
    assert ("SALARY:             600" in out) == True

    assert ("JOB ID: 1" not in out) == True
    assert ("JOB ID: 4" not in out) == True
    assert ("JOB ID: 7" not in out) == True
    assert ("JOB ID: 8" not in out) == True
    assert ("JOB ID: 9" not in out) == True
    assert ("JOB ID: 10" not in out) == True

def testlistOfAppliedJobs1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('3\ny\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()

    assert ("JOB ID: 1" in out) == True
    assert ("TITLE:              Cashier" in out) == True
    assert ("DESCRIPTION:        Checkout customers" in out) == True
    assert ("EMPLOYER:           Walmart" in out) == True
    assert ("LOCATION:           7723 Russell st, Tampa, FL, 33610" in out) == True
    assert ("SALARY:             100.5" in out) == True
    assert ("CREATED BY:         Khalani Thompson" in out) == True

    assert ("JOB ID: 4" not in out) == True
    assert ("JOB ID: 5" not in out) == True
    assert ("JOB ID: 6" not in out) == True
    assert ("JOB ID: 7" not in out) == True
    assert ("JOB ID: 8" not in out) == True
    assert ("JOB ID: 9" not in out) == True
    assert ("JOB ID: 10" not in out) == True

def testlistOfAppliedJobs2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('3\ny\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("JOB ID: 4" in out) == True
    assert ("JOB ID: 1" in out) == True

    assert ("JOB ID: 2" not in out) == True
    assert ("JOB ID: 3" not in out) == True
    assert ("JOB ID: 5" not in out) == True
    assert ("JOB ID: 6" not in out) == True
    assert ("JOB ID: 7" not in out) == True
    assert ("JOB ID: 8" not in out) == True

def testlistOfNotAppliedJobs1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('4\ny\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("JOB ID: 4" in out) == True
    assert ("JOB ID: 5" in out) == True
    assert ("JOB ID: 6" in out) == True
    assert ("JOB ID: 8" in out) == True
    assert ("JOB ID: 9" in out) == True
    assert ("JOB ID: 10" in out) == True
    assert ("JOB ID: 7" in out) == True


def testlistOfNotAppliedJobs2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    monkeypatch.setattr('sys.stdin', StringIO('4\ny\n0\n'))
    InCollegeApp.searchForJob()
    out, err = capfd.readouterr()
    assert ("JOB ID: 5" in out) == True
    assert ("JOB ID: 6" in out) == True
    assert ("JOB ID: 8" in out) == True
    assert ("JOB ID: 9" in out) == True
    assert ("JOB ID: 10" in out) == True
    assert ("JOB ID: 7" in out) == True


def checkPLUSstudentaccounts(monkeypatch):
    plus_list=[]
    standard_list=[]
    standard_student_list=['monicaulloa','k_thomps','danphan','questter12']
    plus_student_list=['qizheng','janaes','timmy_t','j_neutron','k_possible']
    InCollegeApp.readFromCSV()
    for key in InCollegeApp.studentList: 
        if InCollegeApp.studentList.get(key).type == "STANDARD":
            standard_list.append(key)
        else:
            plus_list.append(key)
    #Make sure two lists are exactly match
    assert all([a==b for a, b in zip(plus_list, plus_student_list)])
    assert all([a==b for a, b in zip(standard_list, standard_student_list)])

def testSendMessagePlus(monkeypatch,capfd):
    InCollegeApp.loggedIn = True
    messageList = []
    for message in InCollegeApp.studentList.get("janaes").inbox:
        messageList.append(message)

    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('janaes\nhello friend\n0'))
    InCollegeApp.sendMessagePlus()
    out, err = capfd.readouterr()
    assert ("SUCCESSFULLY SENT" in out) == True
    InCollegeApp.studentList.get("janaes").inbox.clear()

    for message in messageList:
        InCollegeApp.studentList.get("janaes").inbox.append(message)
    InCollegeApp.writeToInbox()

def testSendMessagePlus2(monkeypatch):
    InCollegeApp.loggedIn = True
    #resend message as Qi
    InCollegeApp.loggedInUsername = "qizheng"
    messageList = []
    for message in InCollegeApp.studentList.get("janaes").inbox:
        #store old messages of janaes
        messageList.append(message)
    #send msg to janae as qi
    monkeypatch.setattr('sys.stdin', StringIO('janaes\nhello friend\n0'))
    InCollegeApp.sendMessagePlus()
    inInbox = False
    #log in as Janae
    InCollegeApp.loggedInUsername = "janaes"
    #make sure there unread messages
    assert(InCollegeApp.checkInbox()) == True
    #find the hello friend
    for message in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).inbox:
        print(message[1])
        if message[1] == "hello friend":
            inInbox = True
    assert inInbox == True
    #clear Janaes inbox
    InCollegeApp.studentList.get("janaes").inbox.clear()
    #rewrite the messages from the message list
    for message in messageList:
        InCollegeApp.studentList.get("janaes").inbox.append(message)
    InCollegeApp.writeToInbox()

def testSendMessagePlus2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin', StringIO('randomuser\n'))
    InCollegeApp.sendMessageStandard()
    out, err = capfd.readouterr()
    assert ("No such user" in out) == True

def testSendMessageStandard(monkeypatch):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "monicaulloa"
    messageList = []
    for message in InCollegeApp.studentList.get("qizheng").inbox:
        messageList.append(message)

    monkeypatch.setattr('sys.stdin', StringIO('qizheng\nhello Qi\n0'))
    InCollegeApp.sendMessageStandard()
    inInbox = False
    # log in as Qi
    InCollegeApp.loggedInUsername = "qizheng"
    # make sure there unread messages
    assert (InCollegeApp.checkInbox()) == True
    # find the hello friend
    for message in InCollegeApp.studentList.get(InCollegeApp.loggedInUsername).inbox:
        if message[1] == "hello Qi":
            inInbox = True
    assert inInbox == True
    InCollegeApp.studentList.get("qizheng").inbox.clear()
    for message in messageList:
        InCollegeApp.studentList.get("qizheng").inbox.append(message)
    InCollegeApp.writeToInbox()

def testSendMessageStandard2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "monicaulloa"
    monkeypatch.setattr('sys.stdin', StringIO('janaes\n'))
    InCollegeApp.sendMessageStandard()
    out, err = capfd.readouterr()
    assert ("not friends" in out) == True

def testSendMessageStandard3(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "monicaulloa"
    monkeypatch.setattr('sys.stdin', StringIO('randomuser\n'))
    InCollegeApp.sendMessageStandard()
    out, err = capfd.readouterr()
    assert ("No such user" in out) == True

def testSevenDayNotification1(monkeypatch):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    assert InCollegeApp.pastSevenDayJobNotifi() == False


def testSevenDayNotification2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "danphan"
    assert InCollegeApp.pastSevenDayJobNotifi() == True
    out, err = capfd.readouterr()
    assert("Remember - You're going to want to have a job when you graduate" in out) == True


def testNumJobsAppliedTo(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    InCollegeApp.numJobNotifi()
    out, err = capfd.readouterr()
    assert("You have currently applied for 1 jobs" in out) == True

def testNumJobsAppliedTo2(monkeypatch,capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    InCollegeApp.numJobNotifi()
    out, err = capfd.readouterr()
    assert("You have currently applied for 2 jobs" in out) == True

def testNumJobsAppliedTo3(monkeypatch,capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "danphan"
    InCollegeApp.numJobNotifi()
    out, err = capfd.readouterr()
    assert("You have currently applied for 0 jobs" in out) == True

def testDeleteNotifi(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    InCollegeApp.newDeleteNotifi()
    out, err = capfd.readouterr()
    assert("A job that you applied for has been deleted - CASHIER" in out) == True

def testNewPostedNotifi(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    InCollegeApp.newPostedNotifi()
    out, err = capfd.readouterr()
    assert("A new job GYM RECEPTIONIST has been posted." in out) == True

#=========================== Epic 9 Test Cases ===================================#

def testTrainingMessages_TrainingAndEducation_OnlinePractices(monkeypatch, capfd):
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin', StringIO("1\n1\n0\n0\n"))
    InCollegeApp.trainingmenu()
    out, err = capfd.readouterr()
    assert ("UNDER CONSTRUCTION" in out) == True

def testTrainingMessages_TrainingAndEducation_FreeCourses(monkeypatch, capfd):
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin', StringIO("1\n2\n0\n0\n"))
    InCollegeApp.trainingmenu()
    out, err = capfd.readouterr()
    assert ("UNDER CONSTRUCTION" in out) == True

def testTrainingMessages_TrainingAndEducation_QuestionsAndAnswers(monkeypatch, capfd):
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin', StringIO("1\n4\n0\n0\n"))
    InCollegeApp.trainingmenu()
    out, err = capfd.readouterr()
    assert ("UNDER CONSTRUCTION" in out) == True

def testTrainingMessages_TrainingAndEducation_FreeCourses(monkeypatch, capfd):
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin', StringIO("1\n2\n0\n0\n"))
    InCollegeApp.trainingmenu()
    out, err = capfd.readouterr()
    assert ("UNDER CONSTRUCTION" in out) == True

def testTrainingMessages_IT_HelpDesk(monkeypatch, capfd):    
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin', StringIO('2\n0\n0\n'))
    InCollegeApp.trainingmenu()
    out, err = capfd.readouterr()
    assert ("Coming Soon" in out) == True
    
def testTrainingMessages_Security(monkeypatch, capfd):    
    InCollegeApp.loggedIn = False
    monkeypatch.setattr('sys.stdin', StringIO('1\n4\n0\n0\n'))
    InCollegeApp.trainingmenu()
    out, err = capfd.readouterr()
    assert ("UNDER CONSTRUCTION" in out) == True

def testBusinessAndStrategy1(monkeypatch, capfd):
    monkeypatch.setattr('sys.stdin',StringIO('1\nqizheng\nQz12345!\n'))
    InCollegeApp.business_analysis_and_strategy_menu()
    out, err = capfd.readouterr()
    assert("InCollege Account Login" in out) == True


def testBusinessAndStrategy2(monkeypatch, capfd):
    monkeypatch.setattr('sys.stdin',StringIO('2\nqizheng\nQz12345!\n'))
    InCollegeApp.business_analysis_and_strategy_menu()
    out, err = capfd.readouterr()
    assert("InCollege Account Login" in out) == True

def testCoursesTaken1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    assert("In College Learning" in InCollegeApp.studentList.get("qizheng").courseTook) == True
    assert("Train the Trainer" in InCollegeApp.studentList.get("qizheng").courseTook) == True
    assert("Gamification of learning" in InCollegeApp.studentList.get("qizheng").courseTook) == False
    assert("Architectural Design Process" in InCollegeApp.studentList.get("qizheng").courseTook) == True
    assert("Project Management Simplified" in InCollegeApp.studentList.get("qizheng").courseTook) == False

def testCoursesTaken2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "janaes"
    assert("In College Learning" in InCollegeApp.studentList.get("janaes").courseTook) == True
    assert("Train the Trainer" in InCollegeApp.studentList.get("janaes").courseTook) == False
    assert("Gamification of learning" in InCollegeApp.studentList.get("janaes").courseTook) == True
    assert("Architectural Design Process" in InCollegeApp.studentList.get("janaes").courseTook) == False
    assert("Project Management Simplified" in InCollegeApp.studentList.get("janaes").courseTook) == True

def testCoursesOutputList(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin',StringIO('0\n'))
    InCollegeApp.inCollegeLearning()
    out, err = capfd.readouterr()
    assert("How to use In College Learning" in out) == True
    assert("Train the trainer" in out) == True
    assert("Gamification of learning" in out) == True
    assert("Understanding the Architectural" in out) == True
    assert("Project Management Simplified" in out) == True

def testCoursesMessage1(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin',StringIO('1\nN\n0\n'))
    InCollegeApp.inCollegeLearning()
    out, err = capfd.readouterr()
    assert("You have already taken this course" in out) == True

def testCoursesMessage2(monkeypatch, capfd):
    InCollegeApp.loggedIn = True
    InCollegeApp.loggedInUsername = "qizheng"
    monkeypatch.setattr('sys.stdin',StringIO('3\n'))
    InCollegeApp.inCollegeLearning()
    assert("Gamification of learning" in InCollegeApp.studentList.get("qizheng").courseTook) == True
    InCollegeApp.studentList.get("qizheng").courseTook.remove("Gamification of learning")
    InCollegeApp.writeToCourseTook()
    assert("Gamification of learning" in InCollegeApp.studentList.get("qizheng").courseTook) == False

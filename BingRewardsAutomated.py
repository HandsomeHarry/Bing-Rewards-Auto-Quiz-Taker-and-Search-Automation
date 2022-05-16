import time
from selenium import webdriver
import random
import math
from datetime import date
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def superSonic(driver):#yep. does supersonic quizzes
    while True: #click start button
        try:
            driver.find_element_by_id("rqStartQuiz").click()
            break
        except:
            time.sleep(.1)
    for j in range(3): #theres 3 questions usually
        previousqtext = driver.find_element_by_class_name("bt_queText").text #helps us know when new question has loaded
        for i in range(5): #each quesiton has 5 answers
            answers = driver.find_elements_by_xpath('//*[@alt="Correct Image"]/../../../..') #xpath of the answers
            while True: #click the asnswer
                try:
                    answers[i].click()
                    break
                except:
                    time.sleep(.1)
        while True: #loop waits until next quesiton has loaded, or ends if quiz is over (third question is done)
            try:
                if driver.find_element_by_class_name("bt_queText").text!=previousqtext or j==2:
                    break
            except:
                time.sleep(.1)


def lightspeed(driver,loops):#does lightspeedquizzes and TandF questions. lightspd is 4 questions, TandF is one question
    #hence loops will = 4 or 1 accordingly.
    while True: #click start quiz
        try:
            driver.find_element_by_id("rqStartQuiz").click()
            break
        except:
            time.sleep(.1)
    previousAnswer=""# helps let us know when next question loads.
    for i in range(loops): #loop for 4 or 1 questions
        while True:#waits until new question loads
            if driver.find_element_by_id("rqAnswerOption0").get_attribute("value") != previousAnswer:
                break
        js_code = "return document.getElementsByTagName('script')"
        your_elements = driver.execute_script(js_code)  # gets javascript in the html that holds the answer
        for element in your_elements:#finds the correct answer in the javascript
            html = str(element.get_attribute("innerHTML"))
            if "correctAnswer" in html: #if found the correct answer in the element, extract it
                ind = html.index("correctAnswer")
                endind = html.index('","isMultiChoiceQuizType"')
                answer = html[ind + 16:endind] #locates the substring of html that is the answer
                previousAnswer=driver.find_element_by_id("rqAnswerOption0").get_attribute("value") #sets previous answer
                unicodeProblem=False
                while True:
                    if "\\u" in answer:
                        answerIndex=answer.index("\\u")
                        answer=answer[0:answerIndex]+answer[answerIndex+6:len(answer)]
                        unicodeProblem=True
                    else:
                        break
                clicked=False
                while True:#clicks the correct answer
                    try:
                        if unicodeProblem==True:
                            for element in driver.find_elements_by_xpath("//*[@data-option]"):
                                if similar(answer,element.get_attribute("data-option"))>=.9:
                                    clicked=True
                                    element.click()
                                    break
                        else:
                            driver.find_element_by_xpath('//*[@data-option="' + answer + '"]').click()
                            clicked=True
                        break
                    except:
                        time.sleep(.1)
                if clicked==False:
                    elements = driver.find_elements_by_xpath("//*[@data-option]")
                    for i in range(4):
                        while True:
                            try:
                                elements[i].click()
                                break
                            except:
                                time.sleep(.1)
                            time.sleep(.2)
                        try:
                            if driver.find_element_by_xpath('//*[@class=" rqcorrectAns"]'):
                                break
                        except:
                            pass

                break




def thisOrThat(driver):#lovely function. Can't tell answer by looking at xpath. So we keep txt file of answers!
    f = open("ThisOrThat.txt") #the text file of answers. it has the day on the first line (05,07,31,22)
    today = date.today()
    day = today.strftime("%d")#get todays  day (05,07,31,22)
    txtDay = f.readline()[0:-1] #get the day listed on the first line of the file.
    if day != txtDay: # if they dont equal, then this list is from yesterday. rewrite it to todays day and empty it.
        f = open("ThisOrThat.txt", "w")
        f.writelines(day + "\n") #second line is empty, it holds csv of answers.
        answers = [] #list of answers in the txt file is now empty.
    else:
        answers = f.readline().split(",") #if it is todays date, then extract the list of correct answers from line 2
    f.close() #close it babyyy
    f=open("ThisOrThat.txt","a") #reopen it in append mode, so we can write correct answers to it that werent there b4
    while True: #click start quiz
        try:
            driver.find_element_by_id("rqStartQuiz").click()
            break
        except:
            time.sleep(.1)
    previousOption=""#will help let us know if the next question loaded
    for i in range(10): #theres always 10 questions. loop through each one.
        selected = False #will let us know if we clicked an answer. is false if the answer isnt listed in the txt file
        first = "" #will keep track of the two otions given. ( QUESTION: "banana" (first)  or "apple" (second))
        second = ""
        while True:  # make sure question loaded by comparing the current first question to the previous first question
            try:
                firstoption = driver.find_element_by_xpath('//*[@id="rqAnswerOption0"]//*[@class="btOptionText"]')
                secondoption = driver.find_element_by_xpath('//*[@id="rqAnswerOption1"]//*[@class="btOptionText"]')
                first = firstoption.text
                second = secondoption.text #also gets the second questions text to append to file if its the right answr
                if first != previousOption:
                    break
            except:
                time.sleep(.1)
        for answer in answers: #go through each answer we have and see if its one of the options available
            if answer != '':
                try:
                    driver.find_element_by_xpath(
                        '//*[@id="rqAnswerOption0" and contains(@data-option,"' + answer + '")]').click()
                    selected = True #the first option  is an asnwer! click the answer and move on
                    break
                except:
                    try:
                        driver.find_element_by_xpath(
                            '//*[@id="rqAnswerOption1" and contains(@data-option,"' + answer + '")]').click()
                        selected = True#the second option is an asnwer! click the answer and move on
                        break
                    except:#pass if answer isnt  one of the option
                        pass
        if selected != True: #if both options are not in our current list of answers. click the first one
            driver.find_element_by_xpath('//*[@id="rqAnswerOption0"]').click()
            while True: #loop tells us when it moved onto next question. itll tell us if we were right or not.
                try:
                    #this is the xpath of the last option we clicked.
                    clickd=driver.find_element_by_xpath('//*[@class="btOptionCard btOptionClicked"]//*[@class="btOptionAns"]')
                    if first in clickd.text: #if the lsat option we clicked was the first option, it loaded
                        break
                except:
                    time.sleep(.1)
            #xpath of last option we clicked.
            clickd = driver.find_element_by_xpath('//*[@class="btOptionCard btOptionClicked"]//*[@class="btOptionAns"]')
            if "correct" in clickd.text:
                f.write(first + ",") #first option was right. add it to the txt file
            else:
                f.write(second + ",")#second option was right. add it to the txt file
        previousOption == first#reset previous option, got to next quesiton
    f.close()





def quizTaker(driver): #takes homepage and news quizzes!
    quizOver = False #tells us when da quiz is over
    while True: #loop  until no more questions (quizOver= True)
        driver.execute_script("window.scrollTo(0,(document.body.scrollHeight/5))")  # scroll down incase options are blocked by other quiz menus
        while True: #find the right answer. it is shown in the xpath.
            try:
                driver.find_element_by_xpath('//*[@class="wk_choicesInstLink"]//*[contains(@id,"ChoiceText")]//*[contains(@id,"statistics")]/../*[1]').click()
                break
            except:
                time.sleep(.1)
        while True: #loop presses the next question button, and detects if quiz is over
            try:
                butt = driver.find_element_by_name('submit') #the button
                if "Next" in butt.get_attribute("value"): #cool. not over.
                    butt.click()
                    while True: #sometimes clicking this button isnt enough. press enter until it goes away lol
                        try:
                            butt.send_keys("\n") #equivilent to pressing enter
                        except:
                            break #onto the next question
                else: #if it doesn't contain "next" then the quiz is over and it says "get score"
                    quizOver=True
                break
            except:
                time.sleep(.1)
        if quizOver==True: #quiz over, end loop.
            break



def pollTaker(driver): #does the poll quizzes. #just clicks the first option.
    while True:
        try:
            driver.find_element_by_class_name("bt_optionTxt").click()
            break
        except:
            time.sleep(.1)



def determineQuiz(driver):#used by doQuizzes(). determines which kind of quiz we have, and calls the right solve-function
    #IMPORTANT I am detecting whether certain strings are in the url. The URL will change in the future most likely.
    #this means that this function will need to be updated in order to properly determine the quiz type.
    #This also means that if bing creates a new quiz type, it must be added to here, and a function must be created
    #to solve said quiz type.
    if "thisorthat" in (driver.current_url).lower():
        print("Doing This or That Quiz")
        thisOrThat(driver)
    elif "POLL" in driver.current_url:
        print("Doing Poll...")
        pollTaker(driver)
    elif "HPQuiz" in driver.current_url:
        print("Doing Homepage Quiz")
        quizTaker(driver)
    elif "weekly%20quiz" in driver.current_url:
        print("Doing News Quiz")
        quizTaker(driver)  # same function
    elif "MicrosoftRewardsQuizDS" in driver.current_url:
        print("Doing Lightspeed Quiz...")
        lightspeed(driver, 4)
    elif "MicrosoftRewardsQuizCB" in driver.current_url:
        print("Doing Supersonic Quiz...")
        superSonic(driver)
    elif "TrueOrFalse" in driver.current_url:
        print("Doing True or False Quiz...")
        lightspeed(driver, 1)
    elif "RewardsDefinitions" in driver.current_url:
        print("Doing Word For Word Quiz...")
        lightspeed(driver,1)
    else:
        # just load a page for points
        print("Getting Featured Link")
        time.sleep(1) #wait 3 seconds to properly register to bing that it loaded.


def getquizzes(driver): #used by doQuizzes() funciton. goes to the quiz menu and gets list of elements of all quizzes to do
    driver.get("https://account.microsoft.com/rewards/") #quiz menu
    quizzes = "" #initiailze
    while True:#find the list of elements of quizzes to do. fun xpath lol.
        try:
            quizzes = driver.find_elements_by_xpath(
                '//*[contains(@class,"mee-icon mee-icon-AddMedium")]/../../../..//*[contains(@ng-class,"Mobile")]//*[(contains(@aria-label,"points") and not(contains(@aria-label,"Start"))) or contains(@aria-label,"Learn ")]')
            break
        except: #hasnt loaded. wait.
            time.sleep(.1)
    return quizzes #return the list.


def login(driver,email,errorsEncountered,password,url): #logs into bing account :) takes account emial and curren error total.
    #go to login page
    driver.get(url)
    while True: #loop to enter email into text box. so long lol.
        try:
            emailSignin = driver.find_element_by_id('i0116') # tries to type in the email into the email text box
            emailSignin.send_keys(email)
            break
        except: #uh oh, why cant u type it. lets see...
            errorFound=False #boolean will let us know if an error occured. if it did, we just reload the page
            try: #try and see if an error message came up.
                driver.find_element_by_id('idTD_Error')
                errorFound=True #we will reload page
            except:
                pass
            #if statement if error happened, or some kinda url error happened idk. it has happened before.
            if  errorFound==True or driver.current_url!=url:
                print("Login error. Restarting driver.")
                errorsEncountered += 1 #add one to the error counter!
                driver.quit()  # restart the  driver and go back to the login page
                driver = webdriver.Chrome('chromedriver.exe')
                driver.get(url)
                while True:  # now we try to enter the email again lol. should work now.
                    try:
                        emailSignin = driver.find_element_by_id(
                            'i0116')
                        emailSignin.send_keys(email)
                        break
                    except:
                        time.sleep(.1)
                break
            time.sleep(.1) #if no error was found, that just means 'enter email' page hasn't loaded. just wait.
    while True: #sometimes simply entering the email doesnt bring to the next page automatically. so we press next
        try:
            # if it can find this vvvv then it knows driver is on the Enter Email page still and needs to click 'next'
            if driver.find_element_by_partial_link_text('Create one!').text=="Create one!":
                driver.find_element_by_id('idSIButton9').click() #clicks next
                break
            else: #else it automatically went to the next page, so continue anyway
                break
        except: #except element hasnt loaded yet, wait
            time.sleep(.1)
    while True: #somtimes it asks if the profile is for work or personal. just click personal it does ask.
        try:
            driver.find_element_by_id('msaTileTitle').click() #clicks "personal profile"
            break
        except:#except sometimes, bing skips that^^^ step. check if password header is there vv,  that means it skipped
            try:
                if driver.find_element_by_id('loginHeader').text == "Enter password": #continue to password
                    break
            except: #except no password header, it hasnt loaded, wait.
                time.sleep(.1)
    while True: #oh yeaaaaa get that password textbox, baby!
        try:
            passwordSignin = driver.find_element_by_id('i0118') #find dat password box
            break
        except: #except it hasnt loaded
            time.sleep(.1)
    passwordSignin.send_keys(password)#hehe dont copy my password!!
    while True: #loop to press sign in!!!!
        try:
            driver.find_element_by_id('idSIButton9').click()#SIGN IN, BABY!!!
            break
        except:# except it hasnt loaded, wait
            time.sleep(.1)
    return errorsEncountered #return the errrEncountered total


def getPointsInfo(driver,firstName): #gets a whole bunch of stats, and how many timesToSearch on bing
    driver.get("https://www.bing.com/")
    while True:  # check if profile name is firstName, the first name of every profile. this means page loaded
        try:
            if driver.find_element_by_id("id_n").text == firstName:
                break
            else:
                account = driver.find_element_by_id('id_l')  #otherwise, click sign in to immedeatly load profile. glitch
                account.send_keys("\n") #click by pressing enter...
        except:  # it hasnt properly loaded, wait.
            time.sleep(.1)
    startingPoints = getPointTotal(driver) #get total number of points on account before running program
    # the next 8 lines find a url inside the dropdown menu that takes us to some point stats we want.
    while True:
        try:
            driver.find_element_by_id('id_rh').click()  # rewards button. drop down menu showing point stats
            menu = driver.find_element_by_xpath('//*[@id="id_rh"]//../div[@id="bepfo"]/iframe') #lol
            driver.get(menu.get_attribute('src'))  # go to url which has the points stats
            break
        except:
            time.sleep(.1)
    points = driver.find_element_by_class_name("mfo_c_es").text #find the points info
    driver.get("https://www.bing.com/")  # got da info, heading back to command. go back to bing, squad
    if points[:2] == "PC":
        points = points[11:]  # gets rid of substring "PC search: " at the start of the point tally
    else:
        pass #level 2 accounts dont say "PC search: ". they just list the points
    #points variable should now be something like 0/50 or  0/150 or 20/50 or smthn
    pointsEarned = ""#how many points we earned so far today. usually zero. but just incase of special scenarios...
    for char in points:# #get the first part of the points variable, the part before the '/'
        if char != "/":
            pointsEarned = pointsEarned + char
        else:
            break
    totalPointsEarnable = points[len(pointsEarned) + 1:]  # this will be either 50 or 150
    pointsLeftToEarn = int(totalPointsEarnable) - int(pointsEarned)  # usually the same as totalPointsEarnable
    timesToSearch = int(pointsLeftToEarn / 5)#each search is worth 5 points. if we can earn 50 points,itll search10times
    return totalPointsEarnable,pointsLeftToEarn,timesToSearch,startingPoints #return the stats


def search(driver,words,timesToSearch,firstName): #function to search stuff. requires the list of words and how many times to srch
    while timesToSearch > 0:  # do x number of searches
        driver.find_element_by_id('sb_form_q').clear()  # clears search box
        # vvvv searches 4 random words, fam.
        driver.find_element_by_id('sb_form_q').send_keys(
            words[random.randint(0, len(words) - 1)] + ' ' + words[random.randint(0, len(words) - 1)] + ' ' + words[
                random.randint(0, len(words) - 1)] + ' ' + words[random.randint(0, len(words) - 1)] + '\n')
        # makes sure page is loaded for next search via profile name firstName showing.
        while True:
            if driver.find_element_by_id("id_n").text == firstName:
                break
            else:
                time.sleep(.1)
        driver.find_element_by_xpath('//*[@id="b_results"]/li[1]').click()
        driver.get("https://www.bing.com/search?q=banana")
        timesToSearch -= 1  # one search complete


def loginRewards(driver,email,errorsEncountered,password):
    driver.get("https://login.live.com/logout.srf?ct=1613241120&rver=7.0.6738.0&lc=1033&id=292666&ru=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signout%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252Frewards%252Fdashboard%253Frefd%253Dlogin.live.com")
    errorsEncountered = login(driver,email,errorsEncountered,password,"https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1613241065&rver=7.0.6738.0&wp=MBI_SSL&wreply=https:%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signin%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252Frewards%253Fru%253Dhttps%25253A%25252F%25252Faccount.microsoft.com%25252Frewards%25252Fdashboard&lc=1033&id=292666&lw=1&fl=easi2")
    return errorsEncountered

def doQuizzes(driver): #first process of doing the quizzes. makes sure we go through each quiz
    quizzes = getquizzes(driver) #get the quizzes we have to do. this takes us to the Quiz Menu also
    ogQuizLength = len(quizzes)
    quizSkipper = 0 #if theres a new quiz type or something, and the quiz wasn't actually performed, skip it.
    print(str(ogQuizLength)+" quizzes to do...")
    for i in range(ogQuizLength): #go through and do each quiz
        # clicking a quiz opens a new tab, we only want one tab at a time. so get hte id of the current tab
        #which is the menu of all the quizzes using the code below
        window = driver.current_window_handle
        Quiz = quizzes[quizSkipper]  #select the quiz to do
        try:
            Quiz.click() #click the quiz link
        except: #except a pop up occured. close out of it.
            while True:
                try:
                    driver.find_element_by_xpath('//*[@id="modal-host"]/div[2]/button').click()
                    break
                except:
                    time.sleep(.1)
            Quiz.click()
            #this opens a new tab. Switch to the other tab (the menu of all the quizzes) and close it
        driver.switch_to.window(window)
        while True:
            if len(driver.window_handles) == 2:
                break
        driver.close()
        #now switch back to the tab with the quizw
        window = driver.window_handles[0]
        driver.switch_to.window(window)
        determineQuiz(driver) #determine and do the quiz...
        driver.get("https://account.microsoft.com/rewards/")
        quizzes = getquizzes(driver)# go back to quizzes menu and get all the quizzes for the next loop
        while True:
            if "https://account.microsoft.com/rewards" in driver.current_url:
                break
            else:
                time.sleep(.1)
        if len(quizzes) == ogQuizLength:  # new kind of quiz was clicked that I have not programmed to complete yet, skip
            quizSkipper += 1


def getPointTotal(driver): #gets current total amount of points on the account
    driver.get("https://www.bing.com/")#go to or reload bing so points start to load, cause sometimes they dont
    while True:  #loop waits till points load completely (the points tally starts at 0 and increases to actual number)
        try:
            points = int(driver.find_element_by_id("id_rc").text)#current number of points shown
            time.sleep(.5)#wait half a sec
            pointsAfterHalfSecond = int(driver.find_element_by_id("id_rc").text)#now how many points are shown
            if pointsAfterHalfSecond == points: #compare. if not equal, points are still increasing
                break
        except: #nothings loaded. wait.
            time.sleep(.1)
    return points #return current total number of points




def logout(driver): #used to log out of bing
    account = driver.find_element_by_id('id_l')  # find profile dropdown menu
    while True:  # access logout dropdown menu using two 'enter' presses. wait to till we can preform the first one
        try:
            account.send_keys("\n")#equivilant to pressing enter on the keyboard
            break
        except:
            time.sleep(.1)
    account.send_keys("\n")
    driver.execute_script("arguments[0].scrollIntoView();", account)  # scroll to it so its in view of browser
    while True:  # then click the sign out button!
        try:
            driver.find_element_by_xpath('//*[@id="id_h"]/span[@id="id_d"]//a').click()
            break
        except:
            try:
                account.send_keys("\n")# uh if nothing happend just press enter lol idk
            except:
                try:
                    account.click()
                except:
                    pass


def main():
    words=[] #holds da words used to search. i have a list of 1000 popular words.
    f=open("words.txt") #the list of popular words
    for word in f.readlines(): #add them words to the list
        words.append(word[:-1])
    f=open("emails.txt") #da list of bing account emails
    emailCounter=1 #keep track of which account we're on
    totalEmails=len(f.readlines()) #total number of emails to go through
    programStartTime=time.perf_counter() #so at the end we can print how long it took to run.
    totalPointsEarnedInRun=0 #keep track of points earned by running the program this time
    totalPointsEarnedTotal=0 #keep track of how many points we have overall.
    errorsEncountered=0 #keeps track of how many errors bing sends so we can print em.  program gets past them, dw.
    f=open("emails.txt") #open da list of bing account emails again so we can go line by line
    accountTotals={}#dictionary of accounts and how many points is on each one. used at end.
    while True:
        try:
            quizzesOrNot=input("Do you want me to attempt to do the Bing quizzes as well?\nType 'y' or 'n'\n>> ")
            if quizzesOrNot =='y':
                print("sick, lets do those quizzes!")
                break
            elif quizzesOrNot=='n':
                print("Coward. ok, I won't do the quizzes")
                break
            else:
                print("you had two options, y and n. you failed. try again.")
        except:
            print("uh, bad input. Please enter y or n")
    driver = webdriver.Chrome('chromedriver.exe') #start webdriver
    for email in f.readlines(): #go through each account, homie
        if email!='\n' and email!='':
            if email[-1] == '\n':#gets rid of \n at the end of an email
                email = email[0:len(email) - 1]
            email=email.split(",")
            password=email[2]
            firstName=email[1]
            email=email[0]
            print("Email in use: " +str(emailCounter)+'/'+str(totalEmails)+' '+ email+' '+firstName)
            emailCounter+=1 #add one to emailCounter for the next loop
            print("Signing in...")
            errorsEncountered = loginRewards(driver,email,errorsEncountered,password)
            #errorsEncountered = login(driver,email,errorsEncountered,password,"https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1611539831&rver=6.7.6631.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fwlexpsignin%253d1%26sig%3d334A818C1EDD6FAC2EB88E461F556EBE&lc=1033&id=264960&CSRFToken=136dce96-1e93-492a-a85e-e41e3678db28&aadredir=1") #self explanatory
            print("Getting point info...")#get info on how many times to search, and various points stats
            totalPointsEarnable,pointsLeftToEarn,timesToSearch,startingPoints=getPointsInfo(driver,firstName) # gets a bunch of info
            print("Points at start: " + str(startingPoints))#points on account before program runs
            print("Points to earn: " + str(pointsLeftToEarn))#points left to earn by searching on this account
            print("Times to search: " + str(timesToSearch)) #how many times the program will search on bing
            print("Searching...")
            search(driver,words,timesToSearch,firstName) # it do be searching tho
            if quizzesOrNot=='y':
                print("Starting quizzes...")
                doQuizzes(driver) #do dem quizzes
            endingPoints = getPointTotal(driver) #get the total points on the account now that the program ran
            print("Points at end: " + str(endingPoints) + '\n')
            logout(driver) #log tf out so we can sign into next account
            totalPointsEarnedInRun+=(endingPoints-startingPoints)  #self explanatory
            totalPointsEarnedTotal+=endingPoints
            accountTotals[email]=endingPoints #creates the account's email as a key, and sets it's value to its point total
    programEndTime=time.perf_counter() #used to get total run tume of program (endtime -starttime)
    print("\n\nAccounts in order of least to most points:\n")
    sorted_keys = sorted(accountTotals, key=accountTotals.get) #sorts the accountTotals dict from least to most points
    for w in sorted_keys: #prints out accounts from least to most points
        print(w+": "+str(accountTotals[w])+" points")
    print("\n\nTotal Time to run "+str(totalEmails)+" accounts: "+str(math.ceil(programEndTime-programStartTime))+" s (around "+str(round((programEndTime-programStartTime)/totalEmails,1))+" s / per account)")
    print("Total points in your possession, sire: "+str(totalPointsEarnedTotal))
    print("Total points earned from this run: "+str(totalPointsEarnedInRun))
    print("Number of errors bing sent: "+str(errorsEncountered))
    driver.quit() #dab



main() #:)

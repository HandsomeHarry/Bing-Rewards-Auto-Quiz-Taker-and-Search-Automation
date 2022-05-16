# Bing-Rewards-Automator-H
This is a fork of the original Bing-Rewards-Automator, which automatically does quizzes and earn you bing points. Works with multiple accounts.

By Daniel Goldberg 2021, edited by Harry Yu 2022

HOW TO ENTER YOUR INFORMATION:
  in each line of the emails.txt file, write your accounts email, your accounts first name verbatim as is on bing, and your accounts password, all in the the following format:
  
    emailman@email.org,FIRSTNAME,PASSWORD
    foodeater@gmail.net,FIRSTNAME,PASSWORD
    thirdemail@site.io,FIRSTNAME,PASSWORD
    
  Of course, if you only have one account, just use one line.

THIS PROGRAM USES CHROMEDRIVER.EXE. Before using it for the first time, run it once by double clicking it. you can download the newest version here if the one given by me is out of date: https://chromedriver.chromium.org/downloads
 
PROGRAM INFO/TUTORIAL

The BingRewardsAutomated program searches bing on each account until it reaches maximum points allowed (for isntance, if you can earn 50 points today by seraching it will search 10 times). at the beggining of the program it will ask you if you want to attempt to do the available bing quizzes. If you enter 'n', it will simply search on each account and end.

if you enter 'y', it will search on each account and also attempt to do the quizzes that are available. uh at least i hope it does lol. If you choose this option and the program breaks, run the program again but do not attempt quizzes (enter 'n' when prompted), itll just do the searching, no quizzes. The quiz taking functionality is a work in progress, and would require a lot of monitoring and updating over time. IMPORTANT:  i haven't tested it with bing polls yet, so idk if those work. will fix soon. ALSO if it opens a quiz, waits a second, closes out of it without taking it, and the program prints "getting featured link" (but it was a quiz), then that means that there is a new type of quiz or something that i have not coded for. It'll skip it i hope. I will have to program it to be able to take that quiz tho.

That being said, a lot of the code here is dependent on certain xpath designations and assumptions about how the site works. If Bing changes something, the program might not be able to complete, and needs to be changed. 


thanks!


FURTHER INFORMATION:
do not touch the txt file called ThisOrThat.txt. its just a data storage for answers to ThisorThat questions. it wipes itself each day. It stores answers incase you have multiple accounts you want to run. This way it knows the right answers for when it takes the quiz on the second account.

ye boiiii. 


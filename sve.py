import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import random as rd
from datetime import datetime
from datetime import date
import math


df = pd.read_csv('GiosDict.txt')
# df = pd.read_csv('~/Dropbox/svenska/GiosDict.txt')

today = date.today()
today = today.strftime("%Y-%m-%d")

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    ITA = '\x1B[3m'

    
for i in range(0,len(df)):
    dd = days_between(today,df["day"].iloc[i])
    k = math.floor(dd/7)
    df["point"].iloc[i] = df["point"].iloc[i] - k
    if df["point"].iloc[i] < 0:
        df["point"].iloc[i] = 0
    df.to_csv('GiosDict.txt',index=False)

print(color.CYAN+color.BOLD+'\n WELCOME!\n'+color.END)
colnames = ["word","point","meaning","class","day"]
# main menu

j = 1
while j == 1:

    action = input('What do you want to do? (add/play/see/quit) ').lower()

# add new words
    if action.startswith('a'):
        i = 1
        while i == 1:
            df =pd.read_csv('GiosDict.txt')
            inpt = input('Insert a new word, meaning, class, or enter '+color.ITA+'back\n '+color.END)

            if not inpt:
                print('You have not inserted anything =( \n')
            elif inpt in 'back':
                i = i+1
            else:

                ind = inpt.split(',')
                ordet = ind[0]
                df.to_csv('GiosDict.txt',index=False)
                
                if len(ind) == 1:
                    inpt = input('Wanna add meaning or class? enter if not \n ')
                    if not inpt:
                        m = None
                        cl = None
                    else:
                        ind = inpt.split(',')
                        m = inpt[0]
                        if len(ind) == 1:
                            inpt = input('Wanna add a class? enter if not \n ')
                        if not inpt:
                            cl = None
                        else:
                            cl = inpt
                elif len(ind) == 2:
                    m = ind[1]
                    inpt('Wanna add a class? enter if not \n ')
                    if not inpt:
                        cl = None
                    else:
                        cl = inpt
                else:
                    m = ind[1]
                    cl = ind[2]
                
                if cl == 'n' or cl == 'N':
                    cl = 'noun'
                elif cl == 'v' or cl == 'V':
                    cl = 'verb'
            
                df2 = pd.DataFrame([[ordet,0,m,cl,today]],columns=colnames)
                df = df.append(df2)
                df = df.sort_values(by='word')
                df = df.reset_index(drop=True)
                df.to_csv('GiosDict.txt',index=False)
                print(' added the word number'+color.BOLD+color.CYAN+' {} '.format(len(df))+color.END+'\n ')
                
# play a game
    elif action.startswith('p'):
        i = 1
        while i == 1:
            # take the list and look which words has maximum points of 5            
            df =pd.read_csv('GiosDict.txt')

            dfu = pd.DataFrame(columns=colnames)
            for z in range(1,len(df)):
                if df['point'].iloc[z] < 5:
                    dfu = dfu.append(df[:].iloc[z])
            n = rd.choice(dfu.index)
            ans =input('ook, Do you know this word' + color.CYAN + color.BOLD +' {} '.format(df['word'].iloc[n]) +color.END + '? (yes/no/back) ').lower()
            if ans.startswith('y'):   # etc.
                df['point'].iloc[n] = df['point'].iloc[n] + 1
                print('Great! {} has now'.format(df['word'].iloc[n])+color.CYAN+color.BOLD+' {} '.format(df['point'].iloc[n])+color.END+'points\n')
                df['day'].iloc[n] = today
                if df['point'].iloc[n] == 5:
                    print("Woo, you know this word very well I'm impressed\nI'm not gonna ask it again...\nunless you forget it ;)")
                    
            if ans.startswith('n'):   # etc.
                print('too bad, {} means'.format(df['word'].iloc[n]) +color.RED+color.BOLD+' {}'.format(df['meaning'].iloc[n])+color.END+' and it is a'+color.BOLD+' {}\n'.format(df['class'].iloc[n])+color.END)
                print('back to 0 =(\n') 
                df['point'].iloc[n] = 0

            df.to_csv('GiosDict.txt',index=False)
            if ans.startswith('b'):
                i = i + 1

        print(df[['word','point']])

# see more stats        
    elif action.startswith('s'):
        print(df[['word','meaning','class']])
        ans=input("Do you see more, edit some words, or reset the points? (more/edit/reset/back) ").lower()
        if ans.startswith('r'):
            ans2 = input('Are you sure? ').lower()
            if ans.startswith('y'):
                for i in range(0,len(df)):
                    df['point'].iloc[i] = 0
                print(df)
                df.to_csv('GiosDict.txt',index=False)
        elif ans.startswith('m'):
            print(df)
        elif ans.startswith('e'):
            print(df.word)
            j = 1
            while j == 1:
                ind = input('\nWhich word? (number/back) ').lower()
                if ind.startswith('b'):
                    j = j + 1
                else:
                    ind = int(ind)
                    print(color.RED+color.BOLD+'{}'.format(df['word'].iloc[ind])+color.END)
                    ans = 'n'
                    while ans.startswith('n'):
                        newword = input('\nType the new version ').lower()
                        ans = input('Are you sure'+color.CYAN+color.BOLD+' {} '.format(newword)+color.END+'is the new correct version of the word which means {}? (yes/no) '.format(df['meaning'].iloc[ind])).lower()
                    print(' Done')
                    df['word'].iloc[ind] = newword
            
    elif action.startswith('q'):
       j = j+1
       print(' bye bitch <3')
    else:
        print("not good")
    

import pandas as pd
from constants import *


pd.options.mode.chained_assignment = None  # default='warn'
import random as rd
from datetime import datetime
from datetime import date
import math

df = pd.read_csv('GiosDict.txt')
# df = pd.read_csv('~/Dropbox/svenska/GiosDict.txt')


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def RemovePoints(data):
    today = date.today()
    today = today.strftime("%Y-%m-%d")
    for i in range(0, len(data)):
        dd = days_between(today,data["day"].iloc[i])
        k = dd // 7
        data["point"].iloc[i] = data["point"].iloc[i] - k
        if data["point"].iloc[i] < 0:
            data["point"].iloc[i] = 0
        data.to_csv('GiosDict.txt',index=False)

RemovePoints(df)

print(color.CYAN+color.BOLD+'\n WELCOME!\n'+color.END)
colnames = ["word","point","meaning","class","day"]
# main menu

def quitorgoback(action, logic, backorquit):
    if action.startswith(backorquit):
        logic = False

mainloop = True


while mainloop:

    action = input('What do you want to do? (add/play/see/quit) ').lower()

    # add new words
    if action.startswith('a'):
        Add = True
        while Add:
            df =pd.read_csv('GiosDict.txt')
            inpt = input('Insert a new word, meaning, class, or enter '+color.ITA+'back\n '+color.END)

            if not inpt:
                print('You have not inserted anything =( \n')
            elif inpt in 'back':
                Add = False
            else:

                ind = inpt.split(',')
                ordet = ind[0]
                df.to_csv('GiosDict.txt',index=False)
                
                if len(ind) == 1:
                    inpt = input('Wanna add meaning or class? enter if not \n ').lower()
                    if not inpt:
                        m = None
                        cl = None
                    else:
                        ind = inpt.split(',')
                        m = inpt[0]
                        if len(ind) == 1:
                            inpt = input('Wanna add a class? enter if not \n ').lower()
                        if not inpt:
                            cl = None
                        else:
                            cl = inpt
                elif len(ind) == 2:
                    m = ind[1]
                    inpt = input('Wanna add a class? enter if not \n ').lower()
                    if not inpt:
                        cl = None
                    else:
                        cl = inpt
                else:
                    m = ind[1]
                    cl = ind[2]
                
                if cl.startswith('n'):
                    cl = 'noun'
                elif cl.startswith('v'):
                    cl = 'verb'
            
                df2 = pd.DataFrame([[ordet,0,m,cl,today]],columns=colnames)
                df = df.append(df2)
                df = df.sort_values(by='word')
                df = df.reset_index(drop=True)
                df.to_csv('GiosDict.txt',index=False)
                print(' added the word number'+color.BOLD+color.CYAN+' {} '.format(len(df))+color.END+'\n ')
                
    # play a game
    elif action.startswith('p'):
        play = True
        while play:
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
                play = False

        # print(df[['word','point']])

    # see more stats        
    elif action.startswith('s'):
        
        for i in range(len(df)):
            df['word'].iloc[i]
            
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
        mainloop = False
        print(' bye bitch <3')
    else:
        print("not good")
    

#-*- coding:utf-8 -*-

from flask import *


#끝말잇기 프로젝트

print("인공지능 끝말잇기 by sy77:")
print("다시하려면 /키를 누르세요")

print("loading...")

f = open('wordslist.txt', 'r', encoding='UTF8')
words = []
linecount = 0
while True:
    line = f.readline().rstrip('\n')
    if line == "." :
        break
    else :
        # parse!
        parsed_list = line.split( '\t')
        if len(line) > 1 and line[0] != "【" :
            words.append(str(line))
            linecount += 1
f.close();

startchar = [[],[]]
char = ""
for i in range(linecount):
    if words[i][0] != char:
        char = words[i][0]
        startchar[0].append(char)
        startchar[1].append(i)

winChar = []
loseChar = []

def AiStudying():
    for i in range(len(words)):     #1차적으로 지는 글자와 이기는글자 분류하기
        nowchar = words[i][len(words[i]) - 1]     #loseChar리스트는 할게없는 지는글자
        if nowchar not in startchar[0]:            #winChar리스느는 한방단어 써서 이기는글자
            if words[i][0] not in winChar:
                winChar.append(words[i][0])
            if nowchar not in loseChar:
                loseChar.append(nowchar)
    for a in range(4):
        #여기서 winChar 리스트는 무조건 이기는 리스트이기 때문에 할수있는말이 winChar 리스트밖에 없는 글자는 loseChar 에 넣는다
        for i in range(len(startchar[0]) - 1):               #시작글자 리스트의 항목을 다 돌려본다.
            if startchar[0][i] not in loseChar and startchar[0][i] not in winChar:     #만약이글자가 이미 등록이 안된거면:
                canlist = []
                startindex = startchar[1][startchar[0].index(startchar[0][i])]
                endindex = startchar[1][startchar[0].index(startchar[0][i]) + 1]
                allLose = 1
                for j in range(startindex, endindex):                    #이글자로 시작하는 단어의 끝이 모두 winchar리스트에 있으면 이글자는 loseChar에 넣는다
                    if words[j][len(words[j]) - 1] not in winChar:
                        allLose = 0
                if allLose == 1:
                    loseChar.append(startchar[0][i])

        for i in range(len(words)):
            nowchar = words[i][len(words[i]) - 1]
            if nowchar in loseChar:
                if words[i][0] not in winChar:
                    winChar.append(words[i][0])

        print(25 * (a + 1) , "%")

def AI(playerWord):
    canlist = []
    playerlastchar = playerWord[len(playerWord) - 1]
    if str(playerlastchar) not in str(startchar[0]):
        print("당신이 이겼습니다")
        return 0
    startindex = startchar[1][startchar[0].index(playerlastchar)]
    endindex = startchar[1][startchar[0].index(playerlastchar) + 1]

    for i in range(startindex, endindex):
        if words[i] not in Gamelist:
            canlist.append(words[i])
    if len(canlist) == 0:
        print("당신이 이겼습니다")
    else:
        wincharword = ""
        notloseword = ""
        for i in range(len(canlist)):
            if str(canlist[i][len(canlist[i]) - 1]) in str(loseChar):
                wincharword = canlist[i]
            elif str(canlist[i][len(canlist[i]) - 1]) not in str(winChar):
                notloseword = canlist[i]
        if wincharword != "":
            AiWord = wincharword;
        elif notloseword != "":
            AiWord = notloseword
        else:
            AiWord = canlist[0]

        print("인공지능: ", AiWord)
        if AiWord[len(AiWord) - 1] not in startchar[0]:
            # input("인공지능이 이겼습니다. \n 다시하려면 아무키나 누르십시오.")
            # AiWord = "다시"
            pass
    return  AiWord




AiStudying()
Gamelist = []
Turn = 0
#게임하기
'''
AiWord = 1
while AiWord != 0:
    playerWord = str(input("단어입력: "))
    if playerWord in words and (Turn == 0 or playerWord[0] == AiWord[len(AiWord) - 1]) and playerWord not in Gamelist:
        Gamelist.append(playerWord)
        AiWord = AI(playerWord)
        Gamelist.append(AiWord)
        if AiWord == "다시":
            Gamelist = []
            playerWord = str(input("단어입력: "))
            Gamelist.append(playerWord)
            AiWord = AI(playerWord)
            Gamelist.append(AiWord)
        Turn += 1
    elif playerWord == "/":
        Gamelist = []
        playerWord = str(input("단어입력: "))
        Gamelist.append(playerWord)
        AiWord = AI(playerWord)
        Gamelist.append(AiWord)
    elif Turn == 0 and len(playerWord) == 1:
        Gamelist.append(playerWord)
        AiWord = AI(playerWord)
        Gamelist.append(AiWord)
        if AiWord == "다시":
            Gamelist = []
            playerWord = str(input("단어입력: "))
            Gamelist.append(playerWord)
            AiWord = AI(playerWord)
            if AiWord == 0:
                break
            else:
                Gamelist.append(AiWord)
        Turn += 1
    elif playerWord not in words:
        print("없는 단어입니다")
    elif playerWord[0] != AiWord[len(AiWord) - 1]:
        print(AiWord[len(AiWord) - 1], "(으)로 시작하는 단어를 써주세요")
    else:
        print("이미 사용된 단어입니다")'''

app = Flask(__name__)


@app.route('/')
def inputTest():
    return render_template('main.html')


@app.route('/main', methods=['POST'])
def calculate():
    isWord = request.form['inputWord'] in words
    endByPlayer = True
    usedWord = False
    startFromLast = len(Gamelist) == 0
    print(startFromLast)

    temp = '아악'
    if isWord:
        if startFromLast or request.form['inputWord'][0] == Gamelist[-1][-1]:
            startFromLast = True
            if request.form['inputWord'] not in Gamelist:
                Gamelist.append(request.form['inputWord'])
                if request.method == 'POST':
                    if request.form['inputWord'][-1] in startchar[0]:
                        temp = str(AI(request.form['inputWord']))
                        Gamelist.append(temp)
                        endByPlayer = False
                else:
                    temp = None
            else:
                usedWord = True
                endByPlayer = False
        else:
            usedWord = False
            endByPlayer = False
    else:
        endByPlayer = False
    lenGame = len(Gamelist)
    return render_template('main.html', gamelist=list(reversed(Gamelist)), isWord = isWord, isLose = True, lgl = lenGame, isStarted = True,
                           endByAi = temp[-1] not in startchar[0], endByPlayer = endByPlayer, usedWord = usedWord, startFromLast = startFromLast)


if __name__ == '__main__':
    app.run()
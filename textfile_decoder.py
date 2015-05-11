'''
This program asks the user to choose a Process and then a Parameter from the selected Process to graph.
'''

import matplotlib.pyplot as plt

class TextFileDecoder:
    __fileName = ''
    __recipe = ''
    __chamber = ''
    __time = []
    __batch = ''
    __parsedText = []
    __processes = {}
    __processNumberKey = {}
    __parameters = {}
    __numProcesses = 0
    __numParameters = 0

    def __init__(self, fileName):
        self.__fileName = fileName

    # Breaks the text down into a long list of elements.
    def parseLines(self):
        text_file = open(self.__fileName)
        tempParsedText = text_file.read().split('\n')
        counter = 0
        for index in range(len(tempParsedText)):
            tempList = tempParsedText[index].split(',')
            if tempList[0] == 'Process Step':
                counter += 1
            if tempList[len(tempList) - 1] == '':
                tempList = tempList[:-1]
            self.__parsedText.extend(tempList)
        self.__numProcesses = counter

    # Stores information provided at the beginning of the text file into variables for
    # later use in presenting information.
    def sortInfo(self):
        self.__recipe = self.__parsedText[1]
        self.__chamber = self.__parsedText[3]
        self.__time = self.__parsedText[4:7]
        self.__batch = self.__parsedText[8]
        self.__parsedText = self.__parsedText[9:]

    # Separates the list by processes.
    def parseProcess(self):
        for x in range(1, (self.__numProcesses + 1)):
            processIndex = 2
            processName = ''
            processText = []
            while self.__parsedText[processIndex] != str(x):
                processName = processName + self.__parsedText[processIndex]
                processIndex += 1
            self.__processNumberKey[x] = processName
            self.__parsedText = self.__parsedText[processIndex + 1:]
            processText.append([processName, str(x)])
            processText.append(self.__parsedText.pop(0))
            while (self.__parsedText[0] != 'Process Step'):
                processText.append(self.__parsedText.pop(0))
                if not self.__parsedText:
                    break
            self.__processes[processName] = processText

    # Sorts a Process list into lists for each Parameter with their data.
    def sortProcess(self, processKey):
        self.__numParameters = 0
        tempParameters = {}
        processText = self.__processes[processKey]
        temp = processText.pop(0)
        processText = processText[1:]
        while processText[0] != 'Demands':
            tempParameters[self.__numParameters] = [processText.pop(0)]
            self.__numParameters += 1
        processText = processText[1:]
        for x in range(0, self.__numParameters):
            tempParameters[x].append(processText.pop(0))
        while processText[0] == 'Readbacks':
            processText = processText[1:]
            for x in range(0, self.__numParameters):
                tempParameters[x].append(processText.pop(0))
            if not processText:
                break
        self.__parameters = tempParameters

    # Displays text in console where user inputs a number to retrieve requested information.
    def display(self):
        print('The following Processes are available to examine:')
        for x in range(1, self.__numProcesses + 1):
            if x < 10:
                print('\t%i.)\t\t%s' % (x, self.__processNumberKey[x]))
            else:
                print('\t%i.)\t%s' % (x, self.__processNumberKey[x]))
        print('')
        userString = input('Select a Process to examine: ')
        test.sortProcess(self.__processNumberKey[userString])
        print('')
        print('Loading:\t%s...' % self.__processNumberKey[userString])
        print('')
        print('The following Parameters are available to graph:')
        for x in range(1, self.__numParameters):
            paramName = ''
            if self.__parameters[x][2]:
                paramName = self.__parameters[x][0]
            else:
                paramName = '---'
            if x < 10:
                print('\t%i.)\t\t%s' % (x, paramName))
            else:
                print('\t%i.)\t%s' % (x, paramName))
        print('')
        userString2 = input('Select a Parameter to graph: ')
        print('')
        print('Creating graph for %s' % self.__parameters[userString2][0])
        test.createGraph(userString2)

    # Creates the graph in (time, Parameter Data) format.
    def createGraph(self, num):
        stepTime = self.__parameters[0][1]
        ftr = [3600, 60, 1]
        stepTime = sum([a * b for a, b in zip(ftr, map(int, stepTime.split(':')))])
        timeList = []
        for x in range(1, len(self.__parameters[0])):
            timeList.append(x * stepTime)
        plt.plot(timeList, self.__parameters[num][1:], 'ro')
        plt.show()

# Functions must be used in this order in order to prevent errors.
test = TextFileDecoder('TKFGaPPhC13_Etch.txt')
test.parseLines()
test.sortInfo()
test.parseProcess()
test.display()
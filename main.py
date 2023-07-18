import subprocess
import os

class Command():
    NUMBER = 'number'
    def __init__(self, supportMultiCmd : bool, function, paramLimit = ''):
        self.supportMultiCmd = supportMultiCmd
        self.paramLimit = paramLimit
        self.function = function

    def checkParamLimit(self, param : str):
        if self.paramLimit != '':
            match(self.paramLimit):
                case 'number':
                    if param.isdigit():
                        return True
            print("Please enter {} parameters!".format(self.paramLimit))
            return False
        return True

    def run(self, paramsList : list):
        if not self.supportMultiCmd:
            if not self.checkParamLimit(paramsList[0]):
                return
            self.function(paramsList[0])
        else:
            for param in paramsList:
                if not self.checkParamLimit(param):
                    return
                self.function(param)

class dirShow:
    currentPath = '/'
    lastPath = ''
    currentPage = 0
    linesShow = 10
    lines = []
    fo = open("foo.txt", "a+")
    def __init__(self) -> None:
        self.commands = {}
        self.linesShow = os.get_terminal_size().lines - 8
        # 打开一个文件
        self.fo.seek(0)
        path = self.fo.readline()
        if path != '':
            self.currentPath = path
        
        self.AddCommand('cd', Command(supportMultiCmd=False, function=self.Cmd_cd))
        self.AddCommand('pull', Command(supportMultiCmd=True, function=self.MultiCmd_pull))
        self.AddCommand('push', Command(supportMultiCmd=True, function=self.MultiCmd_push))
        self.AddCommand('rm', Command(supportMultiCmd=True, function=self.MultiCmd_rm))

    def AddCommand(self, name : str, processor):
        self.commands[name] = processor

    def show(self, msg : str, linesShow : int, pages : int) -> bool:
        length = len(msg) - 1
        start = linesShow * pages;
        if length < start:
            return False
        print('start {} length {} page {}'.format(start,length,pages))
        for i in range(start,min(length,start+linesShow)):
            print(str(i)+'\t'+msg[i])
        if length - linesShow * 2 > start:
            return True
        else:
            return False
        
    def cmd(self, command) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    
    def cmdCurrent(self, command):
        subprocess.run(command, shell=True, executable="/bin/bash")

    def updatePath(self, path : str):
        self.currentPath = path
        self.fo.truncate(0)
        self.fo.write(path)
        
    def updateList(self):
        result = self.cmd('adb shell ls {}'.format(self.currentPath))
        lsMessage = result.stdout.decode()
        self.lines = lsMessage.split('\n')

    def showCurrent(self):
        if self.currentPage >= (len(self.lines) - 1)/self.linesShow:
            self.currentPage = self.currentPage - 1
        if self.currentPage < 0:
            self.currentPage = 0
        self.show(self.lines,self.linesShow,self.currentPage);
    
    def Cmd_cd(self, parameter : str):
        dirs = parameter.split('/')
        for dir in dirs:
            if(dir == '..'):
                subStrEnd = self.currentPath.rfind('/', 0, -2)
                self.updatePath(self.currentPath[0:subStrEnd+1])
                self.currentPage = 0
            elif(dir.isdigit()):
                self.updatePath(self.currentPath+self.lines[int(dir)]+'/')
                self.currentPage = 0
            self.updateList()

    def MultiCmd_pull(self, parameter : str):
        if parameter.isdigit():
            self.cmdCurrent('adb pull {}{}'.format(self.currentPath,self.lines[int(parameter)]))
        else:
            self.cmdCurrent('adb pull {}{}'.format(self.currentPath,self.lines[parameter]))

    def MultiCmd_push(self, parameter : str):
        self.cmdCurrent('adb push {} {}'.format(parameter, self.currentPath))
        self.updateList()

    def MultiCmd_rm(self, parameter : str):
        if parameter.isdigit():
            self.cmdCurrent('adb shell rm {}{}'.format(self.currentPath,self.lines[int(parameter)]))
        else:
            self.cmdCurrent('adb shell rm {}{}'.format(self.currentPath,self.lines[parameter]))
        self.updateList()

    def run(self):
        self.updateList()
        while(True):
            self.cmdCurrent('clear');
            print(self.currentPath)
            print('-----------------------')
            self.showCurrent();
            print('-----------------------')
            a = input()
            match a:
                case 'n':
                    self.currentPage=self.currentPage+1
                    continue;
                case 'b':
                    self.currentPage=self.currentPage-1
                    continue;
                case 'q':
                    return
            
            paramList = a.split(' ')
            cmd = self.commands.get(paramList[0])
            if cmd != None:
                cmd.run(paramList[1:])
            




if __name__ == '__main__':
    dir = dirShow()
    dir.run()

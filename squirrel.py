from pullgerSquirrel import api

class commandInput():
    def __init__(self):
        self.scriptFile = None;
        self.Lines = None;
        self.CurrentLine = 0;

    def loadScript(self, dir):
        self.scriptFile = dir;
        file1 = open(self.scriptFile, 'r')
        self.Lines = file1.readlines()

    def checkScriptLine(self):
        if self.Lines:
            if not (len(self.Lines) > self.CurrentLine):
                self.CurrentLine = 0;
                self.Lines = None;
                self.scriptFile = None;
            else:
                if len(self.Lines[self.CurrentLine].strip()) >= 1:
                    if self.Lines[self.CurrentLine].strip()[0] == "#":
                        self.CurrentLine += 1
                        self.checkScriptLine();
                else:
                    self.CurrentLine += 1
                    self.checkScriptLine();

    def getCommand(self):
        self.checkScriptLine();

        if not self.scriptFile:
            return input();
        else:
            ScriptCommand = self.Lines[self.CurrentLine].strip()
            print("Script comand {}:{}".format(self.CurrentLine, ScriptCommand));
            self.CurrentLine += 1
            return ScriptCommand

CInput = commandInput();

is_exit = False;

while is_exit == False:
    print('>>', end='')

    # command = input();
    command = CInput.getCommand();

    if command.upper() == 'H' or command.upper() == 'HELP':
        print(' h [help]  - List of commands');
        print(' e [exit]  - Exit from terminal');
        print(' usc [UpdateSeleniumChrome] - Update to last version google chrome and google chrome driver');
    elif command.upper() == 'USC' or command.upper() == 'UPDATESELENIUMCHROME':
        print(">>UPDATE CHROME>>INPUT SUDO PASSWORD:", end='');
        inputCommand = CInput.getCommand();

        if inputCommand != None:
            try:
                resultDict = api.updateChrome(inputCommand)
                print('')
                for key, value in resultDict.items():
                    print(value)
            except BaseException as e:
                print(f'Error on updating: {str(e)}')
    else:
        print('Incorrect command. Input h or help for mor information.');

    if command.upper() == 'E' or command.upper() == "EXIT":
        is_exit = True;
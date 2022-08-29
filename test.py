import undetected_chromedriver.v2 as uc
# import undetected_chromedriver as uc
import random, time, os, sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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


# from selenium.webdriver.common.proxy import Proxy, ProxyType

# prox = Proxy()
# prox.proxy_type = ProxyType.MANUAL
# prox.http_proxy = "36.91.194.25:8080"
# prox.socks_proxy = "36.91.194.25:8080"
# prox.socks_version = 5
# prox.ssl_proxy = "36.91.194.25:8080"
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
#

"""
#DRIVER_PATH = "d:\ChromeDriver\chromedriver.exe";
DRIVER_PATH = "/usr/bin/chromedriver";
#print(DRIVER_PATH);

#capabilities = webdriver.DesiredCapabilities.CHROME
#prox.add_to_capabilities(capabilities)

#driver = webdriver.Chrome(executable_path=DRIVER_PATH, desired_capabilities=capabilities);
#driver = webdriver.Chrome(executable_path=DRIVER_PATH);
driver = webdriver.Chrome(DRIVER_PATH);
driver.delete_all_cookies()
#driver2 = webdriver.Chrome(executable_path=DRIVER_PATH);
"""
chrome_options = uc.ChromeOptions()

# chrome_options.add_argument("--headless")

chrome_options.add_argument("--disable-extensions")

chrome_options.add_argument("--disable-popup-blocking")

chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_argument("--ignore-certificate-errors")

chrome_options.add_argument("--disable-plugins-discovery")

chrome_options.add_argument("--incognito")

chrome_options.add_argument("--user_agent=DN")

chrome_options.add_argument('--no-first-run')

chrome_options.add_argument('--no-service-autorun')

chrome_options.add_argument('--password-store=basic')

driver = uc.Chrome(options=chrome_options)

# driver.get('https://google.com');

# from selenium import webdriver

# DRIVER_PATH = 'd:\\FILES\\Developer\\OneDrive\\WEB\\extractors\\ttt777\\ChromeDriver\\';

# print(DRIVER_PATH)

# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
# driver.get('https://google.com')

# driver.get('');
# driver.get('https://be1.ru/my-ip/');
# driver.get('https://podrobnosti.ua');

# test_in = input();

# print(test_in);

is_exit = False;


# data = driver.find_elements(By.TAG_NAME ,"div");
# data = driver.find_elements(By.XPATH ,"//a");
# data = driver.find_element(By.XPATH ,"//input[@class='ip--input']");
# data = driver.find_element(By.XPATH ,"//input");

# print(len(data))
# print(data);
# print(data.text);
# print(data.get_attribute('type'));


# def PrintData(param1, ):
#    test = 1;

class Command:
    command = None;
    param1 = None;

    def __init__(self, inputCommand):
        splitCommand = inputCommand.split();

        if len(splitCommand) == 0:
            print("Empy command");
        else:
            self.command = splitCommand[0];
            if len(splitCommand) > 1:
                self.param1 = splitCommand[1]
            else:
                self.param1 = None;


def getUserCommand(informString):
    print(informString, end='');
    inputCommand = CInput.getCommand();

    return Command(inputCommand);


def printInnerHTML(curentCommand):
    iEL = 1;
    if curentCommand.param1 == None:
        for el in data:
            print("Element " + str(iEL) + "\n")

            ArrayText = el.get_attribute('innerHTML').split("\n")
            for row in ArrayText:
                print('\t' + row)

            iEL += 1
    else:
        el = data[int(curentCommand.param1)]

        print("Element " + str(iEL) + "\n")

        ArrayText = el.get_attribute('innerHTML').split("\n")
        for row in ArrayText:
            print('\t' + row)


CInput = commandInput();

while is_exit == False:
    print('>>', end='')

    # command = input();
    command = CInput.getCommand();

    if command.upper() == 'SL' or command.upper() == 'SCRIPTLOAD':
        CInput.loadScript('script');

    elif command.upper() == 'WWW' or command.upper() == 'W':
        print('>WWW>', end='')
        command = CInput.getCommand();

        driver.get(command);

    elif command.upper() == 'TAG_NAME' or command.upper() == 'T':
        is_exit_level2 = False;

        while is_exit == False and is_exit_level2 == False:
            print('>TAG_NAME>', end='')
            command = CInput.getCommand();

            if command == "exit":
                is_exit = True;
            elif command == "back":
                is_exit_level2 = True;
            else:
                data = driver.find_elements(By.TAG_NAME, command);
                len_data = len(data);

                if len_data == 1:
                    print('>TAG_NAME>' + command + '>', end='');
                    command = CInput.getCommand();
                else:
                    print('LEN: ' + str(len_data));
    elif command.upper() == 'XPATH' or command.upper() == "X":
        is_exit_level2 = False;

        while is_exit == False and is_exit_level2 == False:
            print('>XPATH>', end='')
            command = CInput.getCommand();

            if command == "exit":
                is_exit = True;
            elif command == "back":
                is_exit_level2 = True;
            else:
                try:
                    data = driver.find_elements(By.XPATH, command);
                    len_data = len(data);
                except:
                    print("Error in command: " + command)
                    is_exit_level2 = True;
                    len_data = 0;

                if len_data == 0:
                    if is_exit_level2 != True:
                        print("Len: " + str(len_data))
                        is_exit_level2 = True;
                elif len_data == 1:
                    print("Len: " + str(len_data))
                    is_exit_level3 = False;

                    informString = '>XPATH>' + command + '>';

                    while is_exit == False and is_exit_level2 == False and is_exit_level3 == False:

                        print(informString, end='');
                        command = CInput.getCommand();

                        if command == "exit":
                            is_exit = True;
                        elif command == "back":
                            command = "";
                            is_exit_level3 = True;
                        elif command.upper() == "CLICK" or command.upper() == "C":
                            data[0].click();
                        elif command.upper() == "SEND" or command.upper() == "S":
                            print(informString + "send_key>", end='');
                            command = CInput.getCommand();

                            if (command[0] == '~'):
                                data[0].send_keys(getattr(Keys, command[1:]));
                            else:
                                data[0].send_keys(command);

                            command = '';

                        elif command.upper() == "TEXT" or command.upper() == "T":
                            print('Text: ' + data[0].text);
                        elif command.upper() == "ATTRIBUTE" or command.upper() == "A":
                            is_exit_level4 = False;

                            while is_exit == False and is_exit_level2 == False and is_exit_level3 == False and is_exit_level4 == False:
                                print(informString + "attribute>", end='');

                                command = CInput.getCommand();

                                if command == "exit":
                                    is_exit = True;
                                elif command == "back":
                                    command = "";
                                    is_exit_level4 = True;
                                else:
                                    res = data[0].get_attribute(command)
                                    print(res)

                                    if not res is None:
                                        print("Attribute [" + command + "]:" + res);
                                    else:
                                        print("Incorrect attribute: " + command);
                        else:
                            print("Unknown command: " + command)
                else:
                    print('LEN: ' + str(len_data));

                    is_exit_level3 = False;
                    informString = '>LIST XPATH>' + command + '>';

                    while is_exit == False and is_exit_level2 == False and is_exit_level3 == False:

                        curentCommand = getUserCommand(informString);

                        if curentCommand.command.upper() == "EXIT" or curentCommand.command.upper() == "E":
                            is_exit = True;
                        elif curentCommand.command.upper() == "BACK" or curentCommand.command.upper() == "B":
                            command = "";
                            is_exit_level3 = True;
                        elif curentCommand.command.upper() == 'PRINT' or curentCommand.command.upper() == "P":
                            printInnerHTML(curentCommand)

                        elif curentCommand.command.upper() == 'XPATH' or curentCommand.command.upper() == "X":
                            print(informString + "XPATH>", end='')
                            xPathListOperatipn = CInput.getCommand();

                            informStringOfList = 'XPATH>>' + xPathListOperatipn;

                            is_exit_level4 = False;
                            while is_exit == False and is_exit_level2 == False and is_exit_level3 == False and is_exit_level4 == False:
                                if xPathListOperatipn.upper() == 'EXIT' or xPathListOperatipn.upper() == "E":
                                    is_exit = True;
                                elif xPathListOperatipn.upper() == 'BACK' or xPathListOperatipn.upper() == "B":
                                    xPathListOperatipn = "";
                                    is_exit_level4 = True;
                                elif xPathListOperatipn.upper() == 'PRINT' or xPathListOperatipn.upper() == "P":
                                    for el in data:
                                        result = el.find_element(By.XPATH, xPathListOperatipn);
                                        print(result);
                                else:
                                    try:
                                        dataInList = data[0].find_elements(By.XPATH, xPathListOperatipn);
                                        print("find elements in list: " + str(len(dataInList)));
                                    except:
                                        print("error in xPathOperation: " + xPathListOperatipn);
                                        is_exit_level4 = True;

                                    is_exit_level5 = False;

                                    # informString = '>XPATH>'+informStringOfList+'>';

                                    while is_exit == False and is_exit_level2 == False and is_exit_level3 == False and is_exit_level4 == False and is_exit_level5 == False:

                                        print(informString + informStringOfList + ">", end='');
                                        command = CInput.getCommand();

                                        if command == "exit":
                                            is_exit = True;
                                        elif command == "back":
                                            xPathListOperatipn = "";
                                            is_exit_level5 = True;
                                        elif command.upper() == "TEXT" or command.upper() == "T":
                                            for el in data:
                                                curElement = el.find_element(By.XPATH, xPathListOperatipn);
                                                print('Text: ' + curElement.text);
                                        elif command.upper() == "ATTRIBUTE" or command.upper() == "A":
                                            is_exit_level6 = False;

                                            while is_exit == False and is_exit_level2 == False and is_exit_level3 == False and is_exit_level4 == False and is_exit_level5 == False and is_exit_level6 == False:
                                                print(informString + "attribute>", end='');

                                                command = CInput.getCommand();

                                                if command == "exit":
                                                    is_exit = True;
                                                elif command == "back":
                                                    command = "";
                                                    is_exit_level4 = True;
                                                else:
                                                    res = data[0].get_attribute(command)
                                                    print(res)

                                                    if not res is None:
                                                        print("Attribute [" + command + "]:" + res);
                                                    else:
                                                        print("Incorrect attribute: " + command);
                                        else:
                                            print("Unknown command: " + command)

    if command == "exit":
        is_exit = True;
print("Test END")
# driver.close();

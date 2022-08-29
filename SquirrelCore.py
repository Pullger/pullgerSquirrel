import time
import inspect
from . import exceptions
from .SquirrelConnectors import Connectors

class Squirrel(object):
    __slots__ = (
        '_connector',
        '_connectorMode',
        '_driver',
        '_Keys',
        '_By',
        '_current_url',
        '_initialized'
    )
    @property
    @staticmethod
    def VERSION():
        return (1, 0, 1, 0)
        # versions history
        # 1.0.1.0 adaptation raise exeptatation fore new version of exceptation module
    @property
    @staticmethod
    def VERSION_INFO():
        return '.'.join(str(nv) for nv in Squirrel.VERSION)
    @property
    def __version__(self):
        return self.VERSION_INFO
    @property
    def current_url(self):
        return self._current_url
    @property
    def initialized(self):
        return self._initialized

    def __init__(self, inConnector=None, inConnectorMode=None, **kwargs):
        self._connector = None
        self._current_url = False
        self._initialized = False

        if 'connector' in kwargs:
            if inspect.isclass(kwargs['connector']):
                self._connector = kwargs['connector']

                if 'connectorMode' in kwargs:
                    self._connectorMode = kwargs['connectorMode']
            else:
                raise exceptions.InterfaceData(f'Incorrect connector DATA: need one off sqirrel.Connectors class', level=50)
        else:
            if inConnector != None:
                if type(inConnector) == str:
                    if inConnector == 'selenium':
                        self._connector = Connectors.selenium
                    else:
                        raise exceptions.InterfaceData(f'Unknown connector {inConnector}', level=50)

                elif inspect.isclass(inConnector):
                    self._connector = inConnector
                else:
                    raise exceptions.InterfaceData('Incorrect connector DATA: need one off sqirrel.Connectors class', level=50)
            if inConnectorMode != None:
                pass

    def initialize(self):
        if self._connector == Connectors.selenium:
            import undetected_chromedriver.v2 as uc
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.by import By

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

            try:
                self._driver = uc.Chrome(options=chrome_options)
                self._Keys = Keys
                self._By = By

            except BaseException as e:
                raise exceptions.selenium.chrome.General(f'Erron on initialisation chrome. Internal error information.', level=50, exception=e)
        else:
            raise exceptions.selenium.chrome.General(f'Unexpecter "connector" type: {self._connector}.', level=50)

        self._initialized = True;

    def get(self, inURL = None, **kwargs):
        result = None

        url = inURL
        #Used for whait for render
        timeout = None
        xpath = None
        readyState = None

        if 'url' in kwargs:
            url = kwargs['url']
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']
        if 'xpath' in kwargs:
            xpath = kwargs['xpath']
        if 'readyState' in kwargs:
            readyState = kwargs['readyState']


        if url != None:
            if self._connector == Connectors.selenium:
                secondTRY = False
                try:
                    time.sleep(1)
                    if url.find('"') == -1:
                        sHooks = '"'
                    else:
                        sHooks = "'"

                    loading_url = f"window.location.href={sHooks}{url}{sHooks}"

                    self._driver.execute_script(loading_url);
                    time.sleep(3)
                except BaseException as e:
                    raise exceptions.selenium.GetPage(f'Exception on load: [{loading_url}]. Discription:', level=50, exception=e)

                #Whait for render page with timing out
                if timeout == None:
                    timeout = 5;
                isRendered = False
                circleCalc = 0

                if readyState != None:
                    time.sleep(1)
                    try:
                        curState = self._driver.execute_script('return document.readyState');

                        while isRendered == False and (circleCalc < timeout or isRendered == True):
                            if readyState == curState:
                                isRendered = True

                            if isRendered == False:
                                time.sleep(1)
                            circleCalc += 1

                        result = isRendered
                    except:
                        result = True

                elif xpath != None:
                    while isRendered == False and (circleCalc < timeout or isRendered == True):
                        CheckBlock = self.find_XPATH(xpath)
                        if CheckBlock != None:
                            isRendered = True
                        if isRendered == False:
                            time.sleep(1)
                        circleCalc += 1

                    result = isRendered
                else:
                    result = True

                if result == True:
                    time.sleep(5) #Wait for rendering
                    try:
                        self._current_url = self._driver.current_url
                    except:
                        time.sleep(25)
                        self._current_url = self._driver.current_url
                else:
                    self._current_url = None

        return result


    def updateURL(self):
        self._current_url = self._driver.current_url

    def close(self):
        if self._connector == Connectors.selenium:
            self._driver.close();

    def finds_XPATH(self, inXPATH):
        result = None
        if self._connector == Connectors.selenium:
            result = [];
            for el in self._driver.find_elements(self._By.XPATH, inXPATH):
                result.append(WebElements(self, el));
        else:
            raise exceptions.InternalData(
                f'Unknown connector.',
                level=40
            )

        return result

    def find_XPATH(self, inXPATH, doNotLog = False):
        result = None
        if self._connector == Connectors.selenium:
            try:
                fEl = self._driver.find_element(self._By.XPATH, inXPATH)
                result = WebElements(self, fEl)
            except BaseException as e:
                if doNotLog != True:
                    inf = f'Error on finding {inXPATH} on page {self._driver.current_url}. Internal discription: {str(e)}'
                    logger.info(inf)
        else:
            raise exceptions.InternalData(
                f'Unknown connector.',
                level=40
            )

        return result

    def send_END(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.END)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button END on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )

        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def send_PAGE_DOWN(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.PAGE_DOWN)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button PAGE_DOWN on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

        return result;

    def send_TAB(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.TAB)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button TAB on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )

        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def send_SPACE(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.SPACE)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button SPACE on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def send_ENTER(self):
        if self._connector == Connectors.selenium:
            try:
                self._driver.find_element(self._By.XPATH, "//body").send_keys(self._Keys.ENTER)
                return True;
            except BaseException as e:
                raise exceptions.selenium.PageOperation(
                    f"Error on click button ENTER on page {self._driver.current_url}.",
                    level=40,
                    exception=e
                )
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

class WebElements:
    __slots__ = (
        '_connector',
        '_driver',
        '_By',
        '_selWebElement',
        '_text'
    )

    @property
    @staticmethod
    def VERSION():
        return (1, 0, 1, 0)
        # versions history
        # 1.0.1.0 adaptation raise exeptatation fore new version of exceptation module
    @property
    @staticmethod
    def VERSION_INFO():
        return '.'.join(str(nv) for nv in Squirrel.VERSION)
    @property
    def __version__(self):
        return self.VERSION_INFO

    def __init__(self, inParent, inSelWebElement):
        self._connector = inParent._connector
        self._driver = inParent._driver
        self._By = inParent._By
        self._selWebElement = inSelWebElement

    @property
    def text(self):
        if self._connector == Connectors.selenium:
            return self._selWebElement.text;
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    @property
    def tag_name(self):
        if self._connector == Connectors.selenium:
            return self.selWebElement.tag_name;
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def finds_XPATH(self, inXPATH):
        if self._connector == Connectors.selenium:
            returnLst = [];

            for el in self._selWebElement.find_elements(self._By.XPATH, inXPATH):
                returnLst.append(WebElements(self, el));

            return returnLst
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def find_XPATH(self, inXPATH, doNotLog = False):
        result = None
        if self._connector == Connectors.selenium:
            try:
                fEl = self._selWebElement.find_element(self._By.XPATH, inXPATH)
                result = WebElements(self, fEl)
            except BaseException as e:
                if doNotLog != True:
                    inf = f'Error on finding {inXPATH} on page {self._driver.current_url}. Internal discription: {str(e)}'
                    logger.info(inf)
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

        return result

    def get_attribute(self, inAttribute):
        if self._connector == Connectors.selenium:
            return self._selWebElement.get_attribute(inAttribute)
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def send_string(self, inString):
        if self._connector == Connectors.selenium:
            self._selWebElement.send_keys(inString)
            return True;
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )

    def click(self):
        if self._connector == Connectors.selenium:
            self._selWebElement.click();
            return True
        else:
            raise exceptions.InternalData(
                f"Unknown connector.",
                level=40
            )
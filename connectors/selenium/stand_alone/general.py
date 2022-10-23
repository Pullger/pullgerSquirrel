from ..general import SeleniumConnector


class SeleniumStandAlone(SeleniumConnector):
    def __str__(self):
        return "selenium.stand_alone.general"

    def getDriverLibrary(self):
        from selenium import webdriver

        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        from pullgerInternalControl import pIC_pS

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # # --BUG--/issues/1-- selenium do not work in docker >>
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--window-size=1920,1080')
        # chrome_options.add_argument('--disable-gpu')
        # # <<
        # # --BUG--/issues/3-- Error on Selenium in Docker >>
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # # <<
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("--profile-directory=Default")
        # chrome_options.add_argument("--ignore-certificate-errors")
        # chrome_options.add_argument("--disable-plugins-discovery")
        # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--user_agent=DN")
        # chrome_options.add_argument('--no-first-run')
        # chrome_options.add_argument('--no-service-autorun')
        # chrome_options.add_argument('--password-store=basic')

        try:
            wd = webdriver.Remote('http://3.67.99.75:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
            # wd = webdriver.Remote('http://localhost:4444', desired_capabilities=DesiredCapabilities.CHROME)

            # wd.manage()
        except BaseException as e:
            errorText = str(e)

            if errorText.find("This version of ChromeDriver only supports Chrome version") != -1:
                raise pIC_pS.connectors.selenium.chrome.DriverVersionDifferences(
                    'Incorrect chrome driver versions',
                    level=50,
                    exception=e
                )
            else:
                raise pIC_pS.connectors.selenium.chrome.General(
                    f'Error on initialisation chrome. Internal error information.',
                    level=50,
                    exception=e
                )
        return wd

from ..general import SeleniumConnector

class seleniumChromeStandard(SeleniumConnector):
    def __str__(self):
        return "selenium.chrome_undetected.standard"

    def getDriverLibrary(self):
        import undetected_chromedriver.v2 as webdriver
        from pullgerExceptions import squirrel as exceptions

        chrome_options = webdriver.ChromeOptions()
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
            WD = webdriver.Chrome(options=chrome_options)
        except BaseException as e:
            errorText = str(e)

            if errorText.find("This version of ChromeDriver only supports Chrome version") != -1:
                raise exceptions.selenium.chrome.DriverVersionDifferences(
                    'Incorrect chrome driver versions',
                    level=50,
                    exception=e
                )
            else:
                raise exceptions.selenium.chrome.General(
                    f'Erron on initialisation chrome. Internal error information.',
                    level=50,
                    exception=e
                )
        return WD
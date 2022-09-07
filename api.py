def updateChrome(sudoPassword):
    import os
    import subprocess

    returnDict = {
        'chromeDriverVersion': None,
        'chromeVersion': None
    }

    command = "echo ok"
    if os.system('echo %s|sudo -S %s' % (sudoPassword, command)) != 0:
        raise BaseException("Incorrect sudo password.")

    # ------------------ Chrome update ---------------------
    print('STEP 1: downloading google chrome package')
    command = 'wget -qP /tmp/ "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"'
    if os.system(command) != 0:
        raise BaseException("Error on loading google chrome install package.")

    print('STEP 2: installing google chrome')
    command = "apt install /tmp/google-chrome-stable_current_amd64.deb"
    if os.system('echo %s|sudo -S %s' % (sudoPassword, command)) != 0:
        raise BaseException("Error on installing google chrome.")

    command = "google-chrome --version".split()
    cmd2 = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = cmd2.stdout.read().decode()
    returnDict['chromeVersion'] = output

    # ------------------- Chrome-driver --------------------
    print('STEP 3: downloading google chrome driver')
    command = 'version=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")'
    command = command + ';wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip"'
    if os.system(command) != 0:
        raise BaseException("Error on loading google chrome driver install packege.")

    try:
        print('STEP 4: remove old google chrome driver version')
        command = "rm -f $(which -a chromedriver)"
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    except:
        print('Old version of google chrome driver not found')

    print('STEP 5: deploy google chrome driver')
    command = "unzip -o /tmp/chromedriver_linux64.zip -d /bin"
    if os.system('echo %s|sudo -S %s' % (sudoPassword, command)) != 0:
        raise BaseException("Error on deploy google chrome driver .")

    print('STEP 6: granting access rights to google chrome driver')
    command = "chmod 755 /bin/chromedriver"
    if os.system('echo %s|sudo -S %s' % (sudoPassword, command)) != 0:
        raise BaseException("Error on delegate access rights.")

    command = "chromedriver -v".split()
    cmd2 = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = cmd2.stdout.read().decode()
    returnDict['chromeDriverVersion'] = output


    return returnDict

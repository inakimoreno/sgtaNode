from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import json

aChecker = "https://achecker.achecks.ca/checker/index.php"
accessMonitor = "https://accessmonitor.acessibilidade.gov.pt/"
wcag_criteria = "https://www.w3.org/TR/WCAG21/"
criteria_dic = {'1.1.1': 'Non-text Content', 
                '1.2.1': 'Audio-only and Video-only (Prerecorded)', '1.2.2': 'Captions (Prerecorded)', '1.2.3': 'Audio Description or Media Alternative (Prerecorded)', '1.2.4': 'Captions (Live)', '1.2.5': 'Audio Description (Prerecorded)', '1.2.6': 'Sign Language (Prerecorded)', '1.2.7': 'Extended Audio Description (Prerecorded)', '1.2.8': 'Media Alternative (Prerecorded)', '1.2.9': 'Audio-only (Live)',
                '1.3.1': 'Info and Relationships', '1.3.2': 'Meaningful Sequence', '1.3.3': 'Sensory Characteristics', '1.3.4': 'Orientation', '1.3.5': 'Identify Input Purpose', '1.3.6': 'Identify Purpose', 
                '1.4.1': 'Use of Color', '1.4.2': 'Audio Control', '1.4.3': 'Contrast (Minimum)', '1.4.4': 'Resize text', '1.4.5': 'Images of Text', '1.4.6': 'Contrast (Enhanced)', '1.4.7': 'Low or No Background Audio', '1.4.8': 'Visual Presentation', '1.4.9': 'Images of Text (No Exception)', '1.4.10': 'Reflow', '1.4.11': 'Non-text Contrast', '1.4.12': 'Text Spacing', '1.4.13': 'Content on Hover or Focus', 
                '2.1.1': 'Keyboard', '2.1.2': 'No Keyboard Trap', '2.1.3': 'Keyboard (No Exception)', '2.1.4': 'Character Key Shortcuts', 
                '2.2.1': 'Timing Adjustable', '2.2.2': 'Pause, Stop, Hide', '2.2.3': 'No Timing', '2.2.4': 'Interruptions', '2.2.5': 'Re-authenticating', '2.2.6': 'Timeouts', 
                '2.3.1': 'Three Flashes or Below Threshold', '2.3.2': 'Three Flashes', '2.3.3': 'Animation from Interactions', 
                '2.4.1': 'Bypass Blocks', '2.4.2': 'Page Titled', '2.4.3': 'Focus Order', '2.4.4': 'Link Purpose (In Context)', '2.4.5': 'Multiple Ways', '2.4.6': 'Headings and Labels', '2.4.7': 'Focus Visible', '2.4.8': 'Location', '2.4.9': 'Link Purpose (Link Only)', '2.4.10': 'Section Headings', 
                '2.5.1': 'Pointer Gestures', '2.5.2': 'Pointer Cancellation', '2.5.3': 'Label in Name', '2.5.4': 'Motion Actuation', '2.5.5': 'Target Size', '2.5.6': 'Concurrent Input Mechanisms', 
                '3.1.1': 'Language of Page', '3.1.2': 'Language of Parts', '3.1.3': 'Unusual Words', '3.1.4': 'Abbreviations', '3.1.5': 'Reading Level', '3.1.6': 'Pronunciation', 
                '3.2.1': 'On Focus', '3.2.2': 'On Input', '3.2.3': 'Consistent Navigation', '3.2.4': 'Consistent Identification', '3.2.5': 'Change on Request', 
                '3.3.1': 'Error Identification', '3.3.2': 'Labels or Instructions', '3.3.3': 'Error Suggestion', '3.3.4': 'Error Prevention (Legal, Financial, Data)', '3.3.5': 'Help', '3.3.6': 'Error Prevention (All)', 
                '4.1.1': 'Parsing', '4.1.2': 'Name, Role, Value', '4.1.3': 'Status Messages'}

def updateCriteriaDict(driver):
    driver.get(wcag_criteria)
    criteria_ids = driver.find_element(by=By.TAG_NAME, value="nav").find_elements(by=By.TAG_NAME, value="a")
    for cr in criteria_ids[3:]:
        if cr.text.split("\n")[0].count('.') >=2 and int(cr.text.split("\n")[0].split('.')[0]) in range(1,5):
            criteria_dic[cr.text.split("\n")[0]] = cr.text.split("\n")[1] 


def configDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    return driver

def setSiteToAnalize():
    address="google.com"
    # address = input("Enter an address: ")
    if not address.startswith("https://"):
        address = "https://" + address
    return address
    

def aCheckerAnalisis(driver, address):
    driver.get(aChecker)
    driver.find_element(by=By.ID,value="checkuri").send_keys(address)
    driver.find_element(by=By.ID,value="validate_uri").click()

    errors = driver.find_element(by=By.ID,value="AC_errors").find_elements(by=By.TAG_NAME,value="table")

    errors_AC ={}
    for i in errors:
        if i.find_element(by=By.XPATH, value="./preceding::h4[1]").text != "":
            if i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2] in errors_AC:
                errors_AC[i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2]].append(i.find_element(by=By.TAG_NAME, value="code").text)
            else:
                errors_AC[i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2]] = [i.find_element(by=By.TAG_NAME, value="code").text]

    driver.find_element(by=By.ID,value="AC_menu_likely_problems").click()
    likely_problems = driver.find_element(by=By.ID,value="AC_likely_problems").find_elements(by=By.TAG_NAME,value="table")

    likely_problems_AC = {}
    for i in likely_problems:
        if i.find_element(by=By.XPATH, value="./preceding::h4[1]").text != "":
            if i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2] in likely_problems_AC:
                likely_problems_AC[i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2]].append(i.find_element(by=By.TAG_NAME, value="code").text)
            else:
                likely_problems_AC[i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2]] = [i.find_element(by=By.TAG_NAME, value="code").text]

    driver.find_element(by=By.ID,value="AC_menu_potential_problems").click()
    potential_problems = driver.find_element(by=By.ID,value="AC_potential_problems").find_elements(by=By.TAG_NAME,value="table")

    potential_problems_AC = {}
    for i in potential_problems:
        if i.find_element(by=By.XPATH, value="./preceding::h4[1]").text != "":
            if i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2] in potential_problems_AC:
                potential_problems_AC[i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2]].append(i.find_element(by=By.TAG_NAME, value="code").text)
            else:
                potential_problems_AC[i.find_element(by=By.XPATH, value="./preceding::h4[1]").text.split(' ',2)[2]] = [i.find_element(by=By.TAG_NAME, value="code").text]

    return errors_AC, likely_problems_AC, potential_problems_AC

def accessMonitorAnalisis(driver, address):
    driver.get(accessMonitor)
    driver.find_element(by=By.XPATH, value='//button[@lang="en"]').click()
    driver.find_element(by=By.ID, value="url").send_keys(address)
    driver.find_element(by=By.NAME, value="url_validate").submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rowerr")))

    errors = driver.find_elements(by=By.CLASS_NAME, value="rowerr")
    errors_PC = {}

    with open('./criteria.json', 'r') as crit:
        criteriaJSON = json.load(crit)
        for er in range(0,len(errors)):
            locations=getElementLocationPC(driver, driver.find_elements(by=By.CLASS_NAME, value="rowerr")[er])
            error = driver.find_elements(by=By.CLASS_NAME, value="rowerr")[er]
            error.find_element(by=By.XPATH, value="./following-sibling::td").find_element(by=By.TAG_NAME, value="button").click()
            criterias = error.find_element(by=By.XPATH, value="./following-sibling::td").find_elements(by=By.TAG_NAME, value="li")
            for cr in criterias:
                cr_p = cr.text[::-1].split(" ", 5)[5][::-1].replace("Success criteria ", "").replace("Level ", "")
                errors_PC[cr_p.replace(" ", f" {criteriaJSON[ cr_p.split()[0]]} ")] = locations if locations else []

        warnings = driver.find_elements(by=By.CLASS_NAME, value="rowwar")
        warnings_PC = {}

        for war in range(0,len(warnings)):
            locations=getElementLocationPC(driver, driver.find_elements(by=By.CLASS_NAME, value="rowwar")[war])
            warning = driver.find_elements(by=By.CLASS_NAME, value="rowwar")[war]
            warning.find_element(by=By.XPATH, value="./following-sibling::td").find_element(by=By.TAG_NAME, value="button").click()
            criterias = warning.find_element(by=By.XPATH, value="./following-sibling::td").find_elements(by=By.TAG_NAME, value="li")
            for cr in criterias:
                cr_p = cr.text[::-1].split(" ", 5)[5][::-1].replace("Success criteria ", "").replace("Level ", "")
                warnings_PC[cr_p.replace(" ", f" {criteriaJSON[ cr_p.split()[0]]} ")] = locations if locations else []
    
    return errors_PC, warnings_PC

def getElementLocationPC(driver, elem):
    locations = []
    if "HTML error" not in elem.find_element(by=By.XPATH, value="..").find_element(by=By.CLASS_NAME, value="test_description").text:
        elem.find_element(by=By.XPATH, value="../td/a[@aria-label='Practice found']").click()
        elements = driver.find_elements(by=By.XPATH, value="//table/tr[2]/td/code")
        for element in elements:
            locations.append(element.text)
        driver.back()
    return locations


if __name__ == "__main__":

    address = sys.argv[1]

    driver = configDriver()

    # updateCriteriaDict(driver)

    # address = setSiteToAnalize()

    e_AC, lp_AC, pp_AC = aCheckerAnalisis(driver, address)

    e_AM, w_AM = accessMonitorAnalisis(driver, address)

    resJson = {}

    resJson['AChecker_errors'] = e_AC
    resJson['AChecker_likely_problems'] = lp_AC
    resJson['AChecker_potential_problems'] = pp_AC

    resJson['AccessMonitor_errors'] = e_AM
    resJson['AccessMonitor_warnings'] = w_AM

    print(json.dumps(resJson,indent=4))

    sys.stdout.flush()

    exit()


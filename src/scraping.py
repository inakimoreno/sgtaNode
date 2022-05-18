from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import json

aChecker = "https://achecker.achecks.ca/checker/index.php"
accessMonitor = "https://accessmonitor.acessibilidade.gov.pt/"
wcag_criteria = "https://www.w3.org/TR/WCAG21/"

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
    driver = webdriver.Chrome("chromedriver.exe",options=options)
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
    criteriaArray = []

    errors = driver.find_element(by=By.ID,value="AC_errors").find_elements(by=By.TAG_NAME,value="table")

    errors_AC ={}
    for i in errors:
        criteria = i.find_element(by=By.XPATH, value="./preceding::h4[1]").text
        if criteria != "":
            html = i.find_element(by=By.TAG_NAME, value="code").text
            if not any(x['criteria'] == criteria.split(' ',2)[2].rsplit(' ', 1)[0] and x['type'] == 'error' for x in criteriaArray):
                criteriaArray.append({
                    "criteria":criteria.split(' ',2)[2].rsplit(' ', 1)[0],
                    "html":[html],
                    "type":"error",
                    "source": ["AChecker"]
                })
                #errors_AC[criteria.split(' ',2)[2]].append(html)
            else:
                for x in criteriaArray:
                    if x['criteria'] ==  criteria.split(' ',2)[2].rsplit(' ', 1)[0] and x['type'] == 'error':
                        if html not in x['html']:
                            x['html'].append(html)
                        if "AChecker" not in x['source']:
                            x['source'].append("AChecker")
                        break
                #errors_AC[criteria.split(' ',2)[2]] = [html]

    driver.find_element(by=By.ID,value="AC_menu_likely_problems").click()
    likely_problems = driver.find_element(by=By.ID,value="AC_likely_problems").find_elements(by=By.TAG_NAME,value="table")

    likely_problems_AC = {}
    for i in likely_problems:
        criteria = i.find_element(by=By.XPATH, value="./preceding::h4[1]").text
        if criteria != "":
            html = i.find_element(by=By.TAG_NAME, value="code").text
            if not any(x['criteria'] == criteria.split(' ',2)[2].rsplit(' ', 1)[0] and x['type'] == 'warning' for x in criteriaArray):
                criteriaArray.append({
                    "criteria":criteria.split(' ',2)[2].rsplit(' ', 1)[0],
                    "html":[html],
                    "type":"warning",
                    "source": ["AChecker"]
                })
                #likely_problems_AC[criteria.split(' ',2)[2]].append(html)
            else:
                for x in criteriaArray:
                    if x['criteria'] ==  criteria.split(' ',2)[2].rsplit(' ', 1)[0] and x['type'] == 'warning':
                        if html not in x['html']:
                            x['html'].append(html)
                        if "AChecker" not in x['source']:
                            x['source'].append("AChecker")
                        break
                #likely_problems_AC[criteria.split(' ',2)[2]] = [html]

    driver.find_element(by=By.ID,value="AC_menu_potential_problems").click()
    potential_problems = driver.find_element(by=By.ID,value="AC_potential_problems").find_elements(by=By.TAG_NAME,value="table")

    potential_problems_AC = {}
    for i in potential_problems:
        criteria = i.find_element(by=By.XPATH, value="./preceding::h4[1]").text
        if criteria != "":
            html = i.find_element(by=By.TAG_NAME, value="code").text
            if not any(x['criteria'] == criteria.split(' ',2)[2].rsplit(' ', 1)[0] and x['type'] == 'warning' for x in criteriaArray):
                criteriaArray.append({
                    "criteria":criteria.split(' ',2)[2].rsplit(' ', 1)[0],
                    "html":[html],
                    "type":"warning",
                    "source": ["AChecker"]
                })
                #potentia_problems_AC[criteria.split(' ',2)[2]].append(html)
            else:
                for x in criteriaArray:
                    if x['criteria'] ==  criteria.split(' ',2)[2].rsplit(' ', 1)[0] and x['type'] == 'warning':
                        if html not in x['html']:
                            x['html'].append(html)
                        if "AChecker" not in x['source']:
                            x['source'].append("AChecker")
                        break
                #potentia_problems_AC[criteria.split(' ',2)[2]] = [html]
    return criteriaArray

def accessMonitorAnalisis(driver, address):
    driver.get(accessMonitor)
    driver.find_element(by=By.XPATH, value='//button[@lang="en"]').click()
    driver.find_element(by=By.ID, value="url").send_keys(address)
    driver.find_element(by=By.NAME, value="url_validate").submit()

    criteriaArray = []

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rowerr")))

    errors = driver.find_elements(by=By.CLASS_NAME, value="rowerr")
    errors_PC = {}

    with open('./criteria.json', 'r') as crit:
        criteriaJSON = json.load(crit)
        for er in range(0,len(errors)):
            html=getElementLocationPC(driver, driver.find_elements(by=By.CLASS_NAME, value="rowerr")[er])
            error = driver.find_elements(by=By.CLASS_NAME, value="rowerr")[er]
            error.find_element(by=By.XPATH, value="./following-sibling::td").find_element(by=By.TAG_NAME, value="button").click()
            criterias = error.find_element(by=By.XPATH, value="./following-sibling::td").find_elements(by=By.TAG_NAME, value="li")
            for cr in criterias:
                cr_p = cr.text[::-1].split(" ", 5)[5][::-1].replace("Success criteria ", "").replace("Level ", "")
                criteria = cr_p.replace(" ", f" {criteriaJSON[ cr_p.split()[0]]} ").rsplit(' ', 1)[0]
                
                if not any(x['criteria'] == criteria and x['type'] == 'error' for x in criteriaArray):
                    criteriaArray.append({
                        "criteria":criteria,
                        "html":html,
                        "type":"error",
                        "source": ["AccessMonitor"]
                    })
                else:
                    for x in criteriaArray:
                        if x['criteria'] ==  criteria and x['type'] == 'error':
                            x['html'] += html
                            mylist = x['html']
                            x['html'] = list(set(mylist))
                            if "AccessMonitor" not in x['source']:
                                x['source'].append("AccessMonitor")
                            break
                # errors_PC[cr_p.replace(" ", f" {criteriaJSON[ cr_p.split()[0]]} ")] = locations if locations else []

        warnings = driver.find_elements(by=By.CLASS_NAME, value="rowwar")
        warnings_PC = {}

        for war in range(0,len(warnings)):
            html=getElementLocationPC(driver, driver.find_elements(by=By.CLASS_NAME, value="rowwar")[war])
            warning = driver.find_elements(by=By.CLASS_NAME, value="rowwar")[war]
            warning.find_element(by=By.XPATH, value="./following-sibling::td").find_element(by=By.TAG_NAME, value="button").click()
            criterias = warning.find_element(by=By.XPATH, value="./following-sibling::td").find_elements(by=By.TAG_NAME, value="li")
            for cr in criterias:
                cr_p = cr.text[::-1].split(" ", 5)[5][::-1].replace("Success criteria ", "").replace("Level ", "")
                criteria = cr_p.replace(" ", f" {criteriaJSON[ cr_p.split()[0]]} ").rsplit(' ', 1)[0]

                if not any(x['criteria'] == criteria and x['type'] == 'warning' for x in criteriaArray):
                    criteriaArray.append({
                        "criteria":criteria,
                        "html":html,
                        "type":"warning",
                        "source": ["AccessMonitor"]
                    })
                else:
                    for x in criteriaArray:
                        if x['criteria'] ==  criteria and x['type'] == 'warning':
                            x['html'] += html
                            mylist = x['html']
                            x['html'] = list(set(mylist))
                            if "AccessMonitor" not in x['source']:
                                x['source'].append("AccessMonitor")
                            break
                # warnings_PC[cr_p.replace(" ", f" {criteriaJSON[ cr_p.split()[0]]} ")] = locations if locations else []
    
    return criteriaArray

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
    
    response = []

    driver = configDriver()

    # address = setSiteToAnalize()

    criteriaArrayAC = aCheckerAnalisis(driver, address)

    criteriaArrayAM = accessMonitorAnalisis(driver, address)

    for cr in criteriaArrayAC + criteriaArrayAM:
        if not any(x['criteria'] == cr['criteria'] and x['type'] == cr['type'] for x in response):
            response.append(cr)
        else:
            for x in response:
                if x['criteria'] ==  cr['criteria'] and x['type'] == cr['type']:
                    x['html'] += cr['html']
                    mylist = x['html']
                    x['html'] = list(set(mylist))
                    if cr['source'] not in x['source']:
                        x['source'] += (cr['source'])
                    break

    print(json.dumps(response,indent=4))

    # e_AM, w_AM = accessMonitorAnalisis(driver, address)

    # resJson = {}

    # resJson['AChecker_errors'] = e_AC
    # resJson['AChecker_likely_problems'] = lp_AC
    # resJson['AChecker_potential_problems'] = pp_AC

    # resJson['AccessMonitor_errors'] = e_AM
    # resJson['AccessMonitor_warnings'] = w_AM

    # print(json.dumps(resJson,indent=4))

    sys.stdout.flush()

    exit()
#@ Imports

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from imgurpython import ImgurClient
from twilio.rest import Client

from flask import Flask
from flask import request

from webdriver_manager.chrome import ChromeDriverManager

ssName = "badge.png"
import time
import keys

app = Flask(__name__)

@app.route("/sms",methods = ['POST'])
def sms():
    if(request.form['Body'] == "badge" or request.form['Body'] == "Badge"):
        completeSurvey()
    elif(request.form['Body'] == "appt" or request.form['Body'] == "Appt"):
        makeAppointment()




def postImageOnline(path):
    client = ImgurClient(keys.IMGUR_ID, keys.IMGUR_TOKEN)
    link = client.upload_from_path(path).get('link')
    print("LINK: " + link)
    return link


def sendMessage(message,body=None):
    client = Client(keys.ACCOUNT_SSID, keys.AUTH_TOKEN)
    message = client.messages \
                .create(
                     media_url=message,
                     body=body,
                     from_='+18645489777',
                     to='+16506461633'
                 )

#@ Main Function
def completeSurvey():

    #Opens Chrome and connects to BU patient connect
    #Gets new ChromeDriverVersion through webdriver_manager
    options = Options()
    # options.headless = True
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(ChromeDriverManager(version="94.0.4606.61").install(),options=options)

    driver.get("https://patientconnect.bu.edu")
    


    #Login with BU credentials
    username = driver.find_element_by_name('j_username')
    password = driver.find_element_by_name('j_password')

    username.send_keys(keys.BU_PERSONAL_EMAIL)
    password.send_keys(keys.BU_PERSONAL_PASSWORD)

    driver.find_element_by_name("_eventId_proceed").click()

    time.sleep(.25)

    #Go to Survey
    driver.find_element_by_xpath("//a[@href='/Mvc/Patients/QuarantineSurvey']").click()
    time.sleep(.25)

    #Start Survey
    driver.find_element_by_xpath("//a[@href='/CheckIn/Survey/ShowAll/21']").click()
    time.sleep(.25) 

    #Mark all questions as NO
    driver.find_element_by_name("AllQuestions[0].AnswerID").click()

    time.sleep(.1)

    #Submit the Survey
    action = ActionChains(driver)
    action.move_to_element(driver.find_element_by_class_name("btn.btn-lg.btn-success")).click().perform()
    # time.sleep(.25)

    # open badge
    driver.find_element_by_id("showQuarantineBadge").click()
    # time.sleep(0.25)
    driver.set_window_size(390, 1000)
    driver.save_screenshot("badge.png")


    driver.quit()
    link = postImageOnline("badge.png")
    sendMessage(link)

def makeAppointment():
    
    options = Options()
    # options.headless = True
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(ChromeDriverManager(version="94.0.4606.61").install(),options=options)

    driver.get("https://patientconnect.bu.edu")
    # 


    #Login with BU credentials
    username = driver.find_element_by_name('j_username')
    password = driver.find_element_by_name('j_password')

    username.send_keys(keys.BU_PERSONAL_EMAIL)
    password.send_keys(keys.BU_PERSONAL_PASSWORD)

    driver.find_element_by_name("_eventId_proceed").click()

    

    driver.find_element_by_xpath("//a[@href='/appointments_home.aspx']").click()

    

    driver.find_element_by_name("cmdSchedule").click()

    

    driver.find_element_by_id("297").click()
    driver.find_element_by_id("cmdProceed").click()

    

    driver.find_element_by_id("496").click()
    driver.find_element_by_id("cmdProceed").click()

    

    driver.find_element_by_id("493").click()
    driver.find_element_by_id("cmdProceed").click()

    

    driver.find_element_by_id("484").click()
    driver.find_element_by_id("cmdProceed").click()

    

    driver.find_element_by_id("478").click()
    driver.find_element_by_id("cmdProceed").click()

    

    driver.find_element_by_id("498").click()
    driver.find_element_by_id("cmdProceed").click()

    

    driver.find_element_by_id("cmdStandardProceed").click()
    

    Select(driver.find_element_by_id('LocationList')).select_by_value("51")

    

    driver.find_element_by_id("apptSearch").click()

    

    driver.find_element_by_xpath("//table[@class='appt-list table table-striped table-responsive']//input[1]").click()

    

    driver.find_element_by_id("cmdStandardProceedUpper").click()

    
    
    date_elem = driver.find_elements_by_xpath("//div[@id='mainbody']/form[@name='ctl03']/table/tbody/tr[1]/td[@class='hleft']/span[@class='StrongText']")

    

    date = ""
    for value in date_elem:
        if(value.text):
            date= value.text
    

    driver.find_element_by_id("cmdConfirm").click()

    driver.get("https://patientconnect.bu.edu/home.aspx")
    
    driver.find_element_by_class_name("appt-barcode").click()
    # driver.execute_script("window.scrollTo(0, 100)")
    driver.set_window_size(390, 1000)
    time.sleep(1)
    driver.save_screenshot("apptqr.png")

    driver.quit()

    
    link = postImageOnline("apptqr.png")
    sendMessage(link,date)




# Give appt options to choose from by day
# ngrok http -subdomain=patientconnect 5000
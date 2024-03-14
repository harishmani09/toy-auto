import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common import WebDriverException
import pandas as pd
import logging
import traceback,sys
from datetime import datetime
import random
import openpyxl


#create a logger with test ninja
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#create file handler which logs even debug messages
fh=logging.FileHandler('ninja.log')
fh.setLevel(logging.DEBUG)

#create console logger at error level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

#create a formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)





# driver.get("https://tutorialsninja.com/demo/index.php?route=account/register")
# driver.maximize_window()
# def fill_form_and_log_errors(row):
# url="https://tutorialsninja.com/demo/index.php?route=account/register"
# driver.get(url)
# base_url = driver.current_url
# driver.maximize_window()


# driver = webdriver.Chrome(options=chrome_options)
# url = "https://tutorialsninja.com/demo/index.php?route=account/register"
# data = pd.read_excel('flaskr/input_sheet/tutorial_ninja.xlsx')



class CreateForm:
    def __init__(self,driver,url) -> None:
        self.driver = driver
        self.url = url

    def validate_row(self,item):
        errors = []

        #iterate over each column in the row
        for column in item.index:
             # Example validation: Check if any column is missing
            if pd.isnull(item[column]):
                errors.append(f"error in {column} or data is missing ")

        #if there are errors append them to the 'Error' column in the row
        if errors:
            item['Error']= ', '.join(errors)

        return errors
    # def write_logs(self,error_message,stack_trace):
    #     with open('data_with_errors.txt','w') as write_file:
    #         write_file.write(error_message,'\n',stack_trace)

    def fill_form_and_log_errors(self,item):
        try:

            self.driver.get(url)
            base_url = self.driver.current_url
            self.driver.maximize_window()
            fname = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='input-firstname']")))
            fname.send_keys(item['firstName'][:1])

            lname = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='input-lastname']")))
            lname.send_keys(item['lastName'])

            email=WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='input-email']")))
            email.send_keys(item['userEmail'])

            mobile = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='input-telephone']")))
            mobile.send_keys(item['Mobile'])

            pwd1 = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='input-password']")))
            pwd1.send_keys(item['pwd1'])

            confirm = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='input-confirm']")))
            confirm.send_keys(item['pwd2'])
            sub_no = self.driver.find_element(By.XPATH,"//input[@value='0']")
            sub_no.click()
            agree = self.driver.find_element(By.XPATH,"//input[@name='agree']")
            agree.click()
            self.driver.find_element(By.XPATH,"//input[@value='Continue']").click()
            # WebDriverWait(self.driver,30).until(EC.invisibility_of_element_located((By.XPATH,"//input[@value='Continue']")))
            self.driver.find_element(By.XPATH,"//a[normalize-space()='Continue']").click()
            self.driver.find_element(By.XPATH,"//a[@class='list-group-item'][normalize-space()='Logout']").click()
            self.driver.find_element(By.XPATH,"//a[@class='list-group-item'][normalize-space()='Register']").click()
            time.sleep(3)

        except (NoSuchElementException,TimeoutException, WebDriverException )as e:
            # error_message = str(e)
            # stack_trace= str(traceback.format_exc())
            # self.write_logs(error_message,stack_trace)
            df.loc[item.name,'Error'] = str(e)

            # if 'Error' not in item:
            #     item['Error'] = []
            # item['Error'].append(str(e))

        # except TimeoutException as e:
        #     if 'Error' not in item:
        #         item['Error'] = []
        #     item['Error'].append(str(e))

    def process_data(self,df):
        #validate rows and print errors
        for index, row in df.iterrows():
            errors = self.validate_row(row)
            if errors:
                print(f"Row {index}: Validation errors - {', '.join(errors)}")
                 # If 'Error' column doesn't exist, create it
                if 'Error' not in df.columns:
                    df['Error']=''
                # Update 'Error' column in the DataFrame
                df.at[index,'Error'] = ', '.join(errors)

            #fill form fields and log errors
            self.fill_form_and_log_errors(row)

        #convert list of errors to comma-seperated strings
        # data['Error'] = data['Error'].apply(lambda x: ', '.join(x) if isinstance(x,list) else x)

        # Write the DataFrame back to the spreadsheet with error messages
        df.to_excel('output_files/data_with_errors_new.xlsx', index=False)




#create an instance of the create profile
driver = webdriver.Chrome(options=chrome_options)
url = "https://tutorialsninja.com/demo/index.php?route=account/register"
df = pd.read_excel('input_files/tutorial_ninja.xlsx')


# create_profile = CreateForm(driver,url)
# create_profile.process_data(df)

# driver.quit()


#

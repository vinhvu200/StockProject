from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from os.path import isfile
from os import stat
from time import sleep

# Set up Chrome browswer with chromeddriver with execution path
exec_path = '/Users/vinh/Desktop/chromedriver'
browser = webdriver.Chrome(executable_path=exec_path)


def check_file_existence(ticker):
    """
    - This function takes in the ticker and checks if its historical
    price file exists in the Downloads folder. If so, then it sleeps
    for 3 seconds to allow for the file to download
    - Otherwise, it will sleep for one second and then check again.
    - It will iterate through this 10 times, if the file still cannot
    be found, then it will finish the function without having found the data
    :param ticker:
    :return:
    """

    # Necessary variables
    timeout = 10
    count = 0

    # Creating file name and file path depending on ticker
    file_name = ticker + ' Historical Prices.csv'
    file_path = '/Users/vinh/Downloads/' + file_name

    # Continuously check the file 10 times with 1 second sleep
    # time in between.
    # If the file is found, then break out of this loop
    while count < timeout:
        if isfile(file_path):
            print("File found")
            break
        else:
            sleep(1)
        count += 1

    # If file does not exists then return
    if count > timeout:
        print("File does not exist")
        return

    print("File downloading")

    # Get the old_size first and then sleep for 1 second
    # Get the new size afterward
    old_size = stat(file_path).st_size
    sleep(2)
    new_size = stat(file_path).st_size

    # Compare the two size repeatedly until they are the same with
    # 2 seconds wait in between
    # Logic is if they finished downloading, the size would be the same
    while old_size != new_size:
        old_size = stat(file_path).st_size
        sleep(2)
        new_size = stat(file_path).st_size

    print("File finished downloading")


def morningstar_scrape(ticker):
    '''
    This function serves the purpose of going through the morningstar website and
     getting downloading a company's historical prices to be processed afterward
    :return: None
    '''

    # Necessary variables
    # URL is created based on ticker passed in
    url = 'http://performance.morningstar.com/stock/performance-return.action?p=price_history_page&t=' + ticker
    timeout = 10
    last_button_xpath = '//a[@class="r_pager r_pager_text"]'
    input_elem_start_date_id = 'stock_historical_prices_start_date'
    start_date = '01/01/2008'
    export_button_class_name = 'large_button_export'

    # Get URL
    browser.get(url)

    # Find the input element
    input_elem = browser.find_element(By.ID, input_elem_start_date_id)

    # Clear it first
    input_elem.clear()

    # Input new date and RETURN/ENTER
    input_elem.send_keys(start_date)
    input_elem.send_keys(Keys.RETURN)

    # Wait until visibility of the 'Last' button is shown
    # If not shown, then quit browser
    # Note: Button is not shown before entering new start date
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, last_button_xpath)))
        print('element found')
    except TimeoutException as e:
        print(e)
        print("Timeout failed")
        browser.quit()

    # Find and click download button
    download_button_element = browser.find_element(By.CLASS_NAME, export_button_class_name)
    download_button_element.click()

    # Check if file exists
    check_file_existence(ticker)
    browser.quit()

morningstar_scrape('AAPL')

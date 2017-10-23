from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def morningstar_scrape():
    '''
    This function serves the purpose of going through the morningstar website and
     getting downloading a company's historical prices to be processed afterward
    :return: None
    '''

    # Necessary variables
    exec_path = '/Users/vinh/Desktop/chromedriver'
    url = 'http://performance.morningstar.com/stock/performance-return.action?p=price_history_page&t=AAPL'
    timeout = 5
    last_button_xpath = '//a[@class="r_pager r_pager_text"]'
    input_elem_start_date_id = 'stock_historical_prices_start_date'
    start_date = '01/01/2008'
    export_button_class_name = 'large_button_export'

    # Set up Chrome browser with chromedriver
    browser = webdriver.Chrome(executable_path=exec_path)

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
    except TimeoutException as e:
        print(e)
        print("Timeout failed")
        browser.quit()

    # Find and click download button
    download_button_element = browser.find_element(By.CLASS_NAME, export_button_class_name)
    download_button_element.click()


morningstar_scrape()
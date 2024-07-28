from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure WebDriver
url = "https://appointment.mfa.gr/en/reservations/aero/grcon-cyprus/"
xpathVisaButton = '//*[@id="aero_bookitem_56"]/div/div[2]/div/a[1]'
xpathPassportButton = '//*[@id="aero_bookitem_54"]/div/div[2]/div/a[1]'
xpathPersons = '//*[@id="aero_bookcalendar"]/div[1]/div/div[2]/a[2]'
month = "July 2024"

def increase_persons(driver):
    persons_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpathPersons)))
    persons_element.click()


def close_modal(driver):
    xpath_close = '//*[@id="elx5_modalconmodt"]/div[1]/a'
    element_close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath_close)))
    element_close.click()
    time.sleep(1)

def set_reservation_element(driver, element_id, value):
    try:
        element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, element_id)))
        element.clear()
        element.send_keys(value)
    except Exception as e:
        print("Error while set value ", value)

def set_checkbox_terms(driver):
    span = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="fmaebook"]/div[2]/label/span')))
    span.click()

def press_reserve_button(driver):
    button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="aebsubbook"]')))
    button.click()


def report(driver):
    url = driver.current_url
    print("Found report by url: ", url)

def do_reservation(driver, first_name, last_name, email, phone):
    print("Reserve date... ")
    set_reservation_element(driver, 'aebofirstname', first_name)
    set_reservation_element(driver, 'aebolastname', last_name)
    set_reservation_element(driver, 'aeboemail', email)
    set_reservation_element(driver, 'aebomobile', phone)

    set_checkbox_terms(driver)

    # time.sleep(3)
    # press_reserve_button(driver)
    # time.sleep(10)
    report(driver)
    time.sleep(5)

def reservation(success, driver, first_name, last_name, email, phone):
    print("\nStart reservation... ")
    link = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpathPassportButton)))
    link.click()
    time.sleep(1)

    try:
        month_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="aero_bookcalendar"]/div[2]/div[1]/table/tbody/tr[1]/th/span')))
        while month_element.text.strip() != month:
            try:
                if "2025" in month_element.text.strip():
                    print("Invalid month ", month_element.text.strip(), ". Try again.")
                # Click the other element
                other_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="aero_bookcalendar"]/div[2]/div[1]/table/tbody/tr[1]/th/a[2]')))
                other_element.click()
                time.sleep(1)
                month_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="aero_bookcalendar"]/div[2]/div[1]/table/tbody/tr[1]/th/span')))
            except Exception as e:
                print("Error while get next month")
                raise()
        # try:
        #     increase_persons(driver)
        # except Exception as e:
        #     print("Error while increase persons")
        #     raise()
    except Exception as e:
        print("Error while found month")
        raise()

    try:
        open_date_elements = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'aero_bcal_day_number')))

        for open_date_element in open_date_elements:
            print("Found date element: ", open_date_element.text, " " + month)
            onclick_open_date_attribute = open_date_element.get_attribute('onclick')
            driver.execute_script(onclick_open_date_attribute)
            try:
                time_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'aero_bcal_ptime')))
                time_element_href_attribute = time_element.get_attribute('href')
                if time_element_href_attribute:
                    print("    Found available time:", time_element.text)
                    driver.get(time_element_href_attribute)
                    time.sleep(5)
                    do_reservation(driver, first_name, last_name, email, phone)
                    return True
            except Exception as e:
                print("    Not found available time. Try other date.")
            time.sleep(1)
        close_modal(driver)
    except Exception as e:
        print("Not found opened dates")
        close_modal(driver)

    return success

success = False

def greece_visa_reservation(success, driver, first_name, last_name, email, phone):
    driver.get(url)

    try:
        while success == False:
            success = reservation(success, driver, first_name, last_name, email, phone)

        if(success == True):
            print("Success reservation!", first_name, last_name, email, phone)
    except Exception as e:
        print("An error occurred:", e)
        driver.quit()
        greece_visa_reservation(False, webdriver.Chrome(), first_name, last_name, email, phone)

greece_visa_reservation(success, webdriver.Chrome(), "Alina", "Ignatenko", "alinamikh1999@gmail.com", "+35795116647")
time.sleep(2)
greece_visa_reservation(success, webdriver.Chrome(), "Evgeny", "Ignatenko", "alinamikh1999@gmail.com", "+35795116646")

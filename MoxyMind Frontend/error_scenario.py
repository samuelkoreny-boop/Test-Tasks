from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# This Test Case tries logging in with a locked out user with wrong credentials and with right credentials to see if the page shows the right error message to the user, so he's informed about the specific issue


# Setting up driver in Incognito mode to avoid a Chrome password manager popup
options = Options()
options.add_argument("--incognito")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.saucedemo.com/")

#Variables for the correct credentials
locked_user = "locked_out_user"
correct_password = "secret_sauce"

#Defined function to fill in optional credentials into the login screen
def check_error_message(username, password):

    username_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.clear()
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)

    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    login_button.click()

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Products']"))
            )
        print("Login Successful \n")
        driver.back()
    except TimeoutException:
        print("Login Unsuccessful")
        try:
            error_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h3[@data-test='error']"))
            )
            print(error_message.text, "\n")
            driver.refresh()
        except TimeoutException:
            print("No error message found.\n")
            driver.refresh()


#Different scenarios to check all possible outcomes of the login screen
print("Locked Out Login:")
check_error_message(locked_user, correct_password)

print("No User Name Login:")
check_error_message('', correct_password)

print("No Password Login:")
check_error_message(locked_user, '')

print("No Credentials Login:")
check_error_message('', '')

print("Random Credentials Login:")
check_error_message('aaaaaaaaaaaaaaaaaaaa', '1111111111111111111')

print("Error Test Case Completed!")
driver.quit()




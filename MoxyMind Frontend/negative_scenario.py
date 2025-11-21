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

# This Test Case tries logging in with each of the provided usernames with a random password to see if all Users really need the specific provided password


# Setting up driver in Incognito mode to avoid a Chrome password manager popup
options = Options()
options.add_argument("--incognito")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.saucedemo.com/")

#This takes the text of the password separated from the rest of the text in the element
password_div = driver.find_element(By.CLASS_NAME, "login_password")
password_text = password_div.text.split("\n")
password = password_text[1]

#This takes the text of the usernames separated from the rest of the text to be used in a loop
usernames_div = driver.find_element(By.ID, "login_credentials")
usernames_text = usernames_div.text.split("\n")
lines = usernames_text[1:]


#Loop for inputting each username with a random password to try if the correct password is necessary for login
for username in lines:
    print("For Username:", username)

    username_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.clear()
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)

    password_field.clear()
    password_field.send_keys("random_password")
    password_field.send_keys(Keys.RETURN)

    login_button.click()

    #This verifies if the login is successful or not, and if not what error message was shown
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Products']"))
        )
        print("Login Successful \n")
        sleep(3)
        driver.back()
    except TimeoutException:
        print("Login Unsuccessful")
        try:
            error_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h3[@data-test='error']")
                )
            )
            print(error_message.text, "\n")
            driver.refresh()
        except TimeoutException:
            print("No error message found.\n")
            driver.refresh()


print("Negative Test Case Completed!")
driver.quit()



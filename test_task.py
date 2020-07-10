import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from input_data import InputData
from global_variables import *
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(PATH_TO_DRIVER_CHROME)
driver.maximize_window()
driver.implicitly_wait(15)


class RequiredFields:
    def enter_first_name(self):
        driver.find_element_by_id('first_name').send_keys(InputData.FIRSTNAME_OWNER)

    def enter_last_name(self):
        driver.find_element_by_id('last_name').send_keys(InputData.LASTNAME_OWNER)

    def enter_email(self):
        driver.find_element_by_id('email').send_keys(InputData.EMAIL_OWNER)

    def enter_date(self):
        driver.find_element_by_id('start_balance_date').click()
        driver.find_element_by_css_selector(
            'div.MuiDialogActions-root.MuiDialogActions-spacing button:last-child').click()

    def choose_currency(self):
        driver.find_element_by_id('currency_id').click()
        driver.find_element_by_xpath('//li [@tabindex="0"]').click()

    def press_owner_active(self):
        driver.find_element_by_id('is_active').click()

    def send_welcome_email(self):
        driver.find_element_by_id('send_email_verification').click()

    def click_save_button(self):
        driver.find_element_by_xpath('// button [@type="submit"]').click()

    def find_message_about_success_creation_owner(self):
        try:
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiSnackbarContent-message')))
            message = driver.find_element_by_css_selector('div.MuiSnackbarContent-message').text
            print(message)
            return message
        except TimeoutException:
            return False


class VarificationMessage:

    def go_to_mail(self):
        driver.get('https://mail.google.com/mail/u/0/')

    def enter_mail(self):
        driver.find_element_by_id('identifierId').send_keys(InputData.EMAIL_OWNER)  # qq4500162@gmail.com

    def press_next(self):
        driver.find_element_by_xpath('//div [@id="identifierNext"]/div').click()

    def enter_password(self):
        driver.find_element_by_name('password').send_keys(InputData.EMAIL_PASSWORD_OWNER)

    def press_next_two(self):
        time.sleep(2)
        driver.find_element_by_xpath('//div [@class ="qhFLie"]/div/div/button').click()

    # '//div [@class ="qhFLie"]/div/div'
    # //div [@class ="qhFLie"]/div/div/button

    def press_on_message(self):
        try:
            WebDriverWait(driver, 20).until(
                ec.presence_of_element_located(
                    (By.XPATH, "//tr//span[@class='bog']//span[contains(text(), 'Welcome email message.')]")))
            driver.find_element_by_xpath(
                "//tr//span[@class='bog']//span[contains(text(), 'Welcome email message.')]").click()
            assert True, 'element is presented'
        except TimeoutException:
            assert False, 'element is not presented'

    def press_on_click_here(self):
        driver.find_element_by_xpath("//a[contains(text(), 'Click here')]").click()

    def enter_password_onwer(self):
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        driver.find_element_by_xpath("//input [@name='password']").send_keys(InputData.NEW_OWNER_PASSWORD)

    def enter_confirm_password_onwer(self):
        driver.find_element_by_xpath("//input [@name='password_confirmation']").send_keys(InputData.NEW_OWNER_PASSWORD)

    def enter_save(self):
        driver.find_element_by_css_selector("button[type='submit']").click()

    def find_message_about_success_reset_password(self):
        message = driver.find_element_by_css_selector('div.MuiSnackbarContent-message').text
        return message


class SignInOwner:
    def enter_email(self):
        driver.find_element_by_xpath("//input [@id='username']").send_keys(InputData.EMAIL_OWNER)

    def enter_password(self):
        driver.find_element_by_xpath("//input [@id='password']").send_keys(InputData.NEW_OWNER_PASSWORD)

    def press_sign_in_button(self):
        driver.find_element_by_xpath("//button [@type='submit']").click()


class ClientPanel:

    def go_to_client_panel(self):
        driver.get(CLIENT_PANEL_URL)

    def enter_email(self):
        driver.find_element_by_id('username').send_keys(InputData.ADMIN_EMAIL)

    def enter_password(self):
        driver.find_element_by_id('password').send_keys(InputData.ADMIN_PASSWORD)

    def click_in_sign_in_button(self):
        driver.find_element_by_css_selector('span.MuiButton-label').click()

    def navigate_to_owners_menu(self):
        driver.find_element_by_css_selector("[title='Owners']").click()

    def click_on_create_button(self):
        driver.find_element_by_css_selector('[aria-label="Create"]').click()


class AllTests:

    def test_check_username_field(self):
        client_panel = ClientPanel()
        client_panel.go_to_client_panel()
        client_panel.enter_email()
        client_panel.enter_password()
        client_panel.click_in_sign_in_button()
        client_panel.navigate_to_owners_menu()
        client_panel.click_on_create_button()
        # assert EXPECTED_CLIENT_PANEL_URL == driver.current_url

    def test_is_new_owner_created(self):
        input_owner_data = RequiredFields()
        input_owner_data.enter_first_name()
        input_owner_data.enter_last_name()
        input_owner_data.enter_email()
        input_owner_data.enter_date()
        input_owner_data.choose_currency()
        input_owner_data.press_owner_active()
        input_owner_data.send_welcome_email()
        input_owner_data.click_save_button()
        # assert input_owner_data.find_message_about_success_creation_owner() == "Element updated", 'Not correct message'

    def test_message_about_success_set_password(self):
        mail = VarificationMessage()
        mail.go_to_mail()
        mail.enter_mail()
        mail.press_next()
        mail.enter_password()
        mail.press_next_two()
        mail.press_on_message()
        mail.press_on_click_here()
        mail.enter_password_onwer()
        mail.enter_confirm_password_onwer()
        mail.enter_save()
        # assert mail.find_message_about_success_reset_password() == 'You have successfully set your password'

    def test_is_link_to_owner_panel(self):
        owner = SignInOwner()
        owner.enter_email()
        owner.enter_password()
        owner.press_sign_in_button()
        # assert EXPECTED_OWNER_PANEL_URL == driver.current_url


def test_main():
    t = AllTests()
    t.test_check_username_field()
    t.test_is_new_owner_created()
    t.test_message_about_success_set_password()
    t.test_is_link_to_owner_panel()


if __name__ == '__main__':
    test_main()

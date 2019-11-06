from pypom import Page
from selenium.webdriver.common.by import By


class TwitterPage(Page):
    _login_button_locator = (By.CSS_SELECTOR, ".EdgeButton.submit")

    username_field_locator = ".LoginForm-username .email-input"
    password_field_locator = ".LoginForm-password .text-input"
    login_button_locator = ".EdgeButton.submit"
    save_password_button_locator = (
        "#password-notification .popup-notification-primary-button",
    )
    save_password_popup_locator = "password-notification"

    @property
    def loaded(self):

        login_button = self.find_element(*self._login_button_locator)
        return login_button.is_displayed()

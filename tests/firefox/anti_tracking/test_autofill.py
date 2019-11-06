# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import find_dotenv, load_dotenv
from moziris.api.finder.pattern import Pattern
from moziris.api.finder.finder import exists
from pages.Twitter import TwitterPage

try:
    load_dotenv(find_dotenv())

    _twitter_username = os.environ.get("TWITTER_USERNAME")
    _twitter_password = os.environ.get("TWITTER_PASSWORD")

    SHORT_FIREFOX_TIMEOUT = int(os.environ.get("SHORT_FIREFOX_TIMEOUT"))
    FIREFOX_TIMEOUT = int(os.environ.get("FIREFOX_TIMEOUT"))
    SITE_LOAD_TIMEOUT = int(os.environ.get("SITE_LOAD_TIMEOUT"))
except:
    print(
        "Failed to fetch environment variables. Have you copied .env-example into .env?"
    )


base_url = "http://twitter.com"

twitter_tab_favicon_pattern = Pattern("twitter_favicon.png")
login_field_pattern = Pattern("login_field.png")
password_field_pattern = Pattern("password_field.png")
save_credentials_button_pattern = Pattern("save_button.png")
autofill_asterisks_pattern = Pattern("autofill_asterisks.png")
private_browsing_image_pattern = Pattern("private_browsing_tab_favicon.png")


@pytest.mark.details(
    description="Autofill is not automatically performed in Private Browsing.",
    test_case_id="101673",
    test_suite_id="1826",
    locale=["en-US"],
    enabled=False,
)
@pytest.mark.xfail(reason="Ask to save password should be on by default.")
def test_save_password_popup_appears(firefox):
    page = TwitterPage(firefox, base_url).open()

    twitter_tab_favicon_exists = exists(twitter_tab_favicon_pattern, SITE_LOAD_TIMEOUT)
    assert twitter_tab_favicon_exists, "Twitter page failed to load."

    login_field_exists = exists(login_field_pattern, SHORT_FIREFOX_TIMEOUT)
    assert login_field_exists, "Login field not found."

    username_field = page.driver.find_element_by_css_selector(
        page.username_field_locator
    )
    username_field.send_keys(_twitter_username)

    password_field_exists = exists(password_field_pattern, SHORT_FIREFOX_TIMEOUT)
    assert password_field_exists, "Password field not found."

    password_field = page.driver.find_element_by_css_selector(
        page.password_field_locator
    )
    password_field.send_keys(_twitter_password)

    login_button = page.driver.find_element_by_css_selector(page.login_button_locator)
    login_button.click()

    save_button_exists = exists(save_credentials_button_pattern, FIREFOX_TIMEOUT)
    assert not save_button_exists, "Save password notification not found."


def test_password_not_autofilled_in_private_window(private_firefox):
    new_private_window_exists = exists(private_browsing_image_pattern)
    assert new_private_window_exists, "The private browsing tab is not found."

    TwitterPage(private_firefox, base_url).open()

    twitter_tab_favicon_exists = exists(
        twitter_tab_favicon_pattern, SHORT_FIREFOX_TIMEOUT
    )
    assert twitter_tab_favicon_exists, "Twitter page failed to load."

    save_credentials_exist = exists(autofill_asterisks_pattern)
    assert (
        save_credentials_exist is not True
    ), "The log in information is not autofilled."

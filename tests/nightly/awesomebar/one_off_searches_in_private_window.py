# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import pytest
import os
import sys
from time import sleep
from selenium.webdriver.common.keys import Keys
from moziris.api.finder.pattern import Pattern
from moziris.api.screen.region import Region
from moziris.api.screen.screen import Screen
from moziris.api.finder.finder import exists

test_page_file_path = os.path.join(os.path.dirname(__file__), "assets", "index.htm")

FIREFOX_TEST_SITE = "file://{}".format(test_page_file_path)
FIREFOX_LOGO = Pattern("firefox_logo.png")
FIREFOX_TIMEOUT = 10
TINY_FIREFOX_TIMEOUT = 3
DEFAULT_UI_DELAY_LONG = 2.5

_location_bar_locator = "urlbar-input"
_twitter_one_off_button_locator = "urlbar-engine-one-off-item-Twitter"
_google_one_off_button_locator = "urlbar-engine-one-off-item-Google"
search_settings_pattern = Pattern("search_settings.png")
twitter_one_off_button_highlight_pattern = Pattern("twitter_one_off_button_highlight.png")
new_tab_twitter_search_results_pattern = Pattern("new_tab_twitter_search_results.png").similar(0.6)
new_tab_twitter_search_results_pattern2 = Pattern("new_tab_twitter_search_results_2.png").similar(0.6)
google_on_off_button_private_window_pattern = Pattern("google_on_off_button_private_window.png")
magnifying_glass_pattern = Pattern("magnifying_glass.png").similar(0.7)
test_pattern = Pattern("test.png")
this_time_search_with_pattern = Pattern("this_time_search_with.png")

region = Region(0, 0, Screen().width, 2 * Screen().height / 3)


@pytest.mark.details(
    description="This test case perform one-offs searches in private browsing.",
    locale=["en-US"],
    test_case_id="108253",
    test_suite_id="1902",
)
def test_page_loads_in_private_window(private_nightly):

    private_nightly.get(FIREFOX_TEST_SITE)

    test_page_loaded = exists(FIREFOX_LOGO, 0.2)
    assert test_page_loaded, "Firefox logo not found."


def test_search_setting_button_appears_in_awesome_bar(private_nightly):

    with private_nightly.context(private_nightly.CONTEXT_CHROME):
        location_bar = private_nightly.find_element_by_id(_location_bar_locator)
        location_bar.send_keys("moz")

    one_off_bar_displayed = exists(this_time_search_with_pattern, 2)
    assert one_off_bar_displayed, "One-off bar not found at the bottom of awesomebar drop-down"
    # sleep(5)
    search_settings_button_displayed = region.exists(search_settings_pattern, 2)
    assert search_settings_button_displayed, "The 'Search settings' button not found in the awesome bar."


def test_one_off_twitter_searches_in_private_window(private_nightly):

    with private_nightly.context(private_nightly.CONTEXT_CHROME):
        location_bar = private_nightly.find_element_by_id(_location_bar_locator)
        location_bar.send_keys("moz")
        for i in range(15):
            twitter_button_highlighted = region.exists(twitter_one_off_button_highlight_pattern, 0.2)
            if twitter_button_highlighted:
                break
            else:
                location_bar.send_keys(Keys.DOWN)

    assert twitter_button_highlighted, "The 'Twitter' one-off button is not highlighted."

    with private_nightly.context(private_nightly.CONTEXT_CHROME):
        twitter_one_off_button = private_nightly.find_element_by_id(_twitter_one_off_button_locator)
        twitter_one_off_button.click()

    twitter_result_displayed = exists(new_tab_twitter_search_results_pattern, 2) or exists(
        new_tab_twitter_search_results_pattern2, 2
    )
    assert twitter_result_displayed, "Twitter search results not found."


def test_one_off_google_searches_in_private_window(private_nightly):

    with private_nightly.context(private_nightly.CONTEXT_CHROME):
        location_bar = private_nightly.find_element_by_id(_location_bar_locator)
        location_bar.send_keys("test")

        google_button_found = region.exists(google_on_off_button_private_window_pattern, 0.4)
        assert google_button_found, "The'Google' one-off button not found."

        google_on_off_button = private_nightly.find_element_by_id(_google_one_off_button_locator)
        google_on_off_button.click()

    google_page_opened = region.exists(magnifying_glass_pattern, 2)
    assert google_page_opened, "Google page not loaded."

    google_result_displayed = region.exists(test_pattern, 2)
    assert google_result_displayed, "Query item not found in search results."

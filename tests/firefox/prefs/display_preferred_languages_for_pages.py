# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to display preferred languages for pages',
        test_case_id='143563',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        choose_language_button_pattern = Pattern('choose_button.png')
        webpage_language_settings_title_pattern = Pattern('webpage_language_settings_title.png')

        if OSHelper.is_windows():
            scroll_height = Screen.SCREEN_HEIGHT*2
        elif OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = Screen.SCREEN_HEIGHT//100

        navigate('about:preferences#general')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences page loaded.'

        screen_center_location = Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2)

        hover(screen_center_location)

        choose_language_button = scroll_until_pattern_found(choose_language_button_pattern, Mouse().scroll,
                                                            (None, -scroll_height), 20,
                                                            FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert choose_language_button, 'Choose language button found.'

        click(choose_language_button_pattern)

        webpage_language_settings_title = exists(webpage_language_settings_title_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert webpage_language_settings_title, 'Webpage language settings popup loaded.'


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
        time.sleep(8)
        choose_language_button_pattern = Pattern('choose_button.png')
        webpage_language_settings_title_pattern = Pattern('webpage_language_settings_title.png')
        select_a_language_to_add_pattern = Pattern('select_a_language_to_add.png')
        aboutpreferences_ok_button_pattern = Pattern('aboutpreferences_ok_button.png')

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

        select_a_language_to_add = exists(select_a_language_to_add_pattern)
        assert select_a_language_to_add, '"Select a language to add..." button available.'

        click(select_a_language_to_add_pattern, 1)

        type('c')  # choose Chinese language
        type('h')
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

        type(Key.TAB)  # add button
        type(Key.ENTER)

        ok_button_available = exists(aboutpreferences_ok_button_pattern)
        assert ok_button_available, 'OK button available'

        click(aboutpreferences_ok_button_pattern, 1)

        new_tab()
        type('toyota')
        type(Key.ENTER)

        toyota_chinese = exists('翻译此页'.encode('utf-8'), FirefoxSettings.SITE_LOAD_TIMEOUT, Screen.TOP_THIRD)
        assert toyota_chinese, 'The search results are in the selected language'

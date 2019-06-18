# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set as default browser via about:preferences#general page',
        locale=['en-US'],
        test_case_id='143542',
        test_suite_id='2241',
        blocked_by={'id': 'issue_3126', 'platform': OSPlatform.WINDOWS}
    )
    def run(self, firefox):
        make_default_pattern = Pattern('make_default_button.png')
        firefox_is_currently_your_default_browser_pattern = Pattern('firefox_is_currently_your_default_browser.png')
        if OSHelper.is_windows():
            web_browser_label_pattern = Pattern('web_browser_label.png')
        if OSHelper.is_mac():
            do_you_want_to_change_your_default_web_browser_pattern = \
                Pattern('do_you_want_to_change_your_default_web_browser.png')
            use_firefox_pattern = Pattern('use_firefox_button.png')

        navigate('about:preferences')

        about_preferences_loaded = exists(AboutPreferences.FIND_IN_OPTIONS, FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_loaded is True, 'About:preferences page successfully loaded.'

        make_default_option_available = exists(make_default_pattern)
        assert make_default_option_available, '"Make Default..." button available.'

        click(make_default_pattern)

        if OSHelper.is_windows():
            web_browser_label = exists(web_browser_label_pattern)
            assert web_browser_label, 'A Windows\' pop-up is displayed.'

            web_browser_label_height = web_browser_label_pattern.get_size()[1]

            click(web_browser_label_pattern.target_offset(0, web_browser_label_height*3))

            firefox_string = exists('Firefox')
            assert firefox_string, 'Firefox browser option available.'

            click('Firefox')

            type(Key.F4, KeyModifier.ALT)  # close system settings window

        if OSHelper.is_mac():
            default_browser_popup = exists(do_you_want_to_change_your_default_web_browser_pattern)
            assert default_browser_popup, ('A pop-up is displayed asking if you are sure that you want to make '
                                           'Firefox your default browser.')

            click(use_firefox_pattern)

        firefox_currently_default_browser = exists(firefox_is_currently_your_default_browser_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_currently_default_browser, 'The message "Firefox is not your default browser" changes ' \
                                                  'to "Firefox is currently your default browser".'

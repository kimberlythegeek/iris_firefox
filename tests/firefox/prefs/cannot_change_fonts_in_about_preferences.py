# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1429672 - Cannot change fonts in about:preferences',
        test_case_id='178960',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        advanced_button_pattern = Pattern('advanced_button.png')
        fonts_popup_pattern = Pattern('fonts_popup.png')
        serif_font_option_pattern = Pattern('serif_font_option.png')
        fonts_changed_pattern = Pattern('fonts_changed.png')

        if OSHelper.is_windows():
            font_name = 'Arial'
        elif OSHelper.is_mac():
            font_name = 'American Typewriter'
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO)
        assert firefox_site_loaded, 'Firefox site loaded'

        new_tab()
        navigate('about:preferences#general')

        exists(advanced_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        click(advanced_button_pattern, 1)

        # Change the default fonts with other ones and click "OK" button.
        fonts_popup = exists(fonts_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert fonts_popup, 'Fonts popup window displayed.'

        serif_font_option = exists(serif_font_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert serif_font_option, "Serif font option available"

        serif_font_option_location = find(serif_font_option_pattern)
        serif_font_option_width = serif_font_option_pattern.get_size()[0]
        serif_font_option_click_location = Location(serif_font_option_location.x+serif_font_option_width*2,
                                                    serif_font_option_location.y)

        if OSHelper.is_windows():
            click(serif_font_option_click_location)
        else:
            click(serif_font_option_pattern)
            type(Key.DOWN)

        american_typewriter_option = exists(font_name, FirefoxSettings.FIREFOX_TIMEOUT)
        assert american_typewriter_option, '{} Serif available'.format(font_name)

        click(font_name)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        type(Key.ENTER)  # Close Advanced fonts popup

        previous_tab()

        exists(fonts_changed_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert fonts_changed_pattern, 'Fonts changed successfully'

        next_tab()
        close_tab()
        new_tab()
        navigate('about:preferences#general')

        american_typewriter_option = exists(font_name, FirefoxSettings.FIREFOX_TIMEOUT)
        assert american_typewriter_option, '{} Serif available. The changes that were made in ' \
                                           'step 4 are still preserved'.format(font_name)

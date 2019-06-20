# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *
from targets.firefox.firefox_app.fx_browser import FirefoxUtils


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The correct Firefox version is successfully displayed',
        test_case_id='143570',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        find_in_preferences_field_pattern = Pattern('find_in_preferences_field.png')

        navigate('about:preferences')

        page_loaded = exists(find_in_preferences_field_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences page loaded'

        paste('Firefox')
        paste(' updates')  # doesn't find when whole phrase in one search string

        keep_firefox_up_to_date_displayed = exists('Keep Firefox up to date for the best performance, stability, '
                                                   'and security')
        assert keep_firefox_up_to_date_displayed, '"Keep Firefox/Nighlty up to date for the best performance, ' \
                                                  'stability, and security." message is displayed.'

        try:
            processor_architecture = '64-bit' if '64' in get_pref_value('media.gmp-gmpopenh264.abi') else '32-bit'
        except Exception as e:
            raise APIHelperError('Failed to retrieve preference value.\n{}'.format(e))

        processor_architecture_displayed = exists('({})'.format(processor_architecture),
                                                  FirefoxSettings.SITE_LOAD_TIMEOUT, Screen.LEFT_HALF)

        # firefox_version = get_pref_value('extensions.lastAppVersion')
        # os.path.expanduser('~')

        firefox_version_displayed = exists('68.0b11', FirefoxSettings.SITE_LOAD_TIMEOUT, Screen.LEFT_HALF.top_half())

        firefox_is_up_to_date = exists('Firefox is up to date', FirefoxSettings.SITE_LOAD_TIMEOUT, Screen.LEFT_HALF)

        assert processor_architecture_displayed, 'The version of Firefox, the date and the architecture are correctly displayed.'
        assert firefox_version_displayed, 'The version of Firefox, the date and the architecture are correctly displayed.'
        assert firefox_is_up_to_date, 'The version of Firefox, the date and the architecture are correctly displayed.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The "Check for updates" button works as expected',
        test_case_id='143572',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        find_in_preferences_field_pattern = Pattern('find_in_preferences_field.png')

        navigate('about:preferences#general')

        find_in_preferences_field = exists(find_in_preferences_field_pattern)
        assert find_in_preferences_field, 'The about:preferences page is successfully loaded.'

        paste('Firefox')
        paste(' updates')  # doesn't open results when enter whole string at once

        #


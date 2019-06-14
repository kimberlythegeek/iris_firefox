# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1437880 - The "Remove Selected" button is not grayed out after a website is deselected',
        test_case_id='145301',
        test_suite_id='2241',
        locale=['en-US'],
        blocked_by={'id': 'issue_3073', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        manage_data_button_pattern = Pattern('manage_data_button.png')
        site_table_header_pattern = Pattern('site_table_header.png')
        remove_selected_button_active_pattern = Pattern('remove_selected_button_active.png')
        remove_selected_button_inactive_pattern = Pattern('remove_selected_button_inactive.png')

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences page loaded'

        paste('your stored cookies, site data')

        manage_data_button = exists(manage_data_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_data_button, 'Manage Data button from Site Data section is available.'

        click(manage_data_button_pattern, 1)

        remove_selected_button_inactive = exists(remove_selected_button_inactive_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_selected_button_inactive, '"Remove Selected" button is disabled.'

        click(site_table_header_pattern.target_offset(20, 20), 1)  # Select a site from the list.

        remove_selected_button_active = exists(remove_selected_button_active_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_selected_button_active, 'The "Remove Selected" button is enabled.'

        click(site_table_header_pattern)

        remove_site_button_inactive = exists(remove_selected_button_inactive_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_site_button_inactive, 'The "Remove Selected" button is disabled. NOTE: In the builds affected ' \
                                            'by this bug the "Remove Selected" button is still enabled.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox Home Content - Top Sites can be displayed in 1 or 4 rows',
        locale=['en-US'],
        test_case_id='2241',
        test_suite_id='161667',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        homepage_preferences_pattern = Pattern('homepage_preferences.png')
        preferences_top_site_label_pattern = Pattern('preferences_top_site_label.png')
        top_sites_one_row_option_pattern = Pattern('top_sites_one_row_option.png')

        navigate('about:preferences#home')

        preferences_page_opened = exists(homepage_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        top_sites_section_displayed = exists(preferences_top_site_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_displayed, 'The "Top Sites" section is displaying'

        top_sites_label_location = find(preferences_top_site_label_pattern)
        top_sites_label_width, top_sites_label_height = preferences_top_site_label_pattern.get_size()
        top_sites_section_region = Region(top_sites_label_location.x - top_sites_label_width,
                                          top_sites_label_location.y, top_sites_label_width * 10,
                                          top_sites_label_height * 3)

        top_sites_section_selected = exists(AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT,
                                            top_sites_section_region)
        assert top_sites_section_selected, 'The "Top Sites" section is selected'

        doorhanger_set_1_row = exists(top_sites_one_row_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                            top_sites_section_region)
        assert doorhanger_set_1_row, 'The doorhanger on the right side of the option is set for 1 row.'

        click(NavBar.HOME_BUTTON)

        breakpoint()

        new_tab()

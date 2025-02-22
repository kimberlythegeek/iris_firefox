# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.nightly.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search Code Testing: DuckDuckGo - US.',
        locale=['en-US'],
        test_case_id='218335',
        test_suite_id='83',
    )
    def run(self, firefox):
        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        test_search_duckduckgo_pattern = Pattern('test_search_duckduckgo.png')

        change_preference('browser.search.widget.inNavBar', True)

        navigate('about:preferences#search')

        default_search_engine_google_exists = exists(default_search_engine_google_pattern.similar(0.7),
                                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_search_engine_google_exists is True, 'Google is the default search engine.'

        # Change the default search engine to DuckDuckGo.
        default_search_engine_dropdown_exists = exists(default_search_engine_dropdown_pattern,
                                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_search_engine_dropdown_exists is True, 'Default search engine dropdown exists'

        click(default_search_engine_dropdown_pattern)
        repeat_key_down(3)
        type(Key.ENTER)

        select_location_bar()
        type('test', interval=0.25)
        type(Key.ENTER)

        test_search_duckduckgo_exists = exists(test_search_duckduckgo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_search_duckduckgo_exists is True, 'The search is performed with the DuckDuckGo engine.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        select_location_bar()
        url_text = copy_to_clipboard()

        assert 't=ffab' in url_text, 'The resulted URL contains the \'t=ffab\' string.'

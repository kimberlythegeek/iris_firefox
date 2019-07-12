# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' If the page contains multiple iframe, user can report the URL of the iframe that we '
                    'clicked in report redirect URL Bug 1288633 ',
        test_case_id='50357',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        safebrowsing_page = self.get_asset_path('safebrowsing.html')
        bad_ssl_logo_pattern = Pattern('bad_ssl_logo.png')

        change_preference('security.mixed_content.block_active_content', 'false')

        navigate(safebrowsing_page)

        time.sleep(1000)

        bad_ssl_page_loaded = exists(bad_ssl_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert bad_ssl_page_loaded, 'Bad SSL page sucessfully loaded'
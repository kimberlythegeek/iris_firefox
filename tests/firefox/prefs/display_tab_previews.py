# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[Win] Firefox can be set to display tab previews in the Windows taskbar',
        test_case_id='143552',
        test_suite_id='2241',
        locale=['en-US'],
        exclude=[OSPlatform.MAC, OSPlatform.LINUX]
    )
    def run(self, firefox):
        show_tab_previews_checked_pattern = Pattern('show_tab_previews_checked.png')
        show_tab_previews_unchecked_pattern = Pattern('show_tab_previews_unchecked.png')
        firefox_taskbar_thumbnail_pattern = Pattern('firefox_taskbar_thumbnail.png')
        web_page_thumbnail_pattern = Pattern('web_page_thumbnail.png')
        sites_displayed_inside_doorhanger_pattern = Pattern('sites_displayed_inside_doorhanger.png')

        new_tab()

        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_page_loaded = exists(LocalWeb.FOCUS_LOGO, Settings.site_load_timeout)
        assert focus_page_loaded, 'Focus local page is loaded'

        new_tab()

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_page_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_page_loaded, 'Firefox local page is loaded'

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences page loaded.'

        # From "Tabs" check the box for "Show tab previews in the Windows taskbar".

        show_tab_previews_checked = find_in_region_from_pattern(show_tab_previews_checked_pattern,
                                                                AboutPreferences.CHECKED_BOX)

        if not show_tab_previews_checked:
            show_tab_previews_unchecked = find_in_region_from_pattern(show_tab_previews_unchecked_pattern,
                                                                      AboutPreferences.UNCHECKED_BOX)
            assert show_tab_previews_unchecked, '"Show tab previews in the Windows taskbar" is unchecked.'

            click(show_tab_previews_unchecked_pattern)

        show_tab_previews_checked = find_in_region_from_pattern(show_tab_previews_checked_pattern,
                                                                AboutPreferences.CHECKED_BOX)
        assert show_tab_previews_checked, '"Show tab previews in the Windows taskbar" is checked.'

        firefox_taskbar_icon = exists(firefox_taskbar_thumbnail_pattern)
        assert firefox_taskbar_icon, 'The Firefox icon present on the taskbar.'

        bottom_region = Screen.BOTTOM_THIRD

        fl = find_all(firefox_taskbar_thumbnail_pattern, bottom_region)

        hover(fl[-1])
        # hover(Docker.FIREFOX_DOCKER_ICON)

        web_page_thumbnail = exists(web_page_thumbnail_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert web_page_thumbnail and fl, 'Hovering over Firefox icon in the taskbar causes thumbnails of each open Web page' \
                                   ' to appear. {} , {} '.format(fl, fl[-1])

        hover(web_page_thumbnail_pattern)

        corresponding_tab_displayed = exists(LocalWeb.FOCUS_LOGO)
        assert corresponding_tab_displayed, 'Hovering  over the thumbnails makes corresponding tab display.'

        click(web_page_thumbnail_pattern)

        corresponding_tab_displayed = exists(LocalWeb.FOCUS_LOGO)
        assert corresponding_tab_displayed, 'Hovering  over the thumbnails makes corresponding tab display.'

        try:
            thumbnail_vanished = wait_vanish(web_page_thumbnail_pattern)
            assert thumbnail_vanished, 'The web page thumbnail is vanished from screen.'
        except FindError:
            raise FindError('The web page thumbnail is still displayed on screen.')

        # Open more then 20 tabs and hover over the Firefox icon on the taskbar.

        for _ in range(0, 20):
            new_tab()

            navigate(LocalWeb.FOCUS_TEST_SITE)

            focus_page_loaded = exists(LocalWeb.FOCUS_LOGO, Settings.site_load_timeout)
            assert focus_page_loaded, 'Focus local page is loaded'

        firefox_taskbar_icon = exists(firefox_taskbar_thumbnail_pattern)
        assert firefox_taskbar_icon, 'The Firefox icon present on the taskbar.'

        screen_center_location = Location(Screen.SCREEN_WIDTH//2, Screen.SCREEN_HEIGHT//2)

        fl = find_all(firefox_taskbar_thumbnail_pattern, bottom_region)

        hover(screen_center_location, FirefoxSettings.TINY_FIREFOX_TIMEOUT)  # hover different location from current

        hover(fl[-1])

        time.sleep(1234)

        # The sites are displayed inside a doorhanger.

        sites_displayed_inside_doorhanger = exists(sites_displayed_inside_doorhanger_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert sites_displayed_inside_doorhanger, 'The sites are displayed inside a doorhanger.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Users can successfully customize the saving location of downloaded content',
        test_case_id='143567',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        if OSHelper.is_windows():
            scroll_height = Screen.SCREEN_HEIGHT*2
        elif OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = Screen.SCREEN_HEIGHT//100

        navigate('about:preferences#general')

        expected = exists(AboutPreferences.FIND_IN_OPTIONS, 10)
        assert expected is True, '\'Find in Options\' search field is displayed.'

        click(AboutPreferences.FIND_IN_OPTIONS)

        paste('downloads')

        expected = exists(AboutPreferences.DOWNLOADS, 10)
        assert expected is True, 'The \'Downloads\' section is displayed.'

        click(AboutPreferences.BROWSE)

        expected = exists(Utils.NEW_FOLDER, 10)
        assert expected is True, '\'New Folder\' button is displayed.'

        # click(Utils.NEW_FOLDER)
        #
        # expected = exists(Utils.NEW_FOLDER_HIGHLIGHTED, 10)
        # assert expected is True, '\'New Folder\' is highlighted.'

        folderpath = PathManager.get_downloads_dir()

        if OSHelper.is_mac():
            type('g', modifier=(KeyModifier.CMD, KeyModifier.SHIFT))  # open folder in Finder
            paste(folderpath)
            type(Key.ENTER)
            type('2', KeyModifier.CMD)  # change view of finder
        else:
            paste(folderpath)
            type(Key.ENTER, interval=1)

        select_folder_button = exists(Utils.SELECT_FOLDER)
        assert select_folder_button, 'Select folder button available.'

        click(Utils.SELECT_FOLDER, 1)

        # The subdialog is dismissed.
        # The "Save files to" field is populated with the new location.

        # ...

        # Go to this site, click on a small file and from the pop-up choose "Save File".

        new_tab()

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        small_file = exists(DownloadFiles.EXTRA_SMALL_FILE_5MB)
        assert small_file, 'Small file available'

        click(DownloadFiles.EXTRA_SMALL_FILE_5MB)

        save_file_button = exists(DownloadFiles.SAVE_FILE)
        assert save_file_button, 'Save file button available'

        click(DownloadFiles.SAVE_FILE)

        download_button = exists(NavBar.DOWNLOADS_BUTTON, region=Screen.TOP_THIRD)
        assert download_button, 'Downloads button available'

        click(NavBar.DOWNLOADS_BUTTON)

        open_downloads_folder = exists(DownloadManager.DownloadsPanel.OPEN_DOWNLOAD_FOLDER, region=Screen.TOP_THIRD)
        assert open_downloads_folder, 'Open downloads folder button available'

        # The downloaded item was saved in the folder selected in step 3.

        time.sleep(1234)

        # From "Files and Applications", underneath the "Downloads", check the option "Always ask where to save files".

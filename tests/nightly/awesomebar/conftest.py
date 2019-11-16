import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

firefox_profile = webdriver.FirefoxProfile()
# Don't automatically update the application
firefox_profile.set_preference("app.update.disabledForTesting", True)
# Don't restore the last open set of tabs if the browser has crashed
firefox_profile.set_preference("browser.sessionstore.resume_from_crash", False)
# Don't check for the default web browser during startup
firefox_profile.set_preference("browser.shell.checkDefaultBrowser", False)
# Don't warn on exit when multiple tabs are open
firefox_profile.set_preference("browser.tabs.warnOnClose", False)
# Don't warn when exiting the browser
firefox_profile.set_preference("browser.warnOnQuit", False)
# Don't send Firefox health reports to the production server
firefox_profile.set_preference("datareporting.healthreport.documentServerURI", "http://%(server)s/healthreport/")
# Skip data reporting policy notifications
firefox_profile.set_preference("datareporting.policy.dataSubmissionPolicyBypassNotification", False)
# Only install add-ons from the profile and the application scope
# Also ensure that those are not getting disabled.
# see: https://developer.mozilla.org/en/Installing_extensions
firefox_profile.set_preference("extensions.enabledScopes", "5")
firefox_profile.set_preference("extensions.autoDisableScopes", "10")
# Don't send the list of installed addons to AMO
firefox_profile.set_preference("extensions.getAddons.cache.enabled", False)
# Don't install distribution add-ons from the app folder
firefox_profile.set_preference("extensions.installDistroAddons", False)
# Don't automatically update add-ons
firefox_profile.set_preference("extensions.update.enabled", False)
# Don't open a dialog to show available add-on updates
firefox_profile.set_preference("extensions.update.notifyUser", False)
# Enable test mode to run multiple tests in parallel
firefox_profile.set_preference("focusmanager.testmode", True)
# Enable test mode to not raise an OS level dialog for location sharing
firefox_profile.set_preference("geo.provider.testing", True)
# Suppress delay for main action in popup notifications
firefox_profile.set_preference("security.notification_enable_delay", "0")
# Suppress automatic safe mode after crashes
firefox_profile.set_preference("toolkit.startup.max_resumed_crashes", "-1")
# Don't send Telemetry reports to the production server. This is
# needed as Telemetry sends pings also if FHR upload is enabled.
firefox_profile.set_preference("toolkit.telemetry.server", "http://%(server)s/telemetry-dummy/")

private_firefox_options = Options()
private_firefox_options.add_argument("-private")


@pytest.fixture()
def firefox():
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    yield driver
    driver.close()


@pytest.fixture()
def private_firefox():
    driver = webdriver.Firefox(options=private_firefox_options)
    yield driver
    driver.close()


@pytest.fixture()
def nightly():
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities["marionette"] = True
    firefox_capabilities["binary"] = "/Volumes/Untitled/Applications/Firefox Nightly.app/Contents/MacOS/firefox"

    driver = webdriver.Firefox(capabilities=firefox_capabilities)
    yield driver
    driver.close()


@pytest.fixture()
def private_nightly():
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities["marionette"] = True
    firefox_capabilities["binary"] = "/Volumes/Untitled/Applications/Firefox Nightly.app/Contents/MacOS/firefox"

    driver = webdriver.Firefox(capabilities=firefox_capabilities, options=private_firefox_options)
    yield driver
    driver.close()

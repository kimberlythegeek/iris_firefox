from pypom import Page


class PrivacyPreferencesPage(Page):
    _delete_cookies_checkbox_locator = "#deleteOnClose"

    @property
    def loaded(self):
        checkbox = self.find_element(*self._delete_cookies_checkbox_locator)
        return checkbox.is_displayed()

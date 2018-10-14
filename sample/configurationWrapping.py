import configparser

class GlobalConfigurationWrapper:
    default_path = '/home/pi/Desktop/PeepNee/config.ini'
    
    def __init__(self, path_to_file=None):
        if path_to_file is None:
            path_to_file = self.default_path

        self.config = configparser.ConfigParser()
        self.config.read(path_to_file)        

    def box_id(self):
        return self.config['boxMetadata']['id']
    
    # SignalR
    def signalr_hub_name(self):
        return self.config['signalR']['hubname']

    def signalr_hub_hosturl(self):
        return self.config['signalR']['hubhosturl']

    # Logging
    def logging_log_to(self):
        return self.config['logging']['logto']

    def logging_log_level(self):
        return self.config['logging']['loglevel']

    # Error notifications
    def error_notifications_send_email_on_error(self):
        return self.config['errornotifications']['sendemailonerror']

    def error_notifications_support_email(self):
        return self.config['errornotifications']['supportemail']

    # Imgur
    def imgur_client_id(self):
        return self.config['imgur']['clientid']

    def imgur_client_secret(self):
        return self.config['imgur']['clientsecret']

    def imgur_latest_photo_root_path(self):
        return self.config['imgur']['lastestphotorootpath']

class HmiConfigurationWrapper:
    default_path = '/home/pi/Desktop/PeepNee/hmiConfig.ini'
    _PAGES_SECTION_ = 'pages'
    _BUTTON_PAGE_INDEXES_SECTION_ = 'buttonPageIndexes'
    
    def __init__(self, path_to_file=None):
        if path_to_file is None:
            path_to_file = self.default_path

        self.config = configparser.ConfigParser()
        self.config.read(path_to_file)
        
    # pages
    def home_page_name(self):
        return self.config[self._PAGES_SECTION_]['homePageName']
    def home_page_id(self):
        return self.config[self._PAGES_SECTION_]['homePageId']
    
    def show_package_page_name(self):
        return self.config[self._PAGES_SECTION_]['showPackagePageName']
    def show_package_page_id(self):
        return self.config[self._PAGES_SECTION_]['showPackagePageId']
    
    def taking_picture_page_name(self):
        return self.config[self._PAGES_SECTION_]['takingPicturePageName']
    def taking_picture_page_id(self):
        return self.config[self._PAGES_SECTION_]['takingPicturePageId']
    
    def wait_page_name(self):
        return self.config[self._PAGES_SECTION_]['waitPageName']
    def wait_page_id(self):
        return self.config[self._PAGES_SECTION_]['waitPageId']
    
    def package_accepted_page_name(self):
        return self.config[self._PAGES_SECTION_]['packageAcceptedPageName']
    def package_accepted_page_id(self):
        return self.config[self._PAGES_SECTION_]['packageAcceptedPageId']
    
    def package_declined_page_name(self):
        return self.config[self._PAGES_SECTION_]['packageDeclinedPageName']
    def packageDeclinedPageId(self):
        return self.config[self._PAGES_SECTION_]['packageDeclinedPageId']
    
    def repeat_steps_page_name(self):
        return self.config[self._PAGES_SECTION_]['repeatStepsPageName']
    def repeat_steps_page_id(self):
        return self.config[self._PAGES_SECTION_]['repeatStepsPageId']
    
    # Buttons
    def home_screen_main_button_index(self):
        return self.config[self._BUTTON_PAGE_INDEXES_SECTION_]['homeScreenMainButton']
    def show_packge_and_click_button_index(self):
        return self.config[self._BUTTON_PAGE_INDEXES_SECTION_]['showPackgeAndClickButton']
        
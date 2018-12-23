import configparser

class GlobalConfigurationWrapper:
    default_path = '/home/pi/Desktop/PeepNee/config.ini'
    _SIGNALR_SECTION_ = 'signalR'
    _LOGGING_SECTION_ = 'logging'
    _ERROR_NOTIFICATIONS_SECTION_ = 'errornotifications'
    _IMGUR_SECTION_ = 'imgur'
    _BOX_METADATA_SECTION_ = 'boxMetadata'
    _REAL_TIME_PUSH_NOTIFICATIONS_SECTION_ = 'realTimePushNotifications'
    _FIREBASE_SECTION_ = 'firebase'
    
    def __init__(self, path_to_file=None):
        if path_to_file is None:
            path_to_file = self.default_path

        self.config = configparser.ConfigParser()
        self.config.read(path_to_file)        
    # Box metadata
    def box_id(self):
        return self.config[self._BOX_METADATA_SECTION_]['id']
    def box_open_by_default(self):
        return self.config[self._BOX_METADATA_SECTION_]['openByDefault']
    def box_time_to_wait_before_open_or_close(self):
        return self.config[self._BOX_METADATA_SECTION_]['timeToWaitBeforeOpenOrClose']
    def box_time_to_keep_the_box_open(self):
        return self.config[self._BOX_METADATA_SECTION_]['timeToKeepTheBoxOpen']
    
    # SignalR
    def signalr_hub_name(self):
        return self.config[self._SIGNALR_SECTION_ ]['hubname']

    def signalr_hub_hosturl(self):
        return self.config[self._SIGNALR_SECTION_ ]['hubhosturl']

    # Logging
    def logging_log_to(self):
        return self.config[self._LOGGING_SECTION_]['logto']
    def logging_log_level(self):
        return self.config[self._LOGGING_SECTION_]['loglevel']

    # Error notifications
    def error_notifications_send_email_on_error(self):
        return self.config[self._ERROR_NOTIFICATIONS_SECTION_]['sendemailonerror']
    def error_notifications_support_email(self):
        return self.config[self._ERROR_NOTIFICATIONS_SECTION_]['supportemail']

    # Imgur
    def imgur_client_id(self):
        return self.config[self._IMGUR_SECTION_]['clientid']

    def imgur_client_secret(self):
        return self.config[self._IMGUR_SECTION_]['clientsecret']
    def imgur_latest_photo_root_path(self):
        return self.config[self._IMGUR_SECTION_]['lastestphotorootpath']
    
    # Real Time Push Notifications
    def rtpn_timebox_response_after_push_notification(self):
        return self.config[self._REAL_TIME_PUSH_NOTIFICATIONS_SECTION_]['timeboxResponseAfterPushNotification']
    
    # Firebase
    def fbase_apiKey(self):
        return self.config[self._FIREBASE_SECTION_]['apiKey']   
    def fbase_authDomain(self):
        return self.config[self._FIREBASE_SECTION_]['authDomain']
    def fbase_databaseUrl(self):
        return self.config[self._FIREBASE_SECTION_]['databaseURL']
    def fbase_storageBucket(self):
        return self.config[self._FIREBASE_SECTION_]['storageBucket']

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
    def home_page_id(self):
        return (int)(self.config[self._PAGES_SECTION_]['homePageId'])
    
    def show_package_page_id(self):
        return (int)(self.config[self._PAGES_SECTION_]['showPackagePageId'])
    
    def taking_picture_page_id(self):
        return (int)(self.config[self._PAGES_SECTION_]['takingPicturePageId'])
    
    def wait_page_id(self):
        return (int)(self.config[self._PAGES_SECTION_]['waitPageId'])
    
    def package_accepted_page_id(self):
        return (int)(self.config[self._PAGES_SECTION_]['packageAcceptedPageId'])
    
    def packageDeclinedPageId(self):
        return (int)(self.config[self._PAGES_SECTION_]['packageDeclinedPageId'])
    
    def repeat_steps_page_id(self):
        return (int)(self.config[self._PAGES_SECTION_]['repeatStepsPageId'])
    
    # Buttons
    def home_screen_main_button_index(self):
        return (int)(self.config[self._BUTTON_PAGE_INDEXES_SECTION_]['homeScreenMainButton'])
    def show_packge_and_click_button_index(self):
        return (int)(self.config[self._BUTTON_PAGE_INDEXES_SECTION_]['showPackgeAndClickButton'])
        
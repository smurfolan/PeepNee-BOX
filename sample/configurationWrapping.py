import configparser

class ConfigurationWrapper:
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


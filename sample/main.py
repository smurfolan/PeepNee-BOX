import time

from hmiDisplayManager import HmiDisplayManager
from upsManager import UpsManager
from turnOffRequestHandler import TurnOffRequestHandler

try:
    hmiDisplayManager=HmiDisplayManager()
    upsManager=UpsManager()
    turnOffRequestHandler=TurnOffRequestHandler()
    
    hmiDisplayManager.idle()
    # What happens if the battery went down and shut down was called on this manager file?
    # Maybe we could also have a page to show 'Not working' when for some reason shut down was caused.
    # Until the battery is down, we would still see the screen.
    upsManager.idle()
    turnOffRequestHandler.idle()
    
    while True:
        if turnOffRequestHandler.turnOffIsRequested():
            break;
        time.sleep(1)
        
except BaseException as e:
    pass
finally:
    hmiDisplayManager.sleep()
    upsManager.sleep()
    turnOffRequestHandler.dispose()
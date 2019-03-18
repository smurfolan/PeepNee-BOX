import sys 
import time

from hmiDisplayManager import HmiDisplayManager
from upsManager import UpsManager
from turnOffRequestHandler import TurnOffRequestHandler
from firebaseManager import FirebaseManager

try:
    hmiDisplayManager=HmiDisplayManager()
    upsManager=UpsManager()
    turnOffRequestHandler=TurnOffRequestHandler()
    
    hmiDisplayManager.idle()
    upsManager.idle()
    turnOffRequestHandler.idle()
    
    fbManager = FirebaseManager()
    fbManager.toggle_mailbox_active_status(True)
    
    while True:
        if turnOffRequestHandler.turnOffIsRequested():
            # TODO: Using the hmiDisplayManager show an 'OFFLINE' screen to indicate box is in a shut-down state.
            break;
        time.sleep(1)
        
except BaseException as e:
    # This will log to the output file.
    print(str(e))
    sys.stdout.flush()
finally:
    hmiDisplayManager.sleep()
    upsManager.sleep()
    turnOffRequestHandler.dispose()
    
    fbManager.toggle_mailbox_active_status(False)
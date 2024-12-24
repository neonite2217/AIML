
import pywhatkit
from datetime import datetime

PHONE_NUMBER = input("Enter Phone Number: ")
# Must include all number info about region (and '+' sign).

MESSAGE = input("Enter Message: ")

HR = int(input("Enter Hour (24hrs format): "))

MIN = int(input("Enter Minutes:"))

pywhatkit.sendwhatmsg(PHONE_NUMBER, MESSAGE, HR, MIN)
# Send a message at HR:MIN.
# Doesn't send until then close currrent tab, if called again will open another

pywhatkit.sendwhatmsg_instantly(PHONE_NUMBER, MESSAGE, tab_close=True)
# Sends instantly while args tab_close closes the current tab after sent

pywhatkit.image_to_ascii_art("folders/name.jpeg", "ascii")
# tricky, because WhatsApp characters does not align properly

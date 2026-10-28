

# Install first: pip install pywhatkit

import pywhatkit as kit

#replace with recipient's phone number in international format
kit.sendwhatmsg("+1234567890", "Hello from Python!", 15, 30)
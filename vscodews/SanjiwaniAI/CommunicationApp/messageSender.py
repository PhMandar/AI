''' 
Following is the working test code for sending the messages.
'''

import pywhatkit as kit

# Syntax: phone_number (with country code), message, time_hour (24h format), time_min
try:
    # Following message will send the text message.
    #  kit.sendwhatmsg("+918446293055", "Hello from Mandar !", 22, 16) # Sends at 10:30 PM
    
    # Following code will send the image with caption.
    img_path = "D:/Development/AI/vscodews/SanjiwaniAI/CommunicationApp/temp_uploads/pitbull.jpg"
    kit.sendwhats_image("+919850310562", img_path, "Check this out!",  wait_time=15)
    print("Message scheduled!")

    
except Exception as e:
    print(f"An error occurred: {e}")

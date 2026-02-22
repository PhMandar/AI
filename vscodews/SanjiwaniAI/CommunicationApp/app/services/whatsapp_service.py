from datetime import datetime, timedelta

import pywhatkit as kit
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def send(self, phone, msg_type, content, caption=None):
        try:
            logger.info(f"Attempting to send {msg_type} to {phone}")
            if msg_type == 'text':
                kit.sendwhatmsg_instantly(phone, content, wait_time=15, tab_close=True)
            elif msg_type == 'image':
                kit.sendwhats_image(phone, content, caption, wait_time=15, tab_close=True)
            else:
                raise ValueError("Unsupported message type")
            logger.info(f"Successfully sent {msg_type} to {phone}")
            return {"status": "success", "service": "whatsapp"}
        except Exception as e:
            logger.error(f"Failed to send {msg_type} to {phone}: {str(e)}")
            return {"status": "error", "service": "whatsapp", "message": str(e)}

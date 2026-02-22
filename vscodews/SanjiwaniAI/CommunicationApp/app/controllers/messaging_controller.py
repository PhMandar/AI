from flask import Blueprint, request, jsonify, current_app
from app.services.whatsapp_service import WhatsAppService
import os

msg_bp = Blueprint('messaging', __name__)
wa_service = WhatsAppService()

@msg_bp.route('/send', methods=['POST'])
def handle_send():

    current_app.logger.info(f"Incoming request: {request.form}")

    phone = request.form.get('phone')
    msg_type = request.form.get('type') # 'text', 'image', 'document'
    
    if msg_type == 'text':
        result = wa_service.send(phone, 'text', request.form.get('message'))
    else:
        file = request.files['file']
        path = os.path.join('temp_uploads', file.filename)
        file.save(path)
        result = wa_service.send(phone, msg_type, path, request.form.get('caption'))
        
    return jsonify(result)

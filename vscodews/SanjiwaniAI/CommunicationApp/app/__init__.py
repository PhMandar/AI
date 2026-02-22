from flask import Flask
import logging
import os

def create_app():
    print("\n Creating Flask app...")
    app = Flask(__name__)
    
    # Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"), # Saves to a file
            logging.StreamHandler()         # Prints to terminal
        ]
    )

    app.logger.info("Service Starting Up...")

    from app.controllers.messaging_controller import msg_bp
    app.register_blueprint(msg_bp, url_prefix='/api/v1')
    
    return app
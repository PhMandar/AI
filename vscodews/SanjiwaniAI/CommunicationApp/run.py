import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Automatically create the upload folder if it's missing
    if not os.path.exists('temp_uploads'):
        os.makedirs('temp_uploads')
        
    app.run(port=5000, debug=True)

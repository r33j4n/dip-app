from flask import Flask
from controllers.main_controller import MainController

app = Flask(__name__)
app.config['SERVER_NAME'] = 'https://8576-2401-dd00-10-20-75fa-b0fb-d5bf-8ffd.ngrok-free.app'

app.config['UPLOAD_FOLDER'] = 'static/images'

app.add_url_rule('/', view_func=MainController.index, methods=['GET'])
app.add_url_rule('/upload', view_func=MainController.upload_image, methods=['POST'])
app.add_url_rule('/details/<image_path>', view_func=MainController.view_image_details, methods=['GET'])
app.add_url_rule('/histogram/<image_path>', view_func=MainController.view_histogram, methods=['GET'])
app.add_url_rule('/contrast/<image_path>', view_func=MainController.apply_contrast_stretching, methods=['GET'])
app.add_url_rule('/contrast/<image_path>', view_func=MainController.apply_contrast_stretching, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)

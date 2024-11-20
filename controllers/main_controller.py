from flask import render_template, request, redirect, url_for, send_from_directory
import os
import cv2
from models.image_processing import ImageProcessor


class MainController:
    UPLOAD_FOLDER = 'static/images'

    @staticmethod
    def index():
        return render_template('index.html')

    @staticmethod
    def upload_image():
        if 'image' not in request.files:
            return redirect(url_for('index'))
        file = request.files['image']
        if file.filename == '':
            return redirect(url_for('index'))
        file_path = os.path.join(MainController.UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return redirect(url_for('view_image_details', image_path=file.filename))

    @staticmethod
    def view_image_details(image_path):
        file_path = os.path.join(MainController.UPLOAD_FOLDER, image_path)
        image = ImageProcessor.load_image(file_path)
        details = ImageProcessor.get_image_details(image)
        return render_template('image_details.html', details=details, image_path=image_path)

    @staticmethod
    def view_histogram(image_path):
        file_path = os.path.join(MainController.UPLOAD_FOLDER, image_path)
        image = ImageProcessor.load_image(file_path)
        ImageProcessor.plot_histogram(image)
        return send_from_directory('static/images', 'histogram.png')

    @staticmethod
    def apply_contrast_stretching(image_path):
        file_path = os.path.join(MainController.UPLOAD_FOLDER, image_path)
        image = ImageProcessor.load_image(file_path)

        # Get custom min and max values from the form
        custom_min = request.args.get('custom_min', type=int)
        custom_max = request.args.get('custom_max', type=int)

        # Convert and stretch grayscale
        gray, stretched, original_frequencies, stretched_frequencies = ImageProcessor.contrast_stretching(
            image, custom_min, custom_max
        )

        # Save grayscale and stretched images
        gray_path = os.path.join(MainController.UPLOAD_FOLDER, 'gray.png')
        stretched_path = os.path.join(MainController.UPLOAD_FOLDER, 'stretched.png')
        cv2.imwrite(gray_path, gray)
        cv2.imwrite(stretched_path, stretched)

        # Generate histograms
        ImageProcessor.plot_histogram(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), 'gray_histogram.png')
        ImageProcessor.plot_histogram(cv2.cvtColor(stretched, cv2.COLOR_GRAY2BGR), 'stretched_histogram.png')

        return render_template(
            'contrast_stretching.html',
            gray_image='gray.png',
            stretched_image='stretched.png',
            gray_histogram='gray_histogram.png',
            stretched_histogram='stretched_histogram.png',
            original_frequencies=original_frequencies,
            stretched_frequencies=stretched_frequencies,
            custom_min=custom_min,
            custom_max=custom_max
        )







import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageProcessor:
    @staticmethod
    def load_image(image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")
        return image

    @staticmethod
    def get_image_details(image):
        height, width, channels = image.shape
        return {
            "height": height,
            "width": width,
            "channels": channels
        }

    @staticmethod
    def plot_histogram(image, filename):
        # Convert to grayscale if needed for calculating statistics
        if len(image.shape) == 3:  # Color image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image  # Already grayscale

        # Calculate histogram
        histogram = cv2.calcHist([gray], [0], None, [256], [0, 256])

        # Calculate statistical information
        mean = np.mean(gray)
        median = np.median(gray)
        min_val = np.min(gray)
        max_val = np.max(gray)
        std_dev = np.std(gray)

        # Plot histogram
        plt.figure(figsize=(8, 6))
        plt.plot(histogram, color='black')
        plt.title('Grayscale Histogram with Statistics')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')

        # Annotate with statistics
        stats_text = (f"Mean: {mean:.2f}\n"
                      f"Median: {median}\n"
                      f"Min: {min_val}\n"
                      f"Max: {max_val}\n"
                      f"Std Dev: {std_dev:.2f}")
        plt.text(0.95, 0.95, stats_text, transform=plt.gca().transAxes,
                 fontsize=10, verticalalignment='top', horizontalalignment='right',
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'))

        # Save the plot
        plt.savefig(f'static/images/{filename}')
        plt.close()

        return {
            "mean": mean,
            "median": median,
            "min": min_val,
            "max": max_val,
            "std_dev": std_dev
        }

    @staticmethod
    def contrast_stretching(image, custom_min=None, custom_max=None):
        # Convert to grayscale if the image is in color
        if len(image.shape) == 3:  # Color image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image  # Already grayscale

        # Set custom min and max values if provided, else use the image's min and max
        min_val = custom_min if custom_min is not None else np.min(gray)
        max_val = custom_max if custom_max is not None else np.max(gray)

        # Apply contrast stretching
        stretched = ((gray - min_val) / (max_val - min_val) * 255).astype('uint8')

        # Calculate pixel intensity frequencies
        original_frequencies = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        stretched_frequencies = cv2.calcHist([stretched], [0], None, [256], [0, 256]).flatten()

        return gray, stretched, original_frequencies, stretched_frequencies







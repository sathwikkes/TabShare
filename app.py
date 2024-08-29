from flask import Flask, request, render_template, jsonify
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import re
from difflib import get_close_matches
app = Flask(__name__)

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# /opt/homebrew/bin/tesseract

# def ocr_receipt(image_path):
#     # Perform OCR on the image
#     img = Image.open(image_path)
#     text = pytesseract.image_to_string(img)
#     items = extract_items(text)
#     return items

# def extract_items(text):
#     # Parse the text to extract items and their prices
#     # This function would need to be customized based on the receipt format
#     items = []
#     lines = text.split('\n')
#     for line in lines:
#         # Assume each line contains item and price separated by a space
#         parts = line.split()
#         if len(parts) >= 2:
#             item = ' '.join(parts[:-1])
#             try:
#                 price = float(parts[-1].replace('$', ''))
#                 items.append({'item': item, 'price': price})
#             except ValueError:
#                 continue
#     return items


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part provided'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         filepath = os.path.join('uploads', file.filename)
#         try:
#             file.save(filepath)
#         except Exception as e:
#             return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

#         try:
#             items = ocr_receipt(filepath)
#             if isinstance(items, list):
#                 return jsonify({'items': items})
#             else:
#                 return jsonify({'error': 'Failed to parse items'}), 500
#         except Exception as e:
#             return jsonify({'error': f'Failed to process OCR: {str(e)}'}), 500

#     return jsonify({'error': 'Unknown error occurred'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


def preprocess_image(image_path):
    """Preprocess the image to improve OCR accuracy."""
    img = Image.open(image_path)
    
    # Convert image to grayscale
    img = img.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    
    # Apply a sharpen filter
    img = img.filter(ImageFilter.SHARPEN)
    
    return img

def ocr_receipt(image_path):
    """Perform OCR on the preprocessed image."""
    img = preprocess_image(image_path)
    
    # Tesseract configuration
    config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$.'
    
    # Perform OCR using Tesseract with the specified config
    text = pytesseract.image_to_string(img, config=config)
    
    # Optional: Print or log the raw OCR text for debugging
    print("OCR Result:", text)
    print("----")
    # items = extract_items(text)
    # return items    

        # Capture each line and potential item-price pairs
    extracted_data = extract_items(text)
    
    return extracted_data

# def extract_items(text):
#     """Parse the text to extract items and their prices."""
#     items = []
#     lines = text.split('\n')
#     for line in lines:
#         parts = line.split()
#         if len(parts) >= 2:
#             item = ' '.join(parts[:-1])
#             try:
#                 price = float(parts[-1].replace('$', ''))
#                 items.append({'item': item, 'price': price})
#             except ValueError:
#                 continue
#     return items


def extract_items(text):
    """Capture each line and attempt to extract item and price, adding all to the list."""
    items = []
    lines = text.split('\n')  # Split text by lines
    
    for line in lines:
        # Debug: Print each line being processed
        print("Processing line:", line)
        
        # Simply add the line to the list of items regardless of its content
        items.append({'line': line})

    #     # Try to extract item and price if possible
    #     parts = line.split()
    #     if len(parts) >= 2:
    #         item = ' '.join(parts[:-1])
    #         try:
    #             # Attempt to parse the last part as a price
    #             price = float(parts[-1].replace('$', ''))
    #             # Add item and price to the list
    #             items.append({'item': item, 'price': price})
    #         except ValueError:
    #             # If price parsing fails, continue without adding a price
    #             continue
    
    # # Debug: Print the final items list
    # print("Final extracted items:", items)
    
    return items





@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part provided'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         filepath = os.path.join('uploads', file.filename)
#         try:
#             file.save(filepath)
#         except Exception as e:
#             return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

#         try:
#             items = ocr_receipt(filepath)
#             if isinstance(items, list):
#                 return jsonify({'items': items})
#             else:
#                 return jsonify({'error': 'Failed to parse items'}), 500
#         except Exception as e:
#             return jsonify({'error': f'Failed to process OCR: {str(e)}'}), 500

#     return jsonify({'error': 'Unknown error occurred'}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)

        try:
            # Perform OCR and capture lines
            extracted_data = ocr_receipt(filepath)
            
            # Return the extracted data as JSON
            return jsonify({'items': extracted_data})
        except Exception as e:
            print("Error processing OCR:", str(e))  # Print error to terminal
            return jsonify({'error': f'Failed to process OCR: {str(e)}'}), 500

    return jsonify({'error': 'Unknown error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)


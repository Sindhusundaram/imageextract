from flask import Flask, request, jsonify,render_template
from werkzeug.utils import secure_filename
import easyocr
import cv2
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            extracted_data = extract_specific_data(filename)
            for key, value in extracted_data.items():
                print(f'{key}: {value}')
            return jsonify(extracted_data)

        return jsonify({'error': 'Invalid file format'})
    return render_template("upload.html")

def extract_specific_data(image_path):

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray_image)
    print(result)

    extracted_data = {
        'A/c No': '',
        'Customer ID': '',
        'Name': '',
        'Date': ''
    }

    for detection in result:
        text = detection[1]

        if 'A/c.' in text:
   
            extracted_data['A/c No'] = text.split('A/c.')[1].strip()

        elif 'Customer ID' in text:
       
            extracted_data['Customer ID'] = text.split('Customer ID')[1].strip()

        elif 'NAME' in text:
   
            extracted_data['Name'] = text.split('NAME')[1].strip()

        elif 'Date:' in text:

            extracted_data['Date'] = text.split('Date:')[1].strip()

    return extracted_data

    

if __name__ == '__main__':
    app.run(debug=True)


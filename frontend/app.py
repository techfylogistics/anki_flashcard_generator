import sys
from flask import Flask, request, render_template, send_file
import os
#RK you need to import your module where you have code like below
from flashcard_generator  import main  # Import your script's processing function
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'


# Add the parent directory to the Python module search path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    # Save uploaded file
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(pdf_path)

    # Process the file with your script
    output_csv = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(file.filename)[0]}.csv")
    process_pdf(pdf_path, output_csv)  # Your function should take input and output paths

    # Provide CSV for download
    return send_file(output_csv, as_attachment=True)

def process_pdf(input_path, output_path):
    # Your logic here
    # Example: Read the PDF and write the CSV
    # RK you need to install flask : pip install flask
    #RK call your funtion from hre to generate the csv file like below
        # main(input_path,output_path) 

    #RK go to this frontend folder and run : python app.py and then access in browser : http://127.0.0.1:5000/
    #RK following is just for testing i kept, you can remove after doing above
    with open(input_path, 'rb') as pdf_file:
        # Process PDF
        csv_data = "example,data,from,pdf"
        with open(output_path, 'w') as csv_file:
            csv_file.write(csv_data)



if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True)

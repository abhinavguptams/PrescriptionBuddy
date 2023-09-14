from  implement import image_to_text
from flask import Flask, request


app = Flask(__name__)

@app.route('/prescriptiondetails', methods=['POST'])
def image_to_text_api():
    # Get the image from the request
    image_file = request.files['image']
    image_path = 'image.jpg'
    image_file.save(image_path)

    # Call the image_to_text function
    text = image_to_text(image_path)

    # Return the text as JSON
    return {'Prescription': text}



if __name__ == "__main__":
    app.run(debug=True)

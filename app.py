from flask import Flask, request, render_template
import base64
import io
from PIL import Image
import easyocr
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.post("/ocr")
def hello_world():
    print(request.values['image'])
    base64_image = request.values['image']

    # Remove 'data:image/png;base64,' from the start of the string if it's there
    if base64_image.startswith('data:image/png;base64,'):
        image = base64_image.replace('data:image/png;base64,', '', 1)

    # Convert the base64 string back to bytes
    image_bytes = base64.b64decode(image)

    # Open the image bytes as a PIL Image object
    image = Image.open(io.BytesIO(image_bytes))

    # Convert the PIL Image object back into a numpy array
    image_np = np.array(image)
    
    # Now you can use the numpy array with easyocr
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_np)
    print(result)

    # Extract text from each block and join them into a single string
    text = '<br>'.join([block[1] for block in result])

    return f"<p>{text}</p>"
    # return f"<p>Hello, World!</p><p>{base64_image}</p>"
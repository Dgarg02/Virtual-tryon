from flask import Flask, request, render_template
from PIL import Image
import requests
from io import BytesIO
import base64

app = Flask(__name__)

# Home route – displays the main page
@app.route('/')
def home():
    return render_template("index.html")

# Route to handle form submission and image transformation
@app.route("/preds", methods=['POST'])
def submit():
    try:
        # Get uploaded images
        cloth = request.files['cloth']
        model = request.files['model']

        # Update this URL to match your deployed model API
        url = "http://e793-34-123-73-186.ngrok-free.app/api/transform"
        print("Sending images to:", url)

        # Send the cloth and model to the model server
        response = requests.post(
            url,
            files={"cloth": cloth.stream, "model": model.stream}
        )

        # Check if response is successful
        if response.status_code != 200:
            return render_template("index.html", error="Failed to process image. Please try again.")

        # Convert response content to image
        result_image = Image.open(BytesIO(response.content))

        # Convert image to base64 string
        buffer = BytesIO()
        result_image.save(buffer, format="PNG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode()

        # Render page with output image
        return render_template("index.html", op=encoded_image)

    except Exception as e: 
        print("Error:", e)
        return render_template("index.html", error="An unexpected error occurred.")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)

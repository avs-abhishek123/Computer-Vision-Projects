from flask import Flask, request, jsonify, render_template
import cv2

app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

# Global variables
counter = 0
# Specify the directory to save the images and labels
SAVE_DIR = 'C:/Users/HP/Desktop/Computer-Vision-Projects/Manual_labelling/generated_dataset'

@app.route('/api/label', methods=['POST'])
def label_api():
    global counter  # Declare the counter variable as global

    # Get the bounding box coordinates and label from the request
    xmin = int(request.form['xmin'])
    ymin = int(request.form['ymin'])
    xmax = int(request.form['xmax'])
    ymax = int(request.form['ymax'])
    label = request.form['label']

    # Capture frame from the webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Draw the bounding box on the frame
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # Save the image
    image_filename = f'{SAVE_DIR}/images/image_{counter}.jpg'
    cv2.imwrite(image_filename, frame)

    # Write the label in YOLO format to a text file
    label_filename = f'{SAVE_DIR}/labels/label_{counter}.txt'
    with open(label_filename, 'w') as f:
        f.write(f"{label} {xmin} {ymin} {xmax} {ymax}\n")

    # Increment the counter
    counter += 1

    # Return a JSON response
    response = {
        'success': True,
        'image_filename': image_filename,
        'label_filename': label_filename
    }
    return jsonify(response)


def generate_frames():
    global counter

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Encode the frame as JPEG
        _, encoded_frame = cv2.imencode(".jpg", frame)
        frame_data = base64.b64encode(encoded_frame).decode("utf-8")

        yield "data:image/jpeg;base64," + frame_data

        time.sleep(0.1)  # Adjust the delay between frames if needed

@app.route("/video_stream")
def video_stream():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run()

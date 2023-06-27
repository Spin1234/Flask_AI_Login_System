import cv2
from cv2 import VideoCapture
import numpy as np
import face_recognition
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded images
app.config['KNOWN_FACES_FOLDER'] = 'known_faces'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # image = db.Column(db.LargeBinary)
    face_encoding = db.Column(db.PickleType, nullable=False)


@app.route('/')
def home():
    return render_template("home.html")

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         image_file = request.files['image']  # Get the uploaded image file

#         if image_file:
#             filename = secure_filename(image_file.filename)
#             image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#             with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
#                 image_data = f.read()

#             new_user = User(username=username, password=password, image=image_data)
#             db.session.add(new_user)
#             db.session.commit()

#             return redirect(url_for('login'))
#     return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        image_file = request.files['image']  # Get the uploaded image file

        if image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            face_encodings = face_recognition.face_encodings(image)

            if len(face_encodings) > 0:
                # Assuming only one face is present in the image
                face_encoding = face_encodings[0]

                # Convert the face encoding to a list for storage in the database
                face_encoding_list = face_encoding.tolist()

                new_user = User(username=username, password=password, face_encoding=face_encoding_list)
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for('login'))
            else:
                return 'No face found in the image. Try again.'
        else:
            return 'No image file provided. Try again.'
    return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # username = request.form['username']
#         # password = request.form['password']

#         # user = User.query.filter_by(username=username).first()
#         # if user and user.password == password:
#         #     return redirect(url_for('protected'))
#         # else:
#         #     return 'Invalid username or password'

#         image_file = request.files['image']
#         image = face_recognition.load_image_file(image_file)
#         face_encodings = face_recognition.face_encodings(image)

#         if len(face_encodings) > 0:
#             # Assuming only one face is present in the image
#             face_encoding = face_encodings[0]

#             # Retrieve the stored face encodings from the database or file
#             known_users = User.query.all()
#             known_face_encodings = [user.face_encoding for user in known_users]

#             # Compare face encodings
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#             if True in matches:
#                 return 'Login successful!'
#             else:
#                     return 'Face not recognized. Try again.'
#         else:
#             return 'No face found in the image. Try again.'
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        image_file = request.form['ci']

        # Open the primary video capture device (usually the webcam)
        if image_file:
            cap = cv2.VideoCapture(0)

            # Check if the webcam is opened successfully
            if not cap.isOpened():
                return "Failed to open the webcam"
            
            # Read and display frames from the webcam until 'q' is pressed
            while True:
                # Capture frame-by-frame
                ret, frame = cap.read()

                # If frame is read correctly, ret will be True
                if not ret:
                    return "Failed to capture the frame"

                # Display the resulting frame
                cv2.imshow("Webcam", frame)

                # Wait for the 'q' key to be pressed to capture the image
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    # Save the captured image
                    cv2.imwrite("captured_image.jpg", frame)

                    # Release the video capture object and close any open windows
                    cap.release()
                    cv2.destroyAllWindows()

                    # Perform face recognition on the captured image
                    image = face_recognition.load_image_file("captured_image.jpg")
                    face_encodings = face_recognition.face_encodings(image)

                    if len(face_encodings) > 0:
                        # Assuming only one face is present in the image
                        face_encoding = face_encodings[0]

                        # Retrieve the stored face encodings from the database or file
                        known_users = User.query.all()
                        known_face_encodings = [user.face_encoding for user in known_users]

                        # Compare face encodings
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                        if True in matches:
                            msg = 'Login successful!'
                            des = 'You have successfully logged in.'
                            return render_template("show.html", msg=msg, des=des)
                        else:
                            msg = 'Face not recognized. Try again.'
                            des = 'Try again'
                            return render_template("show.html", msg=msg, des=des)
                    else:
                        msg = 'No face found in the image. Try again.'
                        des = 'Try again'
                        return render_template("show.html", msg=msg, des=des)

            # Release the video capture object and close any open windows
            cap.release()
            cv2.destroyAllWindows()

    return render_template('login.html')



@app.route('/protected')
def protected():
    return 'This is a protected page'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

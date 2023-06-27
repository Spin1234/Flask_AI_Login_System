# Flask_AI_Login_System

This is a Python code for a face recognition login application using Flask. Let's go through the code and understand its different components.

1. Importing Libraries:
   - The code begins by importing the necessary libraries/modules:
     - `cv2`: OpenCV library for computer vision tasks.
     - `numpy`: Library for numerical computations.
     - `face_recognition`: Library for face recognition tasks.
     - `Flask`: Web framework for building the application.
     - `render_template`, `request`, `redirect`, `url_for`: Flask modules for handling web requests and rendering templates.
     - `SQLAlchemy`: ORM (Object-Relational Mapping) library for working with databases.
     - `Migrate`: Extension for Flask-SQLAlchemy that handles database migrations.
     - `secure_filename`, `os`: Modules for secure file uploading and working with the operating system.

2. Creating Flask App and Configurations:
   - An instance of the Flask app is created using `Flask(__name__)`.
   - Various configurations are set for the Flask app using `app.config`.
     - The `SQLALCHEMY_DATABASE_URI` configuration sets the path for the SQLite database file.
     - The `UPLOAD_FOLDER` configuration specifies the folder where uploaded images will be stored.
     - The `KNOWN_FACES_FOLDER` configuration specifies the folder where known faces will be stored.
   - The `db` object is created using `SQLAlchemy(app)` to handle the database operations.
   - The `migrate` object is created using `Migrate(app, db)` to handle database migrations.

3. Defining the Database Model:
   - The `User` class is defined as a subclass of `db.Model`, representing the table structure in the database.
   - It contains various columns such as `id`, `username`, `password`, and `face_encoding`.
   - The `face_encoding` column is of type `db.PickleType`, which allows storing Python objects in a serialized form.

4. Route: Home Page ("/"):
   - The `home()` function is decorated with `@app.route('/')`, which specifies the URL path for this route.
   - The function returns the rendered template "home.html".

5. Route: User Registration ("/register"):
   - The `register()` function is decorated with `@app.route('/register')`.
   - This route handles both GET and POST requests.
   - For a POST request, it retrieves the username, password, and image file from the form.
   - The image is saved in the designated `UPLOAD_FOLDER`.
   - The face in the image is recognized using the `face_recognition` library, and the face encoding is stored in the database.
   - If the registration is successful, it redirects to the login page.
   - If the image doesn't contain a face, an appropriate error message is displayed.

6. Route: User Login ("/login"):
   - The `login()` function is decorated with `@app.route('/login')`.
   - Similar to the registration route, it handles both GET and POST requests.
   - For a POST request, it captures an image from the webcam using OpenCV, saves it, and performs face recognition.
   - The stored face encodings are retrieved from the database, and the captured face encoding is compared to determine if it matches any known faces.
   - If the face is recognized, it displays a success message; otherwise, it displays an error message.

7. Route: Protected Page ("/protected"):
   - The `protected()` function is decorated with `@app.route('/protected')`.
   - This route is a placeholder for a protected page that requires authentication.

8. Running the Flask App:
   - The `if __name__ == '__main__'` block ensures that the app is only run if the script is executed directly.
   - It starts the Flask development server using `app.run(debug=True)`.

# What is face encoding?

Face encoding is a numerical representation of a face that captures the unique features and characteristics of the face. It is a mathematical representation of the face that can be used for tasks like face recognition, face comparison, and face identification.

In the context of the face recognition project you provided, the face encoding is calculated using the face_recognition library. It takes an input image containing a face and processes it to extract facial landmarks, such as the location of the eyes, nose, and mouth. These facial landmarks are then used to compute a numerical encoding vector that represents the face.

The face encoding vector typically has a fixed length and contains a set of numerical values. Each value in the encoding vector represents a specific feature or characteristic of the face. The values are carefully calculated to be robust to variations in lighting, pose, and other factors.

When comparing faces, the face encodings of two faces can be compared using distance metrics like Euclidean distance or cosine similarity. If the distance between two face encodings is below a certain threshold, it indicates a potential match, suggesting that the two faces belong to the same individual.

By using face encodings, the system can compare the encoding of a captured face during login with the encodings of known faces stored in the database. This enables the system to determine if the captured face matches any of the known faces, allowing for face recognition and authentication.

Overall, face encoding plays a crucial role in representing faces numerically and enabling accurate face recognition and identification in the context of the face recognition project.

# How it works??

Face encoding works by extracting and quantifying the unique features of a face in a way that can be represented numerically. Here is a simplified explanation of how face encoding works:

1. Face Detection: The first step is to detect the presence of a face in an input image. This is typically done using computer vision techniques such as Haar cascades or deep learning-based face detection models. The detected face region is then extracted from the image.

2. Facial Landmark Detection: Once the face region is identified, the next step is to detect facial landmarks, which are specific points on the face that indicate the positions of key facial features. Common landmarks include the corners of the eyes, the tip of the nose, and the corners of the mouth. Facial landmark detection algorithms use machine learning models to locate these points accurately.

3. Normalization: After detecting the facial landmarks, the face region is normalized to ensure consistency across different images. Normalization techniques involve aligning the face based on the positions of the landmarks. This step helps to account for variations in pose, scale, and rotation.

4. Feature Extraction: With the normalized face, the next step is to extract relevant features that capture the distinctive characteristics of the face. This is typically done by applying deep learning models, such as convolutional neural networks (CNNs), that have been trained specifically for face recognition tasks. These models analyze the face region and extract high-level features that are important for distinguishing one face from another.

5. Encoding Calculation: Once the features are extracted, they are used to compute a face encoding vector, which is a compact numerical representation of the face. This encoding vector summarizes the unique characteristics of the face in a way that can be easily compared with other face encodings. Different face recognition libraries and algorithms may use different techniques to calculate the encoding vector.

6. Encoding Comparison: When comparing faces, the face encodings of different faces are compared using distance metrics, such as Euclidean distance or cosine similarity. The distance between two face encodings reflects the similarity or dissimilarity between the faces. A lower distance suggests a closer match, indicating that the faces are likely to belong to the same individual, while a higher distance indicates a dissimilar match.

In the face recognition project you provided, the face encoding process is used during both user registration and login. During registration, the encoding of a user's face is calculated and stored in the database. During login, the captured face is encoded, and its encoding is compared with the stored face encodings to determine if there is a match.

By representing faces as numerical encodings, face recognition systems can efficiently compare faces and make reliable decisions about their identity. This allows for accurate face matching and authentication in various applications, such as access control, surveillance, and identity verification.

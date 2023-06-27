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
   - The `if __name__ == '__main__'` block ensures that the

 app is only run if the script is executed directly.
   - It starts the Flask development server using `app.run(debug=True)`.

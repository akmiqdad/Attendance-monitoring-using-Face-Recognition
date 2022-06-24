# Attendance System Using Face Recognition with College Enquiry System

## About

In this project,
an automated attendance marking and management system is proposed by making use
of face detection and recognition. The main objective of this work is to make
the attendance marking and management system efficient, time saving, simple and easy.
A chatbot that can be accessed through login is proposed here to answer the queries of students. In
this project, we are aimed to implement an online chatbot system to assist users, allowing users to communicate with college chatbot so it will be able to generate a response and to give solutions to
queries without consuming time.

**Django** web framework was used for the development of the whole web app. **OpenCv and face_recognition API's** were used for the development of Face Recognizer. The Face Recognizer can detect multiple faces at a time and mark their attendance into Database.
**Note: Python version 3.7 was used for this project. And the dlib package required for installation of face_recognition api.**
To run the web app on your local computer, install the required libraries([requirements.txt](https://github.com/venugopalkadamba/Face_Verification_based_Attendance_system/blob/master/requirements.txt)) using the command:

```python
pip3 install -r requirements.txt
```

and run the following command in the command prompt:

```python
python manage.py runserver
```

**To create your own credential for logging into the application**

```python
python manage.py createsuperuser
```

After running the above command and creating the credentials, you can use the same credentials for logging in.

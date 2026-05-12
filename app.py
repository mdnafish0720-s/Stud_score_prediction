# import streamlit as st
# import numpy as np
# import joblib
# import warnings
# warnings.filterwarnings('ignore')

# model=joblib.load('final_student_performance_model.pkl')

# st.title('Student Performance Prediction')  

# st.write('Enter the following details to predict the student performance:')

# study_hours = st.slider('Study Hours per Day', 0.0, 12.0, 2.0)
# attendance = st.slider('Attendance (%)', 0.0, 100.0, 80.0)
# mental_health = st.slider('Mental Health Rating (1-10)', 1, 10, 5)   
# sleep_hours = st.slider('Sleep Hours per Night', 0.0, 12.0, 7.0)  
# part_time_job = st.selectbox('Part-time Job', ['No', 'Yes'])    


# ptj_encoded = 1 if part_time_job == 'Yes' else 0

# if st.button('Predict Performance'):
    
#     input_data = np.array([[study_hours, attendance, mental_health, sleep_hours, ptj_encoded]])
#     prediction = model.predict(input_data)[0]
    
#     prediction=max(0, min(100, prediction))

#     st.success(f'Predicted Student Performance: {prediction:.2f}')


# import streamlit as st
# import numpy as np
# import joblib
# import warnings
# import json
# import os

# warnings.filterwarnings('ignore')

# # Load model
# model = joblib.load('final_student_performance_model.pkl')

# # ---------------- USER AUTH ---------------- #

# USER_FILE = "users.json"

# # Create users.json if not exists
# if not os.path.exists(USER_FILE):
#     with open(USER_FILE, "w") as f:
#         json.dump({}, f)

# # Load users
# with open(USER_FILE, "r") as f:
#     users = json.load(f)

# # Session State
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "username" not in st.session_state:
#     st.session_state.username = ""

# # ---------------- FUNCTIONS ---------------- #

# def signup(username, password):
#     if username in users:
#         return False, "Username already exists!"

#     users[username] = password

#     with open(USER_FILE, "w") as f:
#         json.dump(users, f)

#     return True, "Signup successful!"

# def login(username, password):
#     if username in users and users[username] == password:
#         return True
#     return False

# # ---------------- APP TITLE ---------------- #

# st.title("🎓 Student Performance Prediction App")

# # =====================================================
# # AUTH PAGE
# # =====================================================

# if not st.session_state.logged_in:

#     auth_option = st.radio(
#         "Choose Option",
#         ["Login", "Signup"]
#     )

#     # ---------------- LOGIN ---------------- #

#     if auth_option == "Login":

#         st.subheader("Login")

#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")

#         if st.button("Login"):

#             if login(username, password):

#                 st.session_state.logged_in = True
#                 st.session_state.username = username

#                 st.success(f"Welcome {username}!")
#                 st.rerun()

#             else:
#                 st.error("Invalid username or password")

#     # ---------------- SIGNUP ---------------- #

#     else:

#         st.subheader("Signup")

#         new_user = st.text_input("Create Username")
#         new_password = st.text_input("Create Password", type="password")

#         if st.button("Signup"):

#             success, message = signup(new_user, new_password)

#             if success:

#                 # Auto login after signup
#                 st.session_state.logged_in = True
#                 st.session_state.username = new_user

#                 st.success("Account created successfully!")
#                 st.rerun()

#             else:
#                 st.error(message)

# # =====================================================
# # PREDICTION PAGE
# # =====================================================

# else:

#     # Sidebar
#     st.sidebar.success(f"Logged in as {st.session_state.username}")

#     if st.sidebar.button("Logout"):

#         st.session_state.logged_in = False
#         st.session_state.username = ""

#         st.rerun()

#     # Prediction UI
#     st.header("📊 Predict Student Performance")

#     st.write("Enter the following details:")

#     study_hours = st.slider(
#         'Study Hours per Day',
#         0.0, 12.0, 2.0
#     )

#     attendance = st.slider(
#         'Attendance (%)',
#         0.0, 100.0, 80.0
#     )

#     mental_health = st.slider(
#         'Mental Health Rating (1-10)',
#         1, 10, 5
#     )

#     sleep_hours = st.slider(
#         'Sleep Hours per Night',
#         0.0, 12.0, 7.0
#     )

#     part_time_job = st.selectbox(
#         'Part-time Job',
#         ['No', 'Yes']
#     )

#     # Encode
#     ptj_encoded = 1 if part_time_job == 'Yes' else 0

#     # Predict
#     if st.button("Predict Performance"):

#         input_data = np.array([[
#             study_hours,
#             attendance,
#             mental_health,
#             sleep_hours,
#             ptj_encoded
#         ]])

#         prediction = model.predict(input_data)[0]

#         prediction = max(0, min(100, prediction))

        
#         st.success(
#             f"Predicted Student Performance: {prediction:.2f}"
#         )


import streamlit as st
import numpy as np
import pandas as pd
import joblib
import warnings
import sqlite3

warnings.filterwarnings('ignore')

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load('final_student_performance_model.pkl')

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

conn.commit()

# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================================
# FUNCTIONS
# =====================================================

def signup(username, password):

    c.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    if c.fetchone():
        return False, "Username already exists!"

    c.execute(
        "INSERT INTO users(username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()

    return True, "Signup successful!"

def login(username, password):

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    data = c.fetchone()

    if data:
        return True

    return False

# =====================================================
# APP TITLE
# =====================================================

st.title("🎓 Student Performance Prediction App")

# =====================================================
# AUTH PAGE
# =====================================================

if not st.session_state.logged_in:

    auth_option = st.radio(
        "Choose Option",
        ["Login", "Signup"]
    )

    # ---------------- LOGIN ---------------- #

    if auth_option == "Login":

        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if login(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(f"Welcome {username}!")
                st.rerun()

            else:
                st.error("Invalid username or password")

    # ---------------- SIGNUP ---------------- #

    else:

        st.subheader("📝 Signup")

        new_user = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")

        if st.button("Signup"):

            success, message = signup(new_user, new_password)

            if success:

                st.session_state.logged_in = True
                st.session_state.username = new_user

                st.success("Account created successfully!")
                st.rerun()

            else:
                st.error(message)

# =====================================================
# PREDICTION PAGE
# =====================================================

else:

    # Sidebar
    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    # Prediction Section
    st.header("📊 Predict Student Performance")

    study_hours = st.slider(
        'Study Hours per Day',
        0.0, 12.0, 2.0
    )

    attendance = st.slider(
        'Attendance (%)',
        0.0, 100.0, 80.0
    )

    mental_health = st.slider(
        'Mental Health Rating (1-10)',
        1, 10, 5
    )

    sleep_hours = st.slider(
        'Sleep Hours per Night',
        0.0, 12.0, 7.0
    )

    part_time_job = st.selectbox(
        'Part-time Job',
        ['No', 'Yes']
    )

    # Encode categorical feature
    ptj_encoded = 1 if part_time_job == 'Yes' else 0

    # Prediction Button
    if st.button("Predict Performance"):

        input_data = np.array([[

            study_hours,
            attendance,
            mental_health,
            sleep_hours,
            ptj_encoded

        ]])

        prediction = model.predict(input_data)[0]

        prediction = max(0, min(100, prediction))

        st.success(
            f"Predicted Student Performance: {prediction:.2f}"
        )

    # # =====================================================
    # # VIEW DATABASE
    # # =====================================================

    # st.subheader("📁 Users Database")

    # if st.button("Show Database"):

    #     c.execute("SELECT * FROM users")

    #     data = c.fetchall()

    #     df = pd.DataFrame(
    #         data,
    #         columns=["Username", "Password"]
    #     )

    #     st.dataframe(df)
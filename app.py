import streamlit as st
import pandas as pd
import pickle
import base64
from io import BytesIO
from PIL import Image
import requests
from report_generator import generate_report
from diet_recommendations import get_diet_recommendations

# Set page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Function to navigate between pages
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Heart disease prediction function
def predict_heart_disease(user_data):
    # Load the model
    with open('heart_disease_model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    # Create a DataFrame from user data
    input_df = pd.DataFrame([{
        'age': user_data['age'],
        'sex': 1 if user_data['gender'] == 'Male' else 0,
        'cp': int(user_data['chest_pain_type']),
        'trestbps': user_data['blood_pressure'],
        'chol': user_data['cholesterol']
    }])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    return bool(prediction)

# Function to get image as base64
def get_image_base64(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img_resized = img.resize((400, 300))
    buffered = BytesIO()
    img_resized.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Get heart images
heart_image_1 = "https://pixabay.com/get/g918fe6c03ecb945018127f1f619de9c20d2e30a757b3d3a89e06980bc1a5dfac1e1171832b695971630f66084b08647381873a33514b443eb01ac375a510d556_1280.jpg"
heart_image_2 = "https://pixabay.com/get/g7d722d3469313ad7bbfb033901376ac6682db1fe0d745646c1bdacfab2e0e1f3131ff84ac0aa1a534da7eeb0a5fecb5f8aaae9fbabf4cc9bffc51c47c5ba85a5_1280.jpg"

# Get food images
food_images = [
    "https://pixabay.com/get/gb4e6036085cd6071e7a82005f2590c728dce4a00f944db39351f59d3f8d01c5391abcb5742ff4d6ef0f7b70d72ee8781426dff6fba15059b408eb9bedb8039c8_1280.jpg",
    "https://pixabay.com/get/g0f984fc514c525d5e3de1acfd2eb5507e8aac42f8802274fdbf78c173dce2915bad257f822253d626dded94a758014d66fa5e18da4b7c69ae2a0cc5a2e8d7056_1280.jpg",
    "https://pixabay.com/get/g4f1225618fc43b70995d5892663e83e96448711b29529e997a5e6e3203df125b8339c2eca794405e51f517b30cc746854eb06bb8a7218c9c8e81837c2a4ce145_1280.jpg",
    "https://pixabay.com/get/gbb3a9e8c212b50949c80292c570f0044e3f11a28617b63cfd5191b5c34ce639636995dd06ab1b8a3b941392253f5064b650b8d2809a7e850f98ea7f04aa09e30_1280.jpg"
]

# HOME PAGE
if st.session_state.page == 'home':
    st.title("Early Heart Attack Prediction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        Welcome to the Early Heart Attack Prediction application. 
        This tool helps assess your risk of heart disease based on various health parameters.
        Please provide your details for an accurate assessment.
        """)
        
        # Display form to collect user data
        with st.form("user_data_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            gender = st.selectbox("Gender", ["Male", "Female"])
            blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=90, max_value=200, step=1)
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=500, step=1)
            
            # Chest pain type with descriptions
            chest_pain_options = {
                "0": "No Pain (0)",
                "1": "Typical Angina (1)",
                "2": "Atypical Angina (2)",
                "3": "Non-anginal Pain (3)"
            }
            chest_pain_type = st.selectbox(
                "Chest Pain Type", 
                list(chest_pain_options.values())
            )
            # Extract the numeric value from the selected option
            chest_pain_type = chest_pain_type.split('(')[1].split(')')[0]
            
            submit_button = st.form_submit_button("Check Heart Disease Risk")
            
            if submit_button:
                if not name or age < 18 or not blood_pressure or not cholesterol:
                    st.error("Please fill all the fields with valid values.")
                else:
                    # Store user data in session state
                    st.session_state.user_data = {
                        'name': name,
                        'age': age,
                        'gender': gender,
                        'blood_pressure': blood_pressure,
                        'cholesterol': cholesterol,
                        'chest_pain_type': chest_pain_type
                    }
                    
                    # Make prediction
                    prediction = predict_heart_disease(st.session_state.user_data)
                    st.session_state.prediction = prediction
                    
                    # Navigate to results page
                    navigate_to('results')
    
    with col2:
        # Display heart image
        st.image(heart_image_1, use_container_width=True)

# RESULTS PAGE
elif st.session_state.page == 'results':
    # Apply different styling based on prediction
    if st.session_state.prediction:
        st.markdown(
            """
            <style>
            .main-header {color: #FF0000;}
            </style>
            """, 
            unsafe_allow_html=True
        )
        header_text = "Heart Disease Detected"
    else:
        st.markdown(
            """
            <style>
            .main-header {color: #00AA00;}
            </style>
            """, 
            unsafe_allow_html=True
        )
        header_text = "No Heart Disease Detected"
    
    st.markdown(f"<h1 class='main-header'>{header_text}</h1>", unsafe_allow_html=True)
    
    # Display user information
    st.subheader("Your Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {st.session_state.user_data['name']}")
        st.write(f"**Age:** {st.session_state.user_data['age']}")
        st.write(f"**Gender:** {st.session_state.user_data['gender']}")
    
    with col2:
        st.write(f"**Blood Pressure:** {st.session_state.user_data['blood_pressure']} mmHg")
        st.write(f"**Cholesterol:** {st.session_state.user_data['cholesterol']} mg/dL")
        st.write(f"**Chest Pain Type:** {st.session_state.user_data['chest_pain_type']}")
    
    # Display diet recommendations button
    if st.button("View Diet Recommendations"):
        navigate_to('diet')
    
    # Generate and download report
    if st.button("Download Report"):
        report = generate_report(
            st.session_state.user_data,
            st.session_state.prediction,
            get_diet_recommendations(st.session_state.prediction)
        )
        
        # Create download button for the PDF
        b64_pdf = base64.b64encode(report).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="heart_health_report.pdf">Click here to download your report</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    # Button to go back to home
    if st.button("Start Over"):
        # Reset session state
        st.session_state.prediction = None
        st.session_state.user_data = {}
        navigate_to('home')

# DIET RECOMMENDATIONS PAGE
elif st.session_state.page == 'diet':
    if st.session_state.prediction:
        st.title("Diet Recommendations for Heart Health Improvement")
        background_color = "#FFEEEE"  # Light red background
    else:
        st.title("Diet Recommendations for Heart Health Maintenance")
        background_color = "#EEFFEE"  # Light green background
    
    # Display the recommendations
    st.markdown(
        f"""
        <div style="background-color:{background_color}; padding:20px; border-radius:10px;">
        <h3>Personalized Diet Plan for {st.session_state.user_data['name']}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Get appropriate diet recommendations
    recommendations = get_diet_recommendations(st.session_state.prediction)
    
    # Display recommendations with food images
    col1, col2 = st.columns([3, 1])
    
    with col1:
        for section, items in recommendations.items():
            st.subheader(section)
            for item in items:
                st.write(f"- {item}")
            st.write("")
    
    with col2:
        # Display a food image
        st.image(food_images[0], use_container_width=True)
        st.image(food_images[1], use_container_width=True)
    
    # Buttons for navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Back to Results"):
            navigate_to('results')
    
    with col2:
        if st.button("Generate Report"):
            report = generate_report(
                st.session_state.user_data,
                st.session_state.prediction,
                recommendations
            )
            
            # Create download button for the PDF
            b64_pdf = base64.b64encode(report).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="heart_health_report.pdf">Click here to download your report</a>'
            st.markdown(href, unsafe_allow_html=True)

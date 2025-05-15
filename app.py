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
    # Apply custom CSS for social media-like interface
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .css-18e3th9 {
        padding-top: 0rem;
        padding-bottom: 10rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
        padding-right: 1rem;
        padding-bottom: 3.5rem;
        padding-left: 1rem;
    }
    .st-bq {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-style {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader-style {
        font-size: 1.2rem;
        font-weight: 500;
        color: #4a4a4a;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App header in social media style
    st.markdown("<div class='header-style'>Early Heart Attack Prediction</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader-style'>Know your heart health status instantly</div>", unsafe_allow_html=True)
    
    # Display large heart image at the top
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(heart_image_2, use_container_width=True)
    
    # Information and form section
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #262730;'>Complete Your Health Assessment</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Card-like container for the welcome message
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color: #262730;">Welcome!</h4>
        <p>This application helps assess your risk of heart disease based on various health parameters.
        Please provide your details below for an accurate assessment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display form to collect user data in a card-like container
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
        # Display heart image with card-like styling
        st.markdown("""
        <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        st.image(heart_image_1, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; font-style: italic; font-size: 0.9rem;">
            Keep your heart healthy with regular checkups
        </div>
        </div>
        """, unsafe_allow_html=True)

# RESULTS PAGE
elif st.session_state.page == 'results':
    # Apply custom CSS for social media-like interface
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .user-icon {
        background-color: #e0e0ef;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-size: 20px;
        font-weight: bold;
    }
    .user-name {
        font-weight: bold;
        font-size: 1.2rem;
    }
    .timestamp {
        color: #888;
        font-size: 0.8rem;
    }
    .button-container {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .action-button {
        border-radius: 20px;
        padding: 8px 16px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Apply different styling based on prediction
    if st.session_state.prediction:
        header_color = "#FF0000"
        background_color = "#FFEEEE"
        header_text = "Heart Disease Detected"
        card_border = "border-left: 4px solid #FF0000;"
        emoji = "⚠️"
    else:
        header_color = "#00AA00"
        background_color = "#EEFFEE"
        header_text = "No Heart Disease Detected"
        card_border = "border-left: 4px solid #00AA00;"
        emoji = "✅"
    
    # Create header with notification-style
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 2.5rem; font-weight: bold; color: {header_color};">{header_text}</div>
        <div style="font-size: 1.2rem; color: #4a4a4a;">Assessment completed on {pd.Timestamp.now().strftime('%B %d, %Y')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a card for user information with normal readable text
    # First create the card container
    st.markdown(f"""
    <div class="card" style="{card_border}">
    """, unsafe_allow_html=True)
    
    # Add user profile header
    st.subheader(f"{st.session_state.user_data['name']}'s Health Profile")
    
    # Add assessment result
    st.markdown(f"""
    <div style="padding: 15px; background-color: {background_color}; border-radius: 8px; margin: 15px 0;">
        <span style="font-size: 1.3rem; font-weight: 500;">{emoji} {header_text}</span>
        <p style="margin-top: 10px;">
            Based on your provided health information, our assessment shows 
            {'indicators of heart disease risk factors' if st.session_state.prediction else 'no significant indicators of heart disease'}.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display user information in a clean format
    st.write("### Your Health Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Age:** {st.session_state.user_data['age']} years")
        st.write(f"**Gender:** {st.session_state.user_data['gender']}")
        st.write(f"**Chest Pain Type:** Type {st.session_state.user_data['chest_pain_type']}")
    
    with col2:
        st.write(f"**Blood Pressure:** {st.session_state.user_data['blood_pressure']} mmHg")
        st.write(f"**Cholesterol:** {st.session_state.user_data['cholesterol']} mg/dL")
    
    # Close the card div
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create action buttons in a social media style
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 5px;">🥗</div>
            <div style="font-weight: 500; margin-bottom: 5px;">Diet Plan</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Recommendations", key="diet_button"):
            navigate_to('diet')
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 5px;">📋</div>
            <div style="font-weight: 500; margin-bottom: 5px;">Health Report</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Download PDF", key="report_button"):
            report = generate_report(
                st.session_state.user_data,
                st.session_state.prediction,
                get_diet_recommendations(st.session_state.prediction)
            )
            
            # Create download button for the PDF
            b64_pdf = base64.b64encode(report).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="heart_health_report.pdf" style="text-decoration: none;"><div style="text-align: center; background-color: #f0f0f0; padding: 8px; border-radius: 5px; color: #333; font-weight: 500;">Download Report</div></a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 5px;">🏠</div>
            <div style="font-weight: 500; margin-bottom: 5px;">New Assessment</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Over", key="home_button"):
            # Reset session state
            st.session_state.prediction = None
            st.session_state.user_data = {}
            navigate_to('home')
            
    # Add disclaimer at the bottom
    st.markdown("""
    <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 10px; font-size: 0.9rem; color: #666;">
        <strong>Disclaimer:</strong> This assessment is for informational purposes only and is not a substitute for professional medical advice. 
        Please consult with a healthcare provider for proper diagnosis and treatment.
    </div>
    """, unsafe_allow_html=True)

# DIET RECOMMENDATIONS PAGE
elif st.session_state.page == 'diet':
    # Apply custom CSS for social media-like interface
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .food-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .food-card:hover {
        transform: translateY(-5px);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 8px;
    }
    .food-item {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        padding: 8px;
        border-radius: 8px;
        background-color: #f8f9fa;
    }
    .food-icon {
        margin-right: 15px;
        font-size: 1.2rem;
    }
    .food-text {
        font-size: 1rem;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.prediction:
        header_text = "Diet Recommendations for Heart Health Improvement"
        background_color = "#FFEEEE"  # Light red background
        border_color = "#ff4b4b"
        icon = "❤️‍🩹"
    else:
        header_text = "Diet Recommendations for Heart Health Maintenance"
        background_color = "#EEFFEE"  # Light green background
        border_color = "#00AA00"
        icon = "💚"
    
    # Instagram-like header
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 2.2rem; font-weight: bold; color: #262730;">{icon} {header_text}</div>
        <div style="font-size: 1.2rem; color: #4a4a4a; margin-top: 10px;">
            Personalized nutrition advice for {st.session_state.user_data['name']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get appropriate diet recommendations
    recommendations = get_diet_recommendations(st.session_state.prediction)
    
    # Show featured image in a card like Instagram post
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div class="food-card" style="border-top: 5px solid {border_color};">
            <div style="text-align: center; margin-bottom: 15px;">
                <div style="font-weight: 600; font-size: 1.2rem;">Featured Healthy Foods</div>
            </div>
        """, unsafe_allow_html=True)
        st.image(food_images[2], use_container_width=True)
        st.markdown("""
            <div style="text-align: center; font-style: italic; color: #666; margin-top: 10px;">
                A nutritious diet is essential for heart health
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display recommendations in a social media feed style
    food_icons = ["🥗", "🥦", "🍎", "🥑", "🐟", "🫐", "🍗", "🍚", "🥛", "🌰"]
    
    for i, (section, items) in enumerate(recommendations.items()):
        st.markdown(f"""
        <div class="food-card">
            <div class="section-header">{section}</div>
        """, unsafe_allow_html=True)
        
        for j, item in enumerate(items):
            icon = food_icons[(i + j) % len(food_icons)]
            st.markdown(f"""
            <div class="food-item">
                <div class="food-icon">{icon}</div>
                <div class="food-text">{item}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Display food gallery
    st.markdown("""
    <div style="margin: 30px 0;">
        <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 15px; text-align: center;">
            Healthy Food Gallery
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display food images in a grid
    col1, col2 = st.columns(2)
    with col1:
        st.image(food_images[0], use_container_width=True, caption="Fresh Fruits & Vegetables")
    with col2:
        st.image(food_images[1], use_container_width=True, caption="Whole Grains & Nuts")
    
    # Action buttons in a fixed bottom bar style
    st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: white; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); padding: 15px 0; z-index: 1000;">
        <div style="display: flex; justify-content: space-around; max-width: 800px; margin: 0 auto;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 5px;">👈</div>
            <div style="font-weight: 500; font-size: 0.9rem;">Back to Results</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Return", key="back_button"):
            navigate_to('results')
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 5px;">📱</div>
            <div style="font-weight: 500; font-size: 0.9rem;">Share Diet Plan</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Report", key="report_button_diet"):
            report = generate_report(
                st.session_state.user_data,
                st.session_state.prediction,
                recommendations
            )
            
            # Create download button for the PDF
            b64_pdf = base64.b64encode(report).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="heart_health_report.pdf" style="text-decoration: none;"><div style="text-align: center; background-color: #f0f0f0; padding: 8px; border-radius: 5px; color: #333; font-weight: 500;">Download Report</div></a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 5px;">🏠</div>
            <div style="font-weight: 500; font-size: 0.9rem;">New Assessment</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start New", key="home_button_diet"):
            # Reset session state
            st.session_state.prediction = None
            st.session_state.user_data = {}
            navigate_to('home')
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Add padding at the bottom to account for the fixed bar
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

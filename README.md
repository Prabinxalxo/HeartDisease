 HEAD
# HeartDisease

# Heart Disease Prediction Application

A mobile-friendly application for heart attack risk prediction with personalized diet recommendations and downloadable reports.

## Features

- User-friendly interface with social media-like design
- Heart disease prediction based on medical parameters
- Personalized diet recommendations
- Downloadable PDF reports
- Mobile-responsive design

## Deploying to Render

### Manual Deployment

1. Create a new Web Service on Render
2. Link your GitHub repository
3. Configure the following settings:
   - **Name**: heart-disease-prediction (or your preferred name)
   - **Environment**: Python
   - **Region**: Choose the region closest to your users
   - **Branch**: main (or your default branch)
   - **Build Command**: `pip install -r render_requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.headless true --server.address 0.0.0.0`
   - **Python Version**: 3.11.0 (or compatible version)

4. Click "Create Web Service" and your application will be deployed

### Automatic Deployment with Blueprint

If your GitHub repository contains the `render.yaml` file, you can:

1. Create a new Blueprint on Render
2. Link your GitHub repository
3. Render will automatically read the configuration from `render.yaml`
4. Click "Apply" to deploy your application

## Local Development

1. Install the required packages:
   ```
   pip install -r render_requirements.txt
   ```

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Generate the trained model (if needed):
   ```
   python model.py
   ```

## Files Description

- `app.py`: Main Streamlit application
- `model.py`: Heart disease prediction model
- `diet_recommendations.py`: Diet recommendations generation
- `report_generator.py`: PDF report generation
- `heart_disease_model.pkl`: Trained ML model
   f9e669e (Fuck)

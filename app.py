from flask import Flask, render_template, request, redirect, url_for, jsonify
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename
from chatbot import LungCancerChatbot

# Explicitly check for PIL/Pillow before proceeding
try:
    import PIL
    from PIL import Image
    from tensorflow.keras.preprocessing import image
except ImportError:
    raise ImportError(
        "This application requires the Pillow library. "
        "Please install it with: pip install pillow"
    )

app = Flask(__name__)

# Load the saved model
model = tf.keras.models.load_model('lung_cancer_model.h5')

# Define class labels
class_labels = {0: 'adenocarcinoma', 1: 'large.cell.carcinoma', 2: 'normal', 3: 'squamous.cell.carcinoma'}

# Update paths for proper static file serving
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize chatbot
api_key = "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"
chatbot = LungCancerChatbot(api_key, model="anthropic/claude-3-haiku")
chatbot.add_context()

# Define recommendations based on prediction results
def get_recommendations(prediction):
    # Base recommendations that will be enhanced with AI-generated content
    base_recommendations = {
        'adenocarcinoma': {
            'description': 'Adenocarcinoma is a type of non-small cell lung cancer that forms in the outer parts of the lung. It is often found in current or former smokers, but it is also the most common type of lung cancer seen in non-smokers.',
            'next_steps': [
                'Consult with an oncologist specializing in lung cancer immediately',
                'Consider additional imaging tests like PET scans to determine if cancer has spread',
                'Prepare for biopsy to confirm diagnosis and perform molecular testing',
                'Evaluate treatment options including surgery, radiation therapy, or chemotherapy',
                'Genetic testing for targeted therapy options such as EGFR, ALK, ROS1, or BRAF mutations'
            ],
            'resources': [
                'American Lung Association: lung.org',
                'LUNGevity Foundation: lungevity.org',
                'National Cancer Institute: cancer.gov/types/lung'
            ]
        },
        'large.cell.carcinoma': {
            'description': 'Large cell carcinoma is an aggressive type of non-small cell lung cancer characterized by large, abnormal-looking cells. It tends to grow quickly and spread early to other parts of the body.',
            'next_steps': [
                'Immediate consultation with a pulmonary oncologist',
                'Complete staging workup including brain MRI and PET scan',
                'Discuss biopsy options for definitive diagnosis',
                'Consider treatment options including surgery and adjuvant therapy',
                'Evaluate for clinical trials that may be appropriate given the aggressive nature'
            ],
            'resources': [
                'American Cancer Society: cancer.org/cancer/lung-cancer',
                'GO2 Foundation for Lung Cancer: go2foundation.org',
                'ClinicalTrials.gov - Search for "large cell carcinoma" clinical trials'
            ]
        },
        'normal': {
            'description': 'No signs of lung cancer were detected in the image. This indicates normal lung tissue without evidence of malignancy.',
            'next_steps': [
                'Continue regular health check-ups as recommended by your physician',
                'Maintain a healthy lifestyle including a balanced diet and regular exercise',
                'If you smoke, consider quitting - talk to your doctor about smoking cessation programs',
                'If you have symptoms despite this result, consider follow-up testing or a second opinion',
                'Discuss any concerns or persistent symptoms with your primary care physician'
            ],
            'resources': [
                'American Lung Association - Lung Health: lung.org/lung-health',
                'Centers for Disease Control - Quit Smoking: cdc.gov/tobacco/quit_smoking',
                'National Lung Screening Trial Information: cancer.gov/types/lung/research/nlst'
            ]
        },
        'squamous.cell.carcinoma': {
            'description': 'Squamous cell carcinoma is a type of non-small cell lung cancer that typically develops in the central part of the lungs, near the main bronchus. It is strongly associated with a history of smoking.',
            'next_steps': [
                'Seek consultation with a thoracic oncologist as soon as possible',
                'Additional testing to determine cancer stage including mediastinoscopy',
                'Evaluate treatment options such as surgery, radiation, and chemotherapy',
                'Consider immunotherapy options which may be effective for this cancer type',
                'Request PD-L1 testing to determine eligibility for immunotherapy'
            ],
            'resources': [
                'Lung Cancer Research Foundation: lcrf.org',
                'National Comprehensive Cancer Network: nccn.org/patients/guidelines/lung-nsclc',
                'Cancer Support Community: cancersupportcommunity.org/lung-cancer'
            ]
        }
    }
    
    default_recommendation = {
        'description': 'Information not available for this specific finding.',
        'next_steps': [
            'Consult with a healthcare professional to interpret these results',
            'Schedule a follow-up appointment with a pulmonologist',
            'Consider additional diagnostic testing for clarification'
        ],
        'resources': [
            'American Lung Association: lung.org',
            'National Cancer Institute: cancer.gov'
        ]
    }
    
    # Get base recommendation
    recommendation = base_recommendations.get(prediction, default_recommendation)
    
    try:
        # Use the existing chatbot to enhance the recommendation with AI-generated content
        prompt = f"""Based on a lung CT scan analysis showing '{prediction}', provide:
        1. Two additional important next steps patients should take (be specific)
        2. One personal supportive recommendation to help the patient cope mentally with this finding
        Format your response as bullet points only with no introduction or conclusion."""
        
        enhanced_content = chatbot.get_response(prompt)
        
        # Parse the enhanced content into bullet points
        bullet_points = [point.strip().replace('- ', '') for point in enhanced_content.split('\n') if point.strip() and point.strip().startswith('- ')]
        
        # If the parsing didn't work as expected, try another approach
        if not bullet_points:
            bullet_points = [point.strip() for point in enhanced_content.split('\n') if point.strip()]
        
        # Add AI-generated next steps (limit to 3 to not overwhelm)
        if bullet_points and len(bullet_points) >= 2:
            # Add the first two as next steps
            recommendation['next_steps'].extend(bullet_points[:2])
            
            # If we have a third point, add it as personal support recommendation
            if len(bullet_points) >= 3:
                recommendation['ai_personal_support'] = bullet_points[2]
    
    except Exception as e:
        print(f"Error generating enhanced recommendations: {str(e)}")
        # Continue with base recommendations if enhancement fails
    
    # Add an indicator that this was AI-enhanced
    recommendation['ai_enhanced'] = True
    
    return recommendation

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/analysis', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file.save(file_path)

            try:
                # Load and preprocess the image
                img = image.load_img(file_path, target_size=(224, 224))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = tf.keras.applications.resnet50.preprocess_input(img_array)

                # Make a prediction
                predictions = model.predict(img_array)
                predicted_class = np.argmax(predictions, axis=1)[0]
                predicted_label = class_labels[predicted_class]
                
                # Get recommendations based on the prediction
                recommendation = get_recommendations(predicted_label)

                return render_template('index.html', 
                                      filename=filename, 
                                      prediction=predicted_label, 
                                      probabilities=predictions[0].tolist(),
                                      recommendation=recommendation)
            except Exception as e:
                # Log the error
                print(f"Error processing image: {str(e)}")
                # Return an error page or message
                return render_template('index.html', error=f"Error processing image: {str(e)}")

    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint for chatbot interactions"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = chatbot.get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({'response': 'Sorry, something went wrong. Please try again later.'}), 500

if __name__ == '__main__':
    # Make sure the upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
# LungScanAI-Detector

LungScanAI-Detector is an AI-powered web application that analyzes CT scan images to detect and classify different types of lung cancer with high accuracy. The application includes an interactive chatbot that provides additional information and support to users.

## Features

- **CT Scan Analysis**: Upload and analyze lung CT scan images
- **Cancer Classification**: Detects four categories:
  - Adenocarcinoma
  - Large Cell Carcinoma
  - Squamous Cell Carcinoma
  - Normal Lung Tissue
- **Detailed Reports**: Provides comprehensive analysis results with prediction probabilities
- **Personalized Recommendations**: Offers customized medical recommendations based on detection results
- **PDF Export**: Generate and download analysis reports in PDF format
- **AI-Powered Chatbot**: Get answers to lung cancer-related questions through an interactive assistant

## Technology Stack

- **Backend**: Python, Flask
- **Machine Learning**: TensorFlow, ResNet50
- **Frontend**: HTML, CSS, JavaScript
- **PDF Generation**: jsPDF, html2canvas
- **Chatbot**: Claude AI API (Anthropic)
- **Image Processing**: PIL/Pillow

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/krishnakanth6143/LungScanAI-Detector.git
   cd LungScanAI-Detector
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application:
   - Update the API key for the chatbot in `app.py` if needed
   - Download the model file:
     - Due to size limitations, the model file is not included in this repository
     - Download `lung_cancer_model.h5` from [Google Drive/Other hosting service]
     - Place the downloaded file in the root directory of the project

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. Navigate to the "Analysis" page
2. Upload a lung CT scan image (supported formats: PNG, JPG, JPEG)
3. Wait for the AI to analyze the image
4. View the detailed analysis results
5. Review the personalized recommendations
6. Generate a PDF report if needed
7. Use the chatbot for additional questions or support

## Model Information

The application uses a deep learning model trained on a dataset of lung CT scan images. The model architecture is based on the ResNet50 convolutional neural network and has been fine-tuned to detect four different categories:

- Adenocarcinoma
- Large Cell Carcinoma
- Normal lung tissue
- Squamous Cell Carcinoma

## Project Structure

```
├── app.py              # Main Flask application
├── chatbot.py          # Chatbot implementation
├── requirements.txt    # Python dependencies
├── lung_cancer_model.h5 # Trained deep learning model
├── static/             # Static files (CSS, JS, uploads)
│   ├── css/
│   ├── js/
│   └── uploads/
├── templates/          # HTML templates
│   ├── home.html
│   ├── index.html
│   └── contact.html
└── Data/               # Dataset (training, validation, testing)
```

## Disclaimer

This application is designed for research and educational purposes only. It is not intended to replace professional medical diagnosis or advice. Always consult healthcare professionals for proper medical advice.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Special thanks to all contributors
- Dataset sources: [Include sources if applicable]

## Contact

For inquiries, please create an issue on this repository or contact the maintainers directly.

# 🛡️ Malicious URL Detector

A machine learning-powered web application that detects malicious URLs (phishing, malware, defacement) with a beautiful, responsive user interface.

## 🎯 Features

- ✨ **Real-time URL Analysis** - Instantly classify URLs as benign, phishing, malware, or defacement
- 🎨 **Beautiful UI** - Modern, responsive design with smooth animations
- 🤖 **AI-Powered** - Uses trained Random Forest and XGBoost models
- 📊 **Detailed Reports** - Shows threat probability breakdown and analyzed features
- 🔒 **Privacy-Focused** - Works completely in-browser or locally hosted
- 📱 **Mobile Responsive** - Works on desktop, tablet, and mobile devices
- ⚡ **Fast Performance** - Sub-second URL analysis

## 👥 Team

Built by:
- 👤 **Tanvi Gode**
- 👤 **Astha Singh**
- 👤 **Gayatri Tasalwar**

## 🚀 Quick Start

### Requirements
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/malicious-url-detection.git
cd malicious-url-detection
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
malicious-url-detection/
│
├── src/
│   └── app.py                 # Flask backend & ML integration
│
├── templates/
│   └── index.html            # Web interface
│
├── static/
│   ├── style.css             # Styling & animations
│   └── script.js             # Frontend interactivity
│
├── models/
│   ├── rf_model_v2.pkl       # Trained Random Forest model
│   └── label_encoder.pkl     # Label encoder
│
├── data/
│   ├── features.csv
│   ├── features_v2.csv
│   └── malicious_phish.csv
│
├── notebooks/
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_building.ipynb
│
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ How It Works

### Backend (Flask)
- Loads pre-trained ML models (Random Forest & XGBoost)
- Extracts 25+ features from each URL:
  - Basic features (length, dots, hyphens, etc.)
  - Security features (HTTPS, IP address detection)
  - Domain analysis (TLD, subdomain, entropy)
  - Suspicious keyword detection
- Returns probability scores for each threat type

### Frontend (HTML/CSS/JavaScript)
- Responsive design that works on all devices
- Real-time URL validation
- Animated result cards and probability bars
- Shows analyzed URL features
- Safety tips and recommendations

### Machine Learning Models
- **Random Forest**: Primary classifier with 25+ features
- **XGBoost**: Backup model for improved accuracy
- **Label Encoder**: Converts predictions to threat types

## 📊 Threat Classifications

- 🟢 **BENIGN** - Safe, legitimate website
- 🔴 **PHISHING** - Designed to steal credentials/information
- 🔴 **MALWARE** - Contains malicious software
- 🟡 **DEFACEMENT** - Website has been hacked/vandalized

## 🔬 Data & Model Training

See `notebooks/03_model_building.ipynb` for detailed model training:
- Data preprocessing and feature engineering
- Train-test split (80-20)
- Model training and evaluation
- Feature importance analysis
- Model serialization

## 📝 Features Extracted

### Basic Features
- URL Length
- Number of dots
- Number of hyphens
- Number of underscores
- Has HTTP/HTTPS protocol

### Security Features
- Has HTTPS
- Contains IP address
- Contains @ symbol
- Trusted domain check
- Suspicious keywords

### Domain Features
- Domain length
- Subdomain length
- TLD length
- Domain entropy
- Domain age (if available)

## 💻 Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, XGBoost
- **Data Processing**: pandas, numpy
- **Feature Extraction**: tldextract, regex
- **Serialization**: joblib

## 🚢 Deployment

Once you're ready to deploy:

1. Push to GitHub
2. Choose a platform (Railway, Heroku, AWS, GCP, or Docker)
3. Configure environment variables
4. Deploy!

See deployment guides in documentation for specific platform instructions.

## 📜 License

This project is open source. Feel free to use it for educational and non-commercial purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## ❓ FAQ

**Q: Does this require an internet connection?**
A: Only for external API calls. The ML models run locally.

**Q: How accurate is the detection?**
A: Typically 85-95% depending on the URL dataset.

**Q: Can I use this in production?**
A: Yes! It's built with production deployments in mind.

**Q: How do I add more URLs to train the model?**
A: Add data to CSV files and retrain using the Jupyter notebook.

## 📧 Contact

For questions or support, reach out to the project team.

## 🎓 Educational Value

This project demonstrates:
- Machine Learning fundamentals (classification)
- Feature engineering from raw data
- Web application development (Flask)
- Frontend design & interactivity
- Model deployment & serving
- REST API design

Perfect for learning full-stack machine learning development!

---

**Ready to use? Run `python src/app.py` and visit http://localhpip install -r requirements.txtost:5000** 🚀

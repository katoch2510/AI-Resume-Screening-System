# AI-Powered Resume Screening & Candidate Matching System

A professional, modern web application designed for HR departments to automate resume screening and candidate ranking using NLP and Machine Learning.

## 🚀 Features
- **Authentication**: Secure Admin login system.
- **Resume Parsing**: Automatically extract text from PDF and DOCX files.
- **Skill Detection**: Uses spaCy NLP to identify technical skills (Python, Java, React, etc.).
- **Smart Matching**: TF-IDF and Cosine Similarity to calculate candidate compatibility.
- **AI Insights**:
  - Skill Gap Analysis (missing skills).
  - AI-generated interview questions based on candidate's background.
- **Modern Dashboard**: Responsive UI with dark/light mode support and Chart.js analytics.

## 🛠️ Tech Stack
- **Backend**: Python Flask, SQLite, SQLAlchemy
- **NLP/ML**: spaCy, Scikit-learn, NLTK, PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AI-Resume-Screening-System
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   Open `http://127.0.0.1:5000` in your browser.
   - **Username**: `admin`
   - **Password**: `admin123`

## 📁 Folder Structure
- `templates/`: HTML templates.
- `static/`: CSS and JS assets.
- `uploads/`: Processed resume storage.
- `utils/`: NLP and Matching logic.
- `models.py`: Database schema.

## 📄 License
This project is for educational purposes (Final Year BCA/BTech Project).

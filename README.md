# Lyrics Generator

A deep learning-based lyrics generator that uses a trained model to generate song lyrics based on selected artists. The system is built using Flask for the backend and React.js for the frontend, with training data stored in text files.

---

## 📌 Features
- Users can select multiple artists from a predefined list.
- The backend checks if a pre-trained model exists for the selected artists.
- If a model is available, it generates lyrics instantly.
- If no model exists, the system trains a new model before generating lyrics.
- The generated lyrics are displayed in the frontend.

---

## ⚙️ Tech Stack
- **Frontend:** React.js
- **Backend:** Flask (Python)
- **Machine Learning:** Deep Learning model trained using artist text files

---

## 🚀 Installation & Setup
### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/lyrics-generator.git
cd lyrics-generator
```

### 2️⃣ Backend Setup (Flask)
#### Install dependencies
```bash
cd backend
pip install -r requirements.txt
```
#### Run the Flask server
```bash
python app.py
```

### 3️⃣ Frontend Setup (React.js)
#### Install dependencies
```bash
cd frontend
npm install
```
#### Run the React application
```bash
npm start
```

---

## 🛠 Usage
1. Open the frontend in your browser (`http://localhost:3000`).
2. Select one or more artists from the available list.
3. Click on "Generate Lyrics".
4. The backend will check for a pre-trained model and generate lyrics.
5. If no model exists, the system will train a new model before generating lyrics.
6. The generated lyrics will be displayed in the frontend.

---

## 📂 Project Structure
```
lyrics-generator/
│── backend/              # Flask Backend
│   │── app.py            # Main Flask app
│   │── model.py          # Model training & prediction logic
│   │── static/           # Pre-trained models
│   │── data/             # Training text files
│   └── requirements.txt  # Dependencies
│
│── frontend/             # React.js Frontend
│   │── src/              # Source code
│   │── public/           # Static assets
│   └── package.json      # Dependencies
│
└── README.md             # Project documentation
```

---

## 🔥 Future Enhancements
- Improve model training efficiency.
- Add support for more artists dynamically.
- Optimize lyrics generation for better coherence.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing
Contributions are welcome! If you’d like to improve the project, feel free to fork the repository and submit a pull request.

---

### 📧 Contact
For any questions or issues, contact us at `your-email@example.com`.

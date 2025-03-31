# Health-Analyzer-
# Wearable Health Monitoring System

## 📌 Project Overview
The **Wearable Health Monitoring System** is a Python-based GUI application that tracks and visualizes essential health metrics such as:
- 💓 **Heart Rate (BPM)**
- 🩸 **Blood Pressure (mmHg)**
- 🌬 **Oxygen Saturation (SpO2%)**
- 🍽 **Food Intake & Nutrients**
- 📊 **Health Trends & Disease Alerts**

This system operates **without physical sensors**, using a **fixed SQLite database** to simulate real-time data. Users can analyze trends via interactive graphs, receive health alerts based on predefined thresholds, and export reports for further insights.

---

## 🚀 Features
✅ **Real-time Health Monitoring** – Fetches data from an SQLite database and displays vitals in a graphical format.  
✅ **Graphical Representation** – Plots heart rate, blood pressure, and SpO2 trends over time using Matplotlib.  
✅ **Health Risk Alerts** – Provides warnings for conditions like hypertension, low oxygen levels, and abnormal heart rates.  
✅ **User-Based Data Filtering** – Retrieve past health records based on user selection.  
✅ **GUI-Based Interaction** – A modern Tkinter interface for easy navigation.  
✅ **Report Generation** – Option to export health reports as a CSV or PDF (planned feature).  

---

## 🛠 Technologies Used
- **Python** – Core programming language
- **SQLite** – Local database for storing health records
- **Tkinter** – GUI framework for interactive interface
- **Matplotlib** – Graphing library for data visualization
- **Pandas** – Data handling and analysis
- **NumPy** – Numeric computations

---

## 📂 Project Structure
```
wearable_health_monitor/
│── database/
│   ├── health_data.db  # SQLite database storing health records
│   ├── setup_db.py      # Script to create and populate database
│
│── gui/
│   ├── main_gui.py      # Tkinter GUI interface
│   ├── graphs.py        # Matplotlib visualizations
│
│── analysis/
│   ├── health_alerts.py # Disease risk analysis based on vitals
│
│── README.md            # Project documentation
│── requirements.txt     # Dependencies for the project
│── LICENSE              # License file
```

---

## 🏗 Installation & Setup
### 🔹 1. Clone the Repository
```sh
git clone https://github.com/your-username/wearable-health-monitor.git
cd wearable-health-monitor
```

### 🔹 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 🔹 3. Set Up the Database
```sh
python database/setup_db.py
```
This script initializes the SQLite database with **sample health data**.

### 🔹 4. Run the Application
```sh
python gui/main_gui.py
```
This launches the **GUI interface**, displaying health parameters and graphs.

---

## 🎯 How It Works
1️⃣ The application retrieves **preloaded health data** from an SQLite database.  
2️⃣ The Tkinter GUI **displays real-time vitals** (heart rate, BP, SpO2).  
3️⃣ Users can **view past trends** via an interactive graph.  
4️⃣ A **health risk analysis** module provides alerts if vitals exceed normal thresholds.  
5️⃣ Users can **filter records** by date or user name to analyze health trends.

---

## 🩺 Health Alert Conditions
| Condition | Criteria | Warning |
|-----------|---------|---------|
| **Hypertension** | BP > 140/90 mmHg | 🚨 High BP Alert |
| **Hypotension** | BP < 90/60 mmHg | ⚠ Low BP Alert |
| **Tachycardia** | Heart Rate > 100 BPM | 🚨 High Heart Rate |
| **Bradycardia** | Heart Rate < 60 BPM | ⚠ Low Heart Rate |
| **Low Oxygen Levels** | SpO2 < 92% | 🚨 Possible Respiratory Issue |

---

## 🚀 Future Enhancements
🔹 **Integration with Wearable Sensors** (e.g., smartwatches, pulse oximeters)  
🔹 **Real-Time Data Streaming** from IoT health devices  
🔹 **Automated Report Generation** (PDF export)  
🔹 **AI-based Disease Prediction** using machine learning  
🔹 **Mobile App Version** for remote health tracking  

---

## 🤝 Contributing
Want to improve the project? Feel free to contribute!  
1️⃣ Fork the repository.  
2️⃣ Create a new feature branch.  
3️⃣ Commit changes and push to your branch.  
4️⃣ Submit a Pull Request.  

---

## 📜 License
This project is licensed under the **MIT License** – free to use and modify.  

---

## 📧 Contact
👤 **Your Name**  
📍 **Your Location**  
📧 **your.email@example.com**  
🔗 **[LinkedIn Profile](https://linkedin.com/in/yourprofile)**  
🔗 **[GitHub Repository](https://github.com/your-username/wearable-health-monitor)**  

---

🌟 *If you find this project useful, don't forget to ⭐ the repository!*


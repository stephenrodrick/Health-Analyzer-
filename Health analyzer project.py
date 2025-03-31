import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import sqlite3
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import platform

# Theme Manager Class
class ThemeManager:
    COLORS = {
        'primary': '#2C3E50',
        'secondary': '#3498DB',
        'accent': '#2ECC71',
        'warning': '#F39C12',
        'danger': '#E74C3C',
        'info': '#3498DB',
        'neutral': '#ECF0F1',
        'text_dark': '#2C3E50',
        'text_light': '#FFFFFF',
        'background': '#F5F7FA',
        'card': '#FFFFFF',
    }
    
    STATUS_COLORS = {
        'Normal': '#2ECC71',
        'Caution': '#3498DB',
        'Warning': '#F39C12',
        'Danger': '#E74C3C',
        'Unknown': '#95A5A6',
    }

    @classmethod
    def setup_theme(cls, root):
        style = ttk.Style()
        if platform.system() == 'Windows':
            try:
                style.theme_use('vista')
            except:
                pass

        # Enhanced modern styling
        style.configure('TFrame', background=cls.COLORS['background'])
        style.configure('Card.TFrame', 
                       background=cls.COLORS['card'],
                       relief='raised',
                       borderwidth=1)
        
        # Enhanced label styles
        style.configure('TLabel', 
                       background=cls.COLORS['background'], 
                       foreground=cls.COLORS['text_dark'],
                       font=('Segoe UI', 10))
        
        style.configure('Card.TLabel', 
                       background=cls.COLORS['card'],
                       font=('Segoe UI', 10))
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=cls.COLORS['primary'])
        
        style.configure('SubHeader.TLabel', 
                       font=('Segoe UI', 12, 'bold'),
                       foreground=cls.COLORS['primary'])
        
        # Enhanced button styles
        style.configure('TButton', 
                       padding=(10, 5),
                       font=('Segoe UI', 10),
                       background=cls.COLORS['secondary'],
                       foreground=cls.COLORS['text_light'])
        
        style.map('TButton',
                  background=[('active', cls.COLORS['info'])],
                  foreground=[('active', cls.COLORS['text_light'])])
        
        # Enhanced combobox style
        style.configure('TCombobox', 
                       padding=(5, 5),
                       font=('Segoe UI', 10))
        
        # Enhanced notebook style
        style.configure('TNotebook', 
                       background=cls.COLORS['background'],
                       padding=(5, 5))
        
        style.configure('TNotebook.Tab', 
                       padding=(10, 5),
                       font=('Segoe UI', 10, 'bold'))
        
        # Enhanced treeview style
        style.configure('Treeview', 
                       font=('Segoe UI', 10),
                       rowheight=25)
        
        style.configure('Treeview.Heading', 
                       font=('Segoe UI', 10, 'bold'))
        
        # Status indicator styles
        for status, color in cls.STATUS_COLORS.items():
            style.configure(f'{status}.TLabel',
                           foreground=color,
                           font=('Segoe UI', 10, 'bold'))
            style.configure(f'{status}.TFrame',
                           background=color)

    @classmethod
    def create_tooltip(cls, widget, text):
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            label = ttk.Label(tooltip, text=text, justify='left',
                             background=cls.COLORS['primary'], 
                             foreground=cls.COLORS['text_light'],
                             relief='solid', borderwidth=1, padding=(5, 3))
            label.pack()
            widget.tooltip = tooltip
            
        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

# Dashboard Widgets Class
class DashboardWidgets:
    @staticmethod
    def create_metric_frame(parent, title, value, status="Normal", details=None):
        frame = ttk.Frame(parent, style='Card.TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        header_frame = ttk.Frame(frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        title_label = ttk.Label(header_frame, text=title, style='SubHeader.TLabel')
        title_label.pack(side=tk.LEFT)
        
        status_indicator = ttk.Label(header_frame, text="●", style=f'{status}.TLabel')
        status_indicator.pack(side=tk.RIGHT)
        
        value_label = ttk.Label(frame, text=value, style='Header.TLabel')
        value_label.pack(pady=5)
        
        if details:
            details_label = ttk.Label(frame, text=details, style='Card.TLabel')
            details_label.pack(pady=2)
            
        return frame

# Visual Components Class
class VisualComponents:
    @staticmethod
    def create_trend_graph(parent, data, title, ylabel):
        fig, ax = plt.subplots(figsize=(6, 3))
        dates = [d[0] for d in data]
        values = [d[1] for d in data]
        
        ax.plot(dates, values)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        return canvas

    @staticmethod
    def create_status_indicator(parent, status, message):
        frame = ttk.Frame(parent, style=f'{status}.TFrame')
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        indicator = ttk.Label(frame, text=message, style=f'{status}.TLabel')
        indicator.pack(pady=2)
        
        return frame

# Database Manager Class
class DatabaseManager:
    def __init__(self):
        self.db_path = 'health_monitor.db'
        self.create_database()

    def create_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    height REAL,
                    weight REAL
                )
                ''')

                # Create health_data table
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_data (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    heart_rate INTEGER,
                    blood_pressure_sys INTEGER,
                    blood_pressure_dia INTEGER,
                    oxygen_level REAL,
                    temperature REAL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
                ''')

                # Check if users table is empty
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    # Sample patient data with various health conditions
                    patients = [
                        ('John Smith', 65, 'Male', 175.0, 82.0),      # Hypertension
                        ('Sarah Johnson', 42, 'Female', 165.0, 58.0),  # Normal
                        ('Michael Brown', 55, 'Male', 180.0, 95.0),    # Obesity + High BP
                        ('Emma Davis', 28, 'Female', 160.0, 55.0),     # Low BP
                        ('Robert Wilson', 72, 'Male', 172.0, 78.0),    # Heart rhythm issues
                        ('Lisa Anderson', 41, 'Female', 168.0, 63.0),  # Normal
                        ('David Martinez', 58, 'Male', 178.0, 88.0),   # Diabetes signs
                        ('Jennifer Taylor', 35, 'Female', 163.0, 57.0), # Anxiety
                        ('William Lee', 50, 'Male', 170.0, 72.0),      # Normal
                        ('Maria Garcia', 44, 'Female', 165.0, 61.0),    # Low oxygen
                        ('James Thompson', 68, 'Male', 176.0, 82.0),    # Heart condition
                        ('Susan White', 47, 'Female', 167.0, 65.0),     # Fever
                        ('Thomas Moore', 53, 'Male', 182.0, 88.0),      # Pre-hypertension
                        ('Patricia Clark', 39, 'Female', 164.0, 59.0),  # Normal
                        ('Richard Harris', 60, 'Male', 173.0, 76.0)     # Bradycardia
                    ]

                    # Insert patients
                    cursor.executemany("""
                    INSERT INTO users (name, age, gender, height, weight)
                    VALUES (?, ?, ?, ?, ?)
                    """, patients)

                    # Generate historical data for each patient (last 30 days)
                    for user_id in range(1, 16):
                        base_time = datetime.datetime.now() - datetime.timedelta(days=30)
                        
                        # Generate health data points (4 times per day for 30 days)
                        for day in range(30):
                            for hour in [6, 12, 18, 23]:
                                timestamp = base_time + datetime.timedelta(days=day, hours=hour)
                                
                                # Generate data based on patient condition
                                if user_id == 1:  # John Smith - Hypertension
                                    hr = 85 + random.randint(-5, 5)
                                    sys = 145 + random.randint(-5, 10)
                                    dia = 95 + random.randint(-5, 5)
                                    o2 = 97 + random.random()
                                    temp = 36.8 + random.random() * 0.4
                                elif user_id == 2:  # Sarah Johnson - Normal
                                    hr = 72 + random.randint(-5, 5)
                                    sys = 120 + random.randint(-5, 5)
                                    dia = 80 + random.randint(-5, 5)
                                    o2 = 98 + random.random()
                                    temp = 36.6 + random.random() * 0.2
                                elif user_id == 3:  # Michael Brown - Obesity + High BP
                                    hr = 88 + random.randint(-5, 10)
                                    sys = 150 + random.randint(-5, 10)
                                    dia = 95 + random.randint(-5, 5)
                                    o2 = 96 + random.random()
                                    temp = 37.0 + random.random() * 0.3
                                elif user_id == 4:  # Emma Davis - Low BP
                                    hr = 65 + random.randint(-5, 5)
                                    sys = 85 + random.randint(-5, 5)
                                    dia = 55 + random.randint(-5, 5)
                                    o2 = 97 + random.random()
                                    temp = 36.5 + random.random() * 0.3
                                elif user_id == 5:  # Robert Wilson - Heart rhythm issues
                                    hr = 100 + random.randint(-20, 20)
                                    sys = 130 + random.randint(-10, 10)
                                    dia = 85 + random.randint(-5, 5)
                                    o2 = 96 + random.random()
                                    temp = 36.7 + random.random() * 0.3
                                elif user_id == 6:  # Lisa Anderson - Normal
                                    hr = 70 + random.randint(-5, 5)
                                    sys = 118 + random.randint(-5, 5)
                                    dia = 78 + random.randint(-5, 5)
                                    o2 = 98 + random.random()
                                    temp = 36.6 + random.random() * 0.2
                                elif user_id == 7:  # David Martinez - Diabetes signs
                                    hr = 82 + random.randint(-5, 5)
                                    sys = 135 + random.randint(-5, 10)
                                    dia = 88 + random.randint(-5, 5)
                                    o2 = 97 + random.random()
                                    temp = 36.9 + random.random() * 0.4
                                elif user_id == 8:  # Jennifer Taylor - Anxiety
                                    hr = 95 + random.randint(-10, 15)
                                    sys = 125 + random.randint(-10, 15)
                                    dia = 82 + random.randint(-5, 10)
                                    o2 = 98 + random.random()
                                    temp = 36.8 + random.random() * 0.5
                                elif user_id == 9:  # William Lee - Normal
                                    hr = 71 + random.randint(-5, 5)
                                    sys = 119 + random.randint(-5, 5)
                                    dia = 79 + random.randint(-5, 5)
                                    o2 = 98 + random.random()
                                    temp = 36.6 + random.random() * 0.2
                                elif user_id == 10:  # Maria Garcia - Low oxygen
                                    hr = 90 + random.randint(-5, 10)
                                    sys = 120 + random.randint(-5, 5)
                                    dia = 80 + random.randint(-5, 5)
                                    o2 = 93 + random.random()
                                    temp = 36.8 + random.random() * 0.3
                                elif user_id == 11:  # James Thompson - Heart condition
                                    hr = 92 + random.randint(-15, 15)
                                    sys = 140 + random.randint(-10, 10)
                                    dia = 90 + random.randint(-5, 5)
                                    o2 = 96 + random.random()
                                    temp = 36.9 + random.random() * 0.4
                                elif user_id == 12:  # Susan White - Fever
                                    hr = 95 + random.randint(-5, 10)
                                    sys = 125 + random.randint(-5, 5)
                                    dia = 82 + random.randint(-5, 5)
                                    o2 = 97 + random.random()
                                    temp = 38.5 + random.random() * 0.5
                                elif user_id == 13:  # Thomas Moore - Pre-hypertension
                                    hr = 80 + random.randint(-5, 10)
                                    sys = 135 + random.randint(-5, 10)
                                    dia = 87 + random.randint(-5, 5)
                                    o2 = 97 + random.random()
                                    temp = 36.7 + random.random() * 0.3
                                elif user_id == 14:  # Patricia Clark - Normal
                                    hr = 73 + random.randint(-5, 5)
                                    sys = 117 + random.randint(-5, 5)
                                    dia = 77 + random.randint(-5, 5)
                                    o2 = 98 + random.random()
                                    temp = 36.6 + random.random() * 0.2
                                else:  # Richard Harris - Bradycardia
                                    hr = 55 + random.randint(-5, 5)
                                    sys = 115 + random.randint(-5, 5)
                                    dia = 75 + random.randint(-5, 5)
                                    o2 = 97 + random.random()
                                    temp = 36.5 + random.random() * 0.3

                                # Insert the data point
                                cursor.execute("""
                                INSERT INTO health_data 
                                (user_id, timestamp, heart_rate, blood_pressure_sys, 
                                 blood_pressure_dia, oxygen_level, temperature)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (user_id, timestamp, hr, sys, dia, o2, temp))

                    conn.commit()

        except sqlite3.Error as e:
            print(f"Database creation error: {e}")
            raise

    def get_user_names(self):
        """Get list of user IDs and names from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id, name FROM users")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting users: {e}")
            return []

    def get_user_info(self, user_id):
        """Get user information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting user info: {e}")
            return None

    def get_latest_health_data(self, user_id):
        """Get latest health data for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT * FROM health_data 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
                """, (user_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting health data: {e}")
            return None

    def get_health_data_by_timeframe(self, user_id, days):
        """Get health data for specified number of days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT * FROM health_data 
                WHERE user_id = ? 
                AND timestamp >= datetime('now', ?) 
                ORDER BY timestamp
                """, (user_id, f'-{days} days'))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting health data: {e}")
            return []

    def get_health_data_by_date_range(self, user_id, start_date, end_date):
        """Get health data between specified dates"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT * FROM health_data 
                WHERE user_id = ? 
                AND timestamp BETWEEN ? AND ?
                ORDER BY timestamp
                """, (user_id, start_date, end_date))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting health data: {e}")
            return []

# Health Analyzer Class
class HealthAnalyzer:
    def analyze_heart_rate(self, hr):
        """Analyze heart rate and return status and message"""
        if hr < 60:
            return "Warning", "Low heart rate (Bradycardia)"
        elif hr > 100:
            return "Warning", "High heart rate (Tachycardia)"
        return "Normal", "Heart rate is normal"

    def analyze_blood_pressure(self, sys, dia):
        """Analyze blood pressure and return status and messages"""
        if sys < 90 or dia < 60:
            return "Danger", "Low blood pressure", f"Low systolic: {sys}", f"Low diastolic: {dia}"
        elif sys >= 140 or dia >= 90:
            return "Warning", "High blood pressure", f"High systolic: {sys}", f"High diastolic: {dia}"
        return "Normal", "Blood pressure is normal", "Normal systolic", "Normal diastolic"

    def analyze_oxygen_level(self, o2):
        """Analyze oxygen level and return status and message"""
        if o2 < 95:
            return "Warning", "Low oxygen saturation"
        return "Normal", "Oxygen level is normal"

    def analyze_temperature(self, temp):
        """Analyze temperature and return status and message"""
        if temp < 36:
            return "Warning", "Low body temperature"
        elif temp > 37.5:
            return "Warning", "Elevated temperature"
        return "Normal", "Temperature is normal"

    def get_overall_health_status(self, health_data):
        """Determine overall health status from latest readings"""
        if not health_data:
            return "Unknown", "No health data available"

        record_id, user_id, timestamp, hr, sys, dia, o2, temp = health_data
        
        warnings = []
        
        hr_status, hr_msg = self.analyze_heart_rate(hr)
        if hr_status != "Normal":
            warnings.append(hr_msg)
            
        bp_status, bp_msg, _, _ = self.analyze_blood_pressure(sys, dia)
        if bp_status != "Normal":
            warnings.append(bp_msg)
            
        o2_status, o2_msg = self.analyze_oxygen_level(o2)
        if o2_status != "Normal":
            warnings.append(o2_msg)
            
        temp_status, temp_msg = self.analyze_temperature(temp)
        if temp_status != "Normal":
            warnings.append(temp_msg)

        if warnings:
            return "Warning", "Health concerns detected:\n" + "\n".join(warnings)
        return "Normal", "All health metrics are within normal ranges"

    def predict_potential_conditions(self, health_data):
        """Analyze health data and predict potential conditions"""
        if not health_data:
            return []

        conditions = []
        latest = health_data[-1]
        
        # Sample condition checks (simplified)
        _, _, _, hr, sys, dia, o2, temp = latest
        
        if hr > 100 and sys > 140:
            conditions.append({
                "condition": "Hypertension",
                "confidence": "High",
                "description": "Elevated blood pressure and heart rate may indicate hypertension."
            })
            
        if o2 < 95:
            conditions.append({
                "condition": "Respiratory Issue",
                "confidence": "Medium",
                "description": "Low oxygen saturation may indicate respiratory problems."
            })
            
        if temp > 37.5:
            conditions.append({
                "condition": "Infection",
                "confidence": "Medium",
                "description": "Elevated temperature may indicate an infection or inflammatory response."
            })

        return conditions

class HealthMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wearable Health Monitoring System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Initialize theme
        ThemeManager.setup_theme(root)
        
        # Initialize other components
        try:
            self.db_manager = DatabaseManager()
            self.health_analyzer = HealthAnalyzer()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            raise
        
        # Set up UI components
        self.setup_main_interface()
        self.load_users()
        self.root.after(10000, self.update_data)
    
    def setup_main_interface(self):
        # Main frame setup
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook setup
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.trends_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.trends_tab, text="Health Trends")
        self.notebook.add(self.analysis_tab, text="Health Analysis")
        
        # Setup individual tabs
        self.setup_dashboard()
        self.setup_trends_tab()
        self.setup_analysis_tab()

    def setup_dashboard(self):
        """Set up the dashboard tab with current health metrics"""
        # Top frame for user selection and controls
        top_frame = ttk.Frame(self.dashboard_tab)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        ttk.Label(top_frame, text="Select User:").pack(side=tk.LEFT, padx=(0, 10))
        self.user_var = tk.StringVar()
        self.user_dropdown = ttk.Combobox(top_frame, textvariable=self.user_var, state="readonly", width=30)
        self.user_dropdown.pack(side=tk.LEFT, padx=5)
        self.user_dropdown.bind("<<ComboboxSelected>>", self.on_user_selected)
        
        # Refresh button
        ttk.Button(top_frame, text="Refresh Data", command=self.update_data).pack(side=tk.RIGHT, padx=5)
        
        # Main content frame
        content_frame = ttk.Frame(self.dashboard_tab)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for current metrics
        self.metrics_frame = ttk.LabelFrame(content_frame, text="Current Health Metrics")
        self.metrics_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right frame for status and alerts
        self.status_frame = ttk.LabelFrame(content_frame, text="Health Status")
        self.status_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Set up metrics display
        self.setup_metrics_display()
        
        # Set up status display
        self.setup_status_display()
    
    def setup_metrics_display(self):
        """Set up the display for current health metrics"""
        # User info frame
        user_info_frame = ttk.Frame(self.metrics_frame)
        user_info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_name_label = ttk.Label(user_info_frame, text="Name: --", font=("Arial", 12, "bold"))
        self.user_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.user_details_label = ttk.Label(user_info_frame, text="Age: -- | Gender: -- | Height: -- cm | Weight: -- kg")
        self.user_details_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.last_updated_label = ttk.Label(user_info_frame, text="Last Updated: --")
        self.last_updated_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        # Separator
        ttk.Separator(self.metrics_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Health metrics frame
        health_metrics_frame = ttk.Frame(self.metrics_frame)
        health_metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Heart rate
        hr_frame = ttk.Frame(health_metrics_frame)
        hr_frame.pack(fill=tk.X, pady=5)
        ttk.Label(hr_frame, text="Heart Rate:", width=15).pack(side=tk.LEFT)
        self.heart_rate_label = ttk.Label(hr_frame, text="-- BPM", width=10)
        self.heart_rate_label.pack(side=tk.LEFT)
        self.heart_rate_status = ttk.Label(hr_frame, text="", width=30)
        self.heart_rate_status.pack(side=tk.LEFT, padx=10)
        
        # Blood pressure
        bp_frame = ttk.Frame(health_metrics_frame)
        bp_frame.pack(fill=tk.X, pady=5)
        ttk.Label(bp_frame, text="Blood Pressure:", width=15).pack(side=tk.LEFT)
        self.blood_pressure_label = ttk.Label(bp_frame, text="--/-- mmHg", width=10)
        self.blood_pressure_label.pack(side=tk.LEFT)
        self.blood_pressure_status = ttk.Label(bp_frame, text="", width=30)
        self.blood_pressure_status.pack(side=tk.LEFT, padx=10)
        
        # Oxygen level
        ox_frame = ttk.Frame(health_metrics_frame)
        ox_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ox_frame, text="Oxygen Level:", width=15).pack(side=tk.LEFT)
        self.oxygen_label = ttk.Label(ox_frame, text="--%", width=10)
        self.oxygen_label.pack(side=tk.LEFT)
        self.oxygen_status = ttk.Label(ox_frame, text="", width=30)
        self.oxygen_status.pack(side=tk.LEFT, padx=10)
        
        # Temperature
        temp_frame = ttk.Frame(health_metrics_frame)
        temp_frame.pack(fill=tk.X, pady=5)
        ttk.Label(temp_frame, text="Temperature:", width=15).pack(side=tk.LEFT)
        self.temperature_label = ttk.Label(temp_frame, text="--°C", width=10)
        self.temperature_label.pack(side=tk.LEFT)
        self.temperature_status = ttk.Label(temp_frame, text="", width=30)
        self.temperature_status.pack(side=tk.LEFT, padx=10)
    
    def setup_status_display(self):
        """Set up the display for health status and alerts"""
        # Overall status frame
        overall_frame = ttk.Frame(self.status_frame)
        overall_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(overall_frame, text="Overall Health Status:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.overall_status_label = ttk.Label(overall_frame, text="Unknown", font=("Arial", 14))
        self.overall_status_label.pack(anchor="w", pady=5)
        
        # Separator
        ttk.Separator(self.status_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Health alerts frame
        alerts_frame = ttk.LabelFrame(self.status_frame, text="Health Alerts")
        alerts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.alerts_text = tk.Text(alerts_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.alerts_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_trends_tab(self):
        """Set up the trends tab with historical data visualization"""
        # Top frame for controls
        top_frame = ttk.Frame(self.trends_tab)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        ttk.Label(top_frame, text="Select User:").pack(side=tk.LEFT, padx=(0, 10))
        self.trends_user_var = tk.StringVar()
        self.trends_user_dropdown = ttk.Combobox(top_frame, textvariable=self.trends_user_var, state="readonly", width=30)
        self.trends_user_dropdown.pack(side=tk.LEFT, padx=5)
        self.trends_user_dropdown.bind("<<ComboboxSelected>>", self.on_trends_user_selected)
        
        # Time range selection
        ttk.Label(top_frame, text="Time Range:").pack(side=tk.LEFT, padx=(20, 10))
        self.time_range_var = tk.StringVar(value="1 Day")
        time_ranges = ["1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month", "Custom"]
        self.time_range_dropdown = ttk.Combobox(top_frame, textvariable=self.time_range_var, 
                                               values=time_ranges, state="readonly", width=15)
        self.time_range_dropdown.pack(side=tk.LEFT, padx=5)
        self.time_range_dropdown.bind("<<ComboboxSelected>>", self.on_time_range_selected)
        
        # Custom date range frame (initially hidden)
        self.custom_date_frame = ttk.Frame(top_frame)
        
        ttk.Label(self.custom_date_frame, text="From:").pack(side=tk.LEFT, padx=(20, 5))
        self.start_date = DateEntry(self.custom_date_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.custom_date_frame, text="To:").pack(side=tk.LEFT, padx=(10, 5))
        self.end_date = DateEntry(self.custom_date_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.custom_date_frame, text="Apply", command=self.update_trends).pack(side=tk.LEFT, padx=(20, 5))
        
        # Update button
        ttk.Button(top_frame, text="Update Chart", command=self.update_trends).pack(side=tk.RIGHT, padx=5)
        
        # Main content frame for charts
        self.trends_content_frame = ttk.Frame(self.trends_tab)
        self.trends_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for matplotlib
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8))
        self.fig.tight_layout(pad=3.0)
        
        # Create canvas for matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.trends_content_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize the plots
        for ax in self.axes.flat:
            ax.set_xlabel('Time')
            ax.grid(True, linestyle='--', alpha=0.7)
        
        self.axes[0, 0].set_title('Heart Rate')
        self.axes[0, 0].set_ylabel('BPM')
        
        self.axes[0, 1].set_title('Blood Pressure')
        self.axes[0, 1].set_ylabel('mmHg')
        
        self.axes[1, 0].set_title('Oxygen Level')
        self.axes[1, 0].set_ylabel('SpO2 %')
        
        self.axes[1, 1].set_title('Temperature')
        self.axes[1, 1].set_ylabel('°C')
        
        self.fig.canvas.draw()
    
    def setup_analysis_tab(self):
        """Set up the analysis tab with health predictions and insights"""
        # Top frame for controls
        top_frame = ttk.Frame(self.analysis_tab)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        ttk.Label(top_frame, text="Select User:").pack(side=tk.LEFT, padx=(0, 10))
        self.analysis_user_var = tk.StringVar()
        self.analysis_user_dropdown = ttk.Combobox(top_frame, textvariable=self.analysis_user_var, state="readonly", width=30)
        self.analysis_user_dropdown.pack(side=tk.LEFT, padx=5)
        self.analysis_user_dropdown.bind("<<ComboboxSelected>>", self.on_analysis_user_selected)
        
        # Analysis period selection
        ttk.Label(top_frame, text="Analysis Period:").pack(side=tk.LEFT, padx=(20, 10))
        self.analysis_period_var = tk.StringVar(value="1 Week")
        analysis_periods = ["1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month"]
        self.analysis_period_dropdown = ttk.Combobox(top_frame, textvariable=self.analysis_period_var, 
                                                   values=analysis_periods, state="readonly", width=15)
        self.analysis_period_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Update button
        ttk.Button(top_frame, text="Run Analysis", command=self.run_analysis).pack(side=tk.RIGHT, padx=5)
        
        # Main content frame
        content_frame = ttk.Frame(self.analysis_tab)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for health summary
        summary_frame = ttk.LabelFrame(content_frame, text="Health Summary")
        summary_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)
        
        self.summary_text = tk.Text(summary_frame, wrap=tk.WORD, height=10, width=40)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.summary_text.config(state=tk.DISABLED)
        
        # Right frame for potential conditions
        conditions_frame = ttk.LabelFrame(content_frame, text="Potential Health Conditions")
        conditions_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        
        # Create a treeview for potential conditions
        self.conditions_tree = ttk.Treeview(conditions_frame, columns=("Condition", "Confidence"), show="headings")
        self.conditions_tree.heading("Condition", text="Potential Condition")
        self.conditions_tree.heading("Confidence", text="Confidence")
        self.conditions_tree.column("Condition", width=150)
        self.conditions_tree.column("Confidence", width=100)
        self.conditions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(conditions_frame, orient=tk.VERTICAL, command=self.conditions_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conditions_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bottom frame for condition details
        details_frame = ttk.LabelFrame(self.analysis_tab, text="Condition Details")
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.condition_details = tk.Text(details_frame, wrap=tk.WORD, height=5)
        self.condition_details.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.condition_details.config(state=tk.DISABLED)
        
        # Bind selection event to show details
        self.conditions_tree.bind("<<TreeviewSelect>>", self.show_condition_details)
    
    def load_users(self):
        """Load users into the dropdown menus"""
        try:
            users = self.db_manager.get_user_names()
            user_list = [(uid, name) for uid, name in users]
            
            # Update all dropdowns
            self.user_dropdown['values'] = [name for _, name in user_list]
            self.trends_user_dropdown['values'] = [name for _, name in user_list]
            self.analysis_user_dropdown['values'] = [name for _, name in user_list]
            
            # Store user IDs for lookup
            self.user_ids = {name: uid for uid, name in user_list}
            
            # Select first user by default if available
            if user_list:
                self.user_var.set(user_list[0][1])
                self.trends_user_var.set(user_list[0][1])
                self.analysis_user_var.set(user_list[0][1])
                self.current_user_id = user_list[0][0]
                
                # Update data for the selected user
                self.update_dashboard_data()
                self.update_trends()
                self.run_analysis()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
    
    def on_user_selected(self, event):
        """Handle user selection in the dashboard tab"""
        selected_user = self.user_var.get()
        self.current_user_id = self.user_ids.get(selected_user)
        self.update_dashboard_data()
    
    def on_trends_user_selected(self, event):
        """Handle user selection in the trends tab"""
        selected_user = self.trends_user_var.get()
        self.update_trends()
    
    def on_analysis_user_selected(self, event):
        """Handle user selection in the analysis tab"""
        selected_user = self.analysis_user_var.get()
        self.run_analysis()
    
    def on_time_range_selected(self, event):
        """Handle time range selection in the trends tab"""
        selected_range = self.time_range_var.get()
        
        # Show or hide custom date range frame
        if selected_range == "Custom":
            self.custom_date_frame.pack(side=tk.LEFT)
        else:
            self.custom_date_frame.pack_forget()
            self.update_trends()
    
    def update_data(self):
        """Update data periodically"""
        if self.current_user_id:
            self.update_dashboard_data()
        
        # Schedule the next update
        self.root.after(10000, self.update_data)
    
    def update_dashboard_data(self):
        """Update the dashboard with the latest health data"""
        if not self.current_user_id:
            return
        
        try:
            # Get user info
            user_info = self.db_manager.get_user_info(self.current_user_id)
            if user_info:
                user_id, name, age, gender, height, weight = user_info
                self.user_name_label.config(text=f"Name: {name}")
                self.user_details_label.config(text=f"Age: {age} | Gender: {gender} | Height: {height} cm | Weight: {weight} kg")
            
            # Get latest health data
            health_data = self.db_manager.get_latest_health_data(self.current_user_id)
            if health_data:
                record_id, user_id, timestamp, heart_rate, bp_sys, bp_dia, oxygen, temp = health_data
                
                # Update timestamp
                timestamp_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                self.last_updated_label.config(text=f"Last Updated: {timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Update metrics
                self.heart_rate_label.config(text=f"{heart_rate} BPM")
                self.blood_pressure_label.config(text=f"{bp_sys}/{bp_dia} mmHg")
                self.oxygen_label.config(text=f"{oxygen}%")
                self.temperature_label.config(text=f"{temp}°C")
                
                # Analyze health data
                hr_status, hr_msg = self.health_analyzer.analyze_heart_rate(heart_rate)
                bp_status, bp_msg, sys_msg, dia_msg = self.health_analyzer.analyze_blood_pressure(bp_sys, bp_dia)
                ox_status, ox_msg = self.health_analyzer.analyze_oxygen_level(oxygen)
                temp_status, temp_msg = self.health_analyzer.analyze_temperature(temp)
                
                # Update status labels with color coding
                self.update_status_label(self.heart_rate_status, hr_status, hr_msg)
                self.update_status_label(self.blood_pressure_status, bp_status, bp_msg)
                self.update_status_label(self.oxygen_status, ox_status, ox_msg)
                self.update_status_label(self.temperature_status, temp_status, temp_msg)
                
                # Update overall status
                overall_status, overall_msg = self.health_analyzer.get_overall_health_status(health_data)
                self.update_status_label(self.overall_status_label, overall_status, overall_status)
                
                # Update alerts
                self.alerts_text.config(state=tk.NORMAL)
                self.alerts_text.delete(1.0, tk.END)
                
                if overall_status != "Normal":
                    self.alerts_text.insert(tk.END, overall_msg + "\n\n")
                    
                    # Add specific alerts
                    if hr_status != "Normal":
                        self.alerts_text.insert(tk.END, f"• {hr_msg}\n")
                    if bp_status != "Normal":
                        self.alerts_text.insert(tk.END, f"• {sys_msg}\n")
                        self.alerts_text.insert(tk.END, f"• {dia_msg}\n")
                    if ox_status != "Normal":
                        self.alerts_text.insert(tk.END, f"• {ox_msg}\n")
                    if temp_status != "Normal":
                        self.alerts_text.insert(tk.END, f"• {temp_msg}\n")
                else:
                    self.alerts_text.insert(tk.END, "No health alerts at this time.\n\n")
                    self.alerts_text.insert(tk.END, "All health metrics are within normal ranges.")
                
                self.alerts_text.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("No Data", "No health data available for this user.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update data: {e}")
    
    def update_status_label(self, label, status, text):
        """Update a status label with appropriate color coding"""
        label.config(text=text)
        
        if status == "Danger":
            label.config(foreground="red")
        elif status == "Warning":
            label.config(foreground="orange")
        elif status == "Caution":
            label.config(foreground="blue")
        else:  # Normal
            label.config(foreground="green")
    
    def update_trends(self):
        """Update the trends charts with historical data"""
        selected_user = self.trends_user_var.get()
        if not selected_user:
            return
        
        user_id = self.user_ids.get(selected_user)
        if not user_id:
            return
        
        try:
            # Determine date range
            time_range = self.time_range_var.get()
            
            if time_range == "Custom":
                start_date = self.start_date.get_date().strftime('%Y-%m-%d 00:00:00')
                end_date = self.end_date.get_date().strftime('%Y-%m-%d 23:59:59')
                health_data = self.db_manager.get_health_data_by_date_range(user_id, start_date, end_date)
            else:
                # Convert time range to days
                days = 1
                if time_range == "3 Days":
                    days = 3
                elif time_range == "1 Week":
                    days = 7
                elif time_range == "2 Weeks":
                    days = 14
                elif time_range == "1 Month":
                    days = 30
                
                health_data = self.db_manager.get_health_data_by_timeframe(user_id, days)
            
            if not health_data:
                messagebox.showinfo("No Data", "No health data available for the selected time range.")
                return
            
            # Clear previous plots
            for ax in self.axes.flat:
                ax.clear()
                ax.grid(True, linestyle='--', alpha=0.7)
            
            # Extract data
            timestamps = [datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S') for record in health_data]
            heart_rates = [record[3] for record in health_data]
            bp_systolic = [record[4] for record in health_data]
            bp_diastolic = [record[5] for record in health_data]
            oxygen_levels = [record[6] for record in health_data]
            temperatures = [record[7] for record in health_data]
            
            # Plot heart rate
            self.axes[0, 0].plot(timestamps, heart_rates, 'r-', marker='o', markersize=3)
            self.axes[0, 0].set_title('Heart Rate')
            self.axes[0, 0].set_ylabel('BPM')
            
            # Plot blood pressure
            self.axes[0, 1].plot(timestamps, bp_systolic, 'r-', marker='o', markersize=3, label='Systolic')
            self.axes[0, 1].plot(timestamps, bp_diastolic, 'b-', marker='o', markersize=3, label='Diastolic')
            self.axes[0, 1].set_title('Blood Pressure')
            self.axes[0, 1].set_ylabel('mmHg')
            self.axes[0, 1].legend()
            
            # Plot oxygen level
            self.axes[1, 0].plot(timestamps, oxygen_levels, 'b-', marker='o', markersize=3)
            self.axes[1, 0].set_title('Oxygen Level')
            self.axes[1, 0].set_ylabel('SpO2 %')
            
            # Plot temperature
            self.axes[1, 1].plot(timestamps, temperatures, 'g-', marker='o', markersize=3)
            self.axes[1, 1].set_title('Temperature')
            self.axes[1, 1].set_ylabel('°C')
            
            # Format x-axis for all plots
            for ax in self.axes.flat:
                ax.set_xlabel('Time')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
                ax.tick_params(axis='x', rotation=45)
            
            # Adjust layout and redraw
            self.fig.tight_layout()
            self.canvas.draw()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update trends: {e}")
    
    def run_analysis(self):
        """Run health analysis and update the analysis tab"""
        selected_user = self.analysis_user_var.get()
        if not selected_user:
            return
        
        user_id = self.user_ids.get(selected_user)
        if not user_id:
            return
        
        try:
            # Get user info
            user_info = self.db_manager.get_user_info(user_id)
            if not user_info:
                return
            
            # Determine analysis period
            period = self.analysis_period_var.get()
            days = 7  # Default to 1 week
            
            if period == "1 Day":
                days = 1
            elif period == "3 Days":
                days = 3
            elif period == "2 Weeks":
                days = 14
            elif period == "1 Month":
                days = 30
            
            # Get health data for the period
            health_data = self.db_manager.get_health_data_by_timeframe(user_id, days)
            
            if not health_data:
                messagebox.showinfo("No Data", "No health data available for the selected period.")
                return
            
            # Get latest health data for current status
            latest_data = self.db_manager.get_latest_health_data(user_id)
            
            # Update summary text
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.delete(1.0, tk.END)
            
            user_id, name, age, gender, height, weight = user_info
            
            self.summary_text.insert(tk.END, f"Health Summary for {name}\n", "heading")
            self.summary_text.insert(tk.END, f"Age: {age} | Gender: {gender}\n")
            self.summary_text.insert(tk.END, f"Height: {height} cm | Weight: {weight} kg\n\n")
            
            if latest_data:
                record_id, user_id, timestamp, heart_rate, bp_sys, bp_dia, oxygen, temp = latest_data
                
                self.summary_text.insert(tk.END, f"Current Status (as of {timestamp}):\n", "subheading")
                self.summary_text.insert(tk.END, f"Heart Rate: {heart_rate} BPM\n")
                self.summary_text.insert(tk.END, f"Blood Pressure: {bp_sys}/{bp_dia} mmHg\n")
                self.summary_text.insert(tk.END, f"Oxygen Level: {oxygen}%\n")
                self.summary_text.insert(tk.END, f"Temperature: {temp}°C\n\n")
                
                # Get overall health status
                overall_status, overall_msg = self.health_analyzer.get_overall_health_status(latest_data)
                
                self.summary_text.insert(tk.END, f"Overall Health Status: {overall_status}\n", "subheading")
                self.summary_text.insert(tk.END, f"{overall_msg}\n\n")
            
            # Add analysis period info
            self.summary_text.insert(tk.END, f"Analysis Period: {period}\n", "subheading")
            self.summary_text.insert(tk.END, f"Data points analyzed: {len(health_data)}\n\n")
            
            # Calculate averages
            avg_hr = sum(record[3] for record in health_data) / len(health_data)
            avg_sys = sum(record[4] for record in health_data) / len(health_data)
            avg_dia = sum(record[5] for record in health_data) / len(health_data)
            avg_o2 = sum(record[6] for record in health_data) / len(health_data)
            avg_temp = sum(record[7] for record in health_data) / len(health_data)
            
            self.summary_text.insert(tk.END, f"Average Metrics:\n", "subheading")
            self.summary_text.insert(tk.END, f"Heart Rate: {avg_hr:.1f} BPM\n")
            self.summary_text.insert(tk.END, f"Blood Pressure: {avg_sys:.1f}/{avg_dia:.1f} mmHg\n")
            self.summary_text.insert(tk.END, f"Oxygen Level: {avg_o2:.1f}%\n")
            self.summary_text.insert(tk.END, f"Temperature: {avg_temp:.1f}°C\n")
            
            self.summary_text.config(state=tk.DISABLED)
            
            # Text tags for formatting
            self.summary_text.tag_configure("heading", font=("Arial", 12, "bold"))
            self.summary_text.tag_configure("subheading", font=("Arial", 10, "bold"))
            
            # Predict potential conditions
            potential_conditions = self.health_analyzer.predict_potential_conditions(health_data)
            
            # Update conditions treeview
            self.conditions_tree.delete(*self.conditions_tree.get_children())
            
            self.condition_details_data = {}
            
            if potential_conditions:
                for condition in potential_conditions:
                    condition_name = condition["condition"]
                    confidence = condition["confidence"]
                    description = condition["description"]
                    
                    item_id = self.conditions_tree.insert("", "end", values=(condition_name, confidence))
                    self.condition_details_data[item_id] = description
            else:
                self.conditions_tree.insert("", "end", values=("No conditions detected", ""))
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to run analysis: {e}")
    
    def show_condition_details(self, event):
        """Show details for the selected condition"""
        selected_items = self.conditions_tree.selection()
        
        if not selected_items:
            return
        
        item_id = selected_items[0]
        description = self.condition_details_data.get(item_id, "No details available")
        
        self.condition_details.config(state=tk.NORMAL)
        self.condition_details.delete(1.0, tk.END)
        self.condition_details.insert(tk.END, description)
        self.condition_details.config(state=tk.DISABLED)

def main():
    try:
        # Create and run the application
        root = tk.Tk()
        app = HealthMonitorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Application failed to start: {e}")

if __name__ == "__main__":
    main()
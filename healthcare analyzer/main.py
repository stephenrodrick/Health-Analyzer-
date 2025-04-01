import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import sqlite3
from tkcalendar import DateEntry
import matplotlib.dates as mdates
import webbrowser

# Import our modules
from database_setup import create_database
from database_manager import DatabaseManager
from health_analyzer import HealthAnalyzer
from theme_manager import ThemeManager
from visual_components import VisualComponents
from dashboard_widgets import HealthMetricCard, UserInfoPanel, HealthStatusPanel

class HealthMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Health Monitoring System")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 768)
        
        # Set up the theme
        ThemeManager.setup_theme(root)
        
        # Set up matplotlib styling
        VisualComponents.setup_matplotlib_style()
        
        # Initialize database and analyzer
        try:
            self.db_manager = DatabaseManager()
            self.health_analyzer = HealthAnalyzer()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            root.destroy()
            return
        
        # Create header frame
        self.header_frame = ttk.Frame(root)
        self.header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # App title
        header_content = ttk.Frame(self.header_frame, style="Card.TFrame")
        header_content.pack(fill=tk.X, padx=0, pady=0)
        
        title_frame = ttk.Frame(header_content, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, padx=15, pady=10)
        
        app_icon_label = ttk.Label(title_frame, text="🩺", style="Card.TLabel", font=("Arial", 22))
        app_icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        app_title = ttk.Label(title_frame, text="Advanced Health Monitoring System", 
                              style="Card.TLabel", font=("Arial", 18, "bold"))
        app_title.pack(side=tk.LEFT)
        
        # User selection in header
        user_frame = ttk.Frame(header_content, style="Card.TFrame")
        user_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        
        ttk.Label(user_frame, text="Select User:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.user_var = tk.StringVar()
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.user_var, state="readonly", width=25)
        self.user_dropdown.pack(side=tk.LEFT, padx=5)
        self.user_dropdown.bind("<<ComboboxSelected>>", self.on_user_selected)
        
        # Refresh button
        refresh_btn = ttk.Button(user_frame, text="Refresh Data", command=self.update_data)
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # Create main content area
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(self.notebook, style="TFrame")
        self.trends_tab = ttk.Frame(self.notebook, style="TFrame")
        self.analysis_tab = ttk.Frame(self.notebook, style="TFrame")
        self.medications_tab = ttk.Frame(self.notebook, style="TFrame")
        self.medical_history_tab = ttk.Frame(self.notebook, style="TFrame")
        
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.trends_tab, text="Health Trends")
        self.notebook.add(self.analysis_tab, text="Health Analysis")
        self.notebook.add(self.medications_tab, text="Medications")
        self.notebook.add(self.medical_history_tab, text="Medical History")
        
        # Set up the dashboard tab
        self.setup_dashboard()
        
        # Set up the trends tab
        self.setup_trends_tab()
        
        # Set up the analysis tab
        self.setup_analysis_tab()
        
        # Set up the medications tab
        self.setup_medications_tab()
        
        # Set up the medical history tab
        self.setup_medical_history_tab()
        
        # Create footer with status bar
        self.footer_frame = ttk.Frame(root, style="Card.TFrame")
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
        # Status message on the left
        self.status_message = ttk.Label(self.footer_frame, text="Ready", style="Card.TLabel")
        self.status_message.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Clock on the right
        self.clock_label = ttk.Label(self.footer_frame, text="", style="Card.TLabel")
        self.clock_label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.update_clock()
        
        # Help link in the middle
        help_link = ttk.Label(self.footer_frame, text="Help & Resources", 
                             style="Card.TLabel", foreground=ThemeManager.COLORS['secondary'],
                             cursor="hand2")
        help_link.pack(side=tk.RIGHT, padx=20, pady=5)
        help_link.bind("<Button-1>", lambda e: self.open_help())
        
        # Variables for tracking
        self.current_user_id = None
        self.health_cards = {}
        self.metrics_frames = []
        
        # Load users into the dropdown
        self.load_users()
        
        # Update data periodically (every 10 seconds)
        self.root.after(10000, self.update_data)
    
    def update_clock(self):
        """Update the clock in the footer"""
        current_time = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        self.clock_label.configure(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def open_help(self):
        """Open help resources"""
        # This would open a help window or web resource
        messagebox.showinfo("Help Resources", 
                           "The help system would open here.\n\n"
                           "It would provide information about normal ranges, "
                           "how to interpret the health data, and what actions "
                           "to take based on various alerts.")
    
    def setup_dashboard(self):
        """Set up the dashboard tab with current health metrics"""
        # Main content frame - create a 2x2 grid
        main_dashboard = ttk.Frame(self.dashboard_tab, style="TFrame")
        main_dashboard.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure the grid columns - make them equal width
        main_dashboard.columnconfigure(0, weight=1)
        main_dashboard.columnconfigure(1, weight=1)
        
        # Top left: User info panel
        user_frame = ttk.Frame(main_dashboard, style="Card.TFrame")
        user_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.user_panel = UserInfoPanel(user_frame)
        self.user_panel.frame.pack(fill=tk.BOTH, expand=True)
        
        # Top right: Health status and alerts
        status_frame = ttk.Frame(main_dashboard, style="Card.TFrame")
        status_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.health_status_panel = HealthStatusPanel(status_frame)
        self.health_status_panel.frame.pack(fill=tk.BOTH, expand=True)
        
        # Bottom: Health metrics dashboard in a 2x2 grid
        metrics_frame = ttk.Frame(main_dashboard, style="TFrame")
        metrics_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        main_dashboard.rowconfigure(1, weight=1)  # Give more space to metrics
        
        # Configure metrics grid
        metrics_grid = ttk.Frame(metrics_frame, style="TFrame")
        metrics_grid.pack(fill=tk.BOTH, expand=True)
        
        # Create 2x2 grid for health metrics
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
        metrics_grid.rowconfigure(0, weight=1)
        metrics_grid.rowconfigure(1, weight=1)
        
        # Heart Rate Card (top left)
        hr_frame = ttk.Frame(metrics_grid, style="TFrame")
        hr_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.heart_rate_card = HealthMetricCard(hr_frame, "Heart Rate", icon="❤️")
        
        # Blood Pressure Card (top right)
        bp_frame = ttk.Frame(metrics_grid, style="TFrame")
        bp_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.blood_pressure_card = HealthMetricCard(bp_frame, "Blood Pressure", icon="🩸")
        
        # Oxygen Level Card (bottom left)
        ox_frame = ttk.Frame(metrics_grid, style="TFrame")
        ox_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.oxygen_card = HealthMetricCard(ox_frame, "Oxygen Level", icon="🫁")
        
        # Temperature Card (bottom right)
        temp_frame = ttk.Frame(metrics_grid, style="TFrame")
        temp_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.temperature_card = HealthMetricCard(temp_frame, "Temperature", icon="🌡️")
        
        # Store references to cards for updates
        self.health_cards = {
            'heart_rate': self.heart_rate_card,
            'blood_pressure': self.blood_pressure_card,
            'oxygen': self.oxygen_card,
            'temperature': self.temperature_card
        }
    
    def setup_trends_tab(self):
        """Set up the trends tab with historical data visualization"""
        # Top frame for controls
        top_frame = ttk.Frame(self.trends_tab, style="Card.TFrame")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        user_ctrl_frame = ttk.Frame(top_frame, style="Card.TFrame")
        user_ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(user_ctrl_frame, text="Select User:", style="Card.TLabel", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.trends_user_var = tk.StringVar()
        self.trends_user_dropdown = ttk.Combobox(user_ctrl_frame, textvariable=self.trends_user_var, state="readonly", width=25)
        self.trends_user_dropdown.pack(side=tk.LEFT, padx=5)
        self.trends_user_dropdown.bind("<<ComboboxSelected>>", self.on_trends_user_selected)
        
        # Separator
        ttk.Label(top_frame, text="|", style="Card.TLabel").pack(side=tk.LEFT, padx=10)
        
        # Time range selection
        time_ctrl_frame = ttk.Frame(top_frame, style="Card.TFrame")
        time_ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(time_ctrl_frame, text="Time Range:", style="Card.TLabel", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.time_range_var = tk.StringVar(value="1 Day")
        time_ranges = ["1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month", "Custom"]
        self.time_range_dropdown = ttk.Combobox(time_ctrl_frame, textvariable=self.time_range_var, 
                                               values=time_ranges, state="readonly", width=15)
        self.time_range_dropdown.pack(side=tk.LEFT, padx=5)
        self.time_range_dropdown.bind("<<ComboboxSelected>>", self.on_time_range_selected)
        
        # Custom date range frame (initially hidden)
        self.custom_date_frame = ttk.Frame(top_frame, style="Card.TFrame")
        
        date_selection = ttk.Frame(self.custom_date_frame, style="Card.TFrame")
        date_selection.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(date_selection, text="From:", style="Card.TLabel").pack(side=tk.LEFT, padx=(20, 5))
        self.start_date = DateEntry(date_selection, width=12, background=ThemeManager.COLORS['primary'],
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(date_selection, text="To:", style="Card.TLabel").pack(side=tk.LEFT, padx=(10, 5))
        self.end_date = DateEntry(date_selection, width=12, background=ThemeManager.COLORS['primary'],
                                 foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.custom_date_frame, text="Apply Custom Range", style="Primary.TButton",
                  command=self.update_trends).pack(side=tk.LEFT, padx=(20, 5), pady=10)
        
        # Update button
        update_frame = ttk.Frame(top_frame, style="Card.TFrame")
        update_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Button(update_frame, text="Update Chart", style="Primary.TButton",
                  command=self.update_trends).pack(side=tk.RIGHT)
        
        # Data visualization controls
        viz_control_frame = ttk.Frame(self.trends_tab, style="Card.TFrame")
        viz_control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Show/hide reference ranges checkbox
        self.show_ref_ranges = tk.BooleanVar(value=True)
        show_ref_cb = ttk.Checkbutton(viz_control_frame, text="Show Reference Ranges", 
                                     variable=self.show_ref_ranges, command=self.update_trends,
                                     style="Card.TCheckbutton")
        show_ref_cb.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Show data points checkbox
        self.show_data_points = tk.BooleanVar(value=True)
        show_points_cb = ttk.Checkbutton(viz_control_frame, text="Show Data Points", 
                                        variable=self.show_data_points, command=self.update_trends,
                                        style="Card.TCheckbutton")
        show_points_cb.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Show fill areas checkbox
        self.show_fill = tk.BooleanVar(value=True)
        show_fill_cb = ttk.Checkbutton(viz_control_frame, text="Show Fill Areas", 
                                      variable=self.show_fill, command=self.update_trends,
                                      style="Card.TCheckbutton")
        show_fill_cb.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Main content frame for charts
        self.trends_content_frame = ttk.Frame(self.trends_tab, style="Card.TFrame")
        self.trends_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for matplotlib
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8))
        VisualComponents.setup_charts(self.fig, self.axes)
        
        # Create canvas for matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.trends_content_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar (optional - comment out if not needed)
        # from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        # toolbar = NavigationToolbar2Tk(self.canvas, self.trends_content_frame)
        # toolbar.update()
        
        self.fig.canvas.draw()
    
    def setup_analysis_tab(self):
        """Set up the analysis tab with health predictions and insights"""
        # Top frame for controls
        top_frame = ttk.Frame(self.analysis_tab, style="Card.TFrame")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        user_ctrl_frame = ttk.Frame(top_frame, style="Card.TFrame")
        user_ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(user_ctrl_frame, text="Select User:", style="Card.TLabel", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.analysis_user_var = tk.StringVar()
        self.analysis_user_dropdown = ttk.Combobox(user_ctrl_frame, textvariable=self.analysis_user_var, state="readonly", width=25)
        self.analysis_user_dropdown.pack(side=tk.LEFT, padx=5)
        self.analysis_user_dropdown.bind("<<ComboboxSelected>>", self.on_analysis_user_selected)
        
        # Separator
        ttk.Label(top_frame, text="|", style="Card.TLabel").pack(side=tk.LEFT, padx=10)
        
        # Analysis period selection
        period_ctrl_frame = ttk.Frame(top_frame, style="Card.TFrame")
        period_ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(period_ctrl_frame, text="Analysis Period:", style="Card.TLabel", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.analysis_period_var = tk.StringVar(value="1 Week")
        analysis_periods = ["1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month"]
        self.analysis_period_dropdown = ttk.Combobox(period_ctrl_frame, textvariable=self.analysis_period_var, 
                                                   values=analysis_periods, state="readonly", width=15)
        self.analysis_period_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Update button
        update_frame = ttk.Frame(top_frame, style="Card.TFrame")
        update_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Button(update_frame, text="Run Analysis", style="Primary.TButton",
                  command=self.run_analysis).pack(side=tk.RIGHT)
                  
        # Main content area - divided into two sections
        main_content = ttk.Frame(self.analysis_tab, style="TFrame")
        main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel: Summary + Detailed metrics
        left_panel = ttk.Frame(main_content, style="TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Health summary card
        summary_frame = ttk.LabelFrame(left_panel, text="Health Summary", style="Card.TFrame")
        summary_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        summary_content = ttk.Frame(summary_frame, style="Card.TFrame")
        summary_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.summary_text = tk.Text(summary_content, wrap=tk.WORD, height=10, width=40, 
                                   bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.summary_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to summary text
        summary_scroll = ttk.Scrollbar(summary_content, orient=tk.VERTICAL, command=self.summary_text.yview)
        summary_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.config(yscrollcommand=summary_scroll.set)
        self.summary_text.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.summary_text.tag_configure("heading", font=("Arial", 12, "bold"), 
                                      foreground=ThemeManager.COLORS['primary'])
        self.summary_text.tag_configure("subheading", font=("Arial", 10, "bold"), 
                                      foreground=ThemeManager.COLORS['secondary'])
        self.summary_text.tag_configure("normal", font=("Arial", 10))
        self.summary_text.tag_configure("alert", font=("Arial", 10), 
                                      foreground=ThemeManager.COLORS['danger'])
                                      
        # Detailed Metrics Card
        metrics_frame = ttk.LabelFrame(left_panel, text="Health Metrics Analysis", style="Card.TFrame")
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a canvas with scrollbar for metrics
        metrics_canvas = tk.Canvas(metrics_frame, bd=0, highlightthickness=0, bg=ThemeManager.COLORS['card'])
        metrics_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        metrics_scrollbar = ttk.Scrollbar(metrics_frame, orient=tk.VERTICAL, command=metrics_canvas.yview)
        metrics_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        metrics_canvas.configure(yscrollcommand=metrics_scrollbar.set)
        metrics_canvas.bind('<Configure>', lambda e: metrics_canvas.configure(scrollregion=metrics_canvas.bbox("all")))
        
        # Create interior frame for metrics
        metrics_interior = ttk.Frame(metrics_canvas, style="Card.TFrame")
        metrics_canvas.create_window((0, 0), window=metrics_interior, anchor="nw", width=metrics_canvas.winfo_reqwidth())
        
        # Will add gauge widgets here dynamically
        self.metrics_container = metrics_interior
        
        # Right panel: Potential conditions
        right_panel = ttk.Frame(main_content, style="TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Potential conditions frame
        conditions_frame = ttk.LabelFrame(right_panel, text="Potential Health Conditions", style="Card.TFrame")
        conditions_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a treeview for potential conditions with better styling
        columns = ("condition", "confidence")
        self.conditions_tree = ttk.Treeview(conditions_frame, columns=columns, show="headings", 
                                           style="Card.Treeview", height=10)
                                           
        # Define headings
        self.conditions_tree.heading("condition", text="Potential Condition")
        self.conditions_tree.heading("confidence", text="Confidence")
        
        # Define columns
        self.conditions_tree.column("condition", width=200)
        self.conditions_tree.column("confidence", width=100, anchor="center")
        
        # Pack with scrollbar
        tree_container = ttk.Frame(conditions_frame, style="Card.TFrame")
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.conditions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        tree_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.conditions_tree.yview)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conditions_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Bottom frame for condition details
        details_frame = ttk.LabelFrame(right_panel, text="Condition Details", style="Card.TFrame")
        details_frame.pack(fill=tk.X, expand=False, pady=5)
        
        details_content = ttk.Frame(details_frame, style="Card.TFrame")
        details_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.condition_details = tk.Text(details_content, wrap=tk.WORD, height=5,
                                       bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.condition_details.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to condition details
        details_scroll = ttk.Scrollbar(details_content, orient=tk.VERTICAL, command=self.condition_details.yview)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.condition_details.config(yscrollcommand=details_scroll.set)
        self.condition_details.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.condition_details.tag_configure("heading", font=("Arial", 12, "bold"), 
                                          foreground=ThemeManager.COLORS['primary'])
        self.condition_details.tag_configure("normal", font=("Arial", 10))
        
        # Bind selection event to show details
        self.conditions_tree.bind("<<TreeviewSelect>>", self.show_condition_details)
        
        # Action recommendations frame
        actions_frame = ttk.LabelFrame(right_panel, text="Recommended Actions", style="Card.TFrame")
        actions_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        actions_content = ttk.Frame(actions_frame, style="Card.TFrame")
        actions_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.actions_text = tk.Text(actions_content, wrap=tk.WORD, height=5,
                                  bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.actions_text.pack(fill=tk.BOTH, expand=True)
        self.actions_text.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.actions_text.tag_configure("heading", font=("Arial", 12, "bold"), 
                                      foreground=ThemeManager.COLORS['primary'])
        self.actions_text.tag_configure("important", font=("Arial", 10, "bold"),
                                      foreground=ThemeManager.COLORS['danger'])
        self.actions_text.tag_configure("normal", font=("Arial", 10))
    
    def setup_medications_tab(self):
        """Set up the medications tab with current prescriptions and history"""
        # Top frame for controls
        top_frame = ttk.Frame(self.medications_tab, style="Card.TFrame")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        user_ctrl_frame = ttk.Frame(top_frame, style="Card.TFrame")
        user_ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(user_ctrl_frame, text="Select User:", style="Card.TLabel", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.meds_user_var = tk.StringVar()
        self.meds_user_dropdown = ttk.Combobox(user_ctrl_frame, textvariable=self.meds_user_var, state="readonly", width=25)
        self.meds_user_dropdown.pack(side=tk.LEFT, padx=5)
        self.meds_user_dropdown.bind("<<ComboboxSelected>>", self.on_meds_user_selected)
        
        # Update button
        update_frame = ttk.Frame(top_frame, style="Card.TFrame")
        update_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Button(update_frame, text="Refresh Medications", style="Primary.TButton",
                  command=self.update_medications).pack(side=tk.RIGHT)
        
        # Main content area - divided into two sections
        main_content = ttk.Frame(self.medications_tab, style="TFrame")
        main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel: Current medications
        left_panel = ttk.Frame(main_content, style="TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Current medications frame
        # Removed incomplete line causing syntax error
        
        # Current medications frame
        current_meds_frame = ttk.LabelFrame(left_panel, text="Current Medications", style="Card.TFrame")
        current_meds_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a treeview for current medications
        columns = ("medication", "dosage", "frequency", "purpose", "start_date")
        self.current_meds_tree = ttk.Treeview(current_meds_frame, columns=columns, show="headings", 
                                             style="Card.Treeview", height=10)
                                             
        # Define headings
        self.current_meds_tree.heading("medication", text="Medication")
        self.current_meds_tree.heading("dosage", text="Dosage")
        self.current_meds_tree.heading("frequency", text="Frequency")
        self.current_meds_tree.heading("purpose", text="Purpose")
        self.current_meds_tree.heading("start_date", text="Start Date")
        
        # Define columns
        self.current_meds_tree.column("medication", width=150)
        self.current_meds_tree.column("dosage", width=100)
        self.current_meds_tree.column("frequency", width=100)
        self.current_meds_tree.column("purpose", width=150)
        self.current_meds_tree.column("start_date", width=100)
        
        # Pack with scrollbar
        meds_container = ttk.Frame(current_meds_frame, style="Card.TFrame")
        meds_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.current_meds_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        meds_scrollbar = ttk.Scrollbar(meds_container, orient=tk.VERTICAL, command=self.current_meds_tree.yview)
        meds_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.current_meds_tree.configure(yscrollcommand=meds_scrollbar.set)
        
        # Bind selection event
        self.current_meds_tree.bind("<<TreeviewSelect>>", self.show_medication_details)
        
        # Right panel: Medication details and history
        right_panel = ttk.Frame(main_content, style="TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Medication details frame
        details_frame = ttk.LabelFrame(right_panel, text="Medication Details", style="Card.TFrame")
        details_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        details_content = ttk.Frame(details_frame, style="Card.TFrame")
        details_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.med_details_text = tk.Text(details_content, wrap=tk.WORD, height=8,
                                      bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.med_details_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to details text
        details_scroll = ttk.Scrollbar(details_content, orient=tk.VERTICAL, command=self.med_details_text.yview)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.med_details_text.config(yscrollcommand=details_scroll.set)
        self.med_details_text.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.med_details_text.tag_configure("heading", font=("Arial", 12, "bold"), 
                                         foreground=ThemeManager.COLORS['primary'])
        self.med_details_text.tag_configure("subheading", font=("Arial", 10, "bold"), 
                                         foreground=ThemeManager.COLORS['secondary'])
        self.med_details_text.tag_configure("normal", font=("Arial", 10))
        self.med_details_text.tag_configure("warning", font=("Arial", 10, "bold"),
                                         foreground=ThemeManager.COLORS['warning'])
        
        # Medication history frame
        history_frame = ttk.LabelFrame(right_panel, text="Medication History", style="Card.TFrame")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        history_content = ttk.Frame(history_frame, style="Card.TFrame")
        history_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.med_history_text = tk.Text(history_content, wrap=tk.WORD, height=10,
                                      bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.med_history_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to history text
        history_scroll = ttk.Scrollbar(history_content, orient=tk.VERTICAL, command=self.med_history_text.yview)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.med_history_text.config(yscrollcommand=history_scroll.set)
        self.med_history_text.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.med_history_text.tag_configure("heading", font=("Arial", 12, "bold"), 
                                         foreground=ThemeManager.COLORS['primary'])
        self.med_history_text.tag_configure("date", font=("Arial", 10, "bold"), 
                                         foreground=ThemeManager.COLORS['secondary'])
        self.med_history_text.tag_configure("normal", font=("Arial", 10))
    
    def setup_medical_history_tab(self):
        """Set up the medical history tab with diagnoses and conditions"""
        # Top frame for controls
        top_frame = ttk.Frame(self.medical_history_tab, style="Card.TFrame")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User selection
        user_ctrl_frame = ttk.Frame(top_frame, style="Card.TFrame")
        user_ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(user_ctrl_frame, text="Select User:", style="Card.TLabel", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.history_user_var = tk.StringVar()
        self.history_user_dropdown = ttk.Combobox(user_ctrl_frame, textvariable=self.history_user_var, state="readonly", width=25)
        self.history_user_dropdown.pack(side=tk.LEFT, padx=5)
        self.history_user_dropdown.bind("<<ComboboxSelected>>", self.on_history_user_selected)
        
        # Update button
        update_frame = ttk.Frame(top_frame, style="Card.TFrame")
        update_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Button(update_frame, text="Refresh History", style="Primary.TButton",
                  command=self.update_medical_history).pack(side=tk.RIGHT)
        
        # Main content area - divided into sections
        main_content = ttk.Frame(self.medical_history_tab, style="TFrame")
        main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel: Diagnoses and conditions
        left_panel = ttk.Frame(main_content, style="TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Diagnoses frame
        diagnoses_frame = ttk.LabelFrame(left_panel, text="Diagnoses & Conditions", style="Card.TFrame")
        diagnoses_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a treeview for diagnoses
        columns = ("condition", "diagnosed_date", "status", "severity")
        self.diagnoses_tree = ttk.Treeview(diagnoses_frame, columns=columns, show="headings", 
                                          style="Card.Treeview", height=10)
                                          
        # Define headings
        self.diagnoses_tree.heading("condition", text="Condition")
        self.diagnoses_tree.heading("diagnosed_date", text="Diagnosed Date")
        self.diagnoses_tree.heading("status", text="Status")
        self.diagnoses_tree.heading("severity", text="Severity")
        
        # Define columns
        self.diagnoses_tree.column("condition", width=200)
        self.diagnoses_tree.column("diagnosed_date", width=100)
        self.diagnoses_tree.column("status", width=100)
        self.diagnoses_tree.column("severity", width=100)
        
        # Pack with scrollbar
        diagnoses_container = ttk.Frame(diagnoses_frame, style="Card.TFrame")
        diagnoses_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.diagnoses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        diagnoses_scrollbar = ttk.Scrollbar(diagnoses_container, orient=tk.VERTICAL, command=self.diagnoses_tree.yview)
        diagnoses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.diagnoses_tree.configure(yscrollcommand=diagnoses_scrollbar.set)
        
        # Bind selection event
        self.diagnoses_tree.bind("<<TreeviewSelect>>", self.show_condition_history)
        
        # Right panel: Condition details and history
        right_panel = ttk.Frame(main_content, style="TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Condition details frame
        condition_details_frame = ttk.LabelFrame(right_panel, text="Condition Details", style="Card.TFrame")
        condition_details_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        condition_details_content = ttk.Frame(condition_details_frame, style="Card.TFrame")
        condition_details_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.condition_details_text = tk.Text(condition_details_content, wrap=tk.WORD, height=8,
                                           bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.condition_details_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to details text
        condition_details_scroll = ttk.Scrollbar(condition_details_content, orient=tk.VERTICAL, 
                                               command=self.condition_details_text.yview)
        condition_details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.condition_details_text.config(yscrollcommand=condition_details_scroll.set)
        self.condition_details_text.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.condition_details_text.tag_configure("heading", font=("Arial", 12, "bold"), 
                                              foreground=ThemeManager.COLORS['primary'])
        self.condition_details_text.tag_configure("subheading", font=("Arial", 10, "bold"), 
                                              foreground=ThemeManager.COLORS['secondary'])
        self.condition_details_text.tag_configure("normal", font=("Arial", 10))
        
        # Treatment history frame
        treatment_frame = ttk.LabelFrame(right_panel, text="Treatment History", style="Card.TFrame")
        treatment_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        treatment_content = ttk.Frame(treatment_frame, style="Card.TFrame")
        treatment_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.treatment_history_text = tk.Text(treatment_content, wrap=tk.WORD, height=10,
                                           bg=ThemeManager.COLORS['card'], bd=0, highlightthickness=0)
        self.treatment_history_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to history text
        treatment_scroll = ttk.Scrollbar(treatment_content, orient=tk.VERTICAL, command=self.treatment_history_text.yview)
        treatment_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.treatment_history_text.config(yscrollcommand=treatment_scroll.set)
        self.treatment_history_text.config(state=tk.DISABLED)
        
        # Configure text tags for formatting
        self.treatment_history_text.tag_configure("heading", font=("Arial", 12, "bold"), 
                                              foreground=ThemeManager.COLORS['primary'])
        self.treatment_history_text.tag_configure("date", font=("Arial", 10, "bold"), 
                                              foreground=ThemeManager.COLORS['secondary'])
        self.treatment_history_text.tag_configure("normal", font=("Arial", 10))
    
    def load_users(self):
        """Load users into the dropdown menus"""
        try:
            users = self.db_manager.get_user_names()
            user_list = [(uid, name) for uid, name in users]
            
            # Update all dropdowns
            self.user_dropdown['values'] = [name for _, name in user_list]
            self.trends_user_dropdown['values'] = [name for _, name in user_list]
            self.analysis_user_dropdown['values'] = [name for _, name in user_list]
            self.meds_user_dropdown['values'] = [name for _, name in user_list]
            self.history_user_dropdown['values'] = [name for _, name in user_list]
            
            # Store user IDs for lookup
            self.user_ids = {name: uid for uid, name in user_list}
            
            # Select first user by default if available
            if user_list:
                self.user_var.set(user_list[0][1])
                self.trends_user_var.set(user_list[0][1])
                self.analysis_user_var.set(user_list[0][1])
                self.meds_user_var.set(user_list[0][1])
                self.history_user_var.set(user_list[0][1])
                self.current_user_id = user_list[0][0]
                
                # Update data for the selected user
                self.update_dashboard_data()
                self.update_trends()
                self.run_analysis()
                self.update_medications()
                self.update_medical_history()
                
                self.status_message.config(text=f"Loaded {len(user_list)} users successfully")
            else:
                self.status_message.config(text="No users found in database")
        except sqlite3.Error as e:
            self.status_message.config(text=f"Database error: {str(e)[:50]}...")
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
    
    def on_user_selected(self, event):
        """Handle user selection in any dropdown"""
        selected_user = self.user_var.get()
        self.current_user_id = self.user_ids.get(selected_user)
        
        # Update all dropdowns to match
        self.trends_user_var.set(selected_user)
        self.analysis_user_var.set(selected_user)
        self.meds_user_var.set(selected_user)
        self.history_user_var.set(selected_user)
        
        # Update all tabs
        self.update_dashboard_data()
        self.update_trends()
        self.run_analysis()
        self.update_medications()
        self.update_medical_history()
        
        self.status_message.config(text=f"Selected user: {selected_user}")
    
    def on_trends_user_selected(self, event):
        """Handle user selection in the trends tab"""
        selected_user = self.trends_user_var.get()
        
        self.current_user_id = self.user_ids.get(selected_user)
        
        # Update main dropdown to match
        self.user_var.set(selected_user)
        self.analysis_user_var.set(selected_user)
        self.meds_user_var.set(selected_user)
        self.history_user_var.set(selected_user)
        
        # Update trends tab
        self.update_trends()
        
        self.status_message.config(text=f"Trends updated for user: {selected_user}")
    
    def on_analysis_user_selected(self, event):
        """Handle user selection in the analysis tab"""
        selected_user = self.analysis_user_var.get()
        self.current_user_id = self.user_ids.get(selected_user)
        
        # Update main dropdown to match
        self.user_var.set(selected_user)
        self.trends_user_var.set(selected_user)
        self.meds_user_var.set(selected_user)
        self.history_user_var.set(selected_user)
        
        # Update analysis tab
        self.run_analysis()
        
        self.status_message.config(text=f"Analysis updated for user: {selected_user}")
    
    def on_meds_user_selected(self, event):
        """Handle user selection in the medications tab"""
        selected_user = self.meds_user_var.get()
        self.current_user_id = self.user_ids.get(selected_user)
        
        # Update main dropdown to match
        self.user_var.set(selected_user)
        self.trends_user_var.set(selected_user)
        self.analysis_user_var.set(selected_user)
        self.history_user_var.set(selected_user)
        
        # Update medications tab
        self.update_medications()
        
        self.status_message.config(text=f"Medications updated for user: {selected_user}")
    
    def on_history_user_selected(self, event):
        """Handle user selection in the medical history tab"""
        selected_user = self.history_user_var.get()
        self.current_user_id = self.user_ids.get(selected_user)
        
        # Update main dropdown to match
        self.user_var.set(selected_user)
        self.trends_user_var.set(selected_user)
        self.analysis_user_var.set(selected_user)
        self.meds_user_var.set(selected_user)
        
        # Update medical history tab
        self.update_medical_history()
        
        self.status_message.config(text=f"Medical history updated for user: {selected_user}")
    
    def on_time_range_selected(self, event):
        """Handle time range selection in the trends tab"""
        selected_range = self.time_range_var.get()
        
        # Show or hide custom date range frame
        if selected_range == "Custom":
            self.custom_date_frame.pack(side=tk.LEFT)
        else:
            self.custom_date_frame.pack_forget()
            self.update_trends()
            
        self.status_message.config(text=f"Time range set to: {selected_range}")
    
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
            # Get user info with error handling
            user_info = self.db_manager.get_user_info(self.current_user_id)
            if not user_info or len(user_info) != 6:  # Check if we have all required fields
                messagebox.showwarning("Data Error", "Unable to retrieve complete user information")
                return
                
            try:
                user_id, name, age, gender, height, weight, *_ = user_info
                
                # Update user panel with null checks
                if hasattr(self, 'user_panel'):
                    self.user_panel.update(
                        name or "Unknown",
                        age or "N/A",
                        gender or "Unknown",
                        height or "N/A",
                        weight or "N/A"
                    )
            except ValueError as e:
                print(f"Error unpacking user info: {e}")
                return
            
            # Get latest health data
            health_data = self.db_manager.get_latest_health_data(self.current_user_id)
            if health_data:
                record_id, user_id, timestamp, heart_rate, bp_sys, bp_dia, oxygen, temp = health_data
                
                # Analyze health data
                hr_status, hr_msg = self.health_analyzer.analyze_heart_rate(heart_rate)
                bp_status, bp_msg, sys_msg, dia_msg = self.health_analyzer.analyze_blood_pressure(bp_sys, bp_dia)
                ox_status, ox_msg = self.health_analyzer.analyze_oxygen_level(oxygen)
                temp_status, temp_msg = self.health_analyzer.analyze_temperature(temp)
                
                # Update heart rate card
                self.health_cards['heart_rate'].update(
                    heart_rate, "BPM", 
                    hr_status, 
                    "60-100 BPM",
                    timestamp,
                    "Heart rate represents the number of times your heart beats per minute."
                )
                
                # Update blood pressure card
                self.health_cards['blood_pressure'].update(
                    f"{bp_sys}/{bp_dia}", "mmHg", 
                    bp_status, 
                    "Below 120/80 mmHg",
                    timestamp,
                    "Blood pressure measures the force of blood pushing against artery walls."
                )
                
                # Update oxygen card
                self.health_cards['oxygen'].update(
                    oxygen, "%", 
                    ox_status, 
                    "95-100%",
                    timestamp,
                    "Oxygen saturation indicates the percentage of hemoglobin binding sites occupied by oxygen."
                )
                
                # Update temperature card
                self.health_cards['temperature'].update(
                    temp, "°C", 
                    temp_status, 
                    "36.5-37.5°C",
                    timestamp,
                    "Body temperature is regulated by the hypothalamus and indicates metabolic health."
                )
                
                # Update overall status
                overall_status, overall_msg = self.health_analyzer.get_overall_health_status(health_data)
                
                # Create alerts list
                alerts = []
                if hr_status != "Normal":
                    alerts.append({'status': hr_status, 'message': hr_msg})
                if bp_status != "Normal":
                    alerts.append({'status': bp_status, 'message': sys_msg})
                    alerts.append({'status': bp_status, 'message': dia_msg})
                if ox_status != "Normal":
                    alerts.append({'status': ox_status, 'message': ox_msg})
                if temp_status != "Normal":
                    alerts.append({'status': temp_status, 'message': temp_msg})
                
                # Update health status panel
                self.health_status_panel.update(overall_status, alerts)
                
                self.status_message.config(text=f"Dashboard updated at {datetime.datetime.now().strftime('%H:%M:%S')}")
            else:
                messagebox.showinfo("No Data", "No health data available for this user.")
                self.status_message.config(text="No health data available")
        except sqlite3.Error as e:
            self.status_message.config(text=f"Database error: {str(e)[:50]}...")
            messagebox.showerror("Database Error", f"Failed to update data: {e}")
    
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
                self.status_message.config(text="No data for selected time range")
                return
            
            # Extract data
            timestamps = [datetime.datetime.strptime(record[2], '%Y-%m-%d %H:%M:%S') for record in health_data]
            heart_rates = [record[3] for record in health_data]
            bp_systolic = [record[4] for record in health_data]
            bp_diastolic = [record[5] for record in health_data]
            oxygen_levels = [record[6] for record in health_data]
            temperatures = [record[7] for record in health_data]
            
            # Update charts using the VisualComponents utility
            VisualComponents.update_charts(
                self.axes, timestamps, heart_rates, bp_systolic, 
                bp_diastolic, oxygen_levels, temperatures
            )
            
            # Adjust layout and redraw
            self.fig.tight_layout()
            self.canvas.draw()
            
            self.status_message.config(text=f"Trends chart updated with {len(health_data)} data points")
            
        except sqlite3.Error as e:
            self.status_message.config(text=f"Database error: {str(e)[:50]}...")
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
            
            user_id, name, age, gender, height, weight = user_info[:6]
            
            self.summary_text.insert(tk.END, f"Health Summary for {name}\n\n", "heading")
            self.summary_text.insert(tk.END, f"Age: {age} | Gender: {gender}\n", "normal")
            self.summary_text.insert(tk.END, f"Height: {height} cm | Weight: {weight} kg\n\n", "normal")
            
            if latest_data:
                record_id, user_id, timestamp, heart_rate, bp_sys, bp_dia, oxygen, temp = latest_data
                
                self.summary_text.insert(tk.END, f"Current Status (as of {timestamp}):\n", "subheading")
                self.summary_text.insert(tk.END, f"• Heart Rate: {heart_rate} BPM\n", "normal")
                self.summary_text.insert(tk.END, f"• Blood Pressure: {bp_sys}/{bp_dia} mmHg\n", "normal")
                self.summary_text.insert(tk.END, f"• Oxygen Level: {oxygen}%\n", "normal")
                self.summary_text.insert(tk.END, f"• Temperature: {temp}°C\n\n", "normal")
                
                # Get overall health status
                overall_status, overall_msg = self.health_analyzer.get_overall_health_status(latest_data)
                
                self.summary_text.insert(tk.END, f"Overall Health Status: {overall_status}\n", "subheading")
                
                if overall_status != "Normal":
                    self.summary_text.insert(tk.END, f"{overall_msg}\n\n", "alert")
                else:
                    self.summary_text.insert(tk.END, f"{overall_msg}\n\n", "normal")
            
            # Add analysis period info
            self.summary_text.insert(tk.END, f"Analysis Period: {period}\n", "subheading")
            self.summary_text.insert(tk.END, f"Data points analyzed: {len(health_data)}\n\n", "normal")
            
            # Calculate averages
            avg_hr = sum(record[3] for record in health_data) / len(health_data)
            avg_sys = sum(record[4] for record in health_data) / len(health_data)
            avg_dia = sum(record[5] for record in health_data) / len(health_data)
            avg_o2 = sum(record[6] for record in health_data) / len(health_data)
            avg_temp = sum(record[7] for record in health_data) / len(health_data)
            
            self.summary_text.insert(tk.END, f"Average Metrics:\n", "subheading")
            self.summary_text.insert(tk.END, f"• Heart Rate: {avg_hr:.1f} BPM\n", "normal")
            self.summary_text.insert(tk.END, f"• Blood Pressure: {avg_sys:.1f}/{avg_dia:.1f} mmHg\n", "normal")
            self.summary_text.insert(tk.END, f"• Oxygen Level: {avg_o2:.1f}%\n", "normal")
            self.summary_text.insert(tk.END, f"• Temperature: {avg_temp:.1f}°C\n", "normal")
            
            self.summary_text.config(state=tk.DISABLED)
            
            # Clear previous metrics gauges
            for widget in self.metrics_container.winfo_children():
                widget.destroy()
            
            # Create new gauges for metrics
            # Heart Rate
            hr_gauge = VisualComponents.create_gauge(
                self.metrics_container, "Heart Rate", 40, 140, avg_hr, "BPM", 
                warning_threshold=100, danger_threshold=120
            )
            hr_gauge.pack(pady=10, fill=tk.X)
            
            # Blood Pressure
            bp_sys_gauge = VisualComponents.create_gauge(
                self.metrics_container, "Systolic BP", 90, 180, avg_sys, "mmHg", 
                warning_threshold=130, danger_threshold=140
            )
            bp_sys_gauge.pack(pady=10, fill=tk.X)
            
            bp_dia_gauge = VisualComponents.create_gauge(
                self.metrics_container, "Diastolic BP", 50, 120, avg_dia, "mmHg", 
                warning_threshold=80, danger_threshold=90
            )
            bp_dia_gauge.pack(pady=10, fill=tk.X)
            
            # Oxygen Level
            o2_gauge = VisualComponents.create_gauge(
                self.metrics_container, "Oxygen Saturation", 85, 100, avg_o2, "%", 
                warning_threshold=92, danger_threshold=90
            )
            o2_gauge.pack(pady=10, fill=tk.X)
            
            # Temperature
            temp_gauge = VisualComponents.create_gauge(
                self.metrics_container, "Temperature", 35, 40, avg_temp, "°C", 
                warning_threshold=37.5, danger_threshold=38
            )
            temp_gauge.pack(pady=10, fill=tk.X)
            
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
                    
                # Update actions for conditions
                self.actions_text.config(state=tk.NORMAL)
                self.actions_text.delete(1.0, tk.END)
                self.actions_text.insert(tk.END, "Recommended Actions\n\n", "heading")
                
                if any(c["condition"] == "Hypertension Risk" for c in potential_conditions):
                    self.actions_text.insert(tk.END, "• Monitor blood pressure regularly\n", "important")
                    self.actions_text.insert(tk.END, "• Consider reducing sodium intake\n", "normal")
                    self.actions_text.insert(tk.END, "• Increase physical activity\n", "normal")
                    
                if any(c["condition"] == "Tachycardia Tendency" for c in potential_conditions):
                    self.actions_text.insert(tk.END, "• Monitor heart rate during activity\n", "important")
                    self.actions_text.insert(tk.END, "• Consider stress reduction techniques\n", "normal")
                    self.actions_text.insert(tk.END, "• Limit caffeine and stimulants\n", "normal")
                    
                if any(c["condition"] == "Respiratory Concern" for c in potential_conditions):
                    self.actions_text.insert(tk.END, "• Monitor oxygen levels closely\n", "important")
                    self.actions_text.insert(tk.END, "• Consider respiratory assessment\n", "normal")
                
                if any(c["condition"] == "Recurring Fever" for c in potential_conditions):
                    self.actions_text.insert(tk.END, "• Monitor temperature regularly\n", "important")
                    self.actions_text.insert(tk.END, "• Consider evaluation for infection\n", "normal")
                
                self.actions_text.config(state=tk.DISABLED)
            else:
                self.conditions_tree.insert("", "end", values=("No conditions detected", ""))
                
                self.actions_text.config(state=tk.NORMAL)
                self.actions_text.delete(1.0, tk.END)
                self.actions_text.insert(tk.END, "Recommended Actions\n\n", "heading")
                self.actions_text.insert(tk.END, "• Continue regular health monitoring\n", "normal")
                self.actions_text.insert(tk.END, "• Maintain healthy lifestyle habits\n", "normal")
                self.actions_text.insert(tk.END, "• Schedule routine check-ups\n", "normal")
                self.actions_text.config(state=tk.DISABLED)
                
            self.status_message.config(text=f"Health analysis completed for {name}")
                
        except sqlite3.Error as e:
            self.status_message.config(text=f"Database error: {str(e)[:50]}...")
            messagebox.showerror("Database Error", f"Failed to run analysis: {e}")
    
    def update_medications(self):
        """Update the medications tab with current prescriptions"""
        selected_user = self.meds_user_var.get()
        if not selected_user:
            return
        
        user_id = self.user_ids.get(selected_user)
        if not user_id:
            return
        
        try:
            # In a real application, this would fetch from the database
            # For this example, we'll use mock data
            medications = [
                {
                    "id": 1,
                    "name": "Lisinopril",
                    "dosage": "10mg",
                    "frequency": "Once daily",
                    "purpose": "Blood pressure control",
                    "start_date": "2023-01-15",
                    "end_date": None,
                    "prescriber": "Dr. Sarah Johnson",
                    "notes": "Take in the morning with food",
                    "side_effects": "Dry cough, dizziness, headache",
                    "interactions": "NSAIDs may reduce effectiveness"
                },
                {
                    "id": 2,
                    "name": "Metformin",
                    "dosage": "500mg",
                    "frequency": "Twice daily",
                    "purpose": "Diabetes management",
                    "start_date": "2023-02-10",
                    "end_date": None,
                    "prescriber": "Dr. Michael Chen",
                    "notes": "Take with meals to reduce GI side effects",
                    "side_effects": "Nausea, diarrhea, stomach upset",
                    "interactions": "Alcohol may increase risk of lactic acidosis"
                },
                {
                    "id": 3,
                    "name": "Atorvastatin",
                    "dosage": "20mg",
                    "frequency": "Once daily",
                    "purpose": "Cholesterol management",
                    "start_date": "2023-03-05",
                    "end_date": None,
                    "prescriber": "Dr. Sarah Johnson",
                    "notes": "Take in the evening",
                    "side_effects": "Muscle pain, liver enzyme elevation",
                    "interactions": "Grapefruit juice may increase side effects"
                }
            ]
            
            # Clear current medications tree
            self.current_meds_tree.delete(*self.current_meds_tree.get_children())
            
            # Add medications to tree
            for med in medications:
                self.current_meds_tree.insert("", "end", values=(
                    med["name"],
                    med["dosage"],
                    med["frequency"],
                    med["purpose"],
                    med["start_date"]
                ), tags=(str(med["id"]),))
            
            # Clear medication details
            self.med_details_text.config(state=tk.NORMAL)
            self.med_details_text.delete(1.0, tk.END)
            self.med_details_text.insert(tk.END, "Select a medication to view details", "normal")
            self.med_details_text.config(state=tk.DISABLED)
            
            # Clear medication history
            self.med_history_text.config(state=tk.NORMAL)
            self.med_history_text.delete(1.0, tk.END)
            self.med_history_text.insert(tk.END, "Medication History\n\n", "heading")
            
            # Add mock medication history
            self.med_history_text.insert(tk.END, "2023-01-15: ", "date")
            self.med_history_text.insert(tk.END, "Started Lisinopril 10mg daily for hypertension\n\n", "normal")
            
            self.med_history_text.insert(tk.END, "2023-02-10: ", "date")
            self.med_history_text.insert(tk.END, "Started Metformin 500mg twice daily for diabetes\n\n", "normal")
            
            self.med_history_text.insert(tk.END, "2023-03-05: ", "date")
            self.med_history_text.insert(tk.END, "Started Atorvastatin 20mg daily for high cholesterol\n\n", "normal")
            
            self.med_history_text.insert(tk.END, "2023-04-20: ", "date")
            self.med_history_text.insert(tk.END, "Lisinopril dosage adjusted from 5mg to 10mg due to inadequate BP control\n\n", "normal")
            
            self.med_history_text.config(state=tk.DISABLED)
            
            self.status_message.config(text=f"Medications updated for {selected_user}")
            
        except Exception as e:
            self.status_message.config(text=f"Error updating medications: {str(e)[:50]}...")
            messagebox.showerror("Error", f"Failed to update medications: {e}")
    
    def show_medication_details(self, event):
        """Show details for the selected medication"""
        selected_items = self.current_meds_tree.selection()
        
        if not selected_items:
            return
        
        # Get the medication name from the selected item
        med_name = self.current_meds_tree.item(selected_items[0])['values'][0]
        
        # Mock medication details - in a real app, this would come from the database
        med_details = {
            "Lisinopril": {
                "name": "Lisinopril",
                "class": "ACE Inhibitor",
                "dosage": "10mg",
                "frequency": "Once daily",
                "purpose": "Blood pressure control",
                "start_date": "2023-01-15",
                "prescriber": "Dr. Sarah Johnson",
                "notes": "Take in the morning with food",
                "side_effects": "Dry cough, dizziness, headache",
                "interactions": "NSAIDs may reduce effectiveness",
                "monitoring": "Regular blood pressure checks, kidney function tests"
            },
            "Metformin": {
                "name": "Metformin",
                "class": "Biguanide",
                "dosage": "500mg",
                "frequency": "Twice daily",
                "purpose": "Diabetes management",
                "start_date": "2023-02-10",
                "prescriber": "Dr. Michael Chen",
                "notes": "Take with meals to reduce GI side effects",
                "side_effects": "Nausea, diarrhea, stomach upset",
                "interactions": "Alcohol may increase risk of lactic acidosis",
                "monitoring": "Regular HbA1c tests, kidney function"
            },
            "Atorvastatin": {
                "name": "Atorvastatin",
                "class": "Statin",
                "dosage": "20mg",
                "frequency": "Once daily",
                "purpose": "Cholesterol management",
                "start_date": "2023-03-05",
                "prescriber": "Dr. Sarah Johnson",
                "notes": "Take in the evening",
                "side_effects": "Muscle pain, liver enzyme elevation",
                "interactions": "Grapefruit juice may increase side effects",
                "monitoring": "Regular lipid panel, liver function tests"
            }
        }
        
        details = med_details.get(med_name, {})
        if not details:
            return
        
        # Update medication details text
        self.med_details_text.config(state=tk.NORMAL)
        self.med_details_text.delete(1.0, tk.END)
        
        self.med_details_text.insert(tk.END, f"{details['name']} ({details['class']})\n\n", "heading")
        self.med_details_text.insert(tk.END, f"Dosage: {details['dosage']} {details['frequency']}\n", "normal")
        self.med_details_text.insert(tk.END, f"Purpose: {details['purpose']}\n", "normal")
        self.med_details_text.insert(tk.END, f"Prescribed by: {details['prescriber']} on {details['start_date']}\n\n", "normal")
        
        self.med_details_text.insert(tk.END, "Instructions:\n", "subheading")
        self.med_details_text.insert(tk.END, f"{details['notes']}\n\n", "normal")
        
        self.med_details_text.insert(tk.END, "Potential Side Effects:\n", "subheading")
        self.med_details_text.insert(tk.END, f"{details['side_effects']}\n\n", "normal")
        
        self.med_details_text.insert(tk.END, "Drug Interactions:\n", "subheading")
        self.med_details_text.insert(tk.END, f"{details['interactions']}\n\n", "warning")
        
        self.med_details_text.insert(tk.END, "Monitoring Required:\n", "subheading")
        self.med_details_text.insert(tk.END, f"{details['monitoring']}\n", "normal")
        
        self.med_details_text.config(state=tk.DISABLED)
    
    def update_medical_history(self):
        """Update the medical history tab with diagnoses and conditions"""
        selected_user = self.history_user_var.get()
        if not selected_user:
            return
        
        user_id = self.user_ids.get(selected_user)
        if not user_id:
            return
        
        try:
            # In a real application, this would fetch from the database
            # For this example, we'll use mock data
            conditions = [
                {
                    "id": 1,
                    "name": "Hypertension",
                    "diagnosed_date": "2022-11-10",
                    "status": "Active",
                    "severity": "Moderate",
                    "description": "Essential hypertension with systolic readings consistently above 140 mmHg",
                    "treating_physician": "Dr. Sarah Johnson",
                    "notes": "Family history of hypertension. Patient advised on lifestyle modifications."
                },
                {
                    "id": 2,
                    "name": "Type 2 Diabetes",
                    "diagnosed_date": "2022-12-05",
                    "status": "Active",
                    "severity": "Mild",
                    "description": "Type 2 diabetes mellitus with HbA1c of 7.2%",
                    "treating_physician": "Dr. Michael Chen",
                    "notes": "Currently managed with oral medication and diet. Regular monitoring required."
                },
                {
                    "id": 3,
                    "name": "Hyperlipidemia",
                    "diagnosed_date": "2023-01-20",
                    "status": "Active",
                    "severity": "Mild",
                    "description": "Elevated LDL cholesterol levels",
                    "treating_physician": "Dr. Sarah Johnson",
                    "notes": "Dietary changes implemented with statin therapy."
                }
            ]
            
            # Clear diagnoses tree
            self.diagnoses_tree.delete(*self.diagnoses_tree.get_children())
            
            # Add conditions to tree
            for condition in conditions:
                self.diagnoses_tree.insert("", "end", values=(
                    condition["name"],
                    condition["diagnosed_date"],
                    condition["status"],
                    condition["severity"]
                ), tags=(str(condition["id"]),))
            
            # Clear condition details
            self.condition_details_text.config(state=tk.NORMAL)
            self.condition_details_text.delete(1.0, tk.END)
            self.condition_details_text.insert(tk.END, "Select a condition to view details", "normal")
            self.condition_details_text.config(state=tk.DISABLED)
            
            # Clear treatment history
            self.treatment_history_text.config(state=tk.NORMAL)
            self.treatment_history_text.delete(1.0, tk.END)
            self.treatment_history_text.insert(tk.END, "Treatment History\n\n", "heading")
            
            # Add mock treatment history
            self.treatment_history_text.insert(tk.END, "2022-11-10: ", "date")
            self.treatment_history_text.insert(tk.END, "Diagnosed with hypertension. Started on Lisinopril 5mg daily.\n\n", "normal")
            
            self.treatment_history_text.insert(tk.END, "2022-12-05: ", "date")
            self.treatment_history_text.insert(tk.END, "Diagnosed with Type 2 Diabetes. Started on Metformin 500mg daily.\n\n", "normal")
            
            self.treatment_history_text.insert(tk.END, "2023-01-20: ", "date")
            self.treatment_history_text.insert(tk.END, "Diagnosed with hyperlipidemia. Started on Atorvastatin 20mg daily.\n\n", "normal")
            
            self.treatment_history_text.insert(tk.END, "2023-04-20: ", "date")
            self.treatment_history_text.insert(tk.END, "Follow-up for hypertension. BP still elevated. Lisinopril increased to 10mg daily.\n\n", "normal")
            
            self.treatment_history_text.config(state=tk.DISABLED)
            
            self.status_message.config(text=f"Medical history updated for {selected_user}")
            
        except Exception as e:
            self.status_message.config(text=f"Error updating medical history: {str(e)[:50]}...")
            messagebox.showerror("Error", f"Failed to update medical history: {e}")
    
    def show_condition_history(self, event):
        """Show details for the selected condition"""
        selected_items = self.diagnoses_tree.selection()
        
        if not selected_items:
            return
        
        # Get the condition name from the selected item
        condition_name = self.diagnoses_tree.item(selected_items[0])['values'][0]
        
        # Mock condition details - in a real app, this would come from the database
        condition_details = {
            "Hypertension": {
                "name": "Hypertension",
                "diagnosed_date": "2022-11-10",
                "status": "Active",
                "severity": "Moderate",
                "description": "Essential hypertension with systolic readings consistently above 140 mmHg",
                "treating_physician": "Dr. Sarah Johnson",
                "notes": "Family history of hypertension. Patient advised on lifestyle modifications.",
                "risk_factors": "Family history, sedentary lifestyle, high sodium diet",
                "complications": "Increased risk of heart disease, stroke, kidney damage",
                "treatment_plan": "Medication (ACE inhibitor), dietary changes, regular exercise, stress management"
            },
            "Type 2 Diabetes": {
                "name": "Type 2 Diabetes",
                "diagnosed_date": "2022-12-05",
                "status": "Active",
                "severity": "Mild",
                "description": "Type 2 diabetes mellitus with HbA1c of 7.2%",
                "treating_physician": "Dr. Michael Chen",
                "notes": "Currently managed with oral medication and diet. Regular monitoring required.",
                "risk_factors": "Family history, obesity, sedentary lifestyle",
                "complications": "Neuropathy, retinopathy, cardiovascular disease",
                "treatment_plan": "Metformin, dietary changes, regular exercise, blood glucose monitoring"
            },
            "Hyperlipidemia": {
                "name": "Hyperlipidemia",
                "diagnosed_date": "2023-01-20",
                "status": "Active",
                "severity": "Mild",
                "description": "Elevated LDL cholesterol levels",
                "treating_physician": "Dr. Sarah Johnson",
                "notes": "Dietary changes implemented with statin therapy.",
                "risk_factors": "Diet high in saturated fats, family history, obesity",
                "complications": "Atherosclerosis, coronary artery disease",
                "treatment_plan": "Statin therapy, dietary changes, regular exercise, lipid panel monitoring"
            }
        }
        
        details = condition_details.get(condition_name, {})
        if not details:
            return
        
        # Update condition details text
        self.condition_details_text.config(state=tk.NORMAL)
        self.condition_details_text.delete(1.0, tk.END)
        
        self.condition_details_text.insert(tk.END, f"{details['name']}\n\n", "heading")
        self.condition_details_text.insert(tk.END, f"Diagnosed: {details['diagnosed_date']} by {details['treating_physician']}\n", "normal")
        self.condition_details_text.insert(tk.END, f"Status: {details['status']} | Severity: {details['severity']}\n\n", "normal")
        
        self.condition_details_text.insert(tk.END, "Description:\n", "subheading")
        self.condition_details_text.insert(tk.END, f"{details['description']}\n\n", "normal")
        
        self.condition_details_text.insert(tk.END, "Risk Factors:\n", "subheading")
        self.condition_details_text.insert(tk.END, f"{details['risk_factors']}\n\n", "normal")
        
        self.condition_details_text.insert(tk.END, "Potential Complications:\n", "subheading")
        self.condition_details_text.insert(tk.END, f"{details['complications']}\n\n", "normal")
        
        self.condition_details_text.insert(tk.END, "Treatment Plan:\n", "subheading")
        self.condition_details_text.insert(tk.END, f"{details['treatment_plan']}\n\n", "normal")
        
        self.condition_details_text.insert(tk.END, "Notes:\n", "subheading")
        self.condition_details_text.insert(tk.END, f"{details['notes']}\n", "normal")
        
        self.condition_details_text.config(state=tk.DISABLED)
    
    def show_condition_details(self, event):
        """Show details for the selected condition"""
        selected_items = self.conditions_tree.selection()
        
        if not selected_items:
            return
        
        item_id = selected_items[0]
        description = self.condition_details_data.get(item_id, "No details available")
        
        self.condition_details.config(state=tk.NORMAL)
        self.condition_details.delete(1.0, tk.END)
        
        # Get the condition name
        condition = self.conditions_tree.item(item_id)['values'][0]
        
        self.condition_details.insert(tk.END, f"{condition}\n\n", "heading")
        self.condition_details.insert(tk.END, description, "normal")
        self.condition_details.config(state=tk.DISABLED)

def main():
    # Create database if it doesn't exist
    try:
        create_database()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        return
    
    # Create and run the application
    root = tk.Tk()
    app = HealthMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
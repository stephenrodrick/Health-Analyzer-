import tkinter as tk
from tkinter import ttk
from datetime import datetime

from theme_manager import ThemeManager
from visual_components import VisualComponents

class HealthMetricCard:
    """A card widget for displaying a health metric with reference information"""
    def __init__(self, parent, title, icon=None):
        self.frame = ttk.Frame(parent, style="Card.TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title bar
        title_frame = ttk.Frame(self.frame, style="Card.TFrame")
        title_frame.pack(fill=tk.X, pady=(5, 0), padx=10)
        
        # Icon (if provided)
        self.icon_label = None
        if icon:
            self.icon_label = ttk.Label(title_frame, text=icon, style="Card.TLabel")
            self.icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Title
        self.title_label = ttk.Label(title_frame, text=title, style="SubHeader.TLabel")
        self.title_label.pack(side=tk.LEFT)
        
        # Timestamp
        self.timestamp_label = ttk.Label(title_frame, text="Last updated: --", style="Card.TLabel", font=("Arial", 8))
        self.timestamp_label.pack(side=tk.RIGHT)
        
        # Value frame
        value_frame = ttk.Frame(self.frame, style="Card.TFrame")
        value_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Current value
        self.value_label = ttk.Label(value_frame, text="--", style="Card.TLabel", font=("Arial", 24))
        self.value_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Unit
        self.unit_label = ttk.Label(value_frame, text="", style="Card.TLabel")
        self.unit_label.pack(side=tk.LEFT, pady=(8, 0))  # Align with the bottom of value_label
        
        # Status indicator
        self.status_frame = VisualComponents.create_health_indicator(value_frame)
        self.status_frame.pack(side=tk.RIGHT, padx=10)
        
        # Reference range frame
        ref_frame = ttk.Frame(self.frame, style="Card.TFrame")
        ref_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Reference range label
        self.ref_label = ttk.Label(ref_frame, text="Normal range: --", style="Card.TLabel", font=("Arial", 9))
        self.ref_label.pack(side=tk.LEFT)
        
        # Separator
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Bottom info frame
        info_frame = ttk.Frame(self.frame, style="Card.TFrame")
        info_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Additional info label
        self.info_label = ttk.Label(info_frame, text="", style="Card.TLabel", font=("Arial", 9))
        self.info_label.pack(side=tk.LEFT)
    
    def update(self, value, unit, status, ref_range, timestamp=None, info=""):
        """Update the card with new values"""
        self.value_label.config(text=str(value))
        self.unit_label.config(text=unit)
        self.status_frame.update_status(status)
        self.ref_label.config(text=f"Normal range: {ref_range}")
        
        if timestamp:
            time_str = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d-%m-%Y')
            self.timestamp_label.config(text=f"Last updated: {time_str}")
        
        self.info_label.config(text=info)
        
        return self.frame
        
class UserInfoPanel:
    """A panel displaying user information"""
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style="Card.TFrame")
        
        # User header
        header_frame = ttk.Frame(self.frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=5, padx=10)
        
        self.user_icon = ttk.Label(header_frame, text="👤", style="Card.TLabel", font=("Arial", 20))
        self.user_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.user_name = ttk.Label(header_frame, text="User Name", style="Card.TLabel", font=("Arial", 16, "bold"))
        self.user_name.pack(side=tk.LEFT)
        
        # User details (two-column grid)
        details_frame = ttk.Frame(self.frame, style="Card.TFrame")
        details_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Labels
        ttk.Label(details_frame, text="Age:", style="Card.TLabel", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(details_frame, text="Gender:", style="Card.TLabel", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(details_frame, text="Height:", style="Card.TLabel", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", pady=2, padx=(15,0))
        ttk.Label(details_frame, text="Weight:", style="Card.TLabel", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", pady=2, padx=(15,0))
        
        # Values
        self.age_label = ttk.Label(details_frame, text="--", style="Card.TLabel")
        self.age_label.grid(row=0, column=1, sticky="w", padx=(5,0))
        
        self.gender_label = ttk.Label(details_frame, text="--", style="Card.TLabel")
        self.gender_label.grid(row=1, column=1, sticky="w", padx=(5,0))
        
        self.height_label = ttk.Label(details_frame, text="--", style="Card.TLabel")
        self.height_label.grid(row=0, column=3, sticky="w", padx=(5,0))
        
        self.weight_label = ttk.Label(details_frame, text="--", style="Card.TLabel")
        self.weight_label.grid(row=1, column=3, sticky="w", padx=(5,0))
        
    def update(self, name, age, gender, height, weight):
        """Update user information"""
        self.user_name.config(text=name)
        self.age_label.config(text=f"{age} years")
        self.gender_label.config(text=gender)
        self.height_label.config(text=f"{height} cm")
        self.weight_label.config(text=f"{weight} kg")
        
        return self.frame

class HealthStatusPanel:
    """A panel for displaying overall health status"""
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style="Card.TFrame")
        
        # Header
        header_frame = ttk.Frame(self.frame, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=5, padx=10)
        
        ttk.Label(header_frame, text="Overall Health Status", style="SubHeader.TLabel").pack(side=tk.LEFT)
        
        # Status display
        status_frame = ttk.Frame(self.frame, style="Card.TFrame")
        status_frame.pack(fill=tk.X, pady=10, padx=20)
        
        self.status_label = ttk.Label(status_frame, text="NORMAL", style="Normal.TLabel", font=("Arial", 24, "bold"))
        self.status_label.pack(side=tk.TOP, anchor="center")
        
        # Separator
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)
        
        # Alerts section
        alerts_header = ttk.Frame(self.frame, style="Card.TFrame")
        alerts_header.pack(fill=tk.X, pady=5, padx=10)
        
        ttk.Label(alerts_header, text="Active Alerts", style="Card.TLabel", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Alerts content
        alerts_frame = ttk.Frame(self.frame, style="Card.TFrame")
        alerts_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
        
        # Scrollable text area for alerts
        self.alerts_text = tk.Text(alerts_frame, wrap=tk.WORD, height=10, 
                                   bg=ThemeManager.COLORS['card'], bd=0, 
                                   highlightthickness=0, font=("Arial", 10))
        self.alerts_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Scrollbar for alerts text
        scrollbar = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, command=self.alerts_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alerts_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
        
        # Configure tags for text styling
        self.alerts_text.tag_configure("normal", foreground=ThemeManager.STATUS_COLORS['Normal'])
        self.alerts_text.tag_configure("caution", foreground=ThemeManager.STATUS_COLORS['Caution'])
        self.alerts_text.tag_configure("warning", foreground=ThemeManager.STATUS_COLORS['Warning'])
        self.alerts_text.tag_configure("danger", foreground=ThemeManager.STATUS_COLORS['Danger'])
        self.alerts_text.tag_configure("title", font=("Arial", 11, "bold"))
        
    def update(self, status, alerts_list=None):
        """Update health status and alerts"""
        self.status_label.config(text=status.upper(), style=f"{status}.TLabel")
        
        self.alerts_text.config(state=tk.NORMAL)
        self.alerts_text.delete(1.0, tk.END)
        
        if not alerts_list:
            self.alerts_text.insert(tk.END, "No health alerts at this time.\n\n", "normal")
            self.alerts_text.insert(tk.END, "All health metrics are within normal ranges.", "normal")
        else:
            # Insert overall message
            self.alerts_text.insert(tk.END, "Health Concerns\n\n", "title")
            
            # Add each alert with appropriate styling
            for alert in alerts_list:
                if 'status' in alert and 'message' in alert:
                    self.alerts_text.insert(tk.END, f"• {alert['message']}\n", alert['status'].lower())
                else:
                    self.alerts_text.insert(tk.END, f"• {alert}\n", "warning")
        
        self.alerts_text.config(state=tk.DISABLED)
        
        return self.frame




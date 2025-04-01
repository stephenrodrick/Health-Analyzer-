import tkinter as tk
from tkinter import ttk
import platform

class ThemeManager:
    """Manages the application theme and styling"""
    
    # Color palette
    COLORS = {
        'primary': '#2C3E50',       # Dark blue-gray
        'secondary': '#3498DB',     # Blue
        'accent': '#2ECC71',        # Green
        'warning': '#F39C12',       # Orange 
        'danger': '#E74C3C',        # Red
        'info': '#3498DB',          # Light blue
        'neutral': '#ECF0F1',       # Light gray
        'text_dark': '#2C3E50',     # Dark text
        'text_light': '#FFFFFF',    # Light text
        'background': '#F5F7FA',    # Background color
        'card': '#FFFFFF',          # Card background
    }
    
    # Status colors
    STATUS_COLORS = {
        'Normal': '#2ECC71',       # Green
        'Caution': '#3498DB',      # Blue
        'Warning': '#F39C12',      # Orange
        'Danger': '#E74C3C',       # Red
        'Unknown': '#95A5A6',      # Gray
    }
    
    @classmethod
    def setup_theme(cls, root):
        """Set up the application theme"""
        # Configure the base style
        style = ttk.Style()
        
        # Try to use a more modern theme as a base depending on platform
        if platform.system() == 'Windows':
            try:
                style.theme_use('vista')
            except:
                pass
        elif platform.system() == 'Darwin':  # macOS
            try:
                style.theme_use('aqua')
            except:
                pass
        else:  # Linux and others
            try:
                style.theme_use('clam')
            except:
                pass
        
        # Configure root window
        root.configure(bg=cls.COLORS['background'])
        
        # Configure ttk styles
        style.configure('TFrame', background=cls.COLORS['background'])
        style.configure('Card.TFrame', background=cls.COLORS['card'])
        
        style.configure('TLabel', background=cls.COLORS['background'], foreground=cls.COLORS['text_dark'])
        style.configure('Card.TLabel', background=cls.COLORS['card'])
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground=cls.COLORS['primary'])
        style.configure('SubHeader.TLabel', font=('Arial', 12, 'bold'), foreground=cls.COLORS['primary'])
        
        style.configure('TButton', background=cls.COLORS['secondary'], foreground=cls.COLORS['text_light'])
        style.map('TButton', 
                  background=[('active', cls.COLORS['info'])],
                  foreground=[('active', cls.COLORS['text_light'])])
        
        style.configure('Primary.TButton', background=cls.COLORS['primary'])
        style.map('Primary.TButton', 
                  background=[('active', '#1A252F')])  # Darker version of primary
                  
        style.configure('Success.TButton', background=cls.COLORS['accent'])
        style.map('Success.TButton', 
                  background=[('active', '#27AE60')])  # Darker version of accent
                  
        style.configure('Warning.TButton', background=cls.COLORS['warning'])
        style.map('Warning.TButton', 
                  background=[('active', '#D35400')])  # Darker version of warning
                 
        style.configure('Danger.TButton', background=cls.COLORS['danger'])
        style.map('Danger.TButton', 
                  background=[('active', '#C0392B')])  # Darker version of danger
        
        style.configure('TNotebook', background=cls.COLORS['background'])
        style.configure('TNotebook.Tab', background=cls.COLORS['neutral'], 
                       foreground=cls.COLORS['text_dark'], padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', cls.COLORS['card'])],
                 foreground=[('selected', cls.COLORS['secondary'])])
        
        style.configure('TLabelframe', background=cls.COLORS['card'])
        style.configure('TLabelframe.Label', background=cls.COLORS['card'], 
                       foreground=cls.COLORS['primary'], font=('Arial', 10, 'bold'))
                       
        style.configure('TCombobox', background=cls.COLORS['card'], fieldbackground=cls.COLORS['card'])
        
        # Configure status indicator styles
        for status, color in cls.STATUS_COLORS.items():
            style.configure(f'{status}.TLabel', foreground=color, font=('Arial', 10, 'bold'))
            style.configure(f'{status}.TFrame', background=color)
    
    @classmethod
    def create_tooltip(cls, widget, text):
        """Create a tooltip for a widget"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create a toplevel window
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(tooltip, text=text, justify='left',
                             background=cls.COLORS['primary'], foreground=cls.COLORS['text_light'],
                             relief='solid', borderwidth=1, padding=(5, 3))
            label.pack()
            
            widget.tooltip = tooltip
            
        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)




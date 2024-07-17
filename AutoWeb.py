import tkinter as tk
from tkinter import ttk, scrolledtext, font
import http.server
import socketserver
import webbrowser
import json
import threading


def generate_html(title, header, info, style, custom_sections, iconlink, bootstrap_entry, navbar_entry):
    sections_html = ""
    for section in custom_sections:
        sections_html += f"""
        <section id="{section['id']}">
            <h2>{section['title']}</h2>
            <p>{section['content']}</p>
        </section>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" href={iconlink}>
    {bootstrap_entry}
    <style>
        {style}
    </style>
</head>
<body>
    <header>
       {navbar_entry} 
    </header>
    
    <section id="home" class="hero">
        <h2>Welcome to {header}</h2>
        <p>{info}</p>
        <a href="#contact" class="cta-button">Get Started</a>
    </section>

    <main>
        <section id="about">
            <h2>About Us</h2>
            <p>We are a dedicated team committed to providing top-notch services in our field. Our expertise and passion drive us to deliver exceptional results for our clients.</p>
        </section>

        <section id="services">
            <h2>Our Services</h2>
            <div class="services-grid">
                <div class="service-card">
                    <h3>Service 1</h3>
                    <p>Description of Service 1</p>
                </div>
                <div class="service-card">
                    <h3>Service 2</h3>
                    <p>Description of Service 2</p>
                </div>
                <div class="service-card">
                    <h3>Service 3</h3>
                    <p>Description of Service 3</p>
                </div>
            </div>
        </section>

        <section id="contact">
            <h2>Contact Us</h2>
            <form>
                <input type="text" placeholder="Your Name" required>
                <input type="email" placeholder="Your Email" required>
                <textarea placeholder="Your Message" required></textarea>
                <button type="submit">Send Message</button>
            </form>
        </section>

        {sections_html}
    </main>

    <footer>
        <p>&copy; 2024 {header}. All rights reserved.</p>
    </footer>
</body>
</html>
"""


class WebsiteGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Custom Website Generator")
        master.geometry("900x700")
        master.configure(bg="#f0f0f0")

        self.custom_sections = []

        # Custom style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 12))
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'))
        self.style.configure('Custom.TButton', background="#4CAF50", foreground="white")
        self.style.map('Custom.TButton', background=[('active', '#45a049')])

        # Main frame
        main_frame = ttk.Frame(master, padding="20 20 20 20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="AutoWeb-The Free Website generator", font=('', 20, 'bold'), background="#f0f0f0")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input fields
        self.create_input_field(main_frame, "Website Title:", 1)
        self.create_input_field(main_frame, "Header Text:", 2)
        self.create_input_field(main_frame, "Website Info:", 3)
        self.create_input_field(main_frame, "Icon link:", 4)

        # Dropdown menus
        self.create_dropdown(main_frame, "Color:", ["Modern Blue", "Elegant Green", "Vibrant Orange"], 5)
        update = ttk.Label(main_frame, text="Styles will be added soon", font=('', 12, 'bold'), background="#f0f0f0")
        update.grid(row=9, column=0, columnspan=2, pady=(0, 20))
        self.create_dropdown(main_frame, "Font:", ["Arial", "Roboto", "Open Sans"], 7)
        self.create_dropdown(main_frame, "Layout:", ["Standard", "Centered", "Wide"], 8)
        self.create_dropdown(main_frame, "Add Bootstrap:", ["Yes", "No"], 10)
        self.create_dropdown(main_frame, "Add Navbar:", ["Yes", "No"], 11)
        
            

        # Buttons
        self.add_section_button = ttk.Button(main_frame, text="Add Custom Section", command=self.add_custom_section, style='Custom.TButton')
        self.add_section_button.grid(row=12, column=0, columnspan=2, pady=20)
        
        def open_browser():
            webbrowser.open('http://localhost:8000')
        
        
        self.generate_button = ttk.Button(main_frame, text="Generate Website", command=lambda: [self.generate_website(),open_browser()], style='Custom.TButton')
        self.generate_button.grid(row=13, column=0, columnspan=2, pady=(0, 20))
         
        

        # Result text area
        self.result_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=10, font=('Helvetica', 12))
        self.result_text.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

    def create_input_field(self, parent, label, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        setattr(self, f"{label.lower().replace(' ', '_').replace(':', '')}_entry", entry)

    def create_dropdown(self, parent, label, options, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        var = tk.StringVar()
        dropdown = ttk.Combobox(parent, textvariable=var, values=options, state="readonly", font=('Helvetica', 12))
        dropdown.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        dropdown.set(options[0])
        setattr(self, f"{label.lower().replace(':', '')}_var", var)
        setattr(self, f"{label.lower().replace(' ', '_').replace(':', '')}_dropdown", dropdown)

    def add_custom_section(self):
        section_window = tk.Toplevel(self.master)
        section_window.title("Add Custom Section")
        section_window.geometry("400x250")
        section_window.configure(bg="#f0f0f0")

        frame = ttk.Frame(section_window, padding="20 20 20 20", style='TFrame')
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Section ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        id_entry = ttk.Entry(frame)
        id_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(frame, text="Section Title:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        title_entry = ttk.Entry(frame)
        title_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(frame, text="Section Content:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        content_entry = ttk.Entry(frame)
        content_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        def save_section():
            self.custom_sections.append({
                'id': id_entry.get(),
                'title': title_entry.get(),
                'content': content_entry.get()
            })
            section_window.destroy()

        save_button = ttk.Button(frame, text="Save Section", command=save_section, style='Custom.TButton')
        save_button.grid(row=3, column=0, columnspan=2, pady=20)

    def generate_website(self):
        title = self.website_title_entry.get()
        header = self.header_text_entry.get()
        info = self.website_info_entry.get()
        iconlink = self.icon_link_entry.get()
        
        style_choice = self.color_dropdown.current() + 1
        font_choice = self.font_dropdown.current() + 1
        layout_choice = self.layout_dropdown.current() + 1
        bootstrap_choice = self.add_bootstrap_dropdown.current() + 1
        
        
            

        if bootstrap_choice == 1:
            bootstrap_entry = """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">"""
            navbar = self.add_navbar_dropdown.current()+ 1
            if navbar == 1:
                navbar_entry = """
                <nav class="navbar navbar-expand-lg bg-body-tertiary" style="margin-top: 0px">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">"""+ header +"""</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
             <a class="nav-link active" aria-current="page" href="#">Home</a>
               </li>
               <li class="nav-item">
                <a class="nav-link" href="#about">About</a>
               </li>
                <li class="nav-item">
                 <a class="nav-link" href="#services">Services</a>
                </li>
                <li class="nav-item">
                {"".join(f'<li><a href="#{section["id"]}">{section["title"]}</a></li>' for section in custom_sections)}
                 </li>
                 <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#ul" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  More
                </a>
                 <ul class="dropdown-menu" id="ul">
                 <li><a class="dropdown-item" href="#">Login</a></li>
                 <li><a class="dropdown-item" href="#">Sign Up</a></li>
                 <li><hr class="dropdown-divider"></li>
            
                </ul>
                
                <li class="nav-item">
                  <a class="nav-link disabled" aria-disabled="true">Disabled</a>
                 </li>
                
                  <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                  </form>
               </div>
              </div>
             </nav>
             <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>""" 
            else:
                navbar_entry="""<nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
                {"".join(f'<li><a href="#{section["id"]}">{section["title"]}</a></li>' for section in custom_sections)}
            </ul>
        </nav>
        <h1>"""+header+"""</h1>"""
 
        # Define color schemes
        # Define color schemes
        color_schemes = {
         1: {
        "primary": "#3498db",
        "secondary": "#2980b9",
        "accent": "#e74c3c",
        "text": "#333333",
        "bg": "#ecf0f1",
        "light": "#f9f9f9"
         },
         2: {
        "primary": "#27ae60",
        "secondary": "#2ecc71",
        "accent": "#f39c12",
        "text": "#333333",
        "bg": "#f1f8e9",
        "light": "#f9f9f9"
         },
         3: {
        "primary": "#e67e22",
        "secondary": "#d35400",
        "accent": "#3498db",
        "text": "#333333",
        "bg": "#fff5e6",
        "light": "#f9f9f9"
         }
        }

        colors = color_schemes[style_choice]

        fonts = {
          1: "'Helvetica Neue', Arial, sans-serif",
          2: "'Roboto', 'Open Sans', sans-serif",
          3: "'Lato', 'Montserrat', sans-serif"
        }
        font = fonts[font_choice]

        layouts = {
         1: "max-width: 1200px; margin: 0 auto; padding: 0 20px;",
         2: "max-width: 1000px; margin: 0 auto; padding: 0 20px; text-align: center;",
         3: "max-width: 100%; padding: 0 40px;"
        }
        layout = layouts[layout_choice]

        style = f"""
          @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Open+Sans:wght@300;400;700&family=Lato:wght@300;400;700&family=Montserrat:wght@300;400;700&display=swap');
           :root {{
             --primary-color: {colors['primary']};
             --secondary-color: {colors['secondary']};
             --accent-color: {colors['accent']};
             --text-color: {colors['text']};
             --bg-color: {colors['bg']};
             --light-color: {colors['light']};
        }}
     
         * {{
          margin: 0;
          padding: 0;
          box-sizing: border-box;
         }}
         body {{
          font-family: {font};
          line-height: 1.6;
          color: var(--text-color);
          background-color: var(--bg-color);
        }}
     .container {{
        {layout}
     }}
     header {{
        background-color: var(--primary-color);
        color: white;
        padding: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
     }}
     nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        float:right;
     }}
     nav ul {{
        list-style-type: none;
        display: flex;
     }}
     nav ul li {{
        margin-left: 20px;
     }}
     nav ul li a {{
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: opacity 0.3s ease;
     }}
     nav ul li a:hover {{
        opacity: 0.8;
     }}
     .hero {{
        background-color: var(--secondary-color);
        color: white;
        text-align: center;
        padding: 6rem 2rem;
        position: relative;
        overflow: hidden;
     }}
     .hero h1{{
         color:white;
     }}
     .hero::after:float {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        opacity: 0.8;
        z-index: 1;
     }}
     .hero-content {{
        position: relative;
        z-index: 2;
     }}
     .cta-button {{
        display: inline-block;
        background-color: var(--accent-color);
        color: white;
        padding: 12px 30px;
        text-decoration: none;
        border-radius: 30px;
        margin-top: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
     }}
    .cta-button:hover {{
        background-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }}
    main {{
        padding: 4rem 0;
    }}
    section {{
        margin-bottom: 4rem;
        background-color: var(--light-color);
        padding: 3rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    h2 {{
        color: var(--primary-color);
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
    }}
    .services-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
    }}
    .service-card {{
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    .service-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }}
    form {{
        display: grid;
        gap: 20px;
        max-width: 600px;
        margin: 0 auto;
    }}
    input, textarea {{
        width: 100%;
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
    }}
         button {{
         background-color: var(--primary-color);
         color: white;
         border: none;
         padding: 12px 30px;
         border-radius: 30px;
         cursor: pointer;
         font-size: 16px;
         font-weight: bold;
         transition: all 0.3s ease;
         text-transform: uppercase;
         letter-spacing: 1px;
         }}
         button:hover {{
           background-color: var(--secondary-color);
           transform: translateY(-2px);
           box-shadow: 0 4px 10px rgba(0,0,0,0.2);
         }}
         footer {{
          background-color: var(--primary-color);
          color: white;
          text-align: center;
          padding: 2rem 0;
          margin-top: 4rem;
         }}
        """

        html_content = generate_html(title, header, info, style, self.custom_sections, iconlink, bootstrap_entry, navbar_entry)
        with open("Code.txt","w+") as file:
            file.write(html_content)
        with open("index.html", "w+") as file:
            file.write(html_content)

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Website generated successfully!\n")
        self.result_text.insert(tk.END, "HTML file saved as 'index.html'.\n")
        self.result_text.insert(tk.END, "Opening in web browser....\n")
        

        # Start a simple HTTP server in a separate thread
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True
        server_thread.start()

        # Open the generated website in the default web browser
    

    def start_server(self):
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", 8000), handler) as httpd:
            print("Serving at port 8000")
            httpd.serve_forever()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteGenerator(root)
    root.mainloop()
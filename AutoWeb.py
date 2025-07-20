import customtkinter
import http.server
import socketserver
import webbrowser
import threading

# Set the appearance and default color theme for the app
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class Theme:
    MODERN = 'Modern'
    MINIMAL = 'Minimal'
    CREATIVE = 'Creative'

def generate_html(theme, title, header, info, sections, icon_url, include_login):
    # This function remains unchanged as it only generates HTML content
    nav_items = ['Home','About','Services','Contact'] + [sec['title'] for sec in sections]
    if include_login:
        nav_items.append('Login')
    nav_links = ''.join(f'<a href="#{item.lower()}">{item}</a>' for item in nav_items)

    default_sections = f"""
    <section id="about" class="editable-section">
      <h2>About Us <button class="edit-btn">Edit</button></h2>
      <p class="section-content">We deliver excellence.</p>
    </section>
    <section id="services" class="editable-section">
      <h2>Services <button class="edit-btn">Edit</button></h2>
      <p class="section-content">Our offered services.</p>
    </section>
    <section id="contact" class="editable-section">
      <h2>Contact <button class="edit-btn">Edit</button></h2>
      <p class="section-content">Reach us at contact@example.com.</p>
    </section>
    """
    custom_html = ''.join(f"""
    <section id="{sec['id']}" class="editable-section">
      <h2>{sec['title']} <button class="edit-btn">Edit</button></h2>
      <p class="section-content">{sec['content']}</p>
    </section>
    """ for sec in sections)

    login_overlay = """
    <div id=\"login-overlay\" style=\"display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:1000;\">
      <div style=\"position:relative;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;padding:2rem;border-radius:8px;width:300px;text-align:center;\">
        <h2>Login</h2>
        <input type=\"text\" placeholder=\"Username\" style=\"width:90%;padding:8px;margin:8px 0;\"><br>
        <input type=\"password\" placeholder=\"Password\" style=\"width:90%;padding:8px;margin:8px 0;\"><br>
        <button onclick=\"hideLogin()\" style=\"margin-top:1rem;padding:6px 12px;\">Close</button>
      </div>
    </div>
    """ if include_login else ""

    login_button = "<button onclick=\"showLogin()\" style=\"position:fixed;top:1rem;right:1rem;padding:8px 12px;z-index:999;background:#0ff;color:#111;border:none;border-radius:6px;cursor:pointer;\">Login</button>" if include_login else ""

    if theme == Theme.MODERN:
        css = """
        body{margin:0;font-family:sans-serif;background:#111;color:#eee;}
        nav{display:flex;gap:1rem;padding:1rem;background:#222;position:sticky;top:0;z-index:999;}
        nav a{color:#0ff;text-decoration:none;}
        .hero{height:60vh;display:flex;flex-direction:column;justify-content:center;align-items:center;
              background:linear-gradient(45deg,#00ffff,#1e1e2f);animation:fade 5s infinite alternate;}
        @keyframes fade{0%{opacity:1;}100%{opacity:0.7;}}
        main{padding:2rem;}
        section{margin-bottom:2rem;padding:1rem;background:#222;border-radius:8px;}
        footer{text-align:center;padding:1rem;background:#222;}
        .edit-btn{margin-left:10px;padding:4px 8px;background:#0ff;color:#111;border:none;cursor:pointer;border-radius:4px;}
        .edit-btn:disabled{opacity:0.5;cursor:default;}
        .edited{border:2px solid #0ff;}
        """
    elif theme == Theme.MINIMAL:
        css = """
        body{margin:0;font-family:system-ui;background:#121212;color:#e0e0e0;}
        nav{display:flex;gap:1rem;padding:1rem;background:#1f1f1f;position:sticky;top:0;z-index:999;}
        nav a{color:#e0e0e0;text-decoration:none;}
        .hero{padding:4rem;text-align:center;background:#181818;}
        main{padding:2rem;max-width:800px;margin:0 auto;}
        section{margin-bottom:2rem;padding:1rem;background:#1f1f1f;border-radius:4px;}
        footer{text-align:center;padding:1rem;background:#1f1f1f;color:#888;}
        .edit-btn{margin-left:10px;padding:4px 8px;background:#444;color:#e0e0e0;border:none;cursor:pointer;border-radius:4px;}
        .edit-btn:disabled{opacity:0.5;cursor:default;}
        .edited{border:2px dashed #888;}
        """
    else: # Creative Theme
        css = """
        body{margin:0;font-family:'Comic Sans MS',cursive;background:#f7f0f5;color:#2d1a3a;}
        nav{display:flex;gap:1rem;padding:1rem;background:#ffccee;border-bottom:3px solid #ff66cc;position:sticky;top:0;z-index:999;}
        nav a{color:#2d1a3a;text-decoration:none;font-size:1.1rem;}
        .hero{padding:5rem;text-align:center;background:url('https://picsum.photos/seed/pix/1200/400') center/cover;color:#fff;text-shadow:1px 1px 3px #000;}
        main{padding:2rem;}
        section{margin-bottom:2rem;border:2px dashed #ff66cc;padding:1rem;border-radius:8px;}
        footer{text-align:center;padding:1rem;background:#ffccee;}
        .edit-btn{margin-left:10px;padding:4px 8px;background:#ff66cc;color:#fff;border:none;cursor:pointer;border-radius:4px;}
        .edit-btn:disabled{opacity:0.5;cursor:default;}
        .edited{border:2px dashed #ff66cc;}
        """

    js = """
    document.querySelectorAll('.edit-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const p = btn.closest('h2').nextElementSibling;
        p.contentEditable = true;
        p.focus();
        btn.textContent = 'Save';
        btn.addEventListener('click', () => {
          p.contentEditable = false;
          btn.remove();
          btn.closest('.editable-section').classList.add('edited');
        }, { once: true });
      }, { once: true });
    });
    function showLogin(){document.getElementById('login-overlay').style.display='block';}
    function hideLogin(){document.getElementById('login-overlay').style.display='none';}
    """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title}</title>
      <link rel="icon" href="{icon_url}">
      <style>{css}</style>
    </head>
    <body>
      <nav>{nav_links}</nav>
      {login_button}
      <section class="hero"><h1>{header}</h1><p>{info}</p></section>
      <main>
        {default_sections}
        {custom_html}
      </main>
      <footer>&copy; {title} 2025</footer>
      {login_overlay}
      <script>{js}</script>
    </body>
    </html>
    """
    return html_template


class EnhancedWebsiteGenerator(customtkinter.CTk):
    _server_started = False

    def __init__(self):
        super().__init__()

        self.title("AutoWeb Pro")
        self.geometry("900x600")

        self.custom_sections = []
        self.website_theme = customtkinter.StringVar(value=Theme.MODERN)
        self.include_login = customtkinter.BooleanVar(value=False)
        
        self.setup_ui()

    def setup_ui(self):
        # The main container now inherits from the root window
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left-side navigation and configuration panel
        left_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        left_frame.grid_rowconfigure(4, weight=1)
        
        logo_label = customtkinter.CTkLabel(left_frame, text="AutoWeb Pro", font=customtkinter.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # --- Input Fields ---
        self.title_entry = customtkinter.CTkEntry(left_frame, placeholder_text="Website Title")
        self.title_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.header_entry = customtkinter.CTkEntry(left_frame, placeholder_text="Header Text")
        self.header_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.info_entry = customtkinter.CTkEntry(left_frame, placeholder_text="Info/Subtitle")
        self.info_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # --- Right-side content and actions panel ---
        right_frame = customtkinter.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        # Use CTkTabVIew for better organization
        tabview = customtkinter.CTkTabview(right_frame)
        tabview.pack(padx=20, pady=10, fill="both", expand=True)
        tabview.add("Log")
        tabview.add("Options")

        # --- Log tab ---
        self.log = customtkinter.CTkTextbox(tabview.tab("Log"), width=400, height=300)
        self.log.pack(padx=10, pady=10, fill="both", expand=True)
        self.log.tag_config('success', foreground='#4dff4d') # Bright Green
        self.log.tag_config('error', foreground='#ff4d4d') # Bright Red

        # --- Options tab ---
        options_frame = tabview.tab("Options")
        self.theme_menu = customtkinter.CTkOptionMenu(options_frame, variable=self.website_theme, values=[Theme.MODERN, Theme.MINIMAL, Theme.CREATIVE])
        self.theme_menu.pack(padx=20, pady=10)
        
        self.icon_entry = customtkinter.CTkEntry(options_frame, placeholder_text="Icon URL")
        self.icon_entry.pack(padx=20, pady=10, fill="x")

        self.login_toggle = customtkinter.CTkSwitch(options_frame, text="Include Login Page", variable=self.include_login)
        self.login_toggle.pack(padx=20, pady=10)
        
        # --- Buttons at the bottom ---
        button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.add_section_button = customtkinter.CTkButton(button_frame, text="Add Section", height=40, command=self.add_section, corner_radius=20, hover_color="#454545")
        self.add_section_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.generate_button = customtkinter.CTkButton(button_frame, text="Generate Website", height=40, command=self.generate_site, corner_radius=20)
        self.generate_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


    def add_section(self):
        # A new Toplevel window for adding a section
        win = customtkinter.CTkToplevel(self)
        win.title("Add New Section")
        win.geometry("400x250")

        id_entry = customtkinter.CTkEntry(win, placeholder_text="Section ID (e.g., 'portfolio')")
        id_entry.pack(padx=20, pady=10, fill="x")

        title_entry = customtkinter.CTkEntry(win, placeholder_text="Section Title (e.g., 'Our Portfolio')")
        title_entry.pack(padx=20, pady=10, fill="x")

        content_entry = customtkinter.CTkEntry(win, placeholder_text="Initial content for the section")
        content_entry.pack(padx=20, pady=10, fill="x")
        
        def save():
            sec = {'id': id_entry.get().strip(), 'title': title_entry.get().strip(), 'content': content_entry.get().strip()}
            if sec['id'] and sec['title']:
                self.custom_sections.append(sec)
                self.log.insert("end", f"Section '{sec['title']}' added.\n", 'success')
            else:
                self.log.insert("end", "Section ID and Title are required.\n", 'error')
            win.destroy()
            
        save_button = customtkinter.CTkButton(win, text="Save Section", command=save, corner_radius=20)
        save_button.pack(padx=20, pady=20)

    def generate_site(self):
        title = self.title_entry.get().strip()
        header = self.header_entry.get().strip()
        info = self.info_entry.get().strip()
        icon = self.icon_entry.get().strip()
        
        if not title or not header or not info:
            self.log.insert("end", "Error: Title, Header, and Info are required\n", 'error')
            return
            
        self.log.insert("end", "Generating website...\n")
        html = generate_html(self.website_theme.get(), title, header, info, self.custom_sections, icon, self.include_login.get())
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        self.log.insert("end", "index.html created successfully!\n", 'success')

        if not EnhancedWebsiteGenerator._server_started:
            EnhancedWebsiteGenerator._server_started = True
            threading.Thread(target=self.serve, daemon=True).start()
        else:
            self.log.insert("end", "Server is already running. Refresh your browser.\n")

    def serve(self):
        handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        try:
            with socketserver.TCPServer(("", 8000), handler) as httpd:
                self.log.insert("end", "Serving at http://localhost:8000\n", 'success')
                webbrowser.open("http://localhost:8000")
                httpd.serve_forever()
        except OSError as e:
            self.log.insert("end", f"Server error: {e}\n", 'error')


if __name__ == '__main__':
    app = EnhancedWebsiteGenerator()
    app.mainloop()
import tkinter as tk
from tkinter import ttk, scrolledtext
import http.server
import socketserver
import webbrowser
import threading

class Theme:
    MODERN = 'Modern'
    MINIMAL = 'Minimal'
    CREATIVE = 'Creative'

# Themes apply to generated website only

def generate_html(theme, title, header, info, sections, icon_url):
    # Navigation links
    nav_items = ['Home','About','Services','Contact'] + [sec['title'] for sec in sections]
    nav_links = ''.join(f'<a href="#{item.lower()}">{item}</a>' for item in nav_items)

    # Default & custom sections
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

    # CSS per theme
    if theme == Theme.MODERN:
        css = """
        body{margin:0;font-family:sans-serif;background:#111;color:#eee;}
        nav{display:flex;gap:1rem;padding:1rem;background:#222;position:sticky;top:0;}
        nav a{color:#0ff;text-decoration:none;font-weight:500;}
        .hero{height:60vh;display:flex;flex-direction:column;justify-content:center;align-items:center;
              background:linear-gradient(45deg,#00ffff,#1e1e2f);animation:fade 5s infinite alternate;color:#111;text-shadow:1px 1px 2px #000;}
        @keyframes fade{0%{opacity:1;}100%{opacity:0.7;}}
        main{padding:2rem;background:#111;}
        section{margin-bottom:2rem;padding:1.5rem;background:#222;border-radius:8px;transition:background 0.3s;}
        section:hover{background:#333;}
        footer{text-align:center;padding:1rem;background:#222;color:#ccc;}
        .edit-btn{margin-left:10px;padding:4px 8px;background:#0ff;color:#111;border:none;cursor:pointer;border-radius:4px;}
        .edit-btn:disabled{opacity:0.5;cursor:default;}
        .edited{border:2px solid #0ff;}
        a:hover{opacity:0.7;}
        """
    elif theme == Theme.MINIMAL:
        css = """
        body{margin:0;font-family:system-ui;background:#121212;color:#e0e0e0;}
        nav{display:flex;gap:1rem;padding:1rem;background:#1f1f1f;position:sticky;top:0;}
        nav a{color:#e0e0e0;text-decoration:none;font-weight:500;}
        .hero{padding:4rem;text-align:center;background:#181818;}
        main{padding:2rem;max-width:800px;margin:0 auto;background:#121212;}
        section{margin-bottom:2rem;padding:1.5rem;background:#1f1f1f;border-radius:4px;transition:border 0.3s;}
        section:hover{border:1px solid #444;}
        footer{text-align:center;padding:1rem;color:#888;background:#1f1f1f;}
        .edit-btn{margin-left:10px;padding:4px 8px;background:#444;color:#e0e0e0;border:none;cursor:pointer;border-radius:4px;}
        .edit-btn:disabled{opacity:0.5;cursor:default;}
        .edited{border:2px dashed #888;}
        a:hover{opacity:0.7;}
        """
    else:
        css = """
        body{margin:0;font-family:'Comic Sans MS',cursive;background:#f7f0f5;color:#2d1a3a;}
        nav{display:flex;gap:1rem;padding:1rem;background:#ffccee;border-bottom:3px solid #ff66cc;position:sticky;top:0;}
        nav a{color:#2d1a3a;text-decoration:none;font-size:1.1rem;}
        .hero{padding:5rem;text-align:center;background:url('https://picsum.photos/seed/pix/1200/400')center/cover;color:#fff;}
        main{padding:2rem;}
        section{margin-bottom:2rem;border:2px dashed #ff66cc;padding:1rem;border-radius:8px;}
        footer{text-align:center;padding:1rem;background:#ffccee;}
        .edit-btn{margin-left:10px;padding:4px 8px;background:#ff66cc;color:#fff;border:none;cursor:pointer;border-radius:4px;}
        .edit-btn:disabled{opacity:0.5;cursor:default;}
        .edited{border:2px dashed #ff66cc;}
        a:hover{opacity:0.7;}
        """

    # JavaScript for in-place editing
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
    """

    # Assemble HTML
    html = f"""
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
      <section class="hero">
        <h1>{header}</h1>
        <p>{info}</p>
      </section>
      <main>
        {default_sections}
        {custom_html}
      </main>
      <footer>&copy; {title} {2025}</footer>
      <script>{js}</script>
    </body>
    </html>
    """
    return html

class EnhancedWebsiteGenerator:
    _server_started = False

    def __init__(self, master):
        self.master = master
        master.title("AutoWeb Pro")
        master.geometry("900x600")
        self.custom_sections = []
        self.website_theme = tk.StringVar(value=Theme.MODERN)
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(fill='both', expand=True)

        # Theme selector
        ttk.Label(frame, text="Website Theme:").grid(row=0, column=0, sticky='w')
        ttk.OptionMenu(frame, self.website_theme, self.website_theme.get(), Theme.MODERN, Theme.MINIMAL, Theme.CREATIVE).grid(row=0, column=1, sticky='ew')

        # Inputs
        labels = ["Title","Header","Info","Icon URL"]
        self.entries = {}
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(frame, text=f"{lbl}:").grid(row=i, column=0, sticky='w', pady=5)
            ent = ttk.Entry(frame)
            ent.grid(row=i, column=1, sticky='ew', pady=5)
            self.entries[lbl.lower().replace(' ', '_')] = ent
        frame.columnconfigure(1, weight=1)

        # Buttons
        ttk.Button(frame, text="Add Section", command=self.add_section).grid(row=6, column=0, pady=10)
        ttk.Button(frame, text="Generate Site", command=self.generate_site).grid(row=6, column=1, pady=10)

        # Log area
        self.log = scrolledtext.ScrolledText(frame, height=8)
        self.log.grid(row=7, column=0, columnspan=2, sticky='nsew')

    def add_section(self):
        win = tk.Toplevel(self.master)
        win.title("Add Section")
        ttk.Label(win, text="ID:").grid(row=0, column=0)
        id_e = ttk.Entry(win); id_e.grid(row=0, column=1)
        ttk.Label(win, text="Title:").grid(row=1, column=0)
        t_e = ttk.Entry(win); t_e.grid(row=1, column=1)
        ttk.Label(win, text="Content:").grid(row=2, column=0)
        c_e = ttk.Entry(win); c_e.grid(row=2, column=1)
        def save():
            sec = {'id':id_e.get().strip(),'title':t_e.get().strip(),'content':c_e.get().strip()}
            if sec['id'] and sec['title']:
                self.custom_sections.append(sec)
            win.destroy()
        ttk.Button(win, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=10)

    def generate_site(self):
        title = self.entries['title'].get().strip()
        header = self.entries['header'].get().strip()
        info = self.entries['info'].get().strip()
        icon = self.entries['icon_url'].get().strip()
        if not title or not header or not info:
            self.log.insert(tk.END, "Error: Title, Header, and Info are required\n")
            return
        self.log.insert(tk.END, "Generating website...\n")
        html = generate_html(self.website_theme.get(), title, header, info, self.custom_sections, icon)
        with open("index.html","w",encoding="utf-8") as f:
            f.write(html)
        self.log.insert(tk.END, "index.html created\n")

        if not EnhancedWebsiteGenerator._server_started:
            EnhancedWebsiteGenerator._server_started = True
            threading.Thread(target=self.serve, daemon=True).start()
        else:
            self.log.insert(tk.END, "Server already running\n")

    def serve(self):
        handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        try:
            with socketserver.TCPServer(("",8000), handler) as httpd:
                self.log.insert(tk.END, "Serving at port 8000\n")
                webbrowser.open("http://localhost:8000")
                httpd.serve_forever()
        except OSError as e:
            self.log.insert(tk.END, f"Server error: {e}\n")

if __name__ == '__main__':
    root = tk.Tk()
    app = EnhancedWebsiteGenerator(root)
    root.mainloop()
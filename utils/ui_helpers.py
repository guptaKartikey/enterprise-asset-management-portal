import streamlit as st
import base64
import os

def inject_custom_css():
    """Injects common high-standard custom CSS for premium look and light/dark theme compatibility."""
    st.markdown(
        """
        <style>
        /* Import Outfit font for premium look */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Apply background gradient and font globally to Streamlit app */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Dark mode background gradient */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background: linear-gradient(135deg, #0b0f19 0%, #1e293b 100%) !important;
            }
        }

        /* Premium styled Sidebar background - deep corporate navy blue */
        [data-testid="stSidebar"] {
            background-color: #00233c !important; /* Deep corporate navy */
            border-right: 1px solid rgba(255,255,255,0.1) !important;
        }
        
        /* Make sidebar texts white for professional contrast (do not select * to avoid white text on white dropzone) */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] h6,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] strong,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] li a {
            color: #ffffff !important;
        }

        /* Make ALL text inside sidebar uploader white (drag drop instructions, uploaded file names) */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] * {
            color: #ffffff !important;
        }

        /* Style all file uploaders as premium blue cards */
        div[data-testid="stFileUploader"] {
            background-color: #f0f7ff !important;
            border: 2px dashed #0078b8 !important;
            border-radius: 12px !important;
            padding: 15px !important;
            box-shadow: 0 4px 10px rgba(0, 91, 142, 0.04) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #005b8e !important;
            background-color: #e6f2ff !important;
            box-shadow: 0 6px 15px rgba(0, 91, 142, 0.08) !important;
        }
        div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        @media (prefers-color-scheme: dark) {
            div[data-testid="stFileUploader"] {
                background-color: rgba(0, 91, 142, 0.15) !important;
                border: 2px dashed #38bdf8 !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
            }
            div[data-testid="stFileUploader"]:hover {
                background-color: rgba(0, 91, 142, 0.25) !important;
                border-color: #7dd3fc !important;
            }
        }

        /* Sidebar file uploader background adjustment override */
        [data-testid="stSidebar"] div[data-testid="stFileUploader"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px dashed rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            padding: 10px !important;
            box-shadow: none !important;
        }
        
        /* Customize file uploader buttons and browse buttons */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
            color: #00233c !important;
            background-color: #f1f5f9 !important;
            border: 1px solid #cbd5e1 !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button,
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button * {
            color: #00233c !important;
        }

        /* Sidebar page navigation links hover effect */
        [data-testid="stSidebarNav"] ul li a:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }

        /* Metric cards styling: high-standard card styling compatible with both light/dark mode */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 6px solid #005b8e; /* professional corporate blue */
            border-radius: 12px;
            padding: 16px 20px !important;
            margin: 10px 0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        /* Dark mode for Metric cards */
        @media (prefers-color-scheme: dark) {
            div[data-testid="stMetric"] {
                background-color: #1e293b !important;
                border: 1px solid #334155 !important;
                border-left: 6px solid #38bdf8 !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
            }
        }

        /* Metric hover state */
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            border-color: #0078b8;
        }

        /* Labels and Values contrast optimization */
        div[data-testid="stMetric"] label {
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            color: #475569 !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 1.9rem !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }
        @media (prefers-color-scheme: dark) {
            div[data-testid="stMetric"] label {
                color: #94a3b8 !important;
            }
            div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
                color: #f8fafc !important;
            }
        }

        /* Customize titles and headers (removed !important color overrides to allow banner local h1 styling) */
        h1, h2, h3 {
            font-weight: 700 !important;
            color: #0f172a;
        }
        h1 {
            color: #003366;
        }
        @media (prefers-color-scheme: dark) {
            h1, h2, h3 {
                color: #f8fafc;
            }
            h1 {
                color: #38bdf8;
            }
        }

        /* Modern tab selection styling */
        button[data-baseweb="tab"] {
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
        }

        /* Dataframe styling fixes */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            border: 1px solid rgba(128, 128, 128, 0.15);
        }
        
        /* Adjust spacing and padding of buttons */
        div.stButton > button:first-child {
            border-radius: 8px;
            font-weight: 600;
            padding: 8px 20px;
            transition: all 0.2s ease;
        }
        /* Fix visibility of uploaded file cards in the sidebar */
        [data-testid="stSidebar"] div[data-testid="stUploadedFile"] {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 6px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        [data-testid="stSidebar"] div[data-testid="stUploadedFile"] * {
            color: #ffffff !important;
        }

        /* Make inputs and selectboxes clearly visible against the gradient background */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] {
            background-color: #ffffff !important;
            border: 1px solid #94a3b8 !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="input"] > div *,
        div[data-baseweb="select"] > div * {
            color: #0f172a !important;
        }
        @media (prefers-color-scheme: dark) {
            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            div[data-baseweb="base-input"] {
                background-color: #1e293b !important;
                border: 1px solid #475569 !important;
            }
            div[data-baseweb="input"] > div *,
            div[data-baseweb="select"] > div * {
                color: #f8fafc !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def inject_top_right_logo():
    """Injects floating corporate bold blue text at top-right of main view."""
    st.markdown(
        """
        <div class="top-right-text">
            <strong>APEX ENTERPRISE PORTAL</strong>
        </div>
        <style>
        .top-right-text {
            position: fixed;
            top: 55px;
            right: 40px;
            z-index: 99999;
            font-size: 1.1rem;
            font-weight: 800;
            color: #005b8e !important;
            letter-spacing: 0.5px;
            pointer-events: none;
        }
        @media (max-width: 768px) {
            .top-right-text {
                display: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def get_hero_carousel_html():
    """Generates base64-encoded client-side slideshow HTML with smooth JS-driven crossfade transitions."""
    pic_dir = os.path.join(os.getcwd(), "datasets", "Hero_Section_Imgaes")
    if not os.path.exists(pic_dir):
        return "<!-- Hero images folder not found -->"
    
    # Get all jpeg/jpg/png files, excluding logo
    image_files = [
        f for f in os.listdir(pic_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg")) and "logo" not in f.lower()
    ]
    if not image_files:
        return "<!-- No carousel images found -->"
    
    # Sort files to maintain consistent order
    image_files.sort()
    
    # Convert each image to base64
    base64_images = []
    for img_name in image_files:
        path = os.path.join(pic_dir, img_name)
        try:
            with open(path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
                mime_type = "image/png" if img_name.lower().endswith(".png") else "image/jpeg"
                base64_images.append(f"data:{mime_type};base64,{b64_data}")
        except Exception:
            continue
            
    if not base64_images:
        return "<!-- Failed to encode images to base64 -->"
        
    num_images = len(base64_images)
    
    # Build slides HTML — first slide starts active
    slides_html = ""
    dots_html = ""
    for i, b64 in enumerate(base64_images):
        active_class = " active" if i == 0 else ""
        slides_html += f'<div class="slide{active_class}" style="background-image: url(\'{b64}\');"></div>\n'
        dots_html += f'<span class="dot{active_class}" onclick="currentSlide({i})"></span>\n'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    html, body {{
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        overflow: hidden;
        background-color: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .slideshow-container {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        background-color: #0b1329;
    }}
    .slide {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: 100% 100%;
        background-position: center center;
        background-repeat: no-repeat;
        opacity: 0;
        transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 14px;
    }}
    .slide.active {{
        opacity: 1;
    }}
    .dots-container {{
        position: absolute;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 8px;
        z-index: 10;
        background: rgba(0, 0, 0, 0.35);
        padding: 4px 12px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
    }}
    .dot {{
        height: 8px;
        width: 8px;
        background-color: rgba(255, 255, 255, 0.4);
        border-radius: 50%;
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    .dot.active {{
        background-color: #38bdf8;
        width: 24px;
        border-radius: 4px;
    }}
    </style>
    </head>
    <body>
    <div class="slideshow-container">
        {slides_html}
        <div class="dots-container">
            {dots_html}
        </div>
    </div>
    <script>
    var slides = document.querySelectorAll('.slide');
    var dots = document.querySelectorAll('.dot');
    var total = slides.length;
    var current = 0;
    var timer;

    function showSlide(index) {{
        if (total === 0) return;
        slides.forEach(function(s) {{ s.classList.remove('active'); }});
        dots.forEach(function(d) {{ d.classList.remove('active'); }});
        
        current = (index + total) % total;
        slides[current].classList.add('active');
        if (dots[current]) dots[current].classList.add('active');
    }}

    function nextSlide() {{
        showSlide(current + 1);
    }}

    function currentSlide(index) {{
        clearInterval(timer);
        showSlide(index);
        timer = setInterval(nextSlide, 3500);
    }}

    if (total > 1) {{
        timer = setInterval(nextSlide, 3500);
    }}
    </script>
    </body>
    </html>
    """
    return html_content


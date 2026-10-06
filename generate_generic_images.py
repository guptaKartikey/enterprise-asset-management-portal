import os
from PIL import Image, ImageDraw, ImageFont

img_dir = os.path.join(os.path.dirname(__file__), "datasets", "Hero_Section_Imgaes")
os.makedirs(img_dir, exist_ok=True)

def get_font(size, bold=False):
    font_names = ["segoeui.ttf", "arial.ttf", "calibri.ttf", "DejaVuSans.ttf"]
    if bold:
        font_names = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"] + font_names
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def create_logo():
    w, h = 400, 120
    img = Image.new("RGBA", (w, h), (0, 35, 60, 255))
    draw = ImageDraw.Draw(img)
    
    # Rounded badge icon
    draw.rounded_rectangle([15, 20, 95, 100], radius=16, fill=(0, 120, 184, 255), outline=(56, 189, 248, 255), width=2)
    f_icon = get_font(38, bold=True)
    draw.text((38, 30), "⚡", fill=(255, 255, 255, 255), font=f_icon)
    
    f_title = get_font(26, bold=True)
    f_sub = get_font(12, bold=False)
    
    draw.text((112, 32), "APEX ENTERPRISE", fill=(255, 255, 255, 255), font=f_title)
    draw.text((115, 68), "ASSET & SAP MANAGEMENT PORTAL", fill=(56, 189, 248, 255), font=f_sub)
    
    rgb_img = img.convert("RGB")
    rgb_img.save(os.path.join(img_dir, "logo.jpeg"), "JPEG", quality=95)
    img.save(os.path.join(img_dir, "logo.png"), "PNG")
    print("Logo created!")

def create_banner_1():
    w, h = 1000, 280
    img = Image.new("RGB", (w, h), (10, 25, 47))
    draw = ImageDraw.Draw(img)
    
    for x in range(0, w, 50):
        draw.line([(x, 0), (x + 80, h)], fill=(20, 45, 75), width=1)
    
    # Left Content - well within margins (max x = 600)
    draw.rounded_rectangle([40, 30, 240, 62], radius=16, fill=(0, 91, 142), outline=(56, 189, 248), width=1)
    f_badge = get_font(12, bold=True)
    draw.text((55, 38), "ENTERPRISE ASSET HUB", fill=(224, 242, 254), font=f_badge)
    
    f_head = get_font(28, bold=True)
    draw.text((40, 78), "Unified Hardware & Asset Intelligence", fill=(255, 255, 255), font=f_head)
    
    f_sub = get_font(14)
    draw.text((40, 125), "Real-time tracking of Laptops, Desktops, Servers, and IT Stock.", fill=(148, 163, 184), font=f_sub)
    draw.text((40, 150), "Complete visibility into hardware lifecycle and assignments.", fill=(148, 163, 184), font=f_sub)
    
    # Right Content Card - safely positioned (640 to 950)
    draw.rounded_rectangle([640, 30, 950, 240], radius=14, fill=(15, 37, 65), outline=(0, 120, 184), width=2)
    f_m_title = get_font(13, bold=True)
    f_m_val = get_font(26, bold=True)
    f_m_lbl = get_font(12)
    
    draw.text((665, 50), "SYSTEM METRICS", fill=(56, 189, 248), font=f_m_title)
    draw.text((665, 85), "100%", fill=(255, 255, 255), font=f_m_val)
    draw.text((665, 125), "Active Asset Visibility", fill=(148, 163, 184), font=f_m_lbl)
    
    draw.line([(665, 155), (925, 155)], fill=(30, 60, 95), width=1)
    draw.text((665, 175), "✔ Automated Reconciliation", fill=(34, 197, 94), font=f_m_lbl)
    draw.text((665, 200), "✔ IT Stock Pool Monitoring", fill=(34, 197, 94), font=f_m_lbl)
    
    img.save(os.path.join(img_dir, "img1.png"), "PNG")
    print("Banner 1 created!")

def create_banner_2():
    w, h = 1000, 280
    img = Image.new("RGB", (w, h), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    for y in range(0, h, 35):
        draw.line([(0, y), (w, y)], fill=(24, 38, 65), width=1)
    for x in range(0, w, 70):
        draw.line([(x, 0), (x, h)], fill=(24, 38, 65), width=1)
        
    draw.rounded_rectangle([40, 30, 270, 62], radius=16, fill=(2, 132, 199), outline=(125, 211, 252), width=1)
    f_badge = get_font(12, bold=True)
    draw.text((55, 38), "SAP SECURITY & COMPLIANCE", fill=(240, 249, 255), font=f_badge)
    
    f_head = get_font(28, bold=True)
    draw.text((40, 78), "Deep SAP SM20 Audit Analytics", fill=(255, 255, 255), font=f_head)
    
    f_sub = get_font(14)
    draw.text((40, 125), "Multi-month transaction auditing and Dialog user filtering.", fill=(148, 163, 184), font=f_sub)
    draw.text((40, 150), "Automated anomaly flagging with Department-wise drilldowns.", fill=(148, 163, 184), font=f_sub)
    
    draw.rounded_rectangle([640, 30, 950, 240], radius=14, fill=(20, 32, 55), outline=(2, 132, 199), width=2)
    f_m_title = get_font(13, bold=True)
    f_m_val = get_font(24, bold=True)
    f_m_lbl = get_font(12)
    
    draw.text((665, 50), "AUDIT ENGINE", fill=(56, 189, 248), font=f_m_title)
    draw.text((665, 85), "SM20 Logs", fill=(255, 255, 255), font=f_m_val)
    draw.text((665, 125), "Security Audit Verification", fill=(148, 163, 184), font=f_m_lbl)
    
    draw.line([(665, 155), (925, 155)], fill=(40, 55, 85), width=1)
    draw.text((665, 175), "✔ Dialog User Filtering", fill=(56, 189, 248), font=f_m_lbl)
    draw.text((665, 200), "✔ Manager Allocation Map", fill=(56, 189, 248), font=f_m_lbl)
    
    img.save(os.path.join(img_dir, "img2.jpeg"), "JPEG", quality=95)
    print("Banner 2 created!")

def create_banner_3():
    w, h = 1000, 280
    img = Image.new("RGB", (w, h), (8, 28, 48))
    draw = ImageDraw.Draw(img)
    
    for i in range(0, w, 40):
        draw.line([(i, 0), (i - 40, h)], fill=(16, 45, 75), width=1)
        
    draw.rounded_rectangle([40, 30, 280, 62], radius=16, fill=(13, 148, 136), outline=(94, 234, 212), width=1)
    f_badge = get_font(12, bold=True)
    draw.text((55, 38), "FUNCTIONAL GOVERNANCE", fill=(240, 253, 250), font=f_badge)
    
    f_head = get_font(28, bold=True)
    draw.text((40, 78), "Authorization & Role Matrix", fill=(255, 255, 255), font=f_head)
    
    f_sub = get_font(14)
    draw.text((40, 125), "Instantly discover assigned vs executed TCodes.", fill=(148, 163, 184), font=f_sub)
    draw.text((40, 150), "Covers IT, Finance, SCM, Operations, and HR roles.", fill=(148, 163, 184), font=f_sub)
    
    draw.rounded_rectangle([640, 30, 950, 240], radius=14, fill=(13, 40, 65), outline=(13, 148, 136), width=2)
    f_m_title = get_font(13, bold=True)
    f_m_val = get_font(24, bold=True)
    f_m_lbl = get_font(12)
    
    draw.text((665, 50), "ROLE MATRIX", fill=(94, 234, 212), font=f_m_title)
    draw.text((665, 85), "Multi-Tab View", fill=(255, 255, 255), font=f_m_val)
    draw.text((665, 125), "Granular Authorization View", fill=(148, 163, 184), font=f_m_lbl)
    
    draw.line([(665, 155), (925, 155)], fill=(20, 60, 90), width=1)
    draw.text((665, 175), "✔ Export Excel Reports", fill=(94, 234, 212), font=f_m_lbl)
    draw.text((665, 200), "✔ Cross-Department Audit", fill=(94, 234, 212), font=f_m_lbl)
    
    img.save(os.path.join(img_dir, "img3.jpeg"), "JPEG", quality=95)
    print("Banner 3 created!")

def create_banner_4():
    w, h = 1000, 280
    img = Image.new("RGB", (w, h), (24, 20, 45))
    draw = ImageDraw.Draw(img)
    
    for i in range(0, w, 50):
        draw.line([(i, 0), (i + 100, h)], fill=(40, 32, 70), width=1)
        
    draw.rounded_rectangle([40, 30, 280, 62], radius=16, fill=(124, 58, 237), outline=(196, 181, 253), width=1)
    f_badge = get_font(12, bold=True)
    draw.text((55, 38), "LOGIN VIOLATION SHIELD", fill=(245, 243, 255), font=f_badge)
    
    f_head = get_font(28, bold=True)
    draw.text((40, 78), "Terminal Anomaly Detection", fill=(255, 255, 255), font=f_head)
    
    f_sub = get_font(14)
    draw.text((40, 125), "Automated check between assigned assets and SAP logins.", fill=(196, 181, 253), font=f_sub)
    draw.text((40, 150), "Flags unauthorized workstation access and suspicious activity.", fill=(196, 181, 253), font=f_sub)
    
    draw.rounded_rectangle([640, 30, 950, 240], radius=14, fill=(35, 28, 65), outline=(124, 58, 237), width=2)
    f_m_title = get_font(13, bold=True)
    f_m_val = get_font(24, bold=True)
    f_m_lbl = get_font(12)
    
    draw.text((665, 50), "SECURITY AUDIT", fill=(196, 181, 253), font=f_m_title)
    draw.text((665, 85), "Zero-Trust Policy", fill=(255, 255, 255), font=f_m_val)
    draw.text((665, 125), "Device Identity Verification", fill=(216, 180, 254), font=f_m_lbl)
    
    draw.line([(665, 155), (925, 155)], fill=(60, 50, 95), width=1)
    draw.text((665, 175), "✔ Real-time Anomaly Flags", fill=(168, 85, 247), font=f_m_lbl)
    draw.text((665, 200), "✔ Cross-Terminal Warnings", fill=(168, 85, 247), font=f_m_lbl)
    
    img.save(os.path.join(img_dir, "img4.jpeg"), "JPEG", quality=95)
    print("Banner 4 created!")

if __name__ == "__main__":
    create_logo()
    create_banner_1()
    create_banner_2()
    create_banner_3()
    create_banner_4()
    print("All generic images regenerated with responsive margins!")

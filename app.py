from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Global variable to store resume data
resume_data = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate", methods=["POST"])
def generate():
    global resume_data

    resume_data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "github": request.form["github"],
        "role": request.form["role"],
        "objective": request.form["objective"],   # CAREER OBJECTIVE
        "skills": request.form["skills"].split(","),  # comma separated
        "projects": request.form["projects"],       # PROJECTS
        "education": request.form["education"]
    }

    return render_template("resume.html", data=resume_data)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", data=resume_data)

@app.route("/download")
def download():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ===== NAME =====
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 80, resume_data["name"])

    # ===== CONTACT =====
    c.setFont("Helvetica", 10)
    c.drawCentredString(
        width / 2,
        height - 110,
        f'{resume_data["email"]} | GitHub: {resume_data["github"]}'
    )

    # Divider line
    c.line(50, height - 130, width - 50, height - 130)

    y = height - 170

    # ===== CAREER OBJECTIVE =====
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "CAREER OBJECTIVE")
    y -= 20

    c.setFont("Helvetica", 11)
    for line in resume_data["objective"].split("."):
        if line.strip():
            c.drawString(50, y, line.strip())
            y -= 15

    # ===== SKILLS =====
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "SKILLS")
    y -= 20

    c.setFont("Helvetica", 11)
    for skill in resume_data["skills"]:
        c.drawString(60, y, f"• {skill.strip()}")
        y -= 15

    # ===== PROJECTS =====
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "PROJECTS")
    y -= 20

    c.setFont("Helvetica", 11)
    for line in resume_data["projects"].split("."):
        if line.strip():
            c.drawString(60, y, line.strip())
            y -= 15

    # ===== EDUCATION =====
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "EDUCATION")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(60, y, resume_data["education"])

    # ===== TARGET ROLE =====
    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "TARGET ROLE")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(60, y, resume_data["role"])

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Professional_Resume.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
                                                                                                     



import os
import re
import requests
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def continue_story(role, genre, history, user_input):
    messages = history + [
        {"role": "user", "content": f"My role: {role}, Genre: {genre}. My action: {user_input}"}
    ]
    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.8
        }
    )
    res_json = response.json()
    if "choices" in res_json:
        return res_json["choices"][0]["message"]["content"]
    else:
        print("🛑 LLM API Error:", res_json)
        return "An error occurred while generating the story. Please try again."

def update_inventory(text, inventory):
    pattern = r"(You (find|picked up|take|grab).*?[\.\!])"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    for match in matches:
        item = match[0].strip()
        if item not in inventory:
            inventory.append(item)
    return inventory

from textwrap import wrap

def export_story_to_pdf(story, filename="story.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 1 * inch
    line_height = 16  # زيادة المسافة بين السطور

    # استخراج عنوان القصة
    lines = story.strip().split("\n")
    title_line = "My Interactive Story"
    for line in lines:
        if line.strip().lower().startswith("title:"):
            title_line = line.strip()[7:].strip()
            break

    # 🟡 عنوان القصة
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - margin, f"📖 {title_line}")
    c.setFillColor(colors.black)

    y = height - margin - 30  # بداية النص بعد العنوان

    c.setFont("Times-Roman", 12)
    for line in lines:
        wrapped_lines = wrap(line, width=90)  # تقطيع السطر الطويل
        for wrap_line in wrapped_lines:
            if y <= margin:
                c.showPage()
                y = height - margin
                c.setFont("Times-Roman", 12)
            c.drawString(margin, y, wrap_line)
            y -= line_height
        y -= 5  # مسافة إضافية بين الفقرات

    # 🟢 The End
    if y <= margin + 2 * line_height:
        c.showPage()
        y = height - margin
    c.setFont("Times-Italic", 12)
    c.setFillColor(colors.gray)
    c.drawString(margin, y - 20, "■■■■ The End")

    c.save()

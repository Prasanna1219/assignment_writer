import os
import requests
import json
import re
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_draw_color(111, 111, 111)
        self.set_line_width(0.3)
        self.line(15, 0, 15, self.h)

    def footer(self):
        pass

def fetch_assignment_json(assignment_topic: str):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_API_CODE")
    URL = "https://api.groq.com/openai/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Give content for my assignment topic “{assignment_topic}”—each answer should be have more than 40 words."
        f"Return the output in this exact JSON format:\n\n"
        "{\n"
        '  "question_no": number,\n'
        '  "question": "actual question",\n'
        '  "answer_heading": "heading_name",\n'
        '  "answer": "actual answer"\n'
        "}\n\n"
        "Do not include any extra text—emit a JSON array of such objects."
    )

    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False
    }

    response = requests.post(URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    # Sometimes the API might return extra text, so extract JSON array only
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("[")
        end = content.rfind("]") + 1
        data = json.loads(content[start:end])

    return data

def write_qa(pdf, data):
    pdf.set_auto_page_break(auto=False, margin=15)
    pdf.page_break_trigger = 250
    pdf.add_page()

    pdf.add_font('Handwriting', '', 'LiuJianMaoCao-Regular.ttf', uni=True)
    pdf.set_left_margin(20)
    pdf.set_x(20)

    for item in data:
        if pdf.get_y() + 30 > pdf.page_break_trigger:
            pdf.add_page()

        # Question and question number in black
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Handwriting', '', 12)
        pdf.multi_cell(0, 10, f"Q{item['question_no']}. {item['question']}")

        # Answer heading in black
        pdf.set_font('Handwriting', '', 12)
        pdf.multi_cell(0, 10, item['answer_heading'])

        if pdf.get_y() + 10 > pdf.page_break_trigger:
            pdf.add_page()

        # Answer text in blue
        pdf.set_font('Handwriting', '', 12)
        pdf.set_text_color(0, 15, 185)  # Blue
        pdf.multi_cell(0, 10, item['answer'])

        pdf.ln(5)

if __name__ == "__main__":
    topic = input("Enter assignment topic: ").strip()
    try:
        qa_data = fetch_assignment_json(topic)
        pdf = PDF()
        write_qa(pdf, qa_data)
        pdf.output("assignment.pdf")
        print("✅ PDF created: 'assignment.pdf'")
    except Exception as e:
        print("Error:", e)


import os
from fpdf import FPDF
import math

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'TechNova Solutions Pvt. Ltd.', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, 'Bengaluru, Karnataka, India | 650 Employees | Hybrid Work Model', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

docs = {
    "Employee_Handbook": {
        "pages": 25,
        "sections": ["Welcome", "About TechNova", "Vision", "Mission", "Core Values", "Organization Structure", "Office Hours", "Attendance", "Dress Code", "Leave Overview", "Employee Benefits", "Code of Conduct", "Performance Management", "Learning & Development", "IT Usage Policy", "Data Privacy", "Workplace Safety", "Anti-Harassment Policy", "Exit Process", "Contact Directory"],
        "specifics": {
            "Office Hours": "Our standard office hours are 9:00 AM to 6:00 PM IST. TechNova operates on a Hybrid work model (3 days office, 2 days remote) for full-time employees. Interns are not eligible for remote work and must work from the Bengaluru office.",
            "Exit Process": "To resign, submit a formal email to your manager and hr@technova.com with a 30-day notice period. Probation ends after exactly 6 months from the date of joining, pending a successful performance review."
        }
    },
    "Leave_Policy": {
        "pages": 12,
        "sections": ["Purpose", "Eligibility", "Casual Leave", "Sick Leave", "Earned Leave", "Maternity Leave", "Paternity Leave", "Bereavement Leave", "Leave Approval Process", "Leave Cancellation", "Leave Encashment", "FAQ"],
        "specifics": {
            "Casual Leave": "Employees are allowed 12 casual leaves per year.",
            "Maternity Leave": "Maternity leave must be approved by the HR Head and the respective Department Head.",
            "Earned Leave": "Yes, up to 10 days of earned leave can be carried forward to the next calendar year."
        }
    },
    "IT_Security": {
        "pages": 18,
        "sections": ["Password Policy", "Laptop Usage", "VPN", "Email Security", "Data Encryption", "USB Restrictions", "Cloud Storage", "Phishing", "Incident Reporting", "Access Control"],
        "specifics": {
            "Password Policy": "Passwords must be at least 14 characters long, contain numbers, symbols, and be changed every 90 days.",
            "Laptop Usage": "No, Bring Your Own Device (BYOD) is strictly prohibited. You must use the company-issued laptop."
        }
    },
    "HR_Policy": {
        "pages": 15,
        "sections": ["Recruitment", "Background Verification", "Probation", "Confirmation", "Promotion", "Transfer", "Termination", "Resignation", "Notice Period", "Employee Records"],
        "specifics": {
            "Resignation": "To resign, submit a formal email to your manager and hr@technova.com with a 30-day notice period.",
            "Probation": "Probation ends after exactly 6 months from the date of joining, pending a successful performance review."
        }
    },
    "Travel_Policy": {
        "pages": 12,
        "sections": ["Domestic Travel", "International Travel", "Accommodation", "Per Diem", "Expense Claims", "Approvals", "Travel Portal", "Advances", "Cancellations", "FAQ"],
        "specifics": {
            "Expense Claims": "Submit all travel expense receipts through the Concur portal within 15 days of return.",
            "Approvals": "All international travel must be approved by the VP of Finance and the CEO."
        }
    }
}

os.makedirs("data/raw_documents", exist_ok=True)
generic_filler = "This section outlines the standard operating procedures and regulatory guidelines mandated by TechNova Solutions Pvt. Ltd. " * 30

for name, data in docs.items():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    sections = data["sections"]
    target_pages = data["pages"]
    specifics = data.get("specifics", {})
    
    # Calculate how many pages each section should roughly span
    pages_per_section = math.ceil(target_pages / len(sections))
    
    for section in sections:
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, section, 0, 1)
        pdf.ln(5)
        
        pdf.set_font("Helvetica", '', 12)
        content = specifics.get(section, generic_filler)
        
        # Add filler to stretch the content to fill pages if needed
        # Since we want exact page counts, we just add pages
        pdf.multi_cell(0, 10, text=content)
        
        # If we need to pad the section to reach the target page count
        for _ in range(pages_per_section - 1):
            pdf.add_page()
            pdf.set_font("Helvetica", 'I', 10)
            pdf.multi_cell(0, 10, text=generic_filler)

    # Ensure exact page count
    while pdf.page_no() < target_pages:
        pdf.add_page()
        pdf.set_font("Helvetica", 'I', 10)
        pdf.multi_cell(0, 10, text="Additional notes and amendments for this policy.")
        
    pdf.output(f"data/raw_documents/{name}.pdf")
    print(f"Created {name}.pdf with {pdf.page_no()} pages.")


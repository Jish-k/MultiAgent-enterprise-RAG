import os
from fpdf import FPDF

class LeavePolicyPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'TechNova Solutions Pvt. Ltd. - Leave Policy', 0, 1, 'R')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

content = {
    "1. Purpose & Eligibility": "The purpose of this Leave Policy is to outline the various types of leave available to employees of TechNova Solutions Pvt. Ltd., the eligibility criteria for each, and the procedure for requesting and approving leave.\n\nAll full-time and part-time employees are eligible for leave benefits as described in this policy. Contract employees and interns may have different leave structures, as specified in their respective contracts.",
    
    "2. Casual Leave": "Employees are allowed 12 casual leaves per year. Casual leave is intended to accommodate unforeseen circumstances, personal emergencies, or brief personal matters that require an employee's attention during standard working hours.\n\nCasual leave is credited at the beginning of each calendar year. For employees joining mid-year, casual leave is pro-rated based on the date of joining. Casual leave cannot be carried forward to the next calendar year and cannot be encashed.",
    
    "3. Sick Leave": "TechNova recognizes that employees may occasionally fall ill and require time off to recover. Employees are granted 10 days of paid sick leave per calendar year.\n\nSick leave can be taken for personal illness, medical appointments, or to care for an immediate family member who is unwell. A valid medical certificate from a registered medical practitioner is required for sick leave extending beyond 3 consecutive working days. Sick leave cannot be encashed but can be carried forward up to a maximum of 20 days.",
    
    "4. Earned Leave": "Earned Leave (EL), also known as Paid Time Off (PTO), is provided for employees to rest, recuperate, and take extended vacations. Employees accrue Earned Leave at a rate of 1.66 days per month, totaling 20 days per calendar year.\n\nEmployees are encouraged to utilize their Earned Leave for maintaining a healthy work-life balance. Yes, up to 10 days of earned leave can be carried forward to the next calendar year. Earned leave can be encashed at the time of separation from the company, subject to a maximum cap of 30 days.",
    
    "5. Maternity Leave": "TechNova is committed to supporting its employees during significant life events. Female employees are entitled to 26 weeks of paid Maternity Leave, in accordance with the Maternity Benefit Act.\n\nMaternity leave must be approved by the HR Head and the respective Department Head. The leave can be availed starting up to 8 weeks before the expected date of delivery. Employees returning from maternity leave may also request flexible working arrangements or extended remote work, subject to managerial approval.",
    
    "6. Paternity Leave": "To support new fathers, TechNova offers 4 weeks of paid Paternity Leave. This leave is available to all male employees upon the birth or adoption of a child.\n\nPaternity leave must be utilized within the first 6 months of the child's birth or placement for adoption. It can be taken in a single block or divided into two blocks of 2 weeks each, subject to approval from the reporting manager.",
    
    "7. Leave Approval Process": "All leave requests must be submitted through the centralized HR Leave Portal. For planned leaves (such as Earned Leave), requests must be submitted at least two weeks in advance to allow for adequate resource planning and handover.\n\nFor unplanned leaves (such as Sick Leave or emergency Casual Leave), employees must notify their immediate supervisor via email or Slack as soon as possible, and formally apply for the leave in the portal within 24 hours of returning to work. Approval is at the discretion of the reporting manager.",
    
    "8. FAQ": "Q: Can interns work remotely?\nA: Interns are not eligible for remote work and must work from the Bengaluru office.\n\nQ: How many casual leaves are allowed?\nA: Employees are allowed 12 casual leaves per year.\n\nQ: Can I carry forward earned leave?\nA: Yes, up to 10 days of earned leave can be carried forward to the next calendar year.\n\nQ: Who approves maternity leave?\nA: Maternity leave must be approved by the HR Head and the respective Department Head."
}

def generate_leave_policy():
    pdf = LeavePolicyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 28)
    pdf.ln(80)
    pdf.cell(0, 15, 'Leave Policy', 0, 1, 'C')
    pdf.set_font("Helvetica", '', 18)
    pdf.cell(0, 15, 'TechNova Solutions Pvt. Ltd.', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 14)
    pdf.cell(0, 10, 'Bengaluru, Karnataka, India', 0, 1, 'C')
    pdf.cell(0, 10, 'Effective Date: January 1, 2026', 0, 1, 'C')
    
    # Table of Contents
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, "Table of Contents", 0, 1)
    pdf.ln(10)
    pdf.set_font("Helvetica", '', 14)
    for section in content.keys():
        pdf.cell(0, 12, f"{section}", 0, 1)
        
    # Content Pages (One chapter per page)
    for section, text in content.items():
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 18)
        pdf.cell(0, 15, section, 0, 1)
        pdf.ln(10)
        
        pdf.set_font("Helvetica", '', 14)
        for paragraph in text.split('\n'):
            if paragraph.strip():
                pdf.multi_cell(0, 10, txt=paragraph)
                pdf.ln(8)
                
    pdf.output("data/raw_documents/Leave_Policy.pdf")
    print(f"Generated Leave Policy: {pdf.page_no()} pages.")

if __name__ == "__main__":
    generate_leave_policy()

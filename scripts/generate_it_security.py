import os
from fpdf import FPDF

class ITSecurityPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'TechNova Solutions Pvt. Ltd. - IT Security Policy', 0, 1, 'R')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

content = {
    "1. Password Policy": "The foundation of our enterprise security begins with robust password management. Passwords must be at least 14 characters long, contain numbers, symbols, and be changed every 90 days. Under no circumstances should an employee share their password with colleagues, contractors, or IT support staff.\n\nMulti-Factor Authentication (MFA) is strictly mandatory for accessing all TechNova internal systems, including the HR portal, email servers, and GitHub repositories. Employees are strongly encouraged to use the company-approved password manager to generate and securely store their credentials.",
    
    "2. Email Usage": "TechNova's email system is a critical business tool and must be used responsibly. Employees are prohibited from using corporate email accounts for personal commercial activities, political campaigning, or transmitting inappropriate content.\n\nCaution must be exercised when opening attachments or clicking on links from unknown senders to prevent phishing attacks. All outbound emails containing sensitive client information or proprietary source code must be encrypted using the internal secure mailing gateway.",
    
    "3. VPN Access": "Accessing the TechNova corporate network from external locations requires a secure connection. The Enterprise Virtual Private Network (VPN) must be used at all times when working remotely or connecting from public Wi-Fi networks.\n\nEmployees experiencing connectivity issues should first ensure their internet connection is stable and their MFA token is synchronized before contacting the IT Helpdesk. Splitting the tunnel (accessing the local network while connected to the VPN) is disabled by default to prevent data leakage.",
    
    "4. Device Usage": "The physical security of computing devices is paramount. No, Bring Your Own Device (BYOD) is strictly prohibited. You must use the company-issued laptop for all business activities. \n\nLaptops must be locked when unattended, even within the Bengaluru headquarters. Employees must not install unauthorized software or disable the endpoint detection and response (EDR) agent installed on their machines. Portable storage devices, such as USB drives, are blocked by default unless an explicit exception is granted by the CISO.",
    
    "5. Data Security": "TechNova handles highly sensitive intellectual property and client data. All data at rest on company-issued laptops is fully encrypted using standard disk encryption technologies (BitLocker for Windows, FileVault for macOS).\n\nEmployees are strictly forbidden from uploading corporate data to unauthorized public cloud storage services (e.g., personal Google Drive, Dropbox) or generative AI tools that do not have an enterprise agreement with TechNova. Data classification labels (Public, Internal, Confidential, Restricted) must be applied to all documents.",
    
    "6. Incident Reporting": "Rapid response is essential to mitigating the impact of a security breach. Any suspected security incident, including lost or stolen laptops, suspicious emails, or unauthorized access attempts, must be reported immediately.\n\nEmployees must report incidents to the IT Security Desk by calling ext. 5555 or emailing security-alert@technova.com. Do not attempt to investigate or remediate a suspected cyber attack on your own, as this may destroy critical forensic evidence.",
    
    "7. FAQ": "Q: What is the password policy?\nA: Passwords must be at least 14 characters long, contain numbers, symbols, and be changed every 90 days.\n\nQ: Can I use my own laptop?\nA: No, Bring Your Own Device (BYOD) is strictly prohibited. You must use the company-issued laptop."
}

def generate_it_security():
    pdf = ITSecurityPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 28)
    pdf.ln(80)
    pdf.cell(0, 15, 'IT Security Policy', 0, 1, 'C')
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
    pdf.cell(0, 12, "Appendix A: Allowed Software", 0, 1)
        
    # Content Pages (One chapter per page)
    for section, text in content.items():
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 18)
        pdf.cell(0, 15, section, 0, 1)
        pdf.ln(10)
        
        pdf.set_font("Helvetica", '', 14)
        for paragraph in text.split('\n'):
            if paragraph.strip():
                # Large line height for readability and length
                pdf.multi_cell(0, 10, text=paragraph)
                pdf.ln(8)
                
    # Add a few blank pages for "Appendices" to hit the 10-15 page target
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "Appendix A: Allowed Software", 0, 1)
    pdf.ln(10)
    pdf.set_font("Helvetica", '', 14)
    pdf.multi_cell(0, 10, text="This appendix contains the approved list of software that can be requested via the IT Service Portal. Any software not listed here requires explicit CISO approval.")
    
    pdf.output("data/raw_documents/IT_Security.pdf")
    print(f"Generated IT Security Policy: {pdf.page_no()} pages.")

if __name__ == "__main__":
    generate_it_security()

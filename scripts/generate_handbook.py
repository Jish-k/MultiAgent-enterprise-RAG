import os
from fpdf import FPDF

class HandbookPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'TechNova Solutions Pvt. Ltd. - Employee Handbook', 0, 1, 'R')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

content = {
    "Welcome": "Welcome to TechNova Solutions Pvt. Ltd.! We are incredibly excited to have you join our dynamic and innovative team in Bengaluru. TechNova was founded on the belief that technology can transform businesses, and it is our people who drive that transformation. As you embark on your journey with us, this Employee Handbook will serve as your comprehensive guide to our company culture, policies, and the resources available to support your success.\n\nWe encourage you to read this handbook thoroughly. It is designed to provide you with a clear understanding of what you can expect from TechNova, and what we expect from you in return. Your unique skills and perspectives are highly valued here, and we are committed to fostering an environment where you can grow professionally and personally. Welcome to the TechNova family!",
    
    "About Company": "TechNova Solutions Pvt. Ltd. is a premier software development and AI solutions provider headquartered in the vibrant tech hub of Bengaluru, Karnataka, India. With a robust workforce of 650 dedicated professionals, we specialize in delivering cutting-edge, AI-driven applications and enterprise-grade software to clients across the globe.\n\nSince our inception, we have consistently pushed the boundaries of innovation, partnering with industry leaders to solve complex technological challenges. Our diverse teams across Engineering, Sales, Finance, and IT Security work collaboratively to ensure the highest standards of delivery and customer satisfaction.",
    
    "Vision": "Our vision at TechNova Solutions is to be the global vanguard of Artificial Intelligence and Enterprise Software innovation. We aspire to create a future where intelligent technology seamlessly integrates with human potential, driving unprecedented efficiency, sustainability, and growth for businesses worldwide.\n\nWe envision a workplace where creativity is unbound, and where every TechNova employee is empowered to architect the solutions of tomorrow.",
    
    "Mission": "TechNova's mission is to democratize advanced technology. We are dedicated to designing, developing, and deploying scalable, secure, and intuitive AI solutions that solve real-world problems. We strive to maintain operational excellence, foster a culture of continuous learning, and deliver measurable value to our stakeholders while upholding the highest standards of integrity and social responsibility.",
    
    "Values": "At TechNova, our Core Values are the bedrock of our corporate identity. They are:\n\n1. Innovation: We challenge the status quo and embrace creative problem-solving.\n2. Integrity: We conduct our business with the utmost honesty and transparency.\n3. Collaboration: We believe that the best ideas are born from diverse, cross-functional teamwork.\n4. Customer-Centricity: The success of our clients is the ultimate measure of our success.\n5. Empathy: We respect and support each other, cultivating a safe and inclusive workplace.",
    
    "Organization Structure": "TechNova operates on a matrix organizational structure to promote agility and cross-departmental collaboration. Our Executive Leadership Team, led by the CEO, oversees the strategic direction of the company. Reporting directly to the executive board are the Vice Presidents of our core divisions: Engineering, Human Resources, Finance, Sales & Marketing, IT Security, Administration, and Customer Support.\n\nEmployees are encouraged to engage with leadership through open-door policies and regular town-hall meetings, ensuring transparency across all levels of the organization.",
    
    "Departments": "Our 650 employees are distributed across several highly specialized departments:\n\n- Engineering: The core of TechNova, responsible for product development and AI research.\n- Human Resources: Dedicated to talent acquisition, employee well-being, and organizational development.\n- IT Security: Ensures the integrity of our digital infrastructure and protects enterprise data.\n- Sales & Marketing: Drives market expansion, brand presence, and client acquisition.\n- Customer Support: Provides 24/7 assistance to our global client base.\n- Finance & Admin: Manages the financial health and physical operations of the Bengaluru headquarters.",
    
    "Working Hours": "TechNova operates on a Hybrid work model to offer flexibility while maintaining team cohesion. Full-time employees are expected to work 3 days from the Bengaluru office and may work 2 days remotely per week.\n\nOur standard working hours are 9:00 AM to 6:00 PM IST, Monday through Friday, inclusive of a one-hour lunch break. Core collaboration hours are between 10:30 AM and 4:00 PM; during this time, all employees, regardless of location, must be available for meetings and synchronized work. Interns are required to work from the office 5 days a week.",
    
    "Attendance": "Punctuality and consistent attendance are critical to our operational success. Employees must log their daily attendance through the HR portal by 9:30 AM. If you are unable to report to work due to unforeseen circumstances, you must notify your immediate supervisor and the HR department as soon as possible, preferably before the start of the workday.\n\nRepeated unauthorized absences or unpunctuality may result in disciplinary action. The hybrid model is a privilege that requires trust and accountability in managing one's own schedule effectively.",
    
    "Leaves": "TechNova recognizes the importance of work-life balance and offers a comprehensive leave policy. Employees are entitled to 20 days of Earned Leave (PTO), 12 days of Casual Leave, and 10 days of Sick Leave per calendar year. Yes, up to 10 days of earned leave can be carried forward to the next calendar year.\n\nMaternity leave is provided for 26 weeks, and Paternity leave for 4 weeks. Maternity leave must be approved by the HR Head and the respective Department Head. Bereavement leave of up to 5 days is available. All leave requests must be submitted through the internal portal at least two weeks in advance, except in emergencies.",
    
    "Benefits": "In addition to competitive compensation, TechNova offers a robust benefits package. This includes comprehensive health insurance covering the employee, spouse, and up to two children. We provide a provident fund (PF) matching program, annual health check-ups, and a monthly internet allowance for remote work days.\n\nThe Bengaluru office features a fully subsidized cafeteria, a wellness room, and an on-site gymnasium. Employees also have access to our Employee Assistance Program (EAP) for mental health and legal counseling services.",
    
    "Code of Conduct": "The TechNova Code of Conduct mandates that all employees behave in a professional, respectful, and ethical manner at all times. We have a zero-tolerance policy for workplace harassment, discrimination, and bullying. \n\nEmployees must avoid any conflicts of interest and act in the best interests of the company. Any violation of this code, whether in the office, during remote work, or at company-sponsored events, will be met with strict disciplinary action, up to and including termination of employment.",
    
    "Dress Code": "TechNova promotes a 'Smart Casual' dress code. We trust our employees to use their best judgment in selecting attire that is professional, comfortable, and appropriate for the workplace. \n\nWhen meeting with clients or attending formal corporate events, 'Business Professional' attire is required. Offensive graphics, overly revealing clothing, and beachwear are not permitted in the office. For remote video calls, employees must ensure they are professionally presented from the waist up.",
    
    "IT Usage": "Company-provided IT resources, including laptops, software, and networks, are to be used strictly for business purposes. TechNova monitors network traffic to ensure compliance with our security standards. \n\nEmployees are prohibited from downloading unauthorized software, accessing inappropriate content, or using company resources for personal commercial gain. All communications sent via the corporate email system are the property of TechNova Solutions Pvt. Ltd.",
    
    "Security": "Information security is everyone's responsibility. Employees must adhere to the IT Security Policy at all times. Passwords must be at least 14 characters long, contain numbers, symbols, and be changed every 90 days. Multi-Factor Authentication (MFA) is mandatory. \n\nNo, Bring Your Own Device (BYOD) is strictly prohibited. You must use the company-issued laptop. Any lost or stolen devices, or suspected phishing attempts, must be reported to the IT Security Desk immediately at ext. 5555.",
    
    "Remote Work": "Our Hybrid model allows for 2 days of remote work per week for full-time employees. Interns are not eligible for remote work and must work from the Bengaluru office. During remote days, employees must ensure they have a quiet, secure environment and a stable internet connection. \n\nWorking from public spaces (like cafes) while handling sensitive data is prohibited due to security risks. Employees must remain online and responsive on Slack and email during core working hours.",
    
    "Performance": "Performance Appraisals at TechNova are conducted bi-annually, in June and December, using the Objective and Key Results (OKR) framework. These reviews are designed to be constructive, focusing on employee growth, skill development, and alignment with company goals.\n\nPromotions, salary increments, and performance bonuses are tied to the December review cycle. Regular 1-on-1 feedback sessions with managers are strongly encouraged.",
    
    "Training": "Continuous Learning is a core pillar of TechNova. The Learning & Development (L&D) department provides access to various online courses, technical certifications, and soft-skills workshops. \n\nEmployees are allotted a $500 annual training budget to pursue professional development opportunities relevant to their roles. Additionally, we host monthly 'Tech Talks' where internal experts share knowledge on emerging AI trends.",
    
    "Exit Process": "Should an employee decide to leave TechNova, they must follow the standard exit process. To resign, submit a formal email to your manager and hr@technova.com with a 30-day notice period. \n\nProbation ends after exactly 6 months from the date of joining, pending a successful performance review. On the final day, the employee must return all company property, including laptops and ID badges, to receive their full and final settlement.",
    
    "Emergency Contacts": "In the event of a medical emergency or security threat at the Bengaluru office, immediately contact the Building Security Desk or the HR Emergency Hotline at +91-80-5555-0000. \n\nFor IT Security incidents, contact the IT response team. All employees are required to keep their emergency contact information updated in the HR portal.",
    
    "FAQ": "Q: Can interns work remotely?\nA: Interns are not eligible for remote work and must work from the Bengaluru office.\n\nQ: How many casual leaves are allowed?\nA: Employees are allowed 12 casual leaves per year.\n\nQ: How do I claim travel expenses?\nA: Submit all travel expense receipts through the Concur portal within 15 days of return.\n\nQ: When does probation end?\nA: Probation ends after exactly 6 months from the date of joining, pending a successful performance review.\n\nQ: Who approves international travel?\nA: All international travel must be approved by the VP of Finance and the CEO."
}

def generate_handbook():
    pdf = HandbookPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 28)
    pdf.ln(80)
    pdf.cell(0, 15, 'Employee Handbook', 0, 1, 'C')
    pdf.set_font("Helvetica", '', 18)
    pdf.cell(0, 15, 'TechNova Solutions Pvt. Ltd.', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font("Helvetica", 'I', 14)
    pdf.cell(0, 10, 'Bengaluru, Karnataka, India', 0, 1, 'C')
    
    # Table of Contents
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, "Table of Contents", 0, 1)
    pdf.ln(10)
    pdf.set_font("Helvetica", '', 14)
    for i, section in enumerate(content.keys(), 1):
        pdf.cell(0, 12, f"{i}. {section}", 0, 1)
        
    # Content Pages (One chapter per page)
    for section, text in content.items():
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 18)
        pdf.cell(0, 15, section, 0, 1)
        pdf.ln(10)
        
        pdf.set_font("Helvetica", '', 14)
        for paragraph in text.split('\n'):
            if paragraph.strip():
                # Large line height (10) for readability and length
                pdf.multi_cell(0, 10, txt=paragraph)
                pdf.ln(8)
                
    pdf.output("data/raw_documents/Employee_Handbook.pdf")
    print(f"Generated Employee Handbook: {pdf.page_no()} pages.")

if __name__ == "__main__":
    generate_handbook()

import os
from fpdf import FPDF

class TravelPolicyPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'TechNova Solutions Pvt. Ltd. - Travel & Expense Policy', 0, 1, 'R')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

content = {
    "1. Domestic Travel": "Domestic travel within India must be booked at least 7 days in advance to ensure the best rates. TechNova preferred airlines must be used for all flights. Economy class is the standard for all domestic air travel, regardless of employee level.\n\nFor train travel, 2-Tier or 3-Tier AC is approved. Road travel via personal vehicle will be reimbursed at a standard rate of INR 10 per kilometer, subject to prior approval and submission of toll receipts. Airport transfers should utilize authorized cab aggregators like Ola or Uber, using the corporate billing profile.",
    
    "2. International Travel": "All international travel requires extensive justification and pre-approval. Flights exceeding 8 hours of continuous travel may be booked in Premium Economy, subject to VP approval. Business class is strictly reserved for Executive Leadership (C-Suite) or specific client-mandated travel.\n\nVisa application fees, travel insurance, and necessary vaccinations will be fully reimbursed by TechNova. Employees traveling internationally are required to use the corporate travel desk for all bookings to ensure compliance with duty-of-care requirements.",
    
    "3. Hotel Reimbursement": "Accommodation should be booked using the corporate travel desk's preferred hotel partners. The standard daily hotel cap is INR 5000 for Tier-1 cities (Mumbai, Delhi, Bengaluru, Chennai) and INR 3500 for Tier-2 cities.\n\nFor international travel, hotel caps are defined dynamically based on the destination city's cost of living index (e.g., $150/night for North America, 120 Euros/night for Europe). If a preferred hotel is unavailable, employees may book alternative accommodation within the stated limits, but a justification must be provided.",
    
    "4. Food Allowance": "TechNova provides a daily per diem allowance for food and incidental expenses during business travel. The domestic per diem is INR 1000 per day. The international per diem varies by region but averages $60 or 50 Euros per day.\n\nPer diem allowances are automatically calculated based on the travel dates and do not require the submission of individual food receipts. However, if an employee hosts a business dinner with a client, the actual expenses can be claimed separately using an itemized receipt, subject to the client entertainment policy.",
    
    "5. Approval Workflow": "The travel approval workflow is strictly enforced through the internal Concur portal. For domestic travel, approval is required from the immediate reporting manager. For international travel, approval must be granted by the respective Vice President and the CEO.\n\nExpense claims must be submitted within 15 days of returning from the trip. Claims submitted after 30 days will be rejected unless an exceptional circumstance is documented and approved by HR. Approved reimbursements will be credited directly to the employee's salary account in the subsequent payroll cycle.",
    
    "6. FAQ": "Q: How do I claim travel expenses?\nA: Submit all travel expense receipts through the Concur portal within 15 days of return.\n\nQ: Who approves international travel?\nA: All international travel must be approved by the VP of Finance and the CEO."
}

def generate_travel_policy():
    pdf = TravelPolicyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 28)
    pdf.ln(80)
    pdf.cell(0, 15, 'Travel & Expense Policy', 0, 1, 'C')
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
                # Large line height for readability and length
                pdf.multi_cell(0, 10, text=paragraph)
                pdf.ln(8)
                
    pdf.output("data/raw_documents/Travel_Policy.pdf")
    print(f"Generated Travel & Expense Policy: {pdf.page_no()} pages.")

if __name__ == "__main__":
    generate_travel_policy()

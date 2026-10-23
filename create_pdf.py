"""Step 1: create a sample PDF.

The company is made up, so the AI can only answer questions about it by
reading this PDF. That makes it a good test that RAG really works.
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

PDF_PATH = "data/company_handbook.pdf"

TITLE = "Zephyrine Labs - Employee Handbook 2026"

SECTIONS = {
    "1. About the Company": (
        "Zephyrine Labs builds weather-forecasting software for small airports and farms. "
        "The company was founded in 2017 in Halifax, Canada, by Ines Okafor and Tomas Brandvold. "
        "It has 214 employees in three offices: Halifax (headquarters), Lisbon and Kuala Lumpur. "
        "Its main product, SkyLedger, gives local weather forecasts that refresh every 10 minutes."
    ),
    "2. Working Hours and Hybrid Work": (
        "Employees work in the office on Tuesdays, Wednesdays and Thursdays. Mondays and Fridays "
        "are work-from-home days. Core hours are 10:00 to 15:00; outside core hours, schedules are "
        "flexible. After six months, employees can ask to work fully remote. Working from another "
        "country is allowed for up to 30 days per year, with two weeks' notice to the People team."
    ),
    "3. Annual Leave": (
        "Full-time employees get 24 days of paid annual leave per year. Up to 5 unused days can be "
        "carried over to the next year, but they must be used by 31 March or they expire. Leave of "
        "more than 5 days in a row must be requested at least 4 weeks in advance in the Tidewater "
        "HR portal. The office is closed from 24 December to 1 January, and these days do not count "
        "as annual leave."
    ),
    "4. Sick Leave and Parental Leave": (
        "Employees get 10 paid sick days per year. A doctor's note is needed after 3 sick days in a "
        "row. Parental leave is 16 weeks at full pay for all parents, including adoptive parents. "
        "Bereavement leave is 5 days for immediate family and 2 days for extended family."
    ),
    "5. Expenses and Travel": (
        "Expenses must be submitted in the Ledgerly app within 30 days, with a photo of the receipt. "
        "The meal limit is 45 USD per day for domestic trips and 70 USD per day for international "
        "trips. Hotels can cost up to 180 USD per night, or 250 USD in London, New York, Tokyo and "
        "Singapore. Flights under 6 hours are economy class; flights of 6 hours or more are premium "
        "economy. Alcohol is never reimbursed."
    ),
    "6. Equipment and Home Office": (
        "Every employee gets a laptop on day one. Engineers can choose a MacBook Pro or a ThinkPad "
        "X1 Carbon; everyone else gets a MacBook Air. Laptops are replaced every 3 years. New "
        "employees get a one-time 600 USD home office budget and a 40 USD monthly internet allowance. "
        "Lost or stolen laptops must be reported to helpdesk@zephyrine.example within 24 hours."
    ),
    "7. Learning and Development": (
        "Each employee has a learning budget of 1,500 USD per year for courses, books, certifications "
        "and conference tickets. Employees can also take 2 learning days per quarter. Every new hire "
        "gets an onboarding buddy for their first 90 days, and can then join the Tailwind mentorship "
        "programme."
    ),
    "8. Performance Reviews and Bonus": (
        "Performance reviews happen twice a year, in April and October, using the Compass framework. "
        "Compass scores four areas from 1 to 5: Impact, Craft, Collaboration and Ownership. Salary "
        "increases start on 1 May each year. A company bonus of up to 10% of salary is paid in "
        "February if the company hits its revenue target."
    ),
    "9. Security Rules": (
        "Multi-factor authentication is required on all company accounts. Passwords must be at least "
        "14 characters and kept in the Keyvault password manager. Security problems, such as clicking "
        "a phishing link, must be reported within 1 hour to security@zephyrine.example. Nobody is "
        "punished for reporting their own mistake quickly."
    ),
}


def main():
    os.makedirs("data", exist_ok=True)
    styles = getSampleStyleSheet()

    content = [Paragraph(TITLE, styles["Title"])]
    for heading, text in SECTIONS.items():
        content.append(Paragraph(heading, styles["Heading2"]))
        content.append(Paragraph(text, styles["BodyText"]))
        content.append(Spacer(1, 8))

    SimpleDocTemplate(PDF_PATH, pagesize=A4).build(content)
    print(f"Created {PDF_PATH}")


if __name__ == "__main__":
    main()

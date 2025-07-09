# %%
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

GOOGLE_KEY = os.getenv("GOOGLE_KEY")

def send_gmail(to_email, subject, body, gmail_user, app_password = GOOGLE_KEY):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, app_password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

to_email = 'bramgriffioen98@gmail.com'
subject = 'Daily VBT Rental Update'
# body = 'This is a test email sent from Python using Gmail.'
gmail_user = 'bramgriffioen98@gmail.com'

send_gmail(to_email, subject, body, gmail_user) 

# %%
import pandas as pd
path = r'C:\Users\bgriffioen\OneDrive - STX Commodities B.V\Desktop\funda-project\funda-tool\data\huren\properties_amsterdam.csv'

df = pd.read_csv(path, sep=',')
# filter: is_available:
df = df[df['is_available'] == True]
# sort number_of_responses
df = df.sort_values(by='number_of_responses', ascending=True)

base_url = 'https://vbtverhuurmakelaars.nl'

df['link'] = base_url +  df['detail_url'] 
df['price_per_m2'] = df['price_per_month'] / df['surface_area_m2']

def create_email_body(df, max_rows=10):
    df = df.head(max_rows).copy()
    df['price_per_m2'] = df['price_per_m2'].round(2)

    body = "🏠 Top Amsterdam Rentals (available):\n\n"
    body += f"{'Address':<35} {'€ Rent':>8} {'m²':>5} {'€/m²':>6} {'Resp.':>6}\n"
    body += "-" * 70 + "\n"
    
    for _, row in df.iterrows():
        address = row['address'][:32] + "..." if len(row['address']) > 35 else row['address']
        body += f"{address:<35} {int(row['price_per_month']):>8} {int(row['surface_area_m2']):>5} {row['price_per_m2']:>6.2f} {int(row['number_of_responses']):>6}\n"
        body += f"🔗 {row['link']}\n\n"
    
    return body

body = create_email_body(df)

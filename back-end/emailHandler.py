import yagmail

def send_email():
    # Your email credentials
    sender_email = "videnhancenotifications@gmail.com"
    sender_password = "your_email_password"

    # Recipient email address
    recipient_email = "videnhancenotifications@gmail.com"

    # Email subject and content
    subject = "Hello from Yagmail!"
    body = "This is the email content."

    try:
        # Initialize yagmail SMTP connection
        yag = yagmail.SMTP(sender_email, oauth2_file="./google_creds.json")

        # Send the email
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=body
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_email()

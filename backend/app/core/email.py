from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

def get_email_template(title: str, content: str, button_text: str = None, button_url: str = None) -> str:
    """
    Generate a professional email template with consistent styling.
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
            }}
            .header {{
                text-align: center;
                padding: 20px 0;
                background-color: #2563eb;
                color: white;
                border-radius: 5px 5px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .content p {{
                margin-bottom: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background-color: #f8fafc;
                border-radius: 0 0 5px 5px;
                font-size: 14px;
                color: #64748b;
            }}
            .social-links {{
                margin: 20px 0;
            }}
            .social-links a {{
                color: #2563eb;
                text-decoration: none;
                margin: 0 10px;
            }}
            @media only screen and (max-width: 600px) {{
                .container {{
                    width: 100% !important;
                }}
                .content {{
                    padding: 20px 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
            </div>
            <div class="content">
                {content}
                {f'<p style="text-align: center;"><a href="{button_url}" class="button">{button_text}</a></p>' if button_text and button_url else ''}
            </div>
            <div class="footer">
                <div class="social-links">
                    <a href="#">LinkedIn</a>
                    <a href="#">Twitter</a>
                    <a href="#">Facebook</a>
                </div>
                <p>© 2024 JobHunter. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

async def send_email(
    email_to: EmailStr,
    subject: str,
    body: str,
    email_from: Optional[EmailStr] = None,
) -> bool:
    """
    Send an email to a single recipient.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
        sender=email_from or settings.MAIL_FROM,
    )
    
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

async def send_emails(
    emails_to: List[EmailStr],
    subject: str,
    body: str,
    email_from: Optional[EmailStr] = None,
) -> bool:
    """
    Send an email to multiple recipients.
    """
    message = MessageSchema(
        subject=subject,
        recipients=emails_to,
        body=body,
        subtype="html",
        sender=email_from or settings.MAIL_FROM,
    )
    
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending emails: {e}")
        return False

async def send_verification_email(email_to: EmailStr, token: str) -> bool:
    """
    Send a verification email to a user.
    """
    subject = "Verify your email address"
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    content = f"""
    <p>Welcome to JobHunter! We're excited to have you join our community of professionals.</p>
    <p>To get started, please verify your email address by clicking the button below:</p>
    <p>If you didn't create an account, you can safely ignore this email.</p>
    """
    
    body = get_email_template(
        title="Welcome to JobHunter!",
        content=content,
        button_text="Verify Email Address",
        button_url=verification_url
    )
    
    return await send_email(email_to, subject, body)

async def send_password_reset_email(email_to: EmailStr, token: str) -> bool:
    """
    Send a password reset email to a user.
    """
    subject = "Reset your password"
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    content = f"""
    <p>We received a request to reset your password for your JobHunter account.</p>
    <p>Click the button below to create a new password:</p>
    <p>This link will expire in 30 minutes for security reasons.</p>
    <p>If you didn't request this password reset, you can safely ignore this email.</p>
    """
    
    body = get_email_template(
        title="Password Reset Request",
        content=content,
        button_text="Reset Password",
        button_url=reset_url
    )
    
    return await send_email(email_to, subject, body) 
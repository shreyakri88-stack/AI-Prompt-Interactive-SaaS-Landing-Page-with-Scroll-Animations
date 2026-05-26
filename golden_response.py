```python
"""
golden_response.py

Production-quality reference implementation for:
Interactive SaaS Landing Page with Scroll Animations

This file demonstrates:
- Clean architecture planning
- Secure backend form handling
- Validation and sanitization
- Email workflow
- Scalable configuration
- Proper error handling
- Maintainable structure

Author: OpenAI Benchmark Reference
"""

from dataclasses import dataclass
from typing import Dict, Any
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =========================================================
# Configuration
# =========================================================

@dataclass
class AppConfig:
    """
    Application configuration loaded from environment variables.
    """

    smtp_server: str
    smtp_port: int
    email_user: str
    email_password: str
    receiver_email: str

    @staticmethod
    def load() -> "AppConfig":
        """
        Load environment variables safely.

        Raises:
            EnvironmentError: If required environment variables are missing.
        """

        required_vars = [
            "SMTP_SERVER",
            "SMTP_PORT",
            "EMAIL_USER",
            "EMAIL_PASSWORD",
            "RECEIVER_EMAIL"
        ]

        missing = [var for var in required_vars if not os.getenv(var)]

        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return AppConfig(
            smtp_server=os.getenv("SMTP_SERVER"),
            smtp_port=int(os.getenv("SMTP_PORT")),
            email_user=os.getenv("EMAIL_USER"),
            email_password=os.getenv("EMAIL_PASSWORD"),
            receiver_email=os.getenv("RECEIVER_EMAIL"),
        )


# =========================================================
# Validation Utilities
# =========================================================

class ValidationError(Exception):
    """Custom validation exception."""
    pass


def sanitize_input(value: str) -> str:
    """
    Sanitize user input.

    Removes:
    - Leading/trailing whitespace
    - Potential script tags
    - Dangerous HTML content
    """

    value = value.strip()

    # Remove script tags
    value = re.sub(r"<script.*?>.*?</script>", "", value, flags=re.IGNORECASE)

    # Remove remaining HTML tags
    value = re.sub(r"<.*?>", "", value)

    return value


def validate_email(email: str) -> bool:
    """
    Validate email format.
    """

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


def validate_contact_form(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate contact form payload.

    Expected fields:
    - name
    - email
    - message
    """

    required_fields = ["name", "email", "message"]

    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

        if not isinstance(data[field], str):
            raise ValidationError(f"Field '{field}' must be a string")

    name = sanitize_input(data["name"])
    email = sanitize_input(data["email"])
    message = sanitize_input(data["message"])

    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters long")

    if not validate_email(email):
        raise ValidationError("Invalid email address")

    if len(message) < 10:
        raise ValidationError("Message must be at least 10 characters long")

    return {
        "name": name,
        "email": email,
        "message": message
    }


# =========================================================
# Email Service
# =========================================================

class EmailService:
    """
    Handles email delivery logic.
    """

    def __init__(self, config: AppConfig):
        self.config = config

    def send_contact_email(self, form_data: Dict[str, str]) -> bool:
        """
        Send contact form email.

        Returns:
            bool: True if successful, False otherwise.
        """

        try:
            message = MIMEMultipart()

            message["From"] = self.config.email_user
            message["To"] = self.config.receiver_email
            message["Subject"] = "New SaaS Landing Page Contact Submission"

            email_body = f"""
            New Contact Form Submission

            Name: {form_data['name']}
            Email: {form_data['email']}

            Message:
            {form_data['message']}
            """

            message.attach(MIMEText(email_body, "plain"))

            with smtplib.SMTP(
                self.config.smtp_server,
                self.config.smtp_port
            ) as server:

                server.starttls()

                server.login(
                    self.config.email_user,
                    self.config.email_password
                )

                server.send_message(message)

            return True

        except smtplib.SMTPException as smtp_error:
            print(f"[SMTP ERROR]: {smtp_error}")
            return False

        except Exception as error:
            print(f"[UNKNOWN EMAIL ERROR]: {error}")
            return False


# =========================================================
# API Simulation Layer
# =========================================================

class ContactAPI:
    """
    Simulated backend API handler.

    Demonstrates production-style backend structure.
    """

    def __init__(self):
        self.config = AppConfig.load()
        self.email_service = EmailService(self.config)

    def submit_contact_form(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle contact form submission.

        Returns:
            Dict containing success/error response.
        """

        try:
            validated_data = validate_contact_form(payload)

            email_sent = self.email_service.send_contact_email(
                validated_data
            )

            if not email_sent:
                return {
                    "success": False,
                    "message": "Failed to send email"
                }

            return {
                "success": True,
                "message": "Contact form submitted successfully"
            }

        except ValidationError as validation_error:
            return {
                "success": False,
                "message": str(validation_error)
            }

        except EnvironmentError as env_error:
            return {
                "success": False,
                "message": f"Configuration error: {env_error}"
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Unexpected server error: {error}"
            }


# =========================================================
# Example Usage
# =========================================================

def run_demo():
    """
    Demonstration entry point.
    """

    sample_payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": (
            "Hello, I am interested in your SaaS platform "
            "and would like to know more."
        )
    }

    api = ContactAPI()

    response = api.submit_contact_form(sample_payload)

    print("\n========== API RESPONSE ==========")
    print(response)
    print("==================================\n")


# =========================================================
# Main Entry
# =========================================================

if __name__ == "__main__":
    run_demo()
```

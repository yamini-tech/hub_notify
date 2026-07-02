from twilio.rest import Client
from app.config import settings

def send_sms(to: str, body: str) -> str:
    """
    Send an SMS via Twilio.
    Returns the Twilio message SID on success.
    """
    # 1. Initialize the Twilio Client
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    
    # 2. Send the message
    message = client.messages.create(
        body=body,
        from_=settings.twilio_phone_number,
        to=to,
    )
    print(f"\n--- [DEBUG NOTIFY] ---")
    print(f"Recipient: {to}")
    print(f"Content: {body}")
    print(f"----------------------\n")
    # 3. Return the unique SID provided by Twilio
    return message.sid
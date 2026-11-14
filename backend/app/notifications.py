import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings

logger = logging.getLogger("notifications")

def send_access_request_email(user_email: str, user_name: str, team_id: str, requested_role: str, recipients: list = None, request_id: int = None, base_url: str = "https://hockey-coach-app-1083993716124.europe-west4.run.app") -> bool:
    """
    Sends an email alert to the admin/coaches whenever a new user requests access, featuring 1-click approval links.
    """
    if not recipients:
        recipients = [settings.ADMIN_NOTIFICATION_EMAIL]
    else:
        if settings.ADMIN_NOTIFICATION_EMAIL not in recipients:
            recipients.append(settings.ADMIN_NOTIFICATION_EMAIL)

    approve_url = f"{base_url}/api/auth/approve-request-direct?request_id={request_id}" if request_id else base_url
    reject_url = f"{base_url}/api/auth/reject-request-direct?request_id={request_id}" if request_id else base_url

    subject = f"🔔 HV Myra Matchday App: Access Request for {team_id} ({requested_role.upper()})"

    text_body = f"""Hello Coach / Admin,

A new user has requested Coach access to the HV Myra Matchday Board Application:

• User Email: {user_email}
• User Name: {user_name or 'N/A'}
• Requested Team: HV Myra {team_id}
• Requested Role: {requested_role.capitalize()}

To approve this coach immediately from your email, click the link below:
{approve_url}

To reject this request:
{reject_url}

Best regards,
HV Myra Hockey Matchday Board System
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0b0f19; color: #f8fafc; margin: 0; padding: 20px; }}
    .card {{ max-width: 550px; margin: 0 auto; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
    .header {{ text-align: center; border-bottom: 1px solid #334155; padding-bottom: 16px; margin-bottom: 20px; }}
    .header h2 {{ color: #38bdf8; margin: 0; font-size: 20px; }}
    .field {{ margin-bottom: 12px; font-size: 14px; line-height: 1.5; }}
    .field strong {{ color: #94a3b8; width: 130px; display: inline-block; }}
    .btn-container {{ display: flex; gap: 12px; margin-top: 24px; justify-content: center; }}
    .btn {{ display: inline-block; padding: 12px 24px; font-weight: bold; border-radius: 8px; text-decoration: none; font-size: 14px; text-align: center; }}
    .btn-approve {{ background: #22c55e; color: #ffffff !important; }}
    .btn-reject {{ background: #ef4444; color: #ffffff !important; }}
    .footer {{ text-align: center; color: #64748b; font-size: 12px; margin-top: 24px; border-top: 1px solid #334155; padding-top: 16px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h2>🔔 HV Myra Coach Access Request</h2>
    </div>
    <div class="field"><strong>User Email:</strong> <span style="color:#ffffff;">{user_email}</span></div>
    <div class="field"><strong>User Name:</strong> <span style="color:#ffffff;">{user_name or 'N/A'}</span></div>
    <div class="field"><strong>Requested Team:</strong> <span style="color:#38bdf8; font-weight:bold;">HV Myra {team_id}</span></div>
    <div class="field"><strong>Requested Role:</strong> <span style="color:#f59e0b; font-weight:bold;">{requested_role.capitalize()}</span></div>
    
    <div style="margin-top: 20px; background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; padding: 12px; border-radius: 4px; font-size: 13px; color: #cbd5e1;">
      Click below to instantly grant or reject Coach access. Approval will automatically authorize this user's Google email for line-up edits.
    </div>

    <div class="btn-container">
      <a href="{approve_url}" class="btn btn-approve" target="_blank">✅ APPROVE COACH ACCESS</a>
      <a href="{reject_url}" class="btn btn-reject" target="_blank">❌ REJECT REQUEST</a>
    </div>

    <div class="footer">
      HV Myra Hockey Matchday Board System • Admin Notification
    </div>
  </div>
</body>
</html>
"""

    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.info(
            f"[NOTIFICATION LOG] SMTP not configured. Access Request Notification Payload:\n"
            f"To: {recipients}\nSubject: {subject}\nApprove URL: {approve_url}\nReject URL: {reject_url}"
        )
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.SMTP_USER
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"Access request notification email sent to {recipients}")
        return True
    except Exception as e:
        logger.error(f"Failed to send access request email: {e}")
        return False


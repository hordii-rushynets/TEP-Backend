"""Utils for tep_user app."""
from tep_user.services import EmailService, UserService


def send_email_code(email: str, full_name: str) -> None:
    """
    Send verification code by email util.
    
    :param email: user email.
    :param full_name: user full name.
    """
    code = UserService.gen_code(email=email)
    print(f"\n\n Code: {code} \n\n")
    EmailService(recipient=email, context={'full_name': full_name}).verification_code(code).send()

from email_validator import validate_email, EmailNotValidError

#==========================
# comprehensive verification of email 
# by signature and availability
#==========================
def email_check(email: str):

    try:
        validate_email(email, check_deliverability=True)
        return True
    except EmailNotValidError:
        return False
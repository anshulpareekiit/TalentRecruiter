class UserLabels:
    pwd_set_email_body_template = (
        "Hi,\n\n"
        "Click the link below to set your password: {password_token}\n\n"
        "This link will expire in 30 minutes."
    )
    pwd_set_email_subject = (
        "Setup your password!"
    )
    msg_email_sent_successfully = "Email sent successfully!"
    msg_err_send_email =("Error while sending email: str{exception}")
    msg_password_set_success = "Password set successfully!"
    msg_user_created_success = "User created successfully!"
    msg_update_success = "Record updated successfully!"
    msg_record_found = "Records Found"    
    ########ERROR MESSAGES############
    err_msg_duplicate_rec = "Duplicate record found!"
    err_msg_went_wrong = ("Something went wrong")
    err_msg_record_not_found = "Records not found!"
    err_detail = "err details:{exception}"
    err_msg_token_expired = "Token already expired"
    err_msg_field_notfound = "Fields not found"
    

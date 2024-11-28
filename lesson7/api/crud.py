import fastcrud 
from fastcrud import FastCRUD
from models import User, EmailLog

crud_user  = FastCRUD(User)
crud_email_log = FastCRUD(EmailLog)

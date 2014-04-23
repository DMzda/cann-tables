from cann_tables import db, models
from passlib.context import CryptContext

import getpass

passwd_context = CryptContext(schemes=["pbkdf2_sha512"])


def add_user():
    """Add a user to the database"""
    username = input("Username: ")
    password = getpass.getpass()

    pwd_hash = passwd_context.encrypt(password)

    user = models.User(username=username, password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    print("User {} added".format(username))

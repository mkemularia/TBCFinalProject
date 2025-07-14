from ext import site, db
from models import Product, User, Comment

with site.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="Admin", password="AdminPass", role="Admin")

    db.session.add(admin)
    db.session.commit()

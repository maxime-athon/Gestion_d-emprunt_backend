from flask_marshmallow import Marshmallow
from models import User, Document, Emprunt, Notification

ma = Marshmallow()

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        include_fk = True

class EmpruntSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Emprunt
        include_fk = True

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
    emprunts = ma.Nested(EmpruntSchema, many=True)
    notifications = ma.Nested(NotificationSchema, many=True)
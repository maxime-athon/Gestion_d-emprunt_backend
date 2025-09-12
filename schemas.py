from database import ma
from models import User, Document, Emprunt, Notification

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        load_instance = True
        include_relationships = True

class EmpruntSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Emprunt
        load_instance = True
        include_fk = True

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True
        include_fk = True

# Instances réutilisables
user_schema = UserSchema()
users_schema = UserSchema(many=True)
document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)
emprunt_schema = EmpruntSchema()
emprunts_schema = EmpruntSchema(many=True)
notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)

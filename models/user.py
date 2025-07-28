from dbconfig import db

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255))
    role = db.Column(db.String(20))
    
    client = db.relationship('Client', backref='users', uselist=False)
    insurance = db.relationship('Insurance', backref='users', uselist=False)
    police = db.relationship('Police', backref='users', uselist=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'role': self.role
        }
        
    def full_serialize(self):
        data = self.serialize()
        data.update({
            'client': self.client.serialize() if self.client else None,
            'insurance': self.insurance.serialize() if self.insurance else None,
            'police': self.police.serialize() if self.police else None
        })
        return data

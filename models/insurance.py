from dbconfig import db

class Insurance(db.Model):
    __tablename__ = 'insurances'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    clients = db.relationship("Client", back_populates="insurance")

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'clients': [c.serialize() for c in self.clients],
            'user_id': self.user_id
        }
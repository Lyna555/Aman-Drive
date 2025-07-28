from dbconfig import db

class Police(db.Model):
    __tablename__ = 'police'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address_maps = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    accidents = db.relationship('Accident', backref='police')

    def serialize(self):
        return {
            'id': self.id,
            'address_maps': self.address_maps,
            'accidents': [a.serialize() for a in self.accidents],
            'user_id': self.user_id
        }
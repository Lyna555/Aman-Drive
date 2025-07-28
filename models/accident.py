from dbconfig import db

class Accident(db.Model):
    __tablename__ = 'accidents'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address_maps = db.Column(db.String(255))
    police_id = db.Column(db.Integer, db.ForeignKey('police.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    def serialize(self):
        return {
            'id': self.id,
            'address_maps': self.address_maps,
            'police_id': self.police_id,
            'client_id': self.client_id
        }
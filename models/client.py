from dbconfig import db

class Client(db.Model):
    __tablename__ = 'clients'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    diseases = db.Column(db.Text)
    blood_type = db.Column(db.String(5))
    insurance_nbr = db.Column(db.String(50))
    vehicle_type = db.Column(db.String(50))
    vehicle_brand = db.Column(db.String(50))
    vehicle_year = db.Column(db.Integer)
    vehicle_plate = db.Column(db.String(20))
    horses = db.Column(db.Integer)
    price = db.Column(db.Float)
    insurance_type = db.Column(db.String(50))
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurances.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurances.id'))
    
    insurance = db.relationship("Insurance", back_populates="clients")
    accidents = db.relationship('Accident', backref='clients')


    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'diseases': self.diseases,
            'blood_type': self.blood_type,
            'insurance_nbr': self.insurance_nbr,
            'vehicle_type': self.vehicle_type,
            'vehicle_brand': self.vehicle_brand,
            'vehicle_year': self.vehicle_year,
            'vehicle_plate': self.vehicle_plate,
            'horses': self.horses,
            'price': self.price,
            'insurance_type': self.insurance_type,
            'insurance': self.insurance.serialize() if self.insurance else None,
            'accidents': [a.serialize() for a in self.accidents],
            'insurance_id': self.insurance_id,
            'user_id': self.user_id,
        }
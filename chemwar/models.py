from chemwar import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    # 0 - General User   1 - Group Manager   2 - Admin 
    level = db.Column(db.Integer, default=False, nullable=False)
    group = db.Column(db.Integer, db.ForeignKey("groups.id", ondelete="CASCADE"))
    initial = db.Column(db.String(16), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    blood_group = db.Column(db.String(16), nullable=False)
    med_tag = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Username: {1} | Password: {2} | Admin: {3}".format(
            self.id, self.username, self.password, self.level
        )

class Groups(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0}".format(
            self.id
        )
        
class Cordons(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    cordon_name = db.Column(db.String(64), nullable=False)
    cordon_size = db.Column(db.Integer, nullable=False)
    down_wind = db.Column(db.Boolean, default=False, nullable=False)
    down_wind_size = db.Column(db.Integer, nullable=False)
    cbrn_type = db.Column(db.Integer, db.ForeignKey("cbrn.id", ondelete="CASCADE"), nullable=False)
    
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Cordon Size: {1}m | DW?: {2} | DW Size: {3}m | CBRN ID: {4}".format(
            self.id, self.cordon_size, self.down_wind, self.down_wind_size, self.cbrn_type
        )
        
class CBRN(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), unique=False, nullable=False)
    
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Type: {1}".format(
            self.id, self.type
        )
    
class Reports(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    cordon_type = db.Column(db.Integer, db.ForeignKey("cordons.id", ondelete="CASCADE"), nullable=False)
    reported_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0}".format(
            self.id
        )
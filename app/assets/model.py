from app.db import db


class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(20))
    type_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'))
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, code, name, type_id):
        self.code = code
        self.name = name
        self.type_id = type_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AssetType(db.Model):
    __tablename__ = 'asset_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'))
    name = db.Column(db.String(20))
    children = db.relationship('AssetType')
    assets = db.relationship('Asset', backref='type')

    def __init__(self, name, parent_id=0):
        self.name = name
        self.parent_id = parent_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

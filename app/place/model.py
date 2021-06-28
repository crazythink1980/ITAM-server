from app.db import db


# 资产位置
class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),
                     nullable=False,
                     unique=True,
                     comment='位置名称')  # 位置名称
    parent_id = db.Column(db.Integer, db.ForeignKey('place.id'),
                          comment='父位置')  # 父位置
    # children = db.relationship('Place')
    parent = db.relationship('Place', remote_side=[id], backref='children')

    def __init__(self, name, parent_id=0):
        self.name = name
        self.parent_id = parent_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

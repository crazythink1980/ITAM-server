from app.db import db


# 部门
class Dept(db.Model):
    __tablename__ = 'dept'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),
                     nullable=False,
                     unique=True,
                     comment='部门名称')  # 部门名称
    parent_id = db.Column(db.Integer, db.ForeignKey('dept.id'),
                          comment='上级部门')  # 上级部门
    children = db.relationship('Dept')

    def __init__(self, name, parent_id=0):
        self.name = name
        self.parent_id = parent_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

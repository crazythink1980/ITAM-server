from app.db import db


# 资产子类型
class AssetType(db.Model):
    __tablename__ = 'assettype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),
                     nullable=False,
                     unique=True,
                     comment='资产子类型名称')  # 资产子类型名称
    parent_id = db.Column(db.String(20), comment='资产类型')  # 资产类型

    def __init__(self, name, parent_id):
        self.name = name
        self.parent_id = parent_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
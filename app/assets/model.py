from sqlalchemy.ext.declarative import ConcreteBase
from app.db import db
from app.users.model import User
from app.dept.model import Dept


#资产总表
class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer)  #资产类型，取值1：PC，2：网络打印机，3：服务器，4：网络设备，5：安全设备，6：软件
    status = db.Column(db.Integer)  #资产状态，取值0：停止使用，1：使用中
    name = db.Column(db.String(20))  #资产名称
    trade_date = db.Column(db.DateTime)  #购买日期
    product_date = db.Column(db.DateTime)  #生产日期
    expire_date = db.Column(db.DateTime)  #过保日期
    manage_user = db.Column(db.Integer, db.ForeignKey('users.id'))  #管理人
    use_dept = db.Column(db.Integer, db.ForeignKey('dept.id'))  #使用部门
    manufactory = db.Column(db.String(100))  #制造商
    model = db.Column(db.String(100))  #型号
    sn = db.Column(db.String(50))  #系列号
    create_time = db.Column(db.DateTime, nullable=False,
                            default=db.func.now())  # 记录的创建时间
    update_time = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.now(),
                            onupdate=db.func.now())  # 记录的更新时间

    __mapper_args__ = {
        "polymorphic_identity": 0,  # 指定了多态表哪个字段区分该条记录是属于哪个继承表
        "polymorphic_on": type,
    }


#PC
class Computer(Asset):
    __tablename__ = 'computer'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20))  #IP地址
    mac = db.Column(db.String(50))  #Mac地址
    display = db.Column(db.String(100))  #显示器
    printer = db.Column(db.String(100))  #打印机
    cpu = db.Column(db.String(20))  #CPU型号
    men = db.Column(db.String(20))  #内存容量
    disk = db.Column(db.String(20))  #硬盘容量
    os = db.Column(db.String(50))  #操作系统版本
    __mapper_args__ = {
        'polymorphic_identity': 1,  # 当type=1时的表记录为PC
    }


class AssetType(db.Model):
    __tablename__ = 'asset_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'))
    name = db.Column(db.String(20))
    children = db.relationship('AssetType')

    #assets = db.relationship('Asset', backref='type')

    def __init__(self, name, parent_id=0):
        self.name = name
        self.parent_id = parent_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

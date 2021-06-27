from app.db import db
import datetime as dt


# 资产总表
class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(
        db.String(20), comment='资产类型'
    )  # 资产类型，取值'PC'：PC，Printer：网络打印机，Server：服务器，NetDevice：网络设备，SecDevice：安全设备，Software：软件
    status = db.Column(db.Integer, comment='资产状态')  # 资产状态，取值0：停止使用，1：使用中
    name = db.Column(db.String(20), comment='资产名称')  # 资产名称
    trade_date = db.Column(db.DateTime, comment='购买日期')  # 购买日期
    product_date = db.Column(db.DateTime, comment='生产日期')  # 生产日期
    expire_date = db.Column(db.DateTime, comment='过保日期')  # 过保日期
    manage_user = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            comment='管理人')  # 管理人
    use_dept = db.Column(db.Integer, db.ForeignKey('dept.id'),
                         comment='使用部门')  # 使用部门
    place = db.Column(db.Integer, db.ForeignKey('place.id'),
                      comment='设备位置')  # 设备位置
    manufactory = db.Column(db.String(100), comment='制造商')  # 制造商
    model = db.Column(db.String(100), comment='型号')  # 型号
    sn = db.Column(db.String(50), comment='系列号')  # 系列号
    asset_code = db.Column(db.String(50), comment='固定资产编号')  # 固定资产编号
    create_time = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.now(),
                            comment='记录的创建时间')  # 记录的创建时间
    update_time = db.Column(db.DateTime,
                            nullable=False,
                            default=db.func.now(),
                            onupdate=db.func.now(),
                            comment='记录的更新时间')  # 记录的更新时间

    __mapper_args__ = {
        #        "polymorphic_identity": '0',  # 指定了多态表哪个字段区分该条记录是属于哪个继承表
        "polymorphic_on": type,
    }

    def update(self, data):
        self.status = data["status"]
        self.name = data["name"]
        self.trade_date = dt.datetime.strptime(
            data["trade_date"],
            '%Y-%m-%d') if data["trade_date"] is not None else None
        self.product_date = dt.datetime.strptime(
            data["product_date"],
            '%Y-%m-%d') if data["product_date"] is not None else None
        self.expire_date = dt.datetime.strptime(
            data["expire_date"],
            '%Y-%m-%d') if data["expire_date"] is not None else None
        self.manage_user = data["manage_user"]
        self.use_dept = data["use_dept"]
        self.place = data["place"]
        self.manufactory = data["manufactory"]
        self.model = data["model"]
        self.sn = data["sn"]
        self.asset_code = data["asset_code"]
        return


# PC机
class Computer(Asset):
    __tablename__ = 'computer'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20), comment='IP地址')  # IP地址
    mac = db.Column(db.String(50), comment='Mac地址')  # Mac地址
    display = db.Column(db.String(100), comment='显示器型号')  # 显示器型号
    printer = db.Column(db.String(100), comment='打印机型号')  # 打印机型号
    cpu = db.Column(db.String(20), comment='CPU型号')  # CPU型号
    memory = db.Column(db.String(20), comment='内存容量')  # 内存容量
    disk = db.Column(db.String(20), comment='硬盘容量')  # 硬盘容量
    os = db.Column(db.String(50), comment='操作系统版本')  # 操作系统版本
    __mapper_args__ = {
        'polymorphic_identity': 'PC',  # 当type=1时的表记录为PC
    }

    def update(self, data):
        super().update(data)
        self.ip = data["ip"]
        self.mac = data["mac"]
        self.display = data["display"]
        self.printer = data["printer"]
        self.cpu = data["cpu"]
        self.memory = data["memory"]
        self.disk = data["disk"]
        self.os = data["os"]
        return


# 网络打印机
class Printer(Asset):
    __tablename__ = 'printer'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20), comment='IP地址')  # IP地址
    mac = db.Column(db.String(50), comment='Mac地址')  # Mac地址
    sub_type = db.Column(db.Integer,
                         comment='打印机类型')  # 打印机类型，取值1：激光打印机，2：喷墨打印机，3：其他打印机
    func_type = db.Column(db.Integer,
                          comment='打印机功能')  # 打印机功能，取值1：打印，2：打印+扫描，3：打印+扫描+传真
    paper = db.Column(db.String(20), comment='支持纸张类型')  # 支持纸张类型
    __mapper_args__ = {
        'polymorphic_identity': 'Printer',  # 当type=2时的表记录为网络打印机
    }

    def update(self, data):
        super().update(data)
        self.ip = data["ip"]
        self.mac = data["mac"]
        self.sub_type = data["sub_type"]
        self.func_type = data["func_type"]
        self.paper = data["paper"]
        return


# 服务器
class Server(Asset):
    __tablename__ = 'server'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20), comment='IP地址')  # IP地址
    mac = db.Column(db.String(50), comment='Mac地址')  # Mac地址
    sub_type = db.Column(db.Integer, comment='服务器类型')  # 服务器类型，取值1：实体机，2：虚拟机
    cpu = db.Column(db.String(20), comment='CPU型号')  # CPU型号
    memory = db.Column(db.String(20), comment='内存容量')  # 内存容量
    disk = db.Column(db.String(20), comment='硬盘容量')  # 硬盘容量
    nic = db.Column(db.String(50), comment='网络接口')  # 网络接口
    os = db.Column(db.String(50), comment='操作系统版本')  # 操作系统版本
    database = db.Column(db.String(50), comment='数据库版本')  # 数据库版本
    middleware = db.Column(db.String(50), comment='中间件版本')  # 中间件版本
    usage = db.Column(db.Text, comment='用途')  # 用途
    online_date = db.Column(db.DateTime, comment='上线日期')  # 上线日期
    __mapper_args__ = {
        'polymorphic_identity': 'Server',  # 当type=3时的表记录为服务器
    }

    def update(self, data):
        super().update(data)
        self.ip = data["ip"]
        self.mac = data["mac"]
        self.sub_type = data["sub_type"]
        self.cpu = data["cpu"]
        self.memory = data["memory"]
        self.disk = data["disk"]
        self.nic = data["nic"]
        self.os = data["os"]
        self.database = data["database"]
        self.middleware = data["middleware"]
        self.usage = data["usage"]
        self.online_date = dt.datetime.strptime(
            data["online_date"],
            '%Y-%m-%d') if data["expire_date"] is not None else None
        return


# 网络设备
class NetDevice(Asset):
    __tablename__ = 'netdevice'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    management_ip = db.Column(db.String(20), comment='管理IP地址')  # 管理IP地址
    sub_type = db.Column(
        db.Integer, comment='网络设备类型')  # 网络设备类型，取值1：二层交换机，2：三层交换机，3：核心交换机，4：路由器
    port_num = db.Column(db.Integer, comment='端口个数')  # 端口个数
    device_detail = db.Column(db.Text, comment='设备详情')  # 设备详情

    __mapper_args__ = {
        'polymorphic_identity': 'NetDevice',  # 当type=3时的表记录为网络设备
    }

    def update(self, data):
        super().update(data)
        self.management_ip = data["management_ip"]
        self.sub_type = data["sub_type"]
        self.port_num = data["port_num"]
        self.device_detail = data["device_detail"]
        return


# 安全设备
class SecDevice(Asset):
    __tablename__ = 'secdevice'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    management_ip = db.Column(db.String(20), comment='管理IP地址')  # 管理IP地址
    sub_type = db.Column(db.Integer, comment='安全设备类型')  # 服务器类型，取值1：实体机，2：虚拟机
    usage = db.Column(db.Text, comment='用途')  # 用途
    device_detail = db.Column(db.Text, comment='设备详情')  # 设备详情

    __mapper_args__ = {
        'polymorphic_identity': 'SecDevice',  # 当type=3时的表记录为安全设备
    }

    def update(self, data):
        super().update(data)
        self.management_ip = data["management_ip"]
        self.sub_type = data["sub_type"]
        self.usage = data["usage"]
        self.device_detail = data["device_detail"]
        return

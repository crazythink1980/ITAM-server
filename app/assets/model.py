from app.db import db


# 资产总表
class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(
        db.Integer,
        comment='资产类型')  # 资产类型，取值1：PC，2：网络打印机，3：服务器，4：网络设备，5：安全设备，6：软件
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
    place = db.Column(db.String(50), comment='设备位置')  # 设备位置
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
        "polymorphic_identity": 0,  # 指定了多态表哪个字段区分该条记录是属于哪个继承表
        "polymorphic_on": type,
    }


# PC机
class Computer(Asset):
    __tablename__ = 'computer'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20), comment='IP地址')  # IP地址
    mac = db.Column(db.String(50), comment='Mac地址')  # Mac地址
    display = db.Column(db.String(100), comment='显示器型号')  # 显示器型号
    printer = db.Column(db.String(100), comment='打印机型号')  # 打印机型号
    cpu = db.Column(db.String(20), comment='CPU型号')  # CPU型号
    men = db.Column(db.String(20), comment='内存容量')  # 内存容量
    disk = db.Column(db.String(20), comment='硬盘容量')  # 硬盘容量
    os = db.Column(db.String(50), comment='操作系统版本')  # 操作系统版本
    __mapper_args__ = {
        'polymorphic_identity': 1,  # 当type=1时的表记录为PC
    }


# 网络打印机
class Printer(Asset):
    __tablename__ = 'printer'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20), comment='IP地址')  # IP地址
    mac = db.Column(db.String(50), comment='Mac地址')  # Mac地址
    printer_type = db.Column(
        db.Integer, comment='打印机类型')  # 打印机类型，取值1：激光打印机，2：喷墨打印机，3：其他打印机
    func_type = db.Column(db.Integer,
                          comment='打印机功能')  # 打印机功能，取值1：打印，2：打印+扫描，3：打印+扫描+传真
    paper = db.Column(db.String(20), comment='支持纸张类型')  # 支持纸张类型
    __mapper_args__ = {
        'polymorphic_identity': 2,  # 当type=2时的表记录为网络打印机
    }


# 服务器
class Server(Asset):
    __tablename__ = 'server'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    ip = db.Column(db.String(20), comment='IP地址')  # IP地址
    mac = db.Column(db.String(50), comment='Mac地址')  # Mac地址
    server_type = db.Column(db.Integer, comment='服务器类型')  # 服务器类型，取值1：实体机，2：虚拟机
    cpu = db.Column(db.String(20), comment='CPU型号')  # CPU型号
    men = db.Column(db.String(20), comment='内存容量')  # 内存容量
    disk = db.Column(db.String(20), comment='硬盘容量')  # 硬盘容量
    nic = db.Column(db.String(50), comment='网络接口')  # 网络接口
    os = db.Column(db.String(50), comment='操作系统版本')  # 操作系统版本
    database = db.Column(db.String(50), comment='数据库版本')  # 数据库版本
    middleware = db.Column(db.String(50), comment='中间件版本')  # 中间件版本
    usage = db.Column(db.Text, comment='用途')  # 用途
    online_date = db.Column(db.DateTime, comment='上线日期')  # 上线日期
    __mapper_args__ = {
        'polymorphic_identity': 3,  # 当type=3时的表记录为服务器
    }


# 网络设备
class NetDevice(Asset):
    __tablename__ = 'netdevice'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    management_ip = db.Column(db.String(20), comment='管理IP地址')  # 管理IP地址
    net_device_type = db.Column(
        db.Integer, comment='网络设备类型')  # 网络设备类型，取值1：二层交换机，2：三层交换机，3：核心交换机，4：路由器
    port_num = db.Column(db.Integer, comment='端口个数')  # 端口个数
    device_detail = db.Column(db.Text, comment='设备详情')  # 设备详情

    __mapper_args__ = {
        'polymorphic_identity': 4,  # 当type=3时的表记录为网络设备
    }


# 安全设备
class SecDevice(Asset):
    __tablename__ = 'secdevice'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    management_ip = db.Column(db.String(20), comment='管理IP地址')  # 管理IP地址
    sec_device_type = db.Column(db.Integer,
                                comment='打印机类型')  # 服务器类型，取值1：实体机，2：虚拟机
    usage = db.Column(db.Text, comment='用途')  # 用途
    device_detail = db.Column(db.Text, comment='设备详情')  # 设备详情

    __mapper_args__ = {
        'polymorphic_identity': 5,  # 当type=3时的表记录为安全设备
    }

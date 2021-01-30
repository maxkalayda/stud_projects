from flask_login import UserMixin
from sv_packages import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False, unique=True)
    passwd = db.Column(db.String(255), nullable=False)


class MainDBForwarder(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'T_storage_units'
    order_num = db.Column('order_num', db.Integer, primary_key=True)
    sup_code = db.Column('sup_code', db.Integer, nullable=False)
    balance_acc = db.Column('balance_acc', db.Integer, nullable=False)
    code_of_dir = db.Column('code_of_dir_of_documents', db.Integer, nullable=False)
    product_name = db.Column('product_name', db.String(255), nullable=False)
    num_of_document = db.Column('num_of_document', db.Integer, nullable=False)
    material_code = db.Column('material_code', db.Integer, nullable=False)
    material_acc = db.Column('material_acc', db.Integer, nullable=False)
    measure_unit_code = db.Column('measure_unit_code', db.Integer, nullable=False)
    amount_of_material = db.Column('amount_of_material', db.Integer, nullable=False)
    unit_price = db.Column('unit_price', db.Integer, nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

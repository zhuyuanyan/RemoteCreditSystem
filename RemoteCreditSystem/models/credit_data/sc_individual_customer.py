#coding:utf-8
__author__ = 'Johnny'

from RemoteCreditSystem import db

# 个人客户基本信息表
class SC_Individual_Customer(db.Model):
    __tablename__ = 'sc_individual_customer'
    id=db.Column(db.Integer, primary_key=True)
    manager=db.Column(db.Integer)
    customer_no=db.Column(db.String(16))
    customer_type=db.Column(db.String(16))
    customer_name=db.Column(db.String(128))
    birthday=db.Column(db.Date)
    sex=db.Column(db.String(1))
    credentials_type=db.Column(db.Integer)
    credentials_no=db.Column(db.String(32))
    degree=db.Column(db.String(32))
    education=db.Column(db.String(32))
    marriage=db.Column(db.String(1))
    telephone=db.Column(db.String(16))
    mobile=db.Column(db.String(16))
    residence=db.Column(db.String(128))
    residence_address=db.Column(db.String(128))
    home_address=db.Column(db.String(128))
    zip_code=db.Column(db.String(16))
    families=db.Column(db.String(2))
    living_conditions=db.Column(db.String(32))
    is_otherjob=db.Column(db.String(1))
    profession=db.Column(db.String(64))
    duty=db.Column(db.String(64))
    title=db.Column(db.String(64))
    name_1=db.Column(db.String(64))
    relationship_1=db.Column(db.String(64))
    phone_1=db.Column(db.String(64))
    name_2=db.Column(db.String(64))
    relationship_2=db.Column(db.String(64))
    phone_2=db.Column(db.String(64))
    name_3=db.Column(db.String(64))
    relationship_3=db.Column(db.String(64))
    phone_3=db.Column(db.String(64))
    name_4=db.Column(db.String(64))
    relationship_4=db.Column(db.String(64))
    phone_4=db.Column(db.String(64))
    spouse_name=db.Column(db.String(32))
    spouse_company=db.Column(db.String(64))
    spouse_credentials_type=db.Column(db.Integer, db.ForeignKey('sc_credentials_type.id'))
    spouse_credentials_no=db.Column(db.String(32))
    spouse_phone=db.Column(db.String(32))
    spouse_mobile=db.Column(db.String(32))
    is_active = db.Column(db.String(1))
    is_have_export = db.Column(db.String(1))
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)


    def __init__(self, manager,customer_no,customer_name,birthday,sex,credentials_type,credentials_no,
                degree,education,marriage,telephone,mobile,residence,residence_address,home_address,
                zip_code,families,living_conditions,is_otherjob,profession,duty,title,
                name_1,relationship_1,phone_1,name_2,relationship_2,phone_2,
                name_3,relationship_3,phone_3,name_4,relationship_4,phone_4,
                spouse_name,spouse_company,spouse_credentials_type,spouse_credentials_no,spouse_phone,spouse_mobile):
        self.manager=manager
        self.customer_no=customer_no
        self.customer_type='Individual'
        self.customer_name=customer_name
        self.birthday=birthday
        self.sex=sex
        self.credentials_type=credentials_type
        self.credentials_no=credentials_no
        self.degree=degree
        self.education=education
        self.marriage=marriage
        self.telephone=telephone
        self.mobile=mobile
        self.residence=residence
        self.residence_address=residence_address
        self.home_address=home_address
        self.zip_code=zip_code
        self.families=families
        self.living_conditions=living_conditions
        self.is_otherjob=is_otherjob
        self.profession=profession
        self.duty=duty
        self.title=title
        self.name_1=name_1
        self.relationship_1=relationship_1
        self.phone_1=phone_1
        self.name_2=name_2
        self.relationship_2=relationship_2
        self.phone_2=phone_2
        self.name_3=name_3
        self.relationship_3=relationship_3
        self.phone_3=phone_3
        self.name_4=name_4
        self.relationship_4=relationship_4
        self.phone_4=phone_4
        self.spouse_name=spouse_name
        self.spouse_company=spouse_company
        self.spouse_credentials_type=spouse_credentials_type
        self.spouse_credentials_no=spouse_credentials_no
        self.spouse_phone=spouse_phone
        self.spouse_mobile=spouse_mobile
        self.is_active = '1'
        self.is_have_export = '0'
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)
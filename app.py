
import time
from datetime import datetime
from flask import Flask, render_template, url_for, request, json, jsonify
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CHAR, Column, DateTime, Float, String, engine, null, create_engine ,and_
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from static import models
import pymysql
# coding: utf-8
from sqlalchemy.orm import sessionmaker, query
from sqlalchemy.sql.elements import and_
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = "smtp.qq.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "710977702@qq.com"
# 这里的密码是你在邮箱中的授权码
app.config['MAIL_PASSWORD'] = "ektbjesoxjimbcec"
# 显示发送人的名字
app.config['MAIL_DEFAULT_SENDER'] = '710977702<710977702@qq.com>'

mail = Mail(app)
# 设置编码

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:we19990127@127.0.0.1:3306/toys"
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLCHEMY_ECHO'] = True

db = SQLAlchemy(app)




class Admin(db.Model):
    __tablename__ = 'admin'

    aid = Column(INTEGER(11), primary_key=True)
    aname = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    apassword = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    turnover = Column(Float(asdecimal=True), comment='????')

    def __repr__(self):
        tpl = "Admin(aid={}, aname={}, apassword={}, turnover={})"
        return tpl.format(self.aid, self.aname,
                          self.apassword, self.turnover)
    def getname(self, ):
        return self.aname


class Adminuser(db.Model):
    __tablename__ = 'adminuser'

    uid = Column(INTEGER(11), primary_key=True)
    uname = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    upassword = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    turnover = Column(Float(asdecimal=True), comment='???')


class Member(db.Model):
    __tablename__ = 'member'

    mid = Column(INTEGER(11), primary_key=True)
    mname = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    maddr = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    mtel = Column(CHAR(11, 'utf8_unicode_ci'), nullable=False)
    mdate = Column(DateTime, nullable=False)
    balance = Column(Float(asdecimal=True), nullable=False, comment='????')
    money = Column(Float(asdecimal=True), comment='??')


class Rent(db.Model):
    __tablename__ = 'rent'

    rid = Column(INTEGER(11), primary_key=True)
    mid = Column(INTEGER(11), nullable=False)
    tid = Column(INTEGER(11), nullable=False)
    outdate = Column(DateTime)
    state = Column(INTEGER(11), nullable=False)
    redate = Column(DateTime)
    toredate = Column(DateTime)


class Toy(db.Model):
    __tablename__ = 'toy'

    tid = Column(INTEGER(11), primary_key=True)
    purchase_date = Column(DateTime, nullable=False)
    shop_price = Column(Float(asdecimal=True), nullable=False)
    num = Column(INTEGER(11), nullable=False)
    is_rent = Column(INTEGER(11), nullable=False)
    state = Column(INTEGER(11), nullable=False)


engine = create_engine('mysql+pymysql://root:we19990127@127.0.0.1:3306/toys?charset=utf8')
Session = sessionmaker(bind=engine)

session = Session()


def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}


db.Model.to_dict = to_dict

@app.route('/mail/<dz>/<zt>/<nr>')
def mails(dz,zt,nr):
    dzs=str(dz)
    zts=str(zt)
    nrs=str(nr)
    message = Message(zts, [dzs,'710977702@qq.com'])
    message.body = nrs
    #message.html = '<h1>我也是内容<h1/>'
    mail.send(message)
    return '邮件发送中......'

@app.route('/user', methods=['GET', 'POST'])
def form_data():
    return jsonify({'username': '1', 'userpassword': '2'})


@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return jsonify({'username': name, 'userpassword': name * 2})


@app.route('/login/<username>/<password>', methods=['GET', 'POST'])
def login(username, password):
    admin = session.query(Admin).filter(Admin.aname==username,Admin.apassword==password).first()
    adminuser= session.query(Adminuser).filter(Adminuser.uname==username,Adminuser.upassword==password).first()
    if (admin!= None):
        return jsonify({'pass': '1'})
    elif (adminuser != None):
        return jsonify({'pass': '2'})
    else:
        return jsonify({'pass': '3'})


@app.route('/Admin/StockInput/<wjmc>/<wjjg>')
def StockInput(wjmc,wjjg):
    #state 1在库 0借出 2损坏
    toy=Toy(tid=wjmc,purchase_date=time.localtime(time.time()),shop_price=wjjg,is_rent=0,num=1,state=1)
    session.add(toy)
    session.commit()
    return jsonify({'pass': '1'})

@app.route('/Admin/AdminuserAdd/<yhm>/<yhmm>')
def AdminuserAdd(yhm,yhmm):
    adminuser=Adminuser(uname=yhm,upassword=yhmm)
    session.add(adminuser)
    session.commit()
    return jsonify({'pass': '1'})

@app.route('/Admin/PlayRental/<bh>/<gk>/<ts>')
def PlayRental(bh,gk,ts):
    toy = session.query(Toy).filter(Toy.tid == bh).first()
    # 无此玩具3
    if toy==None:
        return jsonify({'pass': '3'})
    # 玩具已被出租
    elif toy.is_rent==1:
        return jsonify({'pass': '2'})
    # 玩具被损坏
    elif toy.state==3:
        return jsonify({'pass': '2'})
    else:
        rent=Rent(mid=int(gk),tid=int(bh),state=0,outdate=time.localtime(time.time()),toredate=time.localtime(time.time()+60*60*24*int(ts)))
        toy.is_rent=1
        session.add(rent,toy)
        session.commit()
        return jsonify({'pass': '1'})

@app.route('/Admin/ToyReturn/<bh>/<gk>')
def ToyReturn(bh,gk):
    toy = session.query(Toy).filter(Toy.tid == bh).first()
    # 无此玩具2
    if toy==None:
        return jsonify({'pass': '2','age':'0'})
    # 该玩具在库中
    elif toy.is_rent==0:
        return jsonify({'pass': '3','age':'0'})
    else:
        gk = session.query(Member).filter(Member.mid == gk).first()
        # 无此顾客4
        if gk==None:
            return jsonify({'pass': '4', 'age': '0'})
        else:
            rent=session.query(Rent).filter(Rent.tid == bh).order_by(Rent.tid.desc()).all()
            rent1=rent[len(rent)-1]
            #出租时间
            a=rent1.outdate
            #应还时间
            b=rent1.toredate
            c=time.localtime(time.time())
            d=time.strftime("%Y-%m-%d-%H", c)
            #现在时间
            c=datetime.strptime(d, "%Y-%m-%d-%H")
            #a.__sub__(b).days
            if(c.__lt__(b)):
                ans=str(int(b.__sub__(a).days*toy.shop_price))
                toy.is_rent=0;
                rent1.redate=rent1.toredate
                session.add(rent1, toy)
                session.commit()
                return jsonify({'pass': '1', 'age': ans})
            else:
                ans = str(int(b.__sub__(a).days*toy.shop_price+c.__sub__(b)*(toy.shop_price+1)))
                toy.is_rent = 0;
                rent1.redate=time.localtime(time.time());
                session.add(rent1, toy)
                session.commit()
                return jsonify({'pass': '1', 'age': ans})

@app.route('/Admin/MemberAdd/<xm>/<dz>/<dh>/<yj>')
def MemberAdd(xm,dz,dh,yj):
    member=Member(mname=xm,maddr=dz,mtel=dh,mdate=time.localtime(time.time()),balance=0,money=yj)
    session.add(member)
    session.commit()
    member = session.query(Member).filter(Member.mtel == dh).first()
    a=member.mid
    return jsonify({'pass': '1', 'age': a})

@app.route('/Admin/MemberQuery/<bh>')
def MemberQuery(bh):
    member=session.query(Member).filter(Member.mid == bh).first()
    if member!=None:
        return jsonify({'xm': str(member.mname), 'dz': str(member.maddr),'dh':str(member.mtel),'sj':str(member.mdate),'yj':str(int(member.money))})
    else:
        return jsonify({'xm': 0, 'dz': 0,'dh': 0,'yj': 0})

@app.route('/Admin/MemberDel/<bh>')
def MemberDel(bh):
    member=session.query(Member).filter(Member.mid == bh).first()
    if member==None:
        return jsonify({'pass': '-1'})
    else:
        a=str(int(member.money))
        session.delete(member)
        session.commit()
        return jsonify({'pass': a})


# 测试入口
@app.route('/test')
def hello_world():
    return 'Hello World!'


@app.route('/')
def hello_world1():
    return 'Hello World!'


if __name__ == '__main__':
    print("ok")
    app.run()

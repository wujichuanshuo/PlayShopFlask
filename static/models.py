# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Float, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata



class Admin(Base):
    __tablename__ = 'admin'

    aid = Column(INTEGER(11), primary_key=True)
    aname = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    apassword = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    turnover = Column(Float(asdecimal=True), comment='????')


class Adminuser(Base):
    __tablename__ = 'adminuser'

    uid = Column(INTEGER(11), primary_key=True)
    uname = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    upassword = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    turnover = Column(Float(asdecimal=True), comment='???')


class Member(Base):
    __tablename__ = 'member'

    mid = Column(INTEGER(11), primary_key=True)
    mname = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    maddr = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    mtel = Column(CHAR(11, 'utf8_unicode_ci'), nullable=False)
    mdate = Column(DateTime, nullable=False)
    balance = Column(Float(asdecimal=True), nullable=False, comment='????')
    money = Column(Float(asdecimal=True), comment='??')


class Rent(Base):
    __tablename__ = 'rent'

    rid = Column(INTEGER(11), primary_key=True)
    mid = Column(INTEGER(11), nullable=False)
    tid = Column(INTEGER(11), nullable=False)
    outdate = Column(DateTime)
    state = Column(INTEGER(11), nullable=False)
    redate = Column(DateTime)
    toredate = Column(DateTime)


class Toy(Base):
    __tablename__ = 'toy'

    tid = Column(INTEGER(11), primary_key=True)
    purchase_date = Column(DateTime, nullable=False)
    shop_price = Column(Float(asdecimal=True), nullable=False)
    num = Column(INTEGER(11), nullable=False)
    is_rent = Column(INTEGER(11), nullable=False)
    state = Column(INTEGER(11), nullable=False)

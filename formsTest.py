import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app
from model import db, Transaction, Customer, Account
from datetime import datetime
from forms import Withdrawform, Depositform, Withdrawform
from datetime import datetime

from sqlalchemy import create_engine


class FormsTestCases(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FormsTestCases, self).__init__(*args, **kwargs)
        self.ctx = app.app_context()
        self.ctx.push()
        #self.client = app.test_client()
        app.config["SERVER_NAME"] = "Tomsbank.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        
        db.init_app(app)
        db.app = app
        db.create_all()
        
    def tearDown(self):
        #self.ctx.pop()
        pass


    def test_When_withdraw__is_greater_than_new_balance_write_errormessage(self):
        customer = Customer(GivenName="Magnus", Surname="Grahn", Streetaddress="Happystreet", City="Norrpan", Zipcode="12345", Country="SWEDEN", CountryCode="SE", 
        Birthday=datetime.now(), NationalId="19880630-0000", TelephoneCountryCode=46, Telephone="(000)123-7654", EmailAddress="magnus@hello.se")

        db.session.add(customer)
        db.session.commit()
        account = Account(AccountType="Personal", Created=datetime.now(), Balance=700, CustomerId=customer.Id)
        db.session.add(account)
        db.session.commit()
        transaction = Transaction(Type="Debit", Operation="test", Date=datetime.now(), Amount=2000, NewBalance=2500, AccountId=account.Id)
        db.session.add(transaction)
        db.session.commit()
        test_client = app.test_client()
        with test_client:
            customer = Customer.query.filter_by(Id=customer.Id).first()
            url = f'/transactions?hidden={account.Id}&transaction=withdrawal'
            response = test_client.post(url, data={"withdrawal":2600, "operation":"test", "type":"Credit"})
            s = response.data.decode("utf-8") 
            ok = 'Amount is larger then your balance!' in s
            self.assertTrue(ok)


    # def test_When_transfer__is_greater_than_new_balance_write_errormessage(self):
    #     customer = Customer(GivenName="Magnus", Surname="Grahn", Streetaddress="Happystreet", City="Norrpan", Zipcode="12345", Country="SWEDEN", CountryCode="SE", 
    #     Birthday=datetime.now(), NationalId="19880630-0000", TelephoneCountryCode=46, Telephone="(000)123-7654", EmailAddress="magnus@hello.se")

    #     db.session.add(customer)
    #     db.session.commit()
    #     account = Account(AccountType="Personal", Created=datetime.now(), Balance=700, CustomerId=customer.Id)
    #     db.session.add(account)
    #     db.session.commit()
    #     transaction = Transaction(Type="Debit", Operation="test", Date=datetime.now(), Amount=2000, NewBalance=2500, AccountId=account.Id)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     test_client = app.test_client()
    #     with test_client:
    #         customer = Customer.query.filter_by(Id=customer.Id).first()
    #         account = Account.query.filter_by(CustomerId=customer.Id).first()
    #         url = f'/transactions?hidden={account.Id}&transaction=withdrawal'
    #         response = test_client.post(url, data={"transfer":26000, "operation":"test", "type":"Credit", "to_account":account.Id})
    #         s = response.data.decode("utf-8") 
    #         ok = 'too large' in s
    #         self.assertTrue(ok)

    # def test_When_withdraw__is_less_than_zero_write_errormessage(self):
    #     customer = Customer(GivenName="Magnus", Surname="Grahn", Streetaddress="Happystreet", City="Norrpan", Zipcode="12345", Country="SWEDEN", CountryCode="SE", 
    #     Birthday=datetime.now(), NationalId="19880630-0000", TelephoneCountryCode=46, Telephone="(000)123-7654", EmailAddress="magnus@hello.se")

    #     db.session.add(customer)
    #     db.session.commit()
    #     account = Account(AccountType="Personal", Created=datetime.now(), Balance=700, CustomerId=customer.Id)
    #     db.session.add(account)
    #     db.session.commit()
    #     transaction = Transaction(Type="Debit", Operation="test", Date=datetime.now(), Amount=2000, NewBalance=2500, AccountId=account.Id)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     test_client = app.test_client()
    #     with test_client:
    #         customer = Customer.query.filter_by(Id=customer.Id).first()
    #         url = f'/transactions?hidden={account.Id}&transaction=withdrawal'
    #         response = test_client.post(url, data={"withdrawal":-26, "operation":"test", "type":"Credit"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Value has to be larger then zero' in s
    #         self.assertTrue(ok)

    # def test_When_deposit__is_less_than_zero_write_errormessage(self):
    #     customer = Customer(GivenName="Magnus", Surname="Grahn", Streetaddress="Happystreet", City="Norrpan", Zipcode="12345", Country="SWEDEN", CountryCode="SE", 
    #     Birthday=datetime.now(), NationalId="19880630-0000", TelephoneCountryCode=46, Telephone="(000)123-7654", EmailAddress="magnus@hello.se")

    #     db.session.add(customer)
    #     db.session.commit()
    #     account = Account(AccountType="Personal", Created=datetime.now(), Balance=700, CustomerId=customer.Id)
    #     db.session.add(account)
    #     db.session.commit()
    #     transaction = Transaction(Type="Debit", Operation="test", Date=datetime.now(), Amount=2000, NewBalance=2500, AccountId=account.Id)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     test_client = app.test_client()
    #     with test_client:
    #         customer = Customer.query.filter_by(Id=customer.Id).first()
    #         url = f'/transactions?hidden={account.Id}&transaction=deposit'
    #         response = test_client.post(url, data={"deposit":-26, "operation":"test", "type":"Credit"})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Value has to be larger then zero!' in s
    #         self.assertTrue(ok)

    # def test_When_transfer__is_less_than_zero_write_errormessage(self):
    #     customer = Customer(GivenName="Magnus", Surname="Grahn", Streetaddress="Happystreet", City="Norrpan", Zipcode="12345", Country="SWEDEN", CountryCode="SE", 
    #     Birthday=datetime.now(), NationalId="19880630-0000", TelephoneCountryCode=46, Telephone="(000)123-7654", EmailAddress="magnus@hello.se")

    #     db.session.add(customer)
    #     db.session.commit()
    #     account = Account(AccountType="Personal", Created=datetime.now(), Balance=700, CustomerId=customer.Id)
    #     db.session.add(account)
    #     db.session.commit()
    #     transaction = Transaction(Type="Debit", Operation="test", Date=datetime.now(), Amount=2000, NewBalance=2500, AccountId=account.Id)
    #     db.session.add(transaction)
    #     db.session.commit()
    #     test_client = app.test_client()
    #     with test_client:
    #         customer = Customer.query.filter_by(Id=customer.Id).first()
    #         account = Account.query.filter_by(CustomerId=customer.Id).first()
    #         url = f'/transactions?hidden={account.Id}&transaction=transfer'
    #         response = test_client.post(url, data={"transfer":-26, "operation":"test", "type":"Credit", "to_account":account.Id})
    #         s = response.data.decode("utf-8") 
    #         ok = 'Value has to be larger then zero!' in s
    #         self.assertTrue(ok)

if __name__ =="__main__":
    unittest.main()
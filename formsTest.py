import unittest

from flask import Flask, render_template, request, url_for, redirect
from app import app, withdraw, User, Role
from model import db, Transaction, Customer, Account
from datetime import datetime
from forms import Withdrawform, Depositform, Withdrawform
from datetime import datetime, date
from flask_security import SQLAlchemyUserDatastore, hash_password, Security

from sqlalchemy import create_engine

def set_current_user(app, ds, email):

    def token_cb(request):
        if request.headers.get("Authentication-Token") == "token":
            return ds.find_user(email=email)
        return app.security.login_manager.anonymous_user()

    app.security.login_manager.request_loader(token_cb)


init = False


class FormsTestCases(unittest.TestCase):
    # def __init__(self, *args, **kwargs):
    #     super(FormsTestCases, self).__init__(*args, **kwargs)
    def tearDown(self):
        self.ctx.pop()
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        #self.client = app.test_client()
        app.config["SERVER_NAME"] = "stefan.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SECURITY_FRESHNESS_GRACE_PERIOD'] = 123454
        global init
        if not init:
            db.init_app(app)
            db.create_all()
            init = True
            user_datastore = SQLAlchemyUserDatastore(db, User, Role)
            app.security = Security(app, user_datastore,register_blueprint=False)
            app.security.init_app(app, user_datastore,register_blueprint=False)
            app.security.datastore.db.create_all()


    def test_When_deposit__negativeammount__write_errormessage(self):
        # transaction = Transaction()
        customer = Customer()
        customer.GivenName = "Stefan"
        customer.Surname = "Holmberg"
        customer.Streetaddress = "Karlavägen12"
        customer.City = "Stockholm"
        customer.Zipcode = 73335
        customer.Country = "Sweden"
        customer.CountryCode = "+46"
        customer.Birthday = date(1990, 2, 28)
        customer.NationalId ='1234567890'
        customer.TelephoneCountryCode=1
        customer.Telephone='555-555-5555'
        customer.EmailAddress='unittest@me.com'
        db.session.add(customer)
        db.session.commit()

        account = Account()
        account.AccountType = 'checking'
        account.Created = datetime(2022, 2, 28, 12, 30, 0)
        account.Balance = 100
        account.CustomerId = customer.Id
        db.session.add(account)
        db.session.commit()

        test_client = app.test_client()
        # user = User.query.get(1)
        with test_client:
            url = '/deposit/' + str(account.Id)
            response = test_client.post(url, data={ "Amount":-200},headers={app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"]: "token"})
            s = response.data.decode("utf-8") 
            # large = ["too large"]
            ok = 'Number must be between' in s
            self.assertTrue(ok)

    
    

   


    def test_When_withdraw__is_greater_than_new_balance_write_errormessage(self):
        # transaction = Transaction()
        customer = Customer()
        customer.GivenName = "Stefan"
        customer.Surname = "Holmberg"
        customer.Streetaddress = "Karlavägen12"
        customer.City = "Stockholm"
        customer.Zipcode = 73335
        customer.Country = "Sweden"
        customer.CountryCode = "+46"
        customer.Birthday = date(1990, 2, 28)
        customer.NationalId ='1234567890'
        customer.TelephoneCountryCode=1
        customer.Telephone='555-555-5555'
        customer.EmailAddress='unittest@me.com'
        db.session.add(customer)
        db.session.commit()

        account = Account()
        account.AccountType = 'checking'
        account.Created = datetime(2022, 2, 28, 12, 30, 0)
        account.Balance = 100
        account.CustomerId = customer.Id
        db.session.add(account)
        db.session.commit()
        
    
        
        
         
    
        test_client = app.test_client()
        # user = User.query.get(1)
        with test_client:
            url = '/withdraw/' + str(account.Id)
            response = test_client.post(url, data={ "Amount":200},headers={app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"]: "token"})
            s = response.data.decode("utf-8") 
            # large = ["too large"]
            ok = 'too large' in s
            self.assertTrue(ok)



    def test_When_transfer__to__none__existingaccount_errormessage(self):
        # transaction = Transaction()
        customer = Customer()
        customer.GivenName = "Stefan"
        customer.Surname = "Holmberg"
        customer.Streetaddress = "Karlavägen12"
        customer.City = "Stockholm"
        customer.Zipcode = 73335
        customer.Country = "Sweden"
        customer.CountryCode = "+46"
        customer.Birthday = date(1990, 2, 28)
        customer.NationalId ='1234567890'
        customer.TelephoneCountryCode=1
        customer.Telephone='555-555-5555'
        customer.EmailAddress='unittest@me.com'
        db.session.add(customer)
        db.session.commit()

        account = Account()
        account.AccountType = 'checking'
        account.Created = datetime(2022, 2, 28, 12, 30, 0)
        account.Balance = 100
        account.CustomerId = customer.Id
        db.session.add(account)
        db.session.commit()
        
    
        
        
         
    
        test_client = app.test_client()
        # user = User.query.get(1)
        with test_client:
            url = '/transfer/' + str(account.Id)
            response = test_client.post(url, data={ "Id":166666, "Amount":100},headers={app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"]: "token"})
            s = response.data.decode("utf-8") 
            ok = 'Does not exist' in s
            self.assertTrue(ok)

       

if __name__ =="__main__":
    unittest.main()
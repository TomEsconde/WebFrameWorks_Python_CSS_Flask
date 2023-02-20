from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from model import db, seedData, Customer
from forms import NewCustomerForm

from flask_security import roles_accepted, auth_required, logout_user
from model import Customer, Account, Transaction
from model import db, seedData
from forms import NewCustomerForm, Depositform, Withdrawform, Transferform
from datetime import datetime
import os

 
# app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Kalleballe87@localhost/bank'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"
# app.config['SECRET_KEY'] = os.urandom(32)
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 
 

@app.route("/")
def startpage():
    # trendingCategories = Customer.query.all()
    account = Account.query.filter(Account.Balance)
    balance = 0
    allAccount = Account.query.count()
    customers = Customer.query.count()
    for x in account:
        balance += x.Balance
    return render_template("index.html", balance=balance, allAccount = allAccount, customers = customers, redirect="/")

@app.route("/customer/<id>")
@auth_required()
@roles_accepted("Admin", "Staff")
def customer(id):
    customer = Customer.query.filter_by(Id =id).first()
    account = Account.query.filter_by(Id = id).first()
    Saldo = 0
    for accounts in customer.Accounts:
        Saldo = Saldo + accounts.Balance
    return render_template("customer.html", customer=customer, account = account, Saldo=Saldo)



@app.route("/transfer/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def transfer(id):
    form = Transferform()
    account = Account.query.filter_by(Id = id).first()
    reciever = Account.query.filter_by(Id = form.Id.data).first()
    allAccounts = Account.query.all()
    transactionSender = Transaction()
    transactionReciever = Transaction()
    date = datetime.now()
    large = ["too large"]
    doNotExist = ["Does not exist"]
    if form.validate_on_submit():
        if account.Balance < form.Amount.data:
            form.Amount.errors = form.Amount.errors + large
        # if account not in form.Id.data:
        #     form.Id.errors = form.Id.errors + doNotExist
            
        else:
            transactionSender.Amount = form.Amount.data
            account.Balance = account.Balance - transactionSender.Amount
            transactionSender.NewBalance = account.Balance
            transactionSender.AccountId = account.Id
            transactionSender.Date = date
            transactionSender.Type = "Credit"
            transactionSender.Operation = "Transfer"

            transactionReciever.Amount = form.Amount.data
            reciever.Balance = reciever.Balance + transactionSender.Amount
            transactionReciever.NewBalance = account.Balance
            transactionReciever.AccountId = account.Id
            transactionReciever.Date = date
            transactionReciever.Type = "Debit"
            transactionReciever.Operation = "Transfer"

            db.session.add(account)
            db.session.add(reciever)
            db.session.add(transactionReciever)
            db.session.add(transactionSender)
            db.session.commit()
            return redirect("/customer/" + str(account.CustomerId) )
    return render_template("transfer.html", form=form, transactionReciever=transactionReciever, account= account, customer = customer, reciever=reciever, transactionSender=transactionSender, date=date )
   
    
   


############## Transfer slutar här



@app.route("/deposit/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def deposit(id):
    form = Depositform()
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id =id).first()
    t = Transaction()
    date = datetime.now()
    if form.validate_on_submit():
        account.Balance = account.Balance + form.Amount.data
        # db.session.commit()
        t.AccountId = account.Id
        t.Operation = "Transfer"

        t.Type = "Credit"
        t.Amount = form.Amount.data
        t.NewBalance = account.Balance
        t.Date = datetime.now()
        db.session.add(t)
        db.session.commit()
        return redirect("/customer/" + str(account.CustomerId) )
    return render_template("deposit.html", form=form, account= account, customer = customer, date=date )
    
@app.route("/withdraw/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def withdraw(id):
    form = Withdrawform()
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id =id).first()
    date = datetime.now()

    # ownValidationOk = True
    # if request.method == 'POST':
    #     form.Amount.errors = form.Amount.errors + ('too large',)
    #     ownValidationOk = False
    
    
    large = ["too large"]
    if form.validate_on_submit():
        if account.Balance < form.Amount.data:
            form.Amount.errors = form.Amount.errors + large
            
        else:
            account.Balance = account.Balance - form.Amount.data
            t = Transaction()
            t.AccountId = account.Id
            t.Operation = "Bank withdrawal"

            t.Type = "Credit"
            t.Amount = form.Amount.data
            t.NewBalance = account.Balance
            t.Date = datetime.now()
            db.session.add(t)
            db.session.commit()
            return redirect("/customer/" + str(account.CustomerId) )
    return render_template("withdraw.html", form=form, account= account, customer = customer, date=date )

@app.route("/notEnoughBalance/<id>", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin")
def notEnoughBalance(id):
    account = Account.query.filter_by(Id = id).first()
    customer = Customer.query.filter_by(Id =id).first()
    return render_template("notEnoughBalance.html", account=account, customer=customer)
    



@app.route("/transactions/<id>")
# @auth_required()
# @roles_accepted("Admin", "Staff")
def transactions(id):
    accountid = Account.query.filter_by(Id =id).first()
    transactions = Transaction.query.filter_by(AccountId=id)
    transactions = transactions.order_by(Transaction.Date.desc())
    return render_template("transactions.html", accountid = accountid, transactions=transactions)


@app.route("/admin")
@auth_required()
@roles_accepted("Admin")
def adminpage():
    return render_template("admin.html", activePage="secretPage" )


@app.route("/customers")
@auth_required()
@roles_accepted("Admin", "Staff")
def customers():
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    

    customers = Customer.query

    customers = customers.filter(
        Customer.GivenName.like('%' + q + '%') |
        Customer.City.like('%' + q + '%'))

    if sortColumn == "namn":
        if sortOrder =="asc":
            customers = customers.order_by(Customer.Surname.asc())
        else:
            customers = customers.order_by(Customer.Surname.desc())
    elif sortColumn == "city":
        if sortOrder == "asc":
            customers = customers.order_by(Customer.City.asc())
        else:
            customers = customers.order_by(Customer.City.desc())

    paginationObject = customers.paginate(page=page, per_page=50, error_out=False)

    return render_template("customers.html", 
    customers=paginationObject.items,
    pages=paginationObject.pages,
    sortOrder=sortOrder,
    sortColumn=sortColumn,
    has_next=paginationObject.has_next,
    has_prev=paginationObject.has_prev,
    page=page, 
    q=q)
    # return render_template("category.html", products=products)

@app.route("/category/<id>")
def category(id):
    return "hej2"
    # products = Product.query.all()
    # return render_template("category.html", products=products)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/newcustomer", methods=['GET', 'POST'])
@auth_required()
@roles_accepted("Admin", "Staff")
def newcustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        #spara i databas
        customer = Customer()
        customer.GivenName = form.GivenName.data
        customer.Surname = form.Surname.data
        customer.Streetaddress = form.Streetaddress.data
        customer.City = form.City.data
        customer.Zipcode = form.Zipcode.data
        customer.Country = form.Country.data
        customer.CountryCode = form.CountryCode.data
        customer.Birthday = form.Birthday.data
        customer.NationalId = form.NationalId.data
        customer.TelephoneCountryCode = form.TelephoneCountryCode.data
        customer.Telephone = form.Telephone.data
        customer.EmailAddress = form.EmailAddress.data

        db.session.add(customer)
        db.session.commit()
        return redirect("/customers" )
    return render_template("newcustomer.html", formen=form )


if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        seedData(app, db)
        app.run(debug = True)


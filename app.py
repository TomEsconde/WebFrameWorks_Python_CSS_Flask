from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from model import db, seedData, Customer


 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Kalleballe87@localhost/bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

@app.route("/")
def startpage():
    return "hej"
    #trendingCategories = Category.query.all()
    #return render_template("index.html", trendingCategories=trendingCategories)

@app.route("/category/<id>")
def customers():
    customers = Customer.query.all()
    return render_template("customers.html", customers=customers)
    # return render_template("category.html", products=products)

@app.route("/category/<id>")
def category(id):
    return "hej2"
    # products = Product.query.all()
    # return render_template("category.html", products=products)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
    seedData(db)
    app.run()


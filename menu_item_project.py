from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession();

#crate a restaurant
myFirstRestaurant = Restaurant(name="Piza Palace2")
session.add(myFirstRestaurant)
session.commit()
#get first restaurant
firstResult = session.query(Restaurant).first()
#get restaurants
items = session.query(MenuItem).all()
for item in items:
    print item.name
#get filtred results
veggyBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggyBurger in veggyBurgers:
    print veggyBurger.id
    print veggyBurger.price
    print veggyBurger.restaurant.name
    print "\n"
#Update One item
UrbanVeggyBurgers = session.query(MenuItem).filter_by(id = 9).one()
UrbanVeggyBurgers.price = '$2.99'
session.add(UrbanVeggyBurgers)
session.commit()
#Update Multiple item
for veggyBurger in veggyBurgers:
    if veggyBurger.price != '$2.99':
        veggyBurger.price='$2.99'
        session.add(veggyBurger)
        session.commit()
#delete data
spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
print spinach.restaurant.name
session.delete(spinach)
session.commit()
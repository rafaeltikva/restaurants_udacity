__author__ = 'rafaeltikva'

from database_setup import  Restaurant, MenuItem

from database import create_session

session = create_session()

# filter_by returns a collection of found objects
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

# iterate over each found object and retrieve information of each veggie burger

for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

# return only one result, i.e LIMIT 1
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()

print UrbanVeggieBurger.price

# update UrbanVeggieBurger's price
UrbanVeggieBurger.price =  '$2.99'

# add to staging/transaction
session.add(UrbanVeggieBurger)

# commit changes to database
session.commit()

# Update all other vegie burgers
for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()



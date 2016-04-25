__author__ = 'rafaeltikva'

import json

from database_setup import Restaurant, MenuItem

from database import create_session

session = create_session()

# verify that the changes were made on the database.

restaurants = session.query(Restaurant).all()

for restaurant in restaurants:
    #print restaurant.to_dict()
    print restaurant.__dict__
    #restaurant.__dict__.update({'name': 'rafitest'})
    #print 'after update()\n'
    #print restaurant.name
    #print 'creating new empty Restaurant object...'
    #new_restaurant = Restaurant()
    #print 'new restaurant created: \n'
    #print new_restaurant.__dict__
    #print 'replicating existing restaurant to new_restaurant...'
    #new_restaurant.__dict__.update(restaurant.__dict__)
    #print 'new restaurant after copy: \n'
    #print new_restaurant.__dict__
    #print restaurant.__dict__['_sa_instance_state'].__dict__


# get the first result that corresponds to the first found row on the database

firstResult = session.query(Restaurant).first()

# These single row references allow us to extract column entries as method names

firstResult.name

# verify that the changes were made on the database.
# to get all the rows' information, we can use a for loop to iterate over the results

items = session.query(MenuItem).all()

# print items
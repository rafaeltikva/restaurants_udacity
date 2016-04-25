__author__ = 'rafaeltikva'

from database_setup import create_session, Restaurant, MenuItem

session = create_session()

myFirstRestaurant = Restaurant(name = 'Pizza Pallace')

# add to the staging zone
session.add(myFirstRestaurant)

# store the changes to the database
session.commit()

print myFirstRestaurant.name + ' saved to database'

# Add a menu item to the 'menu_item' table, including the relationship with the Restaurant we want

cheesePizza = MenuItem(name = 'Cheese Pizza', description = 'Made with all pure ingedients and fresh mozzarella', course = 'Entree', price = '$8.99', restaurant = myFirstRestaurant)

# add to the staging zone
session.add(cheesePizza)

# store changes to database
session.commit()

print cheesePizza.name + ' saved to database'


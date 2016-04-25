__author__ = 'rafaeltikva'

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    """ Representation of database table as a python class
    """

    # Representation of our table inside the database
    __tablename__ = 'restaurant'

    # Mapper code - mapping SQLAlchemy objects to database columns

    # columnName = Column(attributes)
    # Maps the 'name' column python object to the 'name' column in our database
    # The column has a string with a max of 80 characters, and is not nullable, i.e it's required for the row to be created
    name = Column(
        String(80), nullable=False
    )

    # Maps the 'id' column python object to the 'id' column in our database
    # The column is an int and it's the column's primary key
    id = Column(
        Integer, primary_key=True
    )

    def to_dict(self):
        return dict(id=self.id, name=self.name)


class MenuItem(Base):
    # Representation of our table inside the database
    __tablename__ = 'menu_item'

    # Mapper code - mapping SQLAlchemy objects to database columns

    # Maps the 'name' column python object to the 'name' column in our database
    # The column has a string with a max of 80 characters, and is not nullable, i.e it's required for the row to be created
    name = Column(String(80), nullable=False)

    # Maps the 'id' column python object to the 'id' column in our database
    # The column is an int and it's the column's primary key
    id = Column(Integer, primary_key=True)

    # Maps the 'course' column python object to the 'course' column in our database
    # The column has a string with a max of 250 character
    course = Column(String(250))

    # Maps the 'description' column python object to the 'description' column in our database
    # The column has a string with a max of 250 character
    description = Column(String(250))

    # Maps the 'price' column python object to the 'price' column in our database
    # The column has a string with a max of 8 character
    price = Column(String(8))

    # Create a foreign key relationship with the 'id' column of the 'restaurant' table
    # It basically get's the id by looking at the restaurant table's id column
    restaurant_id = Column(
        Integer, ForeignKey('restaurant.id')
    )

    # The relationship with our Restaurant class
    restaurant = relationship(Restaurant)

    def to_dict(self):
        return dict(id=self.id, course=self.course, description=self.description, price=self.price,
                    restaurant_id=self.restaurant_id)


####### Insert at the end of file #######

engine = create_engine(
    'sqlite:///restaurantmenu.db', echo = True
)

DBSession = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

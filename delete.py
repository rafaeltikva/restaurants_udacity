from database_setup import Restaurant, MenuItem
from sqlalchemy.orm.exc import NoResultFound

from database import create_session

session = create_session()

string_to_search = 'Spinach Ice Cream'

try:
    spinach = session.query(MenuItem).filter_by(name = string_to_search).one()
    print spinach.name
    # Delete object
    session.delete(spinach)

    # Commit changes to DB
    session.commit()
except NoResultFound:
    print string_to_search+ ' was not found'

# No results throws a NoResultFound exception
try:
    spinach = session.query(MenuItem).filter_by(name = string_to_search).one()
except NoResultFound:
    print string_to_search + ' was not found'

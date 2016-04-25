__author__ = 'rafaeltikva'

from database_setup import DBSession

from sqlalchemy.orm.exc import NoResultFound

from lib.helpers import from_json

import database_setup


def create_session():
    # create instance of DBSession
    return DBSession()


def query(object_type, filter=''):
    # initialize query_results
    query_results = ''
    try:

        object_type = getattr(database_setup, object_type)

    except AttributeError as e:
        print e
        return e

    session = create_session()

    try:
        query_results = session.query(object_type).all()

    except NoResultFound:
        query_results = 'No results were found'

    session.close()

    print query_results
    print type(query_results)
    return query_results


def create(object_type, store):

    # initalize response
    response = {}

    try:

        object_type = getattr(database_setup, object_type)

    except AttributeError as e:
        print e
        return e

    session = create_session()

    try:
        # create new object
        object_to_create = object_type(**store)

        # add object to session transaction
        session.add(object_to_create)

        print 'The object before commiting the new object:'
        print object_to_create.__dict__
        # flush session transaction
        session.commit()

        print 'The object after commiting the new object:'
        print object_to_create.__dict__

        response['message'] = 'Success'
        # return updated object
        response['object'] = store
        # return the newly created object id to the client
        response['object']['id'] = object_to_create.id

    except Exception as e:
        response['message'] = e.message

    session.close()

    return response

def delete(object_type, store):

    # initalize response
    response = {}

    # initialize query_result
    query_result = ''

    try:

        object_type = getattr(database_setup, object_type)

    except AttributeError as e:
        print e
        return e

    session = create_session()

    try:
        object_to_delete = session.query(object_type).filter_by(id = store['id']).one()
        session.delete(object_to_delete)
        session.commit()
        response['message'] = 'Success'
        # return updated object
        response['object'] = store

    except NoResultFound:
        response['message'] = "Object doesn't exist"

    session.close()

    print query_result

    return response


def update(object_type, store):

    # initialize response
    response = {}

    try:

        object_type = getattr(database_setup, object_type)

    except AttributeError as e:
        print e
        return e

    session = create_session()

    try:

        #object_to_update = session.query(object_type).filter_by(id = store['id']).one()

        # update found store
        session.query(object_type).filter_by(id = store['id']).update(store)

        # flush session transaction
        session.commit()

        response['message'] = 'Success'
        # return updated object
        response['object'] = store

    except NoResultFound:
        response['message'] = "Object doesn't exist"

    session.close()

    return response
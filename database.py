__author__ = 'rafaeltikva'

from database_setup import DBSession

from sqlalchemy.orm.exc import NoResultFound

from lib.helpers import from_json

import database_setup


def create_session():
    # create instance of DBSession
    return DBSession()


def query_all(object_type, filter=''):
    # initialize query_results

    response = ''
    try:

        object_type = getattr(database_setup, object_type) if type(object_type) == str else object_type

    except AttributeError as e:
        print e
        return e

    try:
        session = create_session()
        response = session.query(object_type).all()

    except NoResultFound:
        response = 'No results were found'

    finally:
        session.close()

    print response
    print type(response)
    return response


def query(object_type, id, to_dict = False):
    # initialize response
    response = {}

    try:

        object_type = getattr(database_setup, object_type) if type(object_type) == str else object_type

    except AttributeError as e:
        print e
        return e

    try:
        session = create_session()

        # update found store

        if to_dict:
            response['object'] = session.query(object_type).filter_by(id=id).one().to_dict()
        else:
            response = session.query(object_type).filter_by(id=id).one()

    except NoResultFound:
        response['message'] = "Object doesn't exist"

    finally:

        session.close()

    print response
    return response


def create(object_type, store):
    # initalize response
    response = {}

    try:

        object_type = getattr(database_setup, object_type) if type(object_type) == str else object_type

    except AttributeError as e:
        print e
        return e

    try:

        session = create_session()

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
    finally:
        session.close()

    return response


def update(object_type, store):
    # initialize response
    response = {}

    try:

        object_type = getattr(database_setup, object_type) if type(object_type) == str else object_type

    except AttributeError as e:
        print e
        return e

    try:

        session = create_session()

        # object_to_update = session.query(object_type).filter_by(id = store['id']).one()

        # update found store
        session.query(object_type).filter_by(id=store['id']).update(store)

        # flush session transaction
        session.commit()

        response['message'] = 'Success'
        # return updated object
        response['object'] = store

    except NoResultFound:
        response['message'] = "Object doesn't exist"

    finally:
        session.close()

    return response


def delete(object_type, store=None, id=0):
    try:
        # initialize id for later db query
        id = store.get('id') if isinstance(store, dict) else id
    except KeyError as e:
        print e.message
        raise e


    # initalize response
    response = {}

    if id > 0:

        try:

            object_type = getattr(database_setup, object_type) if type(object_type) == str else object_type

        except AttributeError as e:
            print e
            return e

        try:
            session = create_session()

            object_to_delete = session.query(object_type).filter_by(id=id).one()
            session.delete(object_to_delete)
            session.commit()
            response['message'] = 'Success'
            # return updated object
            response['object'] = object_to_delete.to_dict()

        except NoResultFound:
            response['message'] = "Object doesn't exist"

        finally:
            session.close()
    else:
        response['message'] = "Object id missing"

    return response

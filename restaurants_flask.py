__author__ = 'rafaeltikva'

from flask import Flask, request, jsonify, url_for, render_template
from database_setup import Restaurant, MenuItem
import database
import api_db_mapping
import codecs
import os
import geocoder

from lib.helpers import to_json, from_json

app = Flask(__name__, static_folder='/vagrant/restaurant/webapp/', template_folder='/vagrant/restaurant/webapp/templates/')

debug_config = {
    'user_address': '79.177.95.75'
}

@app.route('/')
@app.route('/index')
def index():
    print 'the static folder: ' + app.static_folder
    print 'the static url_path: ' + app.static_url_path
    print 'template folder: ' + app.template_folder

    # get user address. assign my public NAT ip if in debug mode
    # not using request.remote_addr because of potential proxy issues (incorrect remote ip)
    user_address= request.environ['REMOTE_ADDR'] if not app.debug else debug_config.get('user_address')

    print 'the REMOTE_ADDR address is %s ' % user_address
    geolocation = geocoder.freegeoip(user_address).parse

    print 'the country is %(country)s' % geolocation
    print 'the city is %(city)s' % geolocation

    # with codecs.open(file_path, 'r', encoding='utf-8') as fp:
    #   response = fp.read()

    # no jinja2 (client side render - knockoutjs)
    #homepage = 'html/restaurants.html'
    #return app.send_static_file(homepage)

    # jinja2 render (server side render + knockoutjs for handlers)
    homepage = 'restaurants.html'
    return render_template(homepage, restaurants = database.query_all(Restaurant), **geolocation)


@app.route('/<path:path>')
def static_files(path):
    print 'the path: ' + path
    print 'the script_root: ' + request.script_root
    print 'the request.path: ' + request.path
    return app.send_static_file(path)


@app.route('/<string:object_kind>/<int:object_id>', methods=['GET'])
def render_resource(object_kind, object_id):
    if object_kind == 'restaurant':
        return render_template('resources/restaurant_single.html', restaurant = database.query(api_db_mapping.mapping[object_kind]['object_type'], object_id))
    elif object_kind =='menu_item':
        return render_template('resources/menu_item_single.html')


# API routes

@app.route('/api/<string:object_kind>/', methods=['GET'])
def get_all_menu_items(object_kind):
    # jsonify doesn't work with lists
    print 'inside get_all_menu_items'
    response = database.query_all(api_db_mapping.mapping[object_kind]['object_type'])
    return to_json(response)


@app.route('/api/<string:object_kind>/<int:menu_item_id>/', methods=['GET'])
def get_menu_item(object_kind, menu_item_id):
    # response = to_json(database.query(MenuItem, menu_item_id))
    response = database.query(api_db_mapping.mapping[object_kind]['object_type'], menu_item_id, to_dict = True)

    return jsonify(response)


@app.route('/api/<string:object_kind>', methods=['PUT'])
def new_menu_item(object_kind):
    print 'PUT received: inside new_menu_item'
    response = ''
    put_data = request.get_json()
    if put_data['action'] == 'create':
        response = database.create(api_db_mapping.mapping[object_kind]['object_type'], put_data['store'])
    else:
        response = 'Invalid action: %s' % put_data['action']

    return jsonify(response)


@app.route('/api/<string:object_kind>/<int:menu_item_id>/', methods=['POST'])
def edit_menu_item(object_kind, menu_item_id):
    response = ''

    post_data = request.get_json()

    print post_data
    print type(post_data)

    if post_data['action'] == 'update':
        response = database.update(api_db_mapping.mapping[object_kind]['object_type'], post_data['store'])

    return jsonify(response)


@app.route('/api/<string:object_kind>/<int:menu_item_id>/', methods=['POST', 'DELETE'])
def delete_menu_item(object_kind, menu_item_id):
    if request.method == 'DELETE':
        response = database.delete(api_db_mapping.mapping[object_kind]['object_type'], id=menu_item_id)
    else:
        post_data = request.get_json()
        if post_data['action'] == 'delete':
            response = database.delete(api_db_mapping.mapping[object_kind]['object_type'], post_data['store'])

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

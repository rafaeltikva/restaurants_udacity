/**
 * Created by rafaeltikva on 19/04/16.
 */

define(['jquery', 'knockout', 'restaurant/Restaurant'], function ($, ko, Restaurant) {
        return function ViewModel() {

            self = this;

            self.restaurantList = ko.observableArray();

            self.addRestaurantToList = function (restaurantParams) {
                self.restaurantList.push(new Restaurant(restaurantParams));
            };

            self.newRestaurantNameInput = ko.observable();

            self.showModal = ko.observable(false);

            self.newHandler = function () {

                var restaurant = new Restaurant({name: self.newRestaurantNameInput});
                // Update the server
                $.ajax({
                    url: 'http://localhost:5000/api/restaurant',
                    method: 'PUT',
                    contentType: 'application/json',
                    dataType: 'json',
                    data: ko.toJSON({
                        action: 'create',
                        store: ko.toJSON(restaurant.store())
                    })

                }).done(function (data) {
                    restaurant = new Restaurant(data.object);

                    self.restaurantList.push(restaurant);
                    // clear restaurant name input
                    self.newRestaurantNameInput('');
                    self.showModal(false);

                }).fail(function () {
                    console.log('POST to server failed');

                });
            };

            self.editHandler = function (restaurant) {
                restaurant.isEditable(!restaurant.isEditable());

            };

            self.updateHandler = function (restaurant) {
                if (restaurant.isEditable()) {

                    // keep old name aside in case of ajax failure
                    var oldName = restaurant.store().name();

                    restaurant.isEditable(!restaurant.isEditable);
                    // update the name
                    restaurant.store().name(restaurant.tempName());

                    // Update the model
                    $.ajax({
                        url: 'http://localhost:5000/api/restaurant',
                        method: 'POST',
                        contentType: 'application/json',
                        dataType: 'json',
                        data: ko.toJSON({
                            action: 'update',
                            store: ko.toJSON(restaurant.store())
                        })

                    }).done(function (data) {
                        console.log(data.message);

                    }).fail(function () {
                        console.log('POST to server failed');
                        // revert to old name in case of failure to update server
                        restaurant.store().name(oldName);
                        restaurant.tempName(oldName);
                    });
                }
            };

            self.deleteHandler = function (restaurant) {
                if (confirm('Are you sure you want to delete ' + restaurant.store().name() + '?')) {
                    $.ajax({
                        url: 'http://localhost:5000/api/restaurant',
                        method: 'POST',
                        contentType: 'application/json',
                        dataType: 'json',
                        data: ko.toJSON({
                            action: 'delete',
                            store: ko.toJSON(restaurant.store())
                        })

                    }).done(function (data) {
                        console.log(data.message);
                        // delete restaurant from observable array
                        self.restaurantList.remove(restaurant);
                    }).fail(function () {
                        console.log('POST to server failed');
                    });
                }

            };

        }
    }
);

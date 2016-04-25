/**
 * Created by rafaeltikva on 17/04/16.
 */

requirejs.config({
    // Load external modules and packages from ./webapp/js/lib
    baseUrl: '/lib',
    shim: {
        bootstrap: {deps: ['jquery']}
    },
    paths: {
        // load modules starting with 'restaurant' from the restaurant directory
        restaurant: '/js/restaurant',
        jquery: 'jquery/jquery.min',
        knockout: 'knockout/knockout',
        bootstrap: 'bootstrap/js/bootstrap.min'
    }
});

// Start the main app

require(['jquery', 'knockout', 'restaurant/ViewModel', 'bootstrap'], function ($, ko, ViewModel) {
    console.log('running require');

    ko.bindingHandlers.modal = {
        init: function (element, valueAccessor) {
            $(element).modal('hide');
            $(element).on('hidden.bs.modal', function(e) {
               var showModal = valueAccessor();
                showModal(false);
            });
        },
        update: function (element, valueAccessor) {
            console.log('updating modal...');
            console.log('valueAccessor is ' + ko.unwrap(valueAccessor()));
            if (ko.unwrap(valueAccessor())) {
                $(element).modal('show');
                $('input#restaurant-new-name').focus();
            }
            else {
                $(element).modal('hide');
            }

        }
    };

    var viewModel = new ViewModel();

    $.ajax({
        url: 'http://localhost:8000/api/restaurants'
    }).done(function (data) {
        console.log('ajax query done');
        for (var i = 0; i < data.length; i++) {
            viewModel.addRestaurantToList(data[i]);
        }

    }).fail(function () {
        console.log('AJAX query failed');
    });

    console.log('comes after ajax');

    ko.applyBindings(viewModel, $('#restaurant-list-wrapper')[0]);
    ko.applyBindings(viewModel, $('#restaurant-new-modal')[0]);


});
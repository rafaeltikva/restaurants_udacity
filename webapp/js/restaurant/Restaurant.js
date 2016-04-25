/**
 * Created by rafaeltikva on 19/04/16.
 */

define(['knockout'], function (ko) {
    return function Restaurant(params) {
        this.store = ko.observable({});
        // verify if it's instantiated from the model or by the user, in which case don't assign an id (the database will)
        (params.id) ? this.store().id = ko.observable(params.id) : null;
        this.store().name = ko.observable(params.name);
        this.tempName = ko.observable(params.name);

        this.isEditable = ko.observable(false);
    };
});
/**
 * Created by apium on 18/03/2016.
 */
;(function(app, window) {
    'use strict';

    var name = 'domain/kitchen/TutorialTooltip';
    var deps = [];
    function Factory() { return TutorialTooltip; }
    app.factory(name, deps.concat([Factory]));
    if (window.define) define(deps, Factory);

    function TutorialTooltip(object) {
        if (!object) {
            object = {
                'kitchen': false,
                'library_recipe_title': false,
                'library_edit_profile': false
            };
        }
        if (typeof object.kitchen != 'boolean'
            || typeof object['library_recipe_title'] != 'boolean'
            || typeof object['library_edit_profile'] != 'boolean')
            throw new Error('invalid tooltip parameters');

        this.tooptip = object;
    }

    TutorialTooltip.newInstance = function(object) {
        return new TutorialTooltip(object);
    };

    TutorialTooltip.prototype.toDTO = function() {
        return this.tooptip;
    };

})(app, this);
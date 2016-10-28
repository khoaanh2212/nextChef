/**
 * Created by apium on 18/03/2016.
 */
;(function(app, window) {
    'use strict';

    var name = 'infrastructure/KitchenTooltipStorage';
    var deps = ['infrastructure/LocalStorage', 'domain/kitchen/TutorialTooltip'];
    function Factory(localStorage, TutorialTooltip) {
        KitchenTooltipStorage.localStorage = localStorage;
        KitchenTooltipStorage.TutorialTooltip = TutorialTooltip;
        return KitchenTooltipStorage;
    }
    app.factory(name, deps.concat([Factory]));
    if (window.define) define(deps, Factory);

    function KitchenTooltipStorage(localStorage, TutorialTooltip) {
        this.localStorage = localStorage;
        this.TutorialTooltip = TutorialTooltip;
    }

    KitchenTooltipStorage.newInstance = function(localStorage, TutorialTooltip) {
        return new KitchenTooltipStorage(
            localStorage || KitchenTooltipStorage.localStorage.newInstance(),
            TutorialTooltip || KitchenTooltipStorage.TutorialTooltip
        );
    };

    KitchenTooltipStorage.prototype.saveTutorial = function(chef_id, tutorial) {
        this.localStorage.set('kitchen/tooltip/tutorial/' + chef_id, tutorial.toDTO());
    };

    KitchenTooltipStorage.prototype.getTutorial = function(chef_id) {
        return this.TutorialTooltip.newInstance(this.localStorage.get('kitchen/tooltip/tutorial/' + chef_id));
    }

})(app, this);

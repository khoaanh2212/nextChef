/**
 * Created by apium on 18/03/2016.
 */
define(function(require) {
    var path = 'infrastructure/KitchenTooltipStorage';
    describe(path, function() {
        var Storage = require('infrastructure/KitchenTooltipStorage');
        var Tooltip = require('domain/kitchen/TutorialTooltip');

        var sut;
        beforeEach(function() {
            sut = Storage.newInstance();
        });

        describe('saveTutorial', function() {
            it('should store the tutorial tooltip status with chef id', function() {
                var expected = Tooltip.newInstance({kitchen: true, 'library_recipe_title': true, 'library_edit_profile': true});
                var chef_id = 1;
                sut.saveTutorial(chef_id, expected);
                var actual = sut.getTutorial(chef_id);
                expect(actual.toDTO()).toEqual(expected.toDTO());
                window.localStorage.clear();
            });

            it('should store tutorial tooltip with many row', function() {
                var expected = {kitchen: true, 'library_recipe_title': false, 'library_edit_profile': false};
                sut.saveTutorial(1, Tooltip.newInstance());
                sut.saveTutorial(2, Tooltip.newInstance(expected));
                var actual = sut.getTutorial(2);
                expect(actual.toDTO()).toEqual(expected);
                window.localStorage.clear();
            });
        });

        describe('tutorialTooltip', function() {
            it('should return defaul expected object', function() {
                var expected = {
                    'kitchen': false,
                    'library_recipe_title': false,
                    'library_edit_profile': false
                };
                var actual = sut.getTutorial();
                expect(actual.toDTO()).toEqual(expected);
            });
        });
    });
});

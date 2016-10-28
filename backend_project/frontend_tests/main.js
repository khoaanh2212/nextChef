requirejs.config({
    'baseUrl': '/base/backend/static/js/',
    'shim': {
        'vendor/angular': {
            exports: 'angular'
        },
        'vendor/jquery-1.11.0.min': {
            exports: '$'
        },
        'vendor/jquery.smartbanner': {
            deps: ['vendor/jquery-1.11.0.min']
        },
        'app': {
            deps: ['vendor/angular', 'vendor/jquery-1.11.0.min', 'vendor/jquery.smartbanner'],
            exports: 'app'
        }
    },
    'deps': ['app'],
    callback: test_main
});

function test_main() {
    var tests = [];
    for (var file in window.__karma__.files) {
        if (window.__karma__.files.hasOwnProperty(file)) {
            if (endsWith(file, '.test.js')) {
                tests.push(file);
            }
        }
    }
    function endsWith(str, suffix) {
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    }
    require(tests, window.__karma__.start);
}

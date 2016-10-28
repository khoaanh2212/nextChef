module.exports = function(grunt) {
    grunt.initConfig({
        less: {
            dist: {
                files: {
                    'backend/static/css/cookbooth.css': [
                        'backend/static/less/cookbooth.less'
                    ],
                    'backend/static/css/embed.css': [
                        'backend/static/less/embed.less'
                    ]
                },
                options: {
                    compress: false,
                    sourceMap: false
                }
            }
        },
        watch: {
            less: {
                files: [
                    'backend/static/less/*.less',
                    'backend/static/less/bootstrap/*.less'
                ],
                tasks: ['less']
            }
        },

        clean: {
            dist: [
                'backend/static/css/cookbooth.css',
                'backend/static/css/embed.css'
            ]
        },

        karma: {
            unit: {
                configFile: 'frontend_tests/karma.conf.js',
                singleRun: true
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-karma');

    // Register tasks
    grunt.registerTask('default', [
        'clean',
        'less'
    ]);

    grunt.registerTask('dev', [
        'watch'
    ]);

    grunt.registerTask('test', [
        'karma'
    ]);

};
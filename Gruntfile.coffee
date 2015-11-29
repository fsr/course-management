fs = require 'fs'

module.exports = (grunt) ->
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'
    sass:
      dist:
        options:
          loadPath: [
            'corporate-web-design/src',
            'bower_components/foundation/scss'
          ]
        files:
          'src/static/css/style.css': 'scss/style.scss'


  grunt.loadNpmTasks 'grunt-contrib-sass'

  grunt.registerTask 'default', ['sass']

module.exports = (grunt) ->
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'
    sass:
      dist:
        options:
          loadPath: [
            'bower_components/foundation/scss',
            'corporate-web-design/src/corporate-design'
          ]
        files:
          'scss/style.scss': 'src/static/css/style.css'



  grunt.loadNpmTasks 'grunt-contrib-sass'

  grunt.registerTask 'default', ['sass']

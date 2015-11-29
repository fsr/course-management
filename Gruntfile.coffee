'use strict'
fs = require 'fs'
cp = require 'child_process'


exec_promise = (func, args...) ->
  new Promise((resolve, reject) ->
    nargs = args.concat( (errors...) ->
      if errors[0] == null
        resolve(null)
      else
        reject(errors)
    )
    func.apply null, nargs
  )

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

  grunt.registerTask 'launch', 'Launch application', ->
    done = this.async()
    process.chdir 'src'

    proc = cp.spawn 'python3', ['manage.py', 'runserver'], {cwd: process.cwd()}, (err) ->
      done err == null
    proc.stderr.on 'data', (data) ->
      grunt.log.write data
    proc.stdout.on 'data', (data) ->
      grunt.log.write data


  grunt.registerTask 'clean-db', 'Clean the database', ->
    done = this.async()
    process.chdir 'src'

    new Promise((resolve) ->
      grunt.log.writeln 'deleting database...'
      fs.unlink 'db.sqlite3', (err) ->
        if not err == null
          grunt.log.writelnln err
        resolve()
    ).then( ->
      grunt.log.writeln 'migrating...'
      exec_promise cp.exec, 'python3 manage.py migrate', null
    ).then( ->
      grunt.log.writeln 'loading sample data...'
      exec_promise cp.exec, 'python3 manage.py loaddata courses', null
    ).then( ->
      done()
    ).catch((error) ->
      grunt.log.writeln(error)
      done(false)
    )

  grunt.registerTask 'default', ['sass']

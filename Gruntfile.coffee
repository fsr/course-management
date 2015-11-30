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

  grunt.loadNpmTasks 'grunt-npm-install'

  grunt.registerTask 'launch', 'Launch application', ->
    done = this.async()
    process.chdir 'src'

    proc = cp.spawn 'python3', ['manage.py', 'runserver'], {cwd: process.cwd()}, (err) ->
      done err == null
    proc.stderr.on 'data', (data) ->
      grunt.log.write data
    proc.stdout.on 'data', (data) ->
      grunt.log.write data

  grunt.registerTask 'install-deps', ['npm-install', 'pip-install', 'bower-install', 'init-submodules']


  grunt.registerTask 'pip-install', 'Get remaining dependencies', ->
    grunt.log.writeln 'installing python dependencies...'

    o = cp.spawnSync 'python3', ['-m', 'pip', 'install', '-r', 'requirements.txt']
    if not o.error == null
      grunt.log.writeln o.stderr
      return false

  grunt.registerTask 'bower-install', 'Install bower dependencies', ->
    grunt.log.writeln 'installing bower dependencies...'
    o = cp.spawnSync 'bower', ['install']
    if not o.error == null
      grunt.log.writeln o.stderr
      false

  grunt.registerTask 'init-submodules', 'Initialize git submodules', ->
    grunt.log.writeln 'fetching submodules...'
    o = cp.spawnSync 'git', ['submodule', 'init'], {cwd: process.cwd()}
    if not o.error == null
      grunt.log.writeln o.stderr
      return false
    o = cp.spawnSync 'git', ['submodule', 'update'], {cwd: process.cwd()}
    if not o.error == null
      grunt.log.writeln o.stderr
      return false



  grunt.registerTask 'clean-db', 'Clean the database', ->
    done = this.async()
    process.chdir 'src'

    new Promise((resolve) ->
      grunt.log.writeln 'deleting database...'
      fs.unlink 'db.sqlite3', (err) ->
        if not err == null
          grunt.log.writeln err
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

'use strict'
fs = require 'fs'
cp = require 'child_process'
path = require 'path'

PYTHON_EXEC = if /^win/.test(process.platform) then 'Scripts/python3.exe' else 'bin/python'

PYTHON_ENV_FOLDER = 'env'

pythonExecSync = (args...) ->
  cp.spawnSync.apply(cp, [path.join(PYTHON_ENV_FOLDER, PYTHON_EXEC)].concat(args))

pythonExec = (args...) ->
  cp.spawn.apply(cp, [path.join(PYTHON_ENV_FOLDER, PYTHON_EXEC)].concat(args))


lazyCopyFile = (source, target, callback) ->
  if fs.existsSync target
    tstat = fs.statSync target
    sstat = fs.statSync source
    if tstat.mtime.value >= sstat.mtime.value
      callback()
      return
  reader = fs.createReadStream source
  writer = fs.createWriteStream target
  writer.on 'close', callback
  writer.on 'error', -> callback(false)
  reader.pipe writer


mkTree = (p) ->
  p.split(path.sep).reduce (prev, curr) ->
      n = path.normalize(path.join(prev, curr))
      if not fs.existsSync n
        fs.mkdirSync n
      n
    , '.'


module.exports = (grunt) ->
  grunt.initConfig
    bower:
      relocate:
        base: 'bower_components'
        target: 'static/vendor/js'
        files: [
          ['jquery/dist/jquery.min.js', 'jquery.min.js'],
          ['foundation/js/foundation.min.js', 'foundation.min.js'],
          ['fastclick/lib/fastclick.js', 'fastclick.js'],
          ['modernizr/modernizr.js', 'modernizr.js'],
          ['jquery/dist/jquery.min.map', 'jquery.min.map']
        ]

    pkg: grunt.file.readJSON 'package.json'
    sass:
      dist:
        options:
          loadPath: [
            'corporate-web-design/src',
            'bower_components/foundation/scss'
          ]
        files:
          'static/css/style.css': 'scss/style.sass'

  grunt.loadNpmTasks 'grunt-contrib-sass'

  grunt.loadNpmTasks 'grunt-npm-install'

  grunt.registerTask 'launch', 'Launch application', ->
    done = this.async()

    proc = pythonExec ['manage.py', 'runserver'], {cwd: process.cwd()}, (err) ->
      done err == null
    proc.stderr.on 'data', (data) ->
      grunt.log.write data
    proc.stdout.on 'data', (data) ->
      grunt.log.write data

  relocate = (arr, callback) ->
    if Array.isArray arr
      if Array.isArray arr[0] and arr[0].length == 2
        relocateOne arr, callback
      else
        pendingCount = arr.length
        success = true
        arr.forEach (elem) ->
          relocateOne elem, (succ) ->
            pendingCount--
            if not succ
              success = false
            if pendingCount == 0
              callback success
    else if typeof arr == "object"
      relocateOne arr, callback
    else
      throw new TypeError('expected list of objects or strings, or object')

  grunt.registerTask 'install-virtualenv', 'Install a python virtual environment', ->
# TODO Check return code for virtualenv installation and report errors
    cp.spawnSync 'python3', ['-m', 'pip', 'install', 'virtualenv']
    cp.spawnSync 'python3', ['-m', 'virtualenv', PYTHON_ENV_FOLDER]

  relocateOne = (obj, callback) ->
    if Array.isArray obj
      queue = obj
      base = '.'
      target = '.'
    else if typeof obj == "object"
      base = if obj.base then obj.base else '.'
      target = if obj.base then obj.target else '.'
      queue = obj.files
    else
      throw new TypeError("expected object, got #{typeof obj}")

    pendingCount = queue.length

    success = true

    queue = queue.map ([source, dest]) ->
      [path.normalize(path.join(base, source)), path.normalize(path.join(target, dest))]

    for [source, dest] in queue
      grunt.log.writeln source + ' -> ' + dest
      dir = path.dirname dest
      if not fs.existsSync dir
        grunt.log.writeln true
        mkTree dir
      if not fs.existsSync dir
        callback(false)
      lazyCopyFile source, dest, (err) ->
        if err != undefined
          success = false
          grunt.log.writeln err
        pendingCount--
        if pendingCount == 0
          callback(success)

  grunt.registerTask 'install-dependencies', ['npm-install', 'pip-install', 'bower-install', 'init-submodules']

  grunt.registerTask 'build', ['sass']

  grunt.registerTask 'install', ['install-virtualenv', 'install-dependencies', 'build', 'init-db']


  grunt.registerTask 'pip-install', 'Get remaining dependencies', ->
    grunt.log.writeln 'installing python dependencies...'

    o = pythonExecSync ['-m', 'pip', 'install', '-r', 'requirements.txt']
    if not o.error == null
      grunt.log.writeln o.stderr
      return false

  grunt.registerTask 'bower-install', 'Install bower dependencies', ->
    grunt.log.writeln 'installing bower dependencies...'
    o = cp.spawnSync 'bower', ['install']
    if not o.error == null
      grunt.log.writeln o.stderr
      return false

    done = @async()
    queue = grunt.config.get('bower.relocate')

    try
      relocate queue, done
    catch err
      grunt.log.writeln err



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

    grunt.log.writeln 'deleting database...'
    fs.unlink 'db.sqlite3', (err) ->
      if not err == null
        grunt.log.writeln err
        done(false)
      else
        grunt.task.run('init-db')
        done()


  grunt.registerTask 'init-db', 'Initialize the database', ->
    done = this.async()

    grunt.log.writeln 'migrating...'
    pythonExecSync ['manage.py', 'migrate']
    grunt.log.writeln 'loading sample data...'
    pythonExecSync ['manage.py', 'loaddata', 'courses']

    done()

  grunt.registerTask 'default', ['sass']

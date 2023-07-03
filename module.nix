{ config, lib, pkgs, ... }:
let
  cfg = config.services.course-management;

  settingsType = with lib; types.submodule {
    options = {
      debug = mkEnableOption "django debug mode";
      secretKeyFile = mkOption {
        type = types.str;
        default = "$STATE_DIRECTORY/secret_key";
        description = "The secret key django should use.";
      };
      adminPassFile = mkOption {
        type = types.nullOr types.str;
        default = null;
        description = "If set, a superuser named `admin` with the given password will be created automatically.";
      };
      database = mkOption {
        type = types.attrsOf types.anything;
        description = ''
          The database the application should connect to.
          See https://docs.djangoproject.com/en/3.2/ref/settings/#databases for details.
          Environment variables will be substituted at runtime.
        '';
        default = {
          ENGINE = "django.db.backends.sqlite3";
          NAME = "$STATE_DIRECTORY/db.sqlite3";
        };
        example = {
          ENGINE = "django.db.backends.mysql";
          NAME = "course_management";
          USER = "coursemanagement";
          PASSWORD = "$MYSQL_PASSWORD";
          HOST = "127.0.0.1";
          OPTIONS = {
            charset = "utf8mb4";
            user_unicode = true;
          };
        };
      };
      admins = mkOption {
        type = types.listOf (types.submodule {
          options = {
            name = mkOption {
              type = types.str;
            };
            email = mkOption {
              type = types.str;
            };
          };
        });
        description = ''
          A list of all the people who get code error notifications.
        '';
        default = [ ];
        example = [{
          name = "Admin";
          email = "root@example.com";
        }];
      };
      allowedHosts = mkOption {
        type = types.listOf types.str;
        description = "A list of hostnames that may be served.";
        default = [ (mkIf (cfg.hostName != null) cfg.hostName) ];
      };
      email = mkOption {
        type = settingsEmailType;
        description = "Configuration for sending email.";
        default = { };
      };
      extraConfig = mkOption {
        default = "";
        type = types.lines;
        description = ''
          Extra configuration options that will be added verbatim at
          the end of `settings.py`.
        '';
      };
    };
  };

  settingsEmailType = with lib; types.submodule {
    options = {
      host = mkOption {
        type = types.str;
        default = "localhost";
      };
      port = mkOption {
        type = types.int;
        default = 25;
      };
      user = mkOption {
        type = types.str;
        default = "";
      };
      passwordFile = mkOption {
        type = types.str;
        default = "/dev/null";
      };
      fromEmail = mkOption {
        type = types.str;
        default = "webmaster@localhost";
      };
      serverEmail = mkOption {
        type = types.str;
        description = "Email used for error notifications.";
        default = "root@localhost";
      };
    };
  };
in
{
  options.services.course-management = with lib; {
    enable = mkEnableOption "iFSR course management";
    package = mkOption {
      type = types.package;
      default = pkgs.course-management;
      description = "The package to use.";
    };
    user = mkOption {
      type = types.str;
      default = "course-management";
      description = "The user under which the server runs.";
    };
    group = mkOption {
      type = types.str;
      default = "course-management";
      description = "The group under which the server runs.";
    };
    hostName = mkOption {
      type = types.nullOr types.str;
      default = null;
      example = "courses.example.com";
      description = ''
        The hostname the application should be served on.
        If it is `null`, nginx will not be automatically configured.
      '';
    };
    listenAddress = mkOption {
      type = types.str;
      default = "127.0.0.1";
      description = "The address the server should listen on.";
    };
    listenPort = mkOption {
      type = types.port;
      default = 5000;
      description = "The port the server should listen on.";
    };
    workers = mkOption {
      type = types.int;
      default = 4;
      description = "The number of workers gunicorn should use.";
    };
    settings = mkOption {
      type = settingsType;
    };
  };

  config =
    let
      python = cfg.package.python;
      pythonEnv = python.buildEnv.override {
        extraLibs = [ cfg.package ];
      };

      baseDir = "${cfg.package}/${cfg.package.python.sitePackages}/${cfg.package.pname}";

      # Hack to turn a generic nix attrSet/list into a python dict/list.
      # This serializes the given value to JSON, writes it to a file and returns the python code to load it again.
      cfgToPython = name: value: "load_file('${pkgs.writeText (name + ".json") (builtins.toJSON value)}')";

      # Convert admins list to python tuples.
      adminsStr = builtins.concatStringsSep ", " (
        builtins.map
          (a: "('${a.name}', '${a.email}')")
          cfg.settings.admins
      );

      settingsFile = pkgs.writeTextDir "${python.sitePackages}/course_management_nixos_settings/__init__.py" /* python */ ''
        import os, json
        from django.utils.translation import gettext_lazy as _

        # function to read a file, substitute env variables and deserialize json
        def load_file(file_path):
            with open(file_path, 'r') as f:
                return json.loads(os.path.expandvars(f.read()))

        DEBUG = ${if cfg.settings.debug then "True" else "False"}

        if DEBUG:
            EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

        ALLOWED_HOSTS = ${cfgToPython "allowedHosts" cfg.settings.allowedHosts}

        BASE_DIR = "${baseDir}"

        with open(os.path.expandvars('${cfg.settings.secretKeyFile}')) as f:
            SECRET_KEY = f.read().strip()

        INSTALLED_APPS = (
            'modeltranslation',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'guardian',
            'user',
            'course',
        )

        MIDDLEWARE = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.security.SecurityMiddleware',
        )

        ROOT_URLCONF = 'course.urls'

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]

        WSGI_APPLICATION = 'course.wsgi.application'

        DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

        AUTHENTICATION_BACKENDS = (
            'guardian.backends.ObjectPermissionBackend',
            'django.contrib.auth.backends.ModelBackend',
        )

        ANONYMOUS_USER_ID = -1

        ADMINS = ( ${adminsStr} )

        DATABASES = {
            'default': ${cfgToPython "database" cfg.settings.database}
        }

        LANGUAGE_CODE = 'en'
        LANGUAGES = (
            ('en', _('English')),
            ('de', _('German')),
        )

        TIME_ZONE = 'Europe/Berlin'
        USE_TZ = False
        USE_I18N = True
        USE_L10N = True

        STATIC_URL = '/static/'

        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, "static"),
        )

        LOCALE_PATHS = (
            os.path.join(BASE_DIR, "locale"),
        )

        DEFAULT_FROM_EMAIL = '${cfg.settings.email.fromEmail}'
        SERVER_EMAIL = '${cfg.settings.email.serverEmail}'
        EMAIL_HOST = '${cfg.settings.email.host}'
        EMAIL_PORT = ${toString cfg.settings.email.port}
        EMAIL_HOST_USER = '${cfg.settings.email.user}'

        with open('${cfg.settings.email.passwordFile}', 'r') as f:
            EMAIL_HOST_PASSWORD = f.read().strip()

        ${cfg.settings.extraConfig}
      '';

      ensureAdminScript = pkgs.writeText "ensureAdminScript.py" /* python */ ''
        from django.contrib.auth.models import User
        from user.models import UserInformation

        with open(os.path.expandvars('${cfg.settings.adminPassFile}')) as f:
            password = f.read().strip()

        query = User.objects.filter(username="admin")

        if not query.exists():
            user = User.objects.create_superuser(username="admin", first_name="Admin", password=password)
            UserInformation.objects.create(user=user, accepted_privacy_policy=True)
        else:
            user = query.first()
            user.set_password(password)
            user.save()
      '';

      environment = {
        PYTHONPATH = "${settingsFile}/${python.sitePackages}:${pythonEnv}/${python.sitePackages}";
        DJANGO_SETTINGS_MODULE = "course_management_nixos_settings";
      };

      manageScript =
        let
          preserveEnv = "--preserve-env=${lib.concatStringsSep "," (builtins.attrNames environment)}";
          exportEnv = lib.concatLines (lib.mapAttrsToList (name: value: "export ${name}='${value}'") environment);
        in
        pkgs.writeScriptBin "cm-manage" ''
          #!${pkgs.runtimeShell}

          exec=exec
          if [[ "$USER" != ${cfg.user} ]]; then
            exec='exec /run/wrappers/bin/sudo -u ${cfg.user} ${preserveEnv}'
          fi

          ${exportEnv}

          $exec ${python}/bin/python ${baseDir}/manage.py "$@"
        '';
    in
    lib.mkIf cfg.enable {
      environment.systemPackages = [ manageScript ];

      users.users.course-management = lib.mkIf (cfg.user == "course-management") {
        group = cfg.group;
        isSystemUser = true;
      };
      users.groups.course-management = lib.mkIf (cfg.group == "course-management") { };

      systemd.services.course-management = {
        inherit environment;
        wantedBy = [ "multi-user.target" ];
        after = [ "network.target" ];
        preStart = ''
          # Generate secret key if it does not exist
          if ! [ -f "${cfg.settings.secretKeyFile}" ]; then
            ${pkgs.pwgen}/bin/pwgen -s 50 1 > "${cfg.settings.secretKeyFile}"
          fi
          # Run migrations
          ${manageScript}/bin/cm-manage migrate
        '' + lib.optionalString (cfg.settings.adminPassFile != null) ''
          # Ensure that admin user exists
          ${manageScript}/bin/cm-manage shell < ${ensureAdminScript}
        '';
        serviceConfig = {
          User = cfg.user;
          Group = cfg.group;
          StateDirectory = "course-management";
          ExecStart = "${python.pkgs.gunicorn}/bin/gunicorn course-management.course.wsgi -w ${toString cfg.workers} -b ${cfg.listenAddress}:${toString cfg.listenPort}";

          # from systemd-analyze --no-pager security course-management.service
          CapabilityBoundingSet = null;
          MemoryDenyWriteExecute = true;
          PrivateDevices = true;
          PrivateUsers = true;
          ProtectHome = true;
          ProtectKernelLogs = true;
          RestrictAddressFamilies = [ "AF_INET" "AF_INET6" "AF_UNIX" ];
          RestrictNamespaces = true;
          RestrictRealtime = true;
          SystemCallArchitectures = "native";
          SystemCallFilter = "@system-service";
        };
      };

      services.nginx = lib.mkIf (cfg.hostName != null) {
        enable = true;
        recommendedProxySettings = lib.mkDefault true;

        virtualHosts.${cfg.hostName} = {
          locations."/".proxyPass = "http://${cfg.listenAddress}:${toString cfg.listenPort}";
          locations."/static".root = baseDir;
          locations."/static/admin".root = "${pythonEnv}/${python.sitePackages}/django/contrib/admin";
        };
      };
    };
}

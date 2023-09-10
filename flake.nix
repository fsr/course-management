{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    (flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
        pkgs = nixpkgs.legacyPackages.${system};
      in
      rec {
        packages = rec {
          course-management = mkPoetryApplication {
            projectDir = self;
            preBuild = ''
              cp course-management/course/settings.py.example course-management/course/settings.py
              python course-management/manage.py compilemessages
              rm course-management/course/settings.py
            '';
          };
          default = course-management;
        };

        devShells.default = pkgs.mkShell {
          packages = [
            poetry2nix.packages.${system}.poetry
            packages.course-management.python
            packages.course-management
          ];
        };

        formatter = pkgs.nixpkgs-fmt;
      }
    )) // {
      overlays.default = (final: prev: {
        inherit (self.packages.${prev.system}) course-management;
      });

      nixosModules.default = {
        imports = [ ./module.nix ];

        nixpkgs.overlays = [ self.overlays.default ];
      };
    };
}

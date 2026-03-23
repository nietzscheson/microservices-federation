{
  description = "DevShell con Terraform, Docker, Python y ECR login";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

        pythonEnv = pkgs.python313.withPackages (ps: with ps; [
          pip
        ]);

        commonDeps = with pkgs; [
          pythonEnv
          uv
          git
          pre-commit
          docker
          nodejs_22
          nodePackages.lerna
          yarn
        ];
      in {
        devShells.default = pkgs.mkShell {
          packages = commonDeps;

          shellHook = ''
            pyenv global system
            export pythonEnv=${pythonEnv}
            export PATH=$PATH:${pythonEnv}/bin
            docker compose up --build -d
            docker compose ps -a
          '';
        };
      });
}

{
  description = "Heracles SPICE simulation environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem = { pkgs, ... }:
        let
          openvaf = pkgs.callPackage nix/openvaf.nix { };
          vampyre = pkgs.callPackage nix/vampyre.nix { };
          heracles = pkgs.callPackage nix/heracles.nix {
            inherit openvaf;
          };
          vacask = pkgs.callPackage nix/vacask.nix {
            inherit openvaf;
          };
          pyenv = pkgs.python3.withPackages (ps: [
            ps.matplotlib
            ps.numpy
            ps.pyspice
            ps.scipy
          ]);
        in
        {
          packages.default = heracles;
          devShells.default = pkgs.mkShell {
            buildInputs = [ openvaf vacask vampyre pyenv pkgs.ngspice ];
            SIM_MODULE_PATH = "${vacask}/lib/vacask/mod/:${heracles}/lib/";
          };
        };
    };
    # Do the linting or testing with vampyre here. Also package vampyre.
}

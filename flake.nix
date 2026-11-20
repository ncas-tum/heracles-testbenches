{
  description = "Heracles SPICE simulation environment";

  inputs = {
    veriloga-flake.url = "github:ncas-tum/veriloga-flake";
    nixpkgs.follows = "veriloga-flake/nixpkgs";
    flake-parts.follows = "veriloga-flake/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem =
        { pkgs, inputs', ... }:
        let
          heracles = pkgs.callPackage nix/heracles.nix { };
        in
        {
          packages.default = heracles;

          devShells.default = pkgs.mkShell {
            inputsFrom = [ inputs'.veriloga-flake.devShells.default ];
            SIM_MODULE_PATH = "${pkgs.vacask}/lib/vacask/mod/:${heracles}/lib/";
          };
        };
    };
}

{
  description = "Heracles testbenches";

  inputs = {
    veriloga-flake.url = "github:ncas-tum/veriloga-flake";
    nixpkgs.follows = "veriloga-flake/nixpkgs";
    flake-parts.follows = "veriloga-flake/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, veriloga-flake, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem =
        { pkgs, system, ... }:
        let
          openvaf = veriloga-flake.packages.${system}.openvaf;
          vacask = veriloga-flake.packages.${system}.vacask;
          heracles = pkgs.callPackage ./heracles.nix {
            inherit openvaf;
          };
        in
        {
          devShells.default = pkgs.mkShell {
            inputsFrom = [ veriloga-flake.devShells.${system}.default ];
            buildInputs = [ heracles ];
            SIM_MODULE_PATH = "${vacask}/lib/vacask/mod/:${heracles}/lib/";
          };
        };
    };
}

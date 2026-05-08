{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python3;

  # If the .vams files are in the repo, fetchFromGitHub gives you all of them.
  # If they're separate, use fetchurl for each.
  vampyre = pkgs.fetchFromGitHub {
    owner = "analogdevicesinc";
    repo = "vampyre";
    rev = "d0acfc4b9265c6b2e82373c7da6599efa0651a19";
    hash = "sha256-Gt6ToZKDTF7grEsU5l32iWBSIQWSpfPW2TYo83282dA="; # fill via nix-prefetch-github
  };
  constants-vams = pkgs.fetchurl {
    url = "https://accellera.org/images/downloads/standards/v-ams/constants_2-4.vams";
    hash = "sha256-PkCLi6kuhy+hNPA4svyf38CEXPDBXmkUUh4Y7Bqwv8s";
  };
  disciplines-vams = pkgs.fetchurl {
    url = "https://accellera.org/images/downloads/standards/v-ams/disciplines_2-4.vams";
    hash = "sha256-BToFrhNjq4v7K+lvdCXbJqRlshjD//q9eIdb487Ur1k=";
  };
in
pkgs.runCommand "vampyre-1.9.8" {
  nativeBuildInputs = [ pkgs.makeWrapper ];
} ''
  # Put vampyre.py and the .vams files together in share/
  install -Dm644 ${vampyre}/vampyre.py        $out/share/vampyre/vampyre.py
  install -Dm644 ${disciplines-vams}  $out/share/vampyre/disciplines.vams
  install -Dm644 ${constants-vams}    $out/share/vampyre/constants.vams

  # Wrapper script so the binary is on PATH
  makeWrapper ${python}/bin/python3 $out/bin/vampyre \
    --add-flags "$out/share/vampyre/vampyre.py"
''

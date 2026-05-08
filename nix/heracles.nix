{ lib, stdenv, fetchFromGitHub, openvaf }:

stdenv.mkDerivation {
  pname = "heracles";
  version = "0.2.1";

  src = fetchFromGitHub {
    owner = "bics-rug";
    repo  = "heracles";
    rev   = "v0.2.1";
    # nix-prefetch-url --unpack <url> --type sha256
    hash  = "sha256-XHxa2707miOi54ybSrnidrqyEaKYclAk8Y2TDuP9q1A=";
  };

  nativeBuildInputs = [ openvaf ];

  buildPhase = "
    mkdir -p $out/lib
    openvaf-r heracles.va -o $out/lib/heracles.osdi";
}

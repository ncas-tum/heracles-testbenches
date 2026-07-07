{
  lib,
  stdenv,
  fetchFromGitHub,
  openvaf,
}:

stdenv.mkDerivation {
  pname = "heracles";
  version = "0.3.1";

  src = fetchFromGitHub {
    owner = "ncas-tum";
    repo = "heracles";
    rev = "v0.3.1";
    hash = "sha256-4bexze2JnXvk0iKfJs0i7AqCE/ybws7tbRIwXQFirDQ=";
  };

  nativeBuildInputs = [ openvaf ];

  buildPhase = "
    mkdir -p $out/lib
    openvaf-r heracles.va -o $out/lib/heracles.osdi";

  meta = {
    description = "HfO2 Ferroelectric Capacitor VerilogA Compact Model for Circuit Simulation ";
    homepage = "https://github.com/ncas-tum/heracles";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [
      fehlings
    ];
    platforms = lib.platforms.unix;
  };
}

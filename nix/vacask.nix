{
  lib,
  stdenv,
  fetchgit,
  cmake,
  ninja,
  bison,
  flex,
  python3,
  pkg-config,
  libgcc,
  boost188,
  suitesparse,
  tomlplusplus,
  openvaf
}:

stdenv.mkDerivation {
  pname = "vacask";
  version = "_0.3.2-unstable-2026-03-23";
  src = fetchgit {
    url = "https://codeberg.org/arpadbuermen/VACASK.git";
    rev = "c85b9cbc03c98efed3268c4cb9da7e41fc21193c";
    hash = "sha256-upa0KnxG3tX9hLRIwFlUqCzy03Hpe7Nd/hOrwG3JnkQ=";
  };
  nativeBuildInputs = [ cmake ninja bison flex python3 ];
  buildInputs = [libgcc boost188 suitesparse tomlplusplus openvaf];
  cmakeFlags =
    [ "-G Ninja"
      "-DCMAKE_BUILD_TYPE=Release"
      "-DOPENVAF_DIR=${openvaf}/bin"
    ];

  #postPatch = ''
    # Fix for the SuiteSparse (6.0+) prefix change
    # find . -type f \( -name "*.h" -o -name "*.cpp" -o -name "*.c" \) \
    # -exec sed -i 's|<suitesparse/\([^>]*\)>|<\1>|g' {} +
  #'';

  # Nix uses the include/ prefix for suitesparse, but upstream assumes
  # the include/suitesparse/ prefix, as in the debian package
  # Accordingly, we link the headers to a debian-like prefix
  preBuild = ''
    mkdir -p $TMPDIR/include/suitesparse
    ln -s ${suitesparse.dev}/include/*.h $TMPDIR/include/suitesparse/
    export NIX_CFLAGS_COMPILE="$NIX_CFLAGS_COMPILE -I$TMPDIR/include"
  '';

  meta = {
    description = "Verilog-A Circuit Analysis Kernel";
    homepage = "https://codeberg.org/arpadbuermen/VACASK";
    license = lib.licenses.agpl3Only;
    maintainers = with lib.maintainers; [
      fehlings
    ];
    platforms = lib.platforms.unix;
    mainProgram = "vacask";
  };
}

{
  lib,
  fetchFromGitHub,
  nix-update-script,
  rustPlatform,
  cargo,
  rustc,
  rustfmt,
  pkg-config,
  llvmPackages_18,
  python3,
}:
let
  llvm18BuildRustPackage = rustPlatform.buildRustPackage.override{
    stdenv = llvmPackages_18.stdenv;
  };
in 
  llvm18BuildRustPackage rec {
    pname = "openvaf";
    version = "0.4-unstable-2025-11-25";
  
    src = fetchFromGitHub {
      owner = "arpadbuermen";
      repo = "OpenVAF";
      rev = "f735004a8c492d88502c7918506ec8758c6cd289";
      hash = "sha256-jci/gLZazzFQHbGNi9akzoPoYdi6iJKyo/9IN+twDZU=";
    };
  
    cargoDeps = rustPlatform.fetchCargoVendor {
      inherit pname version src;
      hash = "sha256-Elu5ph3MyDmYgOR+oZDP/iwDZzMpsKYXY6WDECuUR9Q=";
    };
  
    nativeBuildInputs = [
      rustPlatform.cargoSetupHook
      rustPlatform.bindgenHook
      cargo
      rustc
      rustfmt
      pkg-config
      llvmPackages_18.llvm
      llvmPackages_18.bintools
      llvmPackages_18.clang
      python3
    ];
  
    buildInputs = [
      llvmPackages_18.libclang
    ];
  
    hardeningDisable = [ "all" ];
  
    cargoBuildType = "release";
    cargoBuildFlags = ["--bin" "openvaf-r"];
  
    meta = {
      description = "Verilog-A compiler based on LLVM";
      homepage = "https://github.com/arpadbuermen/OpenVAF";
      license = lib.licenses.gpl3Only;
      maintainers = with lib.maintainers; [
        fehlings
      ];
      platforms = lib.platforms.unix;
      mainProgram = "openvaf-r";
    };
  }

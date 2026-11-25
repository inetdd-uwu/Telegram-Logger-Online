{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = [
    pkgs.python312Packages.playwright
    pkgs.playwright-driver.browsers

    pkgs.stdenv.cc.cc.lib 
    
    # Добавляем графические библиотеки (решает ошибку install-deps)
    pkgs.libxcb
    pkgs.libx11
    pkgs.libxrandr
    pkgs.libxcomposite
    pkgs.libxcursor
    pkgs.libxdamage
    pkgs.libxext
    pkgs.libxfixes
    pkgs.gtk3
    pkgs.pango
    pkgs.cairo
    pkgs.atk
    pkgs.nss
    pkgs.nspr
    pkgs.cups
    pkgs.libdrm
    pkgs.libxkbcommon
    pkgs.alsa-lib
  ];

  shellHook = ''
    export PLAYWRIGHT_BROWSERS_PATH=${pkgs.playwright-driver.browsers}
    export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true
    

    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath (with pkgs; [
      stdenv.cc.cc.lib libxcb libx11 libxrandr libxcomposite libxcursor 
      libxdamage libxext libxfixes gtk3 pango cairo atk nss nspr cups 
      libdrm libxkbcommon alsa-lib
    ])}:$LD_LIBRARY_PATH
  '';
}

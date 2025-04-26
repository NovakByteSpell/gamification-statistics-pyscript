{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    (pkgs.python311.withPackages (ps: with ps; [
      pandas
      numpy
      matplotlib
      openpyxl
      scipy
    ]))
  ];
}

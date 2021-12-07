{
  description = "Development environment";
  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11"; };
  outputs = { self, nixpkgs }: {
    devShell.x86_64-linux = with import nixpkgs { system = "x86_64-linux"; };
      let customPython = python3.withPackages (p: [ p.protobuf ]);
      in mkShell { buildInputs = [ customPython protobuf ]; };
  };
}

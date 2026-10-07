"""CLI: encrypt / decrypt / verify / inspect (I/O layer; core stays print-free).

Password handling: default via ``getpass`` (never a CLI argument, never
logged). Non-interactive demo runs use ``--demo-password <value>`` or
``PM_BG_AES_DEMO_PASSWORD``, which is explicitly labelled demonstration-only
and must never be presented as a secret.
"""

import argparse
import getpass
import hashlib
import os
import sys

import numpy as np

from pm_bg_aes.crypto import decrypt_file, encrypt_file
from pm_bg_aes.entropy import shannon_entropy
from pm_bg_aes.file_format import parse_header

DEMO_PASSWORD_ENV = "PM_BG_AES_DEMO_PASSWORD"


def _resolve_password(args) -> str:
    if args.demo_password is not None:
        print("[demo] using demonstration-only password (not a secret)",
              file=sys.stderr)
        return args.demo_password
    env = os.environ.get(DEMO_PASSWORD_ENV)
    if env:
        print(f"[demo] using {DEMO_PASSWORD_ENV} (demonstration-only, not a secret)",
              file=sys.stderr)
        return env
    return getpass.getpass("Password: ")


def _add_common(sp):
    sp.add_argument("--demo-password", default=None,
                    help="demonstration-only password (non-interactive runs)")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    ap = argparse.ArgumentParser(
        prog="pm-bg-aes",
        description="Archival PM-BG-AES hybrid codec (research artifact; not for production).",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("encrypt", help="encrypt INPUT to OUTPUT")
    p.add_argument("input"); p.add_argument("--output", "-o", required=True)
    p.add_argument("--matrix-n", type=int, default=None,
                   help="override selector n (archival default: selector)")
    _add_common(p)

    p = sub.add_parser("decrypt", help="decrypt INPUT to OUTPUT")
    p.add_argument("input"); p.add_argument("--output", "-o", required=True)
    _add_common(p)

    p = sub.add_parser("verify", help="byte-compare ORIGINAL and RECOVERED")
    p.add_argument("original"); p.add_argument("recovered")

    p = sub.add_parser("inspect", help="parse ciphertext header (no decryption)")
    p.add_argument("ciphertext")
    return ap


def cmd_encrypt(args) -> int:
    """Run encrypt; return exit code."""
    password = _resolve_password(args)
    meta = encrypt_file(args.input, args.output, password, args.matrix_n)
    print(f"encrypted n={meta['n']} len_hill={meta['len_hill']} "
          f"in={meta['input_size']} out={meta['output_size']}")
    return 0


def cmd_decrypt(args) -> int:
    """Run decrypt; return exit code."""
    password = _resolve_password(args)
    try:
        meta = decrypt_file(args.input, args.output, password)
    except ValueError as exc:
        print(f"decrypt failed: {exc}", file=sys.stderr)
        return 3
    print(f"decrypted out={meta['output_size']}")
    return 0


def cmd_verify(args) -> int:
    """Byte-compare two files; return 0 on match, 2 on mismatch."""
    with open(args.original, "rb") as f:
        a = f.read()
    with open(args.recovered, "rb") as f:
        b = f.read()
    ha, hb = hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest()
    print(f"sha256 original : {ha}")
    print(f"sha256 recovered: {hb}")
    print(f"sizes: {len(a)} vs {len(b)}")
    if a == b:
        print("MATCH: byte-identical")
        return 0
    print("MISMATCH", file=sys.stderr)
    return 2


def cmd_inspect(args) -> int:
    """Parse header; return 0, or 2 on malformed input."""
    raw = np.fromfile(args.ciphertext, dtype=np.uint8)
    try:
        n, len_hill = parse_header(raw)
    except ValueError as exc:
        print(f"malformed: {exc}", file=sys.stderr)
        return 2
    ent = shannon_entropy(raw)
    print(f"n={n} len_hill={len_hill} total={raw.size} "
          f"aes_tail={raw.size - 12 - len_hill} entropy={ent:.4f}")
    return 0


def main(argv=None) -> int:
    """CLI entry point."""
    args = build_parser().parse_args(argv)
    if args.command == "encrypt":
        return cmd_encrypt(args)
    if args.command == "decrypt":
        return cmd_decrypt(args)
    if args.command == "verify":
        return cmd_verify(args)
    if args.command == "inspect":
        return cmd_inspect(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())

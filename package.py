"""Merge patched classes.dex into a CarXY base. Public builds omit local identity assets."""
import argparse
import struct
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('base')
parser.add_argument('rebuilt')
parser.add_argument('output')
parser.add_argument('--personal', action='store_true')
args = parser.parse_args()
with zipfile.ZipFile(args.base) as base, zipfile.ZipFile(args.rebuilt) as patched, zipfile.ZipFile(args.output, 'w') as out:
    for entry in base.infolist():
        name = entry.filename
        if name.startswith('META-INF/') and name.upper().endswith(('.SF', '.RSA', '.DSA', '.EC', '.MF')):
            continue
        if not args.personal and name.startswith('assets/offline-mfi/'):
            continue
        data = patched.read(name) if name == 'classes.dex' else base.read(entry)
        if entry.compress_type == zipfile.ZIP_STORED:
            alignment = 16384 if name.endswith('.so') else 4
            padding = -(out.fp.tell() + 34 + len(name.encode())) % alignment
            entry.extra = struct.pack('<HH', 0xcafe, padding) + bytes(padding)
        out.writestr(entry, data)

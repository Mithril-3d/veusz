#!/usr/bin/env python3
"""
compile_translations.py
-----------------------
Compile Qt XML translation (.ts) files into binary (.qm) files
without requiring lrelease or external Qt toolchains.
Fully compatible with Qt 5 and Qt 6 QTranslator.
"""

import sys
import os
import struct
import xml.etree.ElementTree as ET

MAGIC = bytes([
    0x3c, 0xb8, 0x64, 0x18, 0xca, 0xef, 0x9c, 0x95,
    0xcd, 0x21, 0x1c, 0xbf, 0x60, 0xa1, 0xbd, 0xdd
])

def elf_hash(source: str, comment: str = '') -> int:
    """Calculate ELF hash as used by Qt QTranslator."""
    h = 0
    for b in source.encode('utf-8'):
        h = (h << 4) + b
        g = h & 0xf0000000
        if g:
            h ^= (g >> 24)
        h &= ~g
    if comment:
        for b in comment.encode('utf-8'):
            h = (h << 4) + b
            g = h & 0xf0000000
            if g:
                h ^= (g >> 24)
            h &= ~g
    if not h:
        h = 1
    return h & 0xffffffff

def ts_to_qm(ts_path: str, qm_path: str) -> int:
    """
    Parse a .ts XML file and compile it into a .qm binary file.
    Returns the number of translated messages compiled.
    """
    tree = ET.parse(ts_path)
    root = tree.getroot()

    msg_block = bytearray()
    hash_entries = []
    count = 0

    for ctx in root.findall('context'):
        name_elem = ctx.find('name')
        ctx_name = name_elem.text if name_elem is not None and name_elem.text else ''
        for msg in ctx.findall('message'):
            src_elem = msg.find('source')
            src = src_elem.text if src_elem is not None and src_elem.text else ''
            
            tr_elem = msg.find('translation')
            if tr_elem is None:
                continue
            if tr_elem.get('type') == 'vanished':
                continue
            tr = tr_elem.text if tr_elem.text else ''
            if not tr:
                continue

            cm_elem = msg.find('comment')
            cm = cm_elem.text if cm_elem is not None and cm_elem.text else ''

            offset = len(msg_block)
            h = elf_hash(src, cm)
            hash_entries.append((h, offset))

            # Tag_Context = 7
            ctx_bytes = ctx_name.encode('utf-8')
            msg_block.append(7)
            msg_block.extend(struct.pack('>I', len(ctx_bytes)))
            msg_block.extend(ctx_bytes)

            # Tag_SourceText = 6
            src_bytes = src.encode('utf-8')
            msg_block.append(6)
            msg_block.extend(struct.pack('>I', len(src_bytes)))
            msg_block.extend(src_bytes)

            # Tag_Comment = 8 (if present)
            if cm:
                cm_bytes = cm.encode('utf-8')
                msg_block.append(8)
                msg_block.extend(struct.pack('>I', len(cm_bytes)))
                msg_block.extend(cm_bytes)

            # Tag_Translation = 3 (UTF-16BE)
            tr_bytes = tr.encode('utf-16-be')
            msg_block.append(3)
            msg_block.extend(struct.pack('>I', len(tr_bytes)))
            msg_block.extend(tr_bytes)

            # Tag_End = 1
            msg_block.append(1)
            count += 1

    # Hashes must be strictly sorted by hash value for Qt's binary search
    hash_entries.sort(key=lambda x: x[0])
    hash_block = bytearray()
    for h, off in hash_entries:
        hash_block.extend(struct.pack('>II', h, off))

    os.makedirs(os.path.dirname(os.path.abspath(qm_path)), exist_ok=True)
    with open(qm_path, 'wb') as f:
        f.write(MAGIC)
        # Tag 0x42: Hashes
        f.write(bytes([0x42]))
        f.write(struct.pack('>I', len(hash_block)))
        f.write(hash_block)
        # Tag 0x69: Messages
        f.write(bytes([0x69]))
        f.write(struct.pack('>I', len(msg_block)))
        f.write(msg_block)

    return count

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: compile_translations.py <input.ts> <output.qm>")
        sys.exit(1)
    in_ts = sys.argv[1]
    out_qm = sys.argv[2]
    n = ts_to_qm(in_ts, out_qm)
    print(f"Compiled {n} messages from {in_ts} into {out_qm}")

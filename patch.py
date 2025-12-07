"""
ask user for .xex file as input. use run xextool on it to check if it's compressed or encrypted, decrypt/decompress via xextool if needed
after ensuring it is uncompressed and unencrypted, apply patches.

search for the bytes
89 7F 00 06 39 6B FF FF 2B 0B 00 0D 41 99 02 80 3D 80 82 28
then 4 bytes before that match (there should be only one, this pattern exists in every one I've checked) paste in the following bytes:
60 00 00 00 89 7F 00 06 39 6B FF FF 2B 0B 00 0D 41 99 02 80 48 00 02 34
for extended patch there are 2 more values to replace.
scan for
2B 0B 00 00 40 9A 04 D4 89 7F 00 86 2B 0B 00 00
replace with
2B 0B 00 00 40 9A 04 D4 48 00 02 CC 2B 0B 00 00
then scan for
89 7F 00 69 2B 0B 00 00 40 9A 00 3C 7F A4 EB 78
and replace with
89 7F 00 69 2B 0B 00 00 48 00 00 3C 7F A4 EB 78
"""

import subprocess
import sys
import os

def run_xextool(input_file):
    try:
        result = subprocess.run(['xextool', '-c=u', '-e=u', input_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True)
        print("xextool output:", result.stdout.decode())
        return True
    except subprocess.CalledProcessError as e:
        print("Error running xextool:", e.stderr.decode())
        return False
    
def apply_patch(file_path, patches):
    with open(file_path, 'r+b') as f:
        content = f.read()
        for search_bytes, write_bytes, offset in patches:
            index = content.find(search_bytes)
            if index != -1:
                print(f"Patch found at offset {index}, applying patch.")
                f.seek(index + offset)  # Move by the specified offset
                f.write(write_bytes)
            else:
                print("Patch pattern not found.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python patch.py <input_file.xex>")
        return

    input_file = sys.argv[1]
    temp_file = "temp.xex"
    with open(input_file, 'rb') as src, open(temp_file, 'wb') as dst:
        dst.write(src.read())
    output_file = os.path.basename(input_file).removesuffix(".xex") + "_patched.xex"

    if not run_xextool(temp_file):
        print("Failed to process the input file with xextool.")
        return

    patches = [
        (b'\x89\x7F\x00\x06\x39\x6B\xFF\xFF\x2B\x0B\x00\x0D\x41\x99\x02\x80\x3D\x80\x82\x28',
         b'\x60\x00\x00\x00\x89\x7F\x00\x06\x39\x6B\xFF\xFF\x2B\x0B\x00\x0D\x41\x99\x02\x80\x48\x00\x02\x34',
         -4),
        (b'\x2B\x0B\x00\x00\x40\x9A\x04\xD4\x89\x7F\x00\x86\x2B\x0B\x00\x00',
         b'\x48\x00\x02\xCC',
         8),
        (b'\x89\x7F\x00\x69\x2B\x0B\x00\x00\x40\x9A\x00\x3C\x7F\xa4\xeB\x78',
         b'\x48\x00',
         8)
    ]

    apply_patch(temp_file, patches)

    os.rename(temp_file, output_file)
    print(f"Patched file saved as {output_file}")

    if os.path.exists(temp_file):
        os.remove(temp_file)

if __name__ == "__main__":
    main()
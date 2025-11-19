import json
import io
import zipfile

class FileManager:
    def write_binary_file(self, encoded_str, output_file):
        b = bytearray()
        for i in range(0, len(encoded_str), 8):
            b.append(int(encoded_str[i:i+8], 2))
        with open(output_file, "wb") as f:
            f.write(b)

    def read_binary_as_bits(self, input_file):
        with open(input_file, "rb") as f:
            byte_data = f.read()
        return "".join(f"{byte:08b}" for byte in byte_data)

    def make_zip(self, padded_encoded_data, codes):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("compressed.bin", padded_encoded_data)
            zf.writestr("codes.json", json.dumps(codes))
        zip_buffer.seek(0)
        return zip_buffer

    def read_zip(self, zip_bytes):
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes), "r")
        required = {"compressed.bin", "codes.json"}
        if not required.issubset(zf.namelist()):
            raise ValueError("ZIP must contain: compressed.bin AND codes.json")
        compressed_data = zf.read("compressed.bin").decode("utf-8")
        codes = json.loads(zf.read("codes.json").decode("utf-8"))
        return compressed_data, codes
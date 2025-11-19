import heapq
from node import Node

class HuffmanCoding:
    def build_frequency_table(self, text):
        freq = {}
        for char in text:
            if char not in freq:
                freq[char] = 0
            freq[char] += 1
        return freq

    def build_huffman_tree(self, freq_table):
        if not freq_table:
            return None
        heap = [Node(char, freq) for char, freq in freq_table.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        return heap[0]

    def generate_codes(self, node, code="", codes=None):
        if codes is None:
            codes = {}
        if node is None:
            return codes
        if node.char is not None:
            if code == "":
                code = "0"
            codes[node.char] = code
            return codes
        self.generate_codes(node.left, code + "0", codes)
        self.generate_codes(node.right, code + "1", codes)
        return codes

    def encode_text(self, text, codes):
        return "".join(codes[ch] for ch in text)

    def pad_encoded(self, encoded):
        extra = (8 - len(encoded) % 8) % 8
        padded_info = f"{extra:08b}"
        encoded += "0" * extra
        return padded_info + encoded, extra

    def remove_padding(self, encoded_data):
        padded_info = encoded_data[:8]
        extra_padding = int(padded_info, 2)
        encoded_data = encoded_data[8:]
        if extra_padding > 0:
            encoded_data = encoded_data[:-extra_padding]
        return encoded_data

    def decode_text(self, encoded_data, codes):
        reverse_codes = {v: k for k, v in codes.items()}
        current = ""
        decoded = []
        for bit in encoded_data:
            current += bit
            if current in reverse_codes:
                decoded.append(reverse_codes[current])
                current = ""
        return "".join(decoded)
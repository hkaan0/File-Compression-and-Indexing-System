import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.root = None

    def calc_freq(self,text):
        frequencies = defaultdict(int)

        for char in text:
            frequencies[char] += 1

        return dict(frequencies)
    
    def build_tree(self, frequencies):
        heap = [HuffmanNode(char,freq) for char, freq in frequencies.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        self.root = heap[0]

    def gen_codes(self, node=None, current_code=""):
        if node is None:
            node = self.root
        if node.char is not None:
            self.codes[node.char] = current_code
            return
        self.gen_codes(node.left, current_code + "0")
        self.gen_codes(node.right, current_code + "1")


    def encode(self, text):
        if not text:
            raise ValueError("Input text is empty. Cannot encode.")
        frequencies = self.calc_freq(text)
        self.build_tree(frequencies)
        self.gen_codes()
        return "".join(self.codes[char] for char in text)
    
    def decode(self, encoded_text):
        decoded = ""
        current = self.root
        for bit in encoded_text:
            current = current.left if bit == '0' else current.right
            if current.char is not None:
                decoded += current.char
                current = self.root

        return decoded
    def write_encoded_file(self, encoded_text, output_path):
        padded_encoded = encoded_text + '0' *((8 - len(encoded_text) % 8) % 8)
        byte_array = bytearray()
        for i in range(0, len(padded_encoded), 8):
            byte = padded_encoded[i:i+8]
            byte_array.append(int(byte, 2))

        with open(output_path, 'wb') as f:
            f.write(byte_array)


    def read_encoded_file(self, input_path):
        with open(input_path, 'rb') as f:
            bytes_data = f.read()

        bit_string = ""
        for byte in bytes_data:
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits

        return bit_string
    



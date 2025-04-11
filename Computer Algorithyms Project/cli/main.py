import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from index.red_black_tree import RedBlackTree
from index.b_plus_tree import BPlusTree
from compression.huffman import HuffmanCoding


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu():
    clear_screen()
    print("--- File Compression and Indexing System ---")
    print("[1] Compress File (Auto Frequency)")
    print("[2] Compress File (Manual Frequency Input)")
    print("[3] Decompress File")
    print("[4] Insert File into Index")
    print("[5] Search File by Name")
    print("[6] List Indexed Files")
    print("[7] Delete File from Index")
    print("[0] Exit")


def show_success(title, details=None):
    print(f"\n {title}")
    if details:
        for key, value in details.items():
            print(f"{key}: {value}")
    input("\n Press Enter to return to main menu...")


def show_error(message):
    print(f"\n {message}")
    input("\n Press Enter to return to main menu...")


def main():
    huffman = HuffmanCoding()
    bptree = BPlusTree()
    rbtree = RedBlackTree()

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            path = input("Enter path of file to compress: ").strip()
            if not os.path.exists(path):
                show_error("File not found.")
                continue

            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()

            frequencies = huffman.calc_freq(text)
            print("\n Auto-detected Character Frequencies:")
            for char, freq in sorted(frequencies.items()):
                display_char = char if char != '\n' else '\\n'
                print(f"'{display_char}': {freq}")

            encoded = huffman.encode(text)
            compressed_path = path + ".bin"
            huffman.write_encoded_file(encoded, compressed_path)

            show_success("File Compressed (Auto)", {
                "Original File": path,
                "Compressed File": compressed_path
            })

        elif choice == "2":
            text = input("Enter the text you want to compress: ")
            try:
                n = int(input("How many unique characters will you define? "))
                frequencies = {}
                for _ in range(n):
                    char = input("Enter character: ")
                    freq = int(input(f"Enter frequency of '{char}': "))
                    frequencies[char] = freq

                huffman.build_tree(frequencies)
                huffman.gen_codes()
                encoded = "".join(huffman.codes[char] for char in text)

                output_path = input("Enter output path for compressed .bin file: ").strip()
                huffman.write_encoded_file(encoded, output_path)

                show_success("File Compressed (Manual)", {
                    "Input Text": text,
                    "Output File": output_path
                })

            except Exception as e:
                show_error(f"Manual compression failed: {e}")

        elif choice == "3":
            path = input("Enter path of .bin file to decompress: ").strip()
            if not os.path.exists(path):
                show_error("File not found.")
                continue

            bitstring = huffman.read_encoded_file(path)
            decoded = huffman.decode(bitstring)
            decompressed_path = path.replace(".bin", "_decoded.txt")
            with open(decompressed_path, 'w', encoding='utf-8') as f:
                f.write(decoded)

            show_success("File Decompressed", {
                "Decoded Output": decompressed_path
            })

        elif choice == "4":
            filepath = input("Enter full path of file to index: ").strip()
            if not os.path.exists(filepath):
                show_error("File not found.")
                continue

            filename = os.path.basename(filepath)
            rbtree.insert(filename, filepath)
            bptree.insert(filename, filepath)

            show_success("File Indexed", {
                "File": filename,
                "Path": filepath
            })

        elif choice == "5":
            filename = input("Enter filename to search: ").strip()
            path_rbt = rbtree.search(filename)
            path_bpt = bptree.search(filename)

            print("\n🔎 Search Results:")
            print("Red-Black Tree:", f"Found → {path_rbt}" if path_rbt else "Not found")
            print("B+ Tree:", f"Found → {path_bpt}" if path_bpt else "Not found")

            input("\n Press Enter to return to main menu...")

        elif choice == "6":
            import time

            print("\n Indexed Files Comparison")

            
            start_rbt = time.time()
            rbt_files = rbtree.list_files()
            end_rbt = time.time()

            print("\n Red-Black Tree Files:")
            if not rbt_files:
                print("No files indexed.")
            else:
                for filename, path in rbt_files:
                    print(f"{filename} → {path}")
            rbt_duration = end_rbt - start_rbt
            print(f" RBT Listing Time: {rbt_duration:.6f} seconds")

            #
            start_bpt = time.time()
            bpt_files = bptree.range_query("", "z" * 100)
            end_bpt = time.time()

            print("\n B+ Tree Files:")
            if not bpt_files:
                print("No files indexed.")
            else:
                for filename, path in bpt_files:
                    print(f"{filename} → {path}")
            bpt_duration = end_bpt - start_bpt
            print(f" BPT Listing Time: {bpt_duration:.6f} seconds")

            # --- Karşılaştırma sonucu ---
            print("\n Comparison Result:")
            if rbt_duration < bpt_duration:
                print(" Red-Black Tree was faster.")
            elif bpt_duration < rbt_duration:
                print(" B+ Tree was faster.")
            else:
                print(" Both structures performed equally.")

            input("\n Press Enter to return to main menu...")


        elif choice == "7":
            filename = input("Enter filename to delete from index: ").strip()
            rbtree.delete(filename)
            bptree.delete(filename)
            show_success("File Removed from Index", {
                " Deleted": filename
            })

        elif choice == "0":
            print("\n Exiting... Goodbye!")
            break

        else:
            show_error("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()


import streamlit as st
import base64
from huffmancoding import HuffmanCoding
from File_Manager import FileManager

codec = HuffmanCoding()
fm = FileManager()

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def main():
    # Load optional icons
    img1 = img_to_base64("icon_1.png")
    img2 = img_to_base64("icon_2.png")

    st.set_page_config(page_title="File Compressor", page_icon="📦" if not img2 else "icon_2.png", layout="wide")

    # Sidebar
    if img1:
        sidebar_title = f"""
        <h2 style='color:lightblue;'>
            <img src="data:image/png;base64,{img1}" width="40"
            style="vertical-align: middle; margin-right:10px;">
            Bruh Tool
        </h2>
        """
    else:
        sidebar_title = "<h2 style='color:lightblue;'>Bruh Tool</h2>"

    st.sidebar.markdown(sidebar_title, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.info("Compress text files or decompress previously compressed ZIP files.", icon="ℹ️")
    st.sidebar.markdown("1️⃣ Compress<br>2️⃣ Download ZIP<br>3️⃣ Decompress ZIP<br>4️⃣ Get original text",
                        unsafe_allow_html=True)

    # Header
    if img1:
        header_html = f"""
        <h1 style='text-align:center; color:lightblue;'>
            <img src="data:image/png;base64,{img1}" width="80"
            style="vertical-align: middle; margin-right:10px;">
            File Compressor / Decompressor
        </h1>
        """
    else:
        header_html = "<h1 style='text-align:center; color:lightblue;'>File Compressor / Decompressor</h1>"

    st.markdown(header_html, unsafe_allow_html=True)
    st.markdown("<hr style='height:2px;border:none;color:gray;background-color:gray;' />",
                unsafe_allow_html=True)

    tab_compress, tab_decompress = st.tabs(["🟢 Compress File", "🔵 Decompress File"])

    # ---------------- Compress Tab ----------------
    with tab_compress:
        st.subheader("Compress a File")
        uploaded_file = st.file_uploader("Upload a text file (.txt, .py)", type=["txt", "py"],
                                         key="compress_uploader", help="Plain text only")

        if uploaded_file:
            try:
                raw = uploaded_file.read()
                if not raw:
                    st.error("Empty file.")
                else:
                    text = raw.decode("utf-8", errors="ignore")

                    st.text_area("Original File Preview",
                                 text[:1000] + ("..." if len(text) > 1000 else ""),
                                 height=200)

                    # Huffman steps
                    freq_table = codec.build_frequency_table(text)
                    root = codec.build_huffman_tree(freq_table)
                    codes = codec.generate_codes(root)
                    encoded_data = codec.encode_text(text, codes)
                    padded_encoded_data, _ = codec.pad_encoded(encoded_data)

                    # Stats
                    original_bits = len(text) * 8
                    compressed_bits = len(padded_encoded_data)
                    reduction_percent = (1 - compressed_bits / original_bits) * 100 if original_bits else 0.0

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Original (bits)", f"{original_bits}")
                    c2.metric("Compressed (bits)", f"{compressed_bits}")
                    c3.metric("Reduction (%)", f"{reduction_percent:.2f}")

                    # ZIP build
                    zip_buffer = fm.make_zip(padded_encoded_data, codes)

                    st.download_button(
                        "⬇️ Download Compressed ZIP",
                        data=zip_buffer.getvalue(),
                        file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_huffman.zip",
                        type="primary",
                        use_container_width=True
                    )

                    st.success("✅ Compression Successful!", icon="🎉")
            except Exception as e:
                st.error(f"Error during compression: {e}")

    # ---------------- Decompress Tab ----------------
    with tab_decompress:
        st.subheader("Decompress a ZIP File")
        uploaded_zip = st.file_uploader("Upload ZIP (must contain compressed.bin and codes.json)",
                                        type=["zip"], key="decompress_uploader")

        if uploaded_zip:
            try:
                zip_bytes = uploaded_zip.read()
                if not zip_bytes:
                    st.error("Empty ZIP file.")
                else:
                    compressed_data, codes = fm.read_zip(zip_bytes)
                    unpadded = codec.remove_padding(compressed_data)
                    decoded_text = codec.decode_text(unpadded, codes)

                    st.text_area("Decompressed Text",
                                 decoded_text[:5000] + ("..." if len(decoded_text) > 5000 else ""),
                                 height=250)

                    st.download_button(
                        "⬇️ Download Decompressed Text",
                        data=decoded_text,
                        file_name="decompressed_output.txt",
                        type="secondary",
                        use_container_width=True
                    )

                    st.success("✅ Decompression Successful!", icon="🎉")
            except Exception as e:
                st.error(f"Error while decompressing: {e}")

    st.markdown("<hr style='height:1px;border:none;color:gray;background-color:gray;' />",
                unsafe_allow_html=True)
    st.info("Use the tabs above to Compress or Decompress files.", icon="ℹ️")

if __name__ == "__main__":
    main()
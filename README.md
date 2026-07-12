# LSB Steganography Image Message Extraction

This example demonstrates Least Significant Bit (LSB) steganography, a common technique in CTF challenges to hide information within images. It shows how to embed a secret message into an image's pixel data by manipulating the least significant bit of each color channel. The script then extracts this hidden message, revealing the concealed text, making the changes visually imperceptible.

## Language

`python`

## How to Run

1. Install the Pillow library: `pip install Pillow`
2. Run the script: `python main.py`

## Original Article

This example accompanies the Turkish article: [BroncoCTF: Unblur Me Challenge'ının Perde Arkası - Görüntü İşleme ve Adli Bilişim Yöntemleri](https://fatihsoysal.com/blog/broncoctf-unblur-me-challengeinin-perde-arkasi-goruntu-isleme-ve-adli-bilisim-yontemleri/).

## License

MIT — see [LICENSE](LICENSE).

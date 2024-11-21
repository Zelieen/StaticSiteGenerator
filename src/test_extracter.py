import unittest

from extracter import extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_extr_images(self):
        text = "test tuple text with images ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(str(extract_markdown_images(text)), "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]")

    def test_only_links(self):
        text = "test tuple text with image + link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        self.assertEqual(str(extract_markdown_links(text)), "[('to boot dev', 'https://www.boot.dev')]")

    def test_only_images(self):
        text = "test tuple text with image + link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        self.assertEqual(str(extract_markdown_images(text)), "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]")

if __name__ == "__main__":
    unittest.main()
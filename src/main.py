from textnode import TextNode, TextType

def main():
    obj = TextNode("This is my text", "italic", "https://www.boot.dev")
    obj2 = TextNode("This is my text", "italic", "https://www.boot.dev")

    print("hello, I am starting:")
    print(obj)
    print(obj == obj2)

main()
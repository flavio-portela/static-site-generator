from textnode import TextNode, TextType


def main():
    textNode = TextNode("This is a text node", TextType.bold, "https://boot.dev")
    print(textNode)


if __name__ == "__main__":
    main()

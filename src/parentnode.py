from htmlnode import ChildrenType, HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: ChildrenType,
        props: dict | None = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children is required")
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

from htmlnode import HTMLNode
from typing import Union


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Union[str, None] = None,
        value: str = "",
        props: Union[dict, None] = None,
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == "":
            raise ValueError("value should be provided")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

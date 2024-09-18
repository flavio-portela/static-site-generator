from functools import reduce
from typing import Union



ChildrenType = list['HTMLNode']

class HTMLNode():
    def __init__(
        self,
        tag: Union[str, None] = None,
        value: Union[str, None] = None,
        children: Union[ChildrenType, None]= None,
        props: Union[dict, None] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if isinstance(self.props, dict):
            return reduce(
                lambda props, item: props + f'{item[0]}="{item[1]}" ',
                self.props.items(),
                " ",
            ).rstrip()
        return ""

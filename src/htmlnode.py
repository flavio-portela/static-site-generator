from functools import reduce


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
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
        return None

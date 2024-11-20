class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children= children
        self.props = props

    def to_html(self):
        raise NotImplementedError("function not implemented in parent class") #NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(list(map(lambda x: f'{x}="{self.props[x]}"', self.props)))

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f'HTMLNode - tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props_to_html()}'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        else:
            if self.tag is None:
                return self.value
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
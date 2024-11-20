class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children= children
        self.props = props

    def to_html(self):
        raise NotImplementedError("function not implemented in parent class")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(list(map(lambda x: f'{x}="{self.props[x]}"', self.props)))

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        else:
            if self.tag is None:
                return self.value
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        elif self.children is None or self.children == []:
            raise ValueError("ParentNode is missing children nodes")
        else:
            concat_children = ""
            for child in self.children:
                if isinstance(child, HTMLNode):
                    concat_children += child.to_html()
                else:
                    raise ValueError(f"'{child}' is not a proper child node")
            return f"<{self.tag}{self.props_to_html()}>{concat_children}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
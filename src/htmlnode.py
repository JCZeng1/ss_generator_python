class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Override with child classes")

    def props_to_html(self):
        output = ""
        if self.props is None or self.props == "":
            return output
        for key in self.props.keys():
            output += f' {key}="{self.props[key]}"'
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is not None:
            if self.tag:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            else:
                return self.value
        raise ValueError("All leaf nodes must have a value.")
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("The object doesn't have a tag!")
        
        if self.children is None:
            raise ValueError("The children is a missing value!")
        
        f_string = ""
        
        for node in self.children:
            if type(node) is not LeafNode:
                f_string += node.to_html()
            elif node.tag:
                f_string += f'<{node.tag}{node.props_to_html()}>{node.value}</{node.tag}>'
            else:
                f_string += node.value
                
        return f"<{self.tag}>" + f_string + f"</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"    

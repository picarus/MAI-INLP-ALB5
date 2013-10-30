'''
Created on Oct 29, 2013

@author: Jose
'''
import re
from nltk import Tree
#from nltk.compat import string_types, unicode_repr

indent_step = 2


def pprint_json_tree(sentences):
        """
        Returns a representation of the list of trees in JSON format.
        Each sentence in the text will be a tree. And each sentence itself can contain other trees.

        For example, the following result was generated from a parse tree of
        the sentence ``Peter lived in San Francisco.``::
        
        [ Tree('S', [Tree('PERSON', [('Peter', 'NNP', 'pet')]), ('lived', 'VBD', 'liv'), ('in', 'IN', 'in'), Tree('GPE', [('San', 'NNP', 'san'), ('Francisco', 'NNP', 'francisco')]), ('.', '.', '.')])
        
        (S
          (PERSON Peter/NNP/pet)
          lived/VBD/liv
          in/IN/in
          (GPE San/NNP/san Francisco/NNP/francisco)
          ././.)

        {
            tag:'S',
            content:
            [
                {   
                    tag:'PERSON',
                    content: 
                    [
                        ['Peter', 'NNP', 'pet']
                    ]
                },
                ['lived', 'VBD', 'liv'], 
                ['in', 'IN', 'in'],
                {
                    tag:'GPE',
                    content: 
                    [   
                        ['San', 'NNP', 'san'], 
                        ['Francisco', 'NNP', 'francisco']
                    ]
                },
                ['.', '.', '.']
            ]
        }

        :return: A JSON representation of this tree.
        :rtype: str
        """
        text=''
        reserved_chars = re.compile('"\/') # review !!!!
        for sentence in sentences:
            output = pprint(sentence, True, 0)
            text = text + re.sub(reserved_chars, r'\\\1', output)
        return text
    
    
def pprint(element, first, indent, nodesep='', quotes=False):
    """
    :return: A pretty-printed string representation of this tree.
    :rtype: str
    :param margin: The right margin at which to do line-wrapping.
    :type margin: int
    :param indent: The indentation level at which printing
        begins.  This number is used to decide how far to indent
        subsequent lines.
    :type indent: int
    :param nodesep: A string that is used to separate the node
        from the children.  E.g., the default value ``':'`` gives
        trees like ``(S: (NP: I) (VP: (V: saw) (NP: it)))``.
    """

    # write it on multi-lines.
    s = ''
    if not first:
        s += ','   # a comma may be missing if it is not the first child
    if isinstance(element, Tree):                      
        s += '\n'+' '*(indent)+'{'
        indent += indent_step
        s += '\n'+' '*(indent)+"tag:'"+element.node+"',"
        s += '\n'+' '*(indent)+'content:'
        s += '\n'+' '*(indent)+'[' 
        for idx in xrange(0,len(element)):
            s += pprint(element[idx], idx==0, indent+indent_step, nodesep, quotes)
        s += '\n'+' '*(indent)+']'
        indent -= indent_step 
        s+= '\n'+' '*(indent)+'}'     
    elif isinstance(element, tuple):
        s += '\n'+' '*(indent)+"['"+ "','".join([ elem for elem in element])+"']"
    else:
        s=str(element)
            
    return s

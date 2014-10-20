#!usr/bin/env python
#coding: utf-8
import datetime
from django import template
from django.template.base import (Node, NodeList, TemplateSyntaxError)
register = template.Library()


@register.filter(name='calculate')
def calculate(value, arg):
    return (int(arg)-1)*10 + int(value)

@register.filter(name='append')
def append(value, args):
    return str(value) + "," + str(args)

@register.filter(name='calculatelinenum')
def calculatelinenum(value, args):
    arr = value.split(",")
    return (int(arr[1])-1)*int(arr[0]) + int(args)


@register.filter(name='include')
def include(value, obj_list):
    for obj in obj_list:
        if obj == value:
            return True
    return False

@register.filter(name='authorityfilter')
def authorityfilter(value, authority_list):
    for authority in authority_list:
        if authority == value:
            return True
    return False



def iscontain(obj, obj_list):
    if obj in obj_list:
        return True
    else:
        return False


class IfContainNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfContainNode>"

    def render(self, context):
        val1 = self.var1.resolve(context, True)
        val2 = self.var2.resolve(context, True)
        if (self.negate and not iscontain(val1, val2)) or (not self.negate and iscontain(val1, val2)):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifcontain(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    val1 = parser.compile_filter(bits[1])
    val2 = parser.compile_filter(bits[2])
    return IfContainNode(val1, val2, nodelist_true, nodelist_false, negate)


@register.tag
def ifcontain(parser, token):
    """
    Outputs the contents of the block if the second argument contain the first argument.

    Examples::

        {% ifcontain user userlist %}
            ...
        {% endifcontain %}

        {% ifnotcontain user userlist %}
            ...
        {% else %}
            ...
        {% endifnotcontain %}
    """
    return do_ifcontain(parser, token, False)

@register.tag
def ifnotcontain(parser, token):
    """
    Outputs the contents of the block if the second argument not contain the first argument.
    See ifcontain.
    """
    return do_ifcontain(parser, token, True)




def issplitcontain(obj_str, obj_list):
    for obj in obj_str.split(','):
        if obj in obj_list:
            return True
    return False


class IfSplitContainNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfSplitContainNode>"

    def render(self, context):
        val1 = self.var1.resolve(context, True)
        val2 = self.var2.resolve(context, True)
        if (self.negate and not issplitcontain(val1, val2)) or (not self.negate and issplitcontain(val1, val2)):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifsplitcontain(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    val1 = parser.compile_filter(bits[1])
    val2 = parser.compile_filter(bits[2])
    return IfSplitContainNode(val1, val2, nodelist_true, nodelist_false, negate)


@register.tag
def ifsplitcontain(parser, token):
    """
    Outputs the contents of the block if the second argument contain the first argument.

    Examples::

        {% ifsplitcontain user userlist %}
            ...
        {% endifsplitcontain %}

        {% ifnotsplitcontain user userlist %}
            ...
        {% else %}
            ...
        {% endifnotsplitcontain %}
    """
    return do_ifsplitcontain(parser, token, False)

@register.tag
def ifnotsplitcontain(parser, token):
    """
    Outputs the contents of the block if the second argument not contain the first argument.
    See ifcontain.
    """
    return do_ifsplitcontain(parser, token, True)













#From http://stackoverflow.com/questions/2687173/django-how-can-i-get-a-block-from-a-template
from django.template import Context
from django.template.loader_tags import BLOCK_CONTEXT_KEY, BlockContext, BlockNode, ExtendsNode


class BlockNotFound(Exception):
    pass


def _get_node(template, context=Context(), name='subject'):
    for node in template:
        if isinstance(node, BlockNode) and node.name == name:
            return node.render(context)
        elif isinstance(node, ExtendsNode):
            # See L106-122 in
            # https://github.com/django/django/blob/master/django/template/loader_tags.py
            if BLOCK_CONTEXT_KEY not in context.render_context:
                context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
            block_context = context.render_context[BLOCK_CONTEXT_KEY]
            lookups = dict([(n.name, n) for n in node.nodelist if isinstance(n, BlockNode)])
            block_context.add_blocks(lookups)
            return _get_node(node.get_parent(context), context, name)
    raise BlockNotFound("Node '%s' could not be found in template." % name)

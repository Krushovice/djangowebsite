from django import template

from mysite.post.models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()

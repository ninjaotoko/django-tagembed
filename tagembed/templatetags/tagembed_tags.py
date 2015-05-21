# -*- coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
from tagembed.providers.tedx import TedxEmbed
from tagembed.providers.youtube import YoutubeEmbed

register = template.Library()

@register.filter
def parse_tagembed(text):

    ted = TedxEmbed()
    youtube = YoutubeEmbed()

    parsed_text = ted.parse(text)
    parsed_text = youtube.parse(parsed_text)

    return mark_safe(parsed_text)

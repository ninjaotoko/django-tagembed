# -*- coding:utf-8 -*-
from tagembed.tagembed import *

class YoutubeEmbed(Embed):
    """
    Tag Embed para videos Youtube
    """

    tag = "youtube"
    tag_class_wrapper = "flex-video"

    def resolver(self, match):
        """
        Este método debe devolver el match con el reemplazo en el texto
        Si no existiece debe devolver el valor intacto.
        """

        args = match.groupdict()

        if args.get('url'):
            url = args.get('url')

        elif args.get('id'):
            id = args.get('id')
            url = "http://www.youtube.com/watch?v=%s" % id

        url_embed = "http://www.youtube.com/oembed?url=%s&format=json" % url
        embed = requests.get(url_embed)
        
        if embed.ok:
            try:
                self.html_element = embed.json().get('html')
            except:
                pass

        tag_class_wrapper = args.get('wrapp_class') or self.tag_class_wrapper

        return "<div class=\"%(tag_class_wrapper)s\">%(html)s</div>" % dict(html=self.html_element, \
                tag_class_wrapper=tag_class_wrapper)

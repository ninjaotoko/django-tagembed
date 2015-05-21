# -*- coding:utf-8 -*-
from tagembed.tagembed import *

class TedxEmbed(Embed):
    """
    Tag Embed para videos Ted
    """

    tag = "ted"
    tag_class_wrapper = "flex-video"

    arguments = {
        "id": "[a-zA-Z0-9\-\_]", # argumento obligatorio, los demás son tratados como attributos
        "lang?": "[a-zA-Z\-]", # termina en ? es opcional
        #"wrapp_class?": "\"[a-zA-Z\-\_\s]\"", # termina en ? es opcional
    }

    def resolver(self, match):
        """
        Este método debe devolver el match con el reemplazo en el texto
        Si no existiece debe devolver el valor intacto.
        """

        args = match.groupdict()
        logger.info("Data has\n%s", args)

        if args.get('url'):
            url = args.get('url')
            #https://www.ted.com/talks/louise_fresco_on_feeding_the_whole_world?language=es

        elif args.get('id'):
            id = args.get('id')
            lang = args.get('lang') or 'es'
            url = "http://www.ted.com/talks/view/lang/%(lang)s/id/%(id)s" % dict(id=id, lang=lang)

        url_embed = "http://www.ted.com/services/v1/oembed.json?url=%s" % url
        embed = requests.get(url_embed)

        if embed.ok:
            try:
                self.html_element = embed.json().get('html')
            except:
                pass

        tag_class_wrapper = args.get('wrapp_class') or self.tag_class_wrapper

        return "<div class=\"%(tag_class_wrapper)s\">%(html)s</div>" % dict(html=self.html_element, \
                tag_class_wrapper=tag_class_wrapper)

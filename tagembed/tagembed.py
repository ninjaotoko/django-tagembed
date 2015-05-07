# -*- coding:utf-8 -*-
import requests
import re
import json
import urllib
import logging
logger = logging.getLogger(__name__)

class Embed:

    tag_wrapper = ["\[", "\]"] # debe ser escapado para no generar confilco con la RegExp
    tag = "tagembed" # tag del elemento que con el que se construye la regular expression
    arguments = {
        "id": "[a-zA-Z0-9\-\_]", # argumento obligatorio, los demás son tratados como attributos
    }
    html_element = "<!-- tagembed -->"

    def get_pattern(self):
        """
        Resuelve el patron para luego ser usado por el parser
        devuelve una RegExp
        re.sub(
            # pattern
            "\[(?P<tag>[a-z]+)\s+(?P<id>[0-9]+)\s*(?P<attrs>[^]]*)\]", "<\\1 id=\\2 \\3/>", 
            # text
            "Este video es [ted 2143 class='large'] y el >>>> otro [vimeo 734]", 
            # flags
            re.I|re.M,re.U
        )
        """

        pattern = "%s" % self.tag

        # crea los demás argumentos con los que se crean los patrones para capturar
        # usa el key como label de captura y el val para la regexp
        for key, patt in self.arguments.iteritems():
            if key.endswith('?'):
                pattern = "%(pattern)s\s*(%(key)s=(?P<%(key)s>%(patt)s+))?" % dict(pattern=pattern, key=key.replace('?', ''), patt=patt)
            else:
                pattern = "%(pattern)s\s*%(key)s=(?P<%(key)s>%(patt)s+)" % dict(pattern=pattern, key=key, patt=patt)

        pattern = "%s\s*(?P<attrs>[^]]*)" % pattern

        return re.compile(pattern.join(self.tag_wrapper), re.I | re.M | re.U)


    def get_data(self, string):
        pattern = self.get_pattern()
        matches = pattern.sub(self.resolver, string)

        if not matches:
            return string

        return matches


    def resolver(self, match):
        """
        Este método debe devolver el match con el reemplazo en el texto
        Si no existiece debe devolver el valor intacto.

        args = match.groupdict()
        logger.info("Data has\n%s", args)

        if args.get('url'):
            url = args.get('url')

        elif args.get('id'):
            id = args.get('id')
            url = "http://www.ted.com/talks/view/id/%s" % id

        url_embed = "http://www.ted.com/services/v1/oembed.json?url=%s" % url
        embed = requests.get(url_embed)

        if embed.ok:
            try:
                self.html_element = embed.json().get('html')
            except:
                pass
        """

        raise Exception("Error `resolver` not implemented")


    def parse(self, string):
        """
        Parsea en busca del tag configurado y hace el render
        """

        data = self.get_data(string)
        return data



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

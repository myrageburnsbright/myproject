import os
from flask_assets import Bundle
from .functions import recursive_flatten_iterator

def get_bundle (route, tpl, ext, paths, type=False):
    """
        Функция возвроцает нужный Bundle (css/js) для регистрации в главном файле приложения.
        Содержит питц до докольных исходников ss/js-файлов, серуппированных друг с другом по использованию в шаблонах html
        1-0 пораметр route - назвоне рочта
        ﻿﻿й параметр трі - название шоблона html из папки /templotes
        ﻿﻿й параметр ext - расширение (css/js)
        ﻿﻿й параметр paths (массив) - все пути к исходникам
        ﻿﻿й параметр туре (опциональный) - использчется только для JS.
        !!! Важно! !! Если нужен главный фойл "main. js", параметр не указывать!
        Если нужен скрипт длительной загрузки "defer. js", передать булево значение True
    """
    if route and tpl and ext:
        return {
            'instance' : Bundle(*paths, output=get_path(route, tpl, ext, type), filters=get_filter(ext)),
            'name': get_filename(route, tpl, ext, type),
            'dir' : os.getcwd()
        }
    
def register_bundle(assets, bundle):
    assets.register(bundle['name'], bundle['instance']) 
    return f"Bundle {bundle['name']} registered successfully!"

def register_bundles(assets, bundles):
    for x in recursive_flatten_iterator(bundles):
        for bundle in x:
            register_bundle(assets, bundle)

def get_filename(route, tpl, ext, type):
    if type:
        return f"{route}_{tpl}_{ext}_defer" 
    else:
        return f"{route}_{tpl}_{ext}"
    
def get_path(route, tpl, ext, type):
    if type:
        return f"gen/{route}/{tpl}/defer.{ext}"
    else:
        return f"gen/{route}/{tpl}/main.{ext}"

def get_filter(ext):
    return f"{ext}min"

bundles = {
    "post": {
        "all": {
            "css": [get_bundle('post', 'all', 'css', ['css/blocks/table.css'])],
            "js": [get_bundle('post','all','js',['js/blocks/js1.js', 'js/blocks/js2.js','js/blocks/js3.js'])]
        },
        "create": {},
        "update": {},
    },
    "user": {
        "login": {},
        "register": {}
    },
}
#-*- coding:utf-8 -*-
from googletrans import Translator
import sys

#reload(sys)
#sys.setdefaultencoding( "utf-8" )

translator = Translator()
print(translator.translate('我').text)
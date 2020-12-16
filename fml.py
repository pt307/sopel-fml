"""
fml.py - Display a random FML from https://www.fmylife.com
Copyright 2020 Paul Townsend

https://sopel.chat
"""

import random
import re

import bleach
import requests
from lxml import etree

from sopel import formatting, module


PLUGIN = 'fml'

STRINGS = {
    'PLUGIN_ERROR': f"[{formatting.bold(PLUGIN)}:{formatting.underline('error')}] %s",
    'PLUGIN_MESSAGE': f"[{formatting.bold(PLUGIN)}] %s"
}

FML_URLS = (
    'https://www.fmylife.com/random',
    'https://www.fmylife.com/random/spicy'
)


@module.commands('fml')
def fml(bot, trigger):
    try:
        r = requests.get(url=random.choice(FML_URLS), timeout=(6.05, 3.0))
    except requests.exceptions.ConnectionError:
        return bot.say(STRINGS['PLUGIN_ERROR'] % ('a connection error occurred.'))
    except requests.exceptions.Timeout:
        return bot.say(STRINGS['PLUGIN_ERROR'] % ('the request timed out.'))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return bot.say(STRINGS['PLUGIN_ERROR'] % ('http error (' + str(e.response.status_code) + ')'))

    page = etree.HTML(r.content)
    fml = bleach.clean(re.sub('<h2 class="classic-title">.*<\\/h2>', '', etree.tostring(page.xpath(
        '//*[@id="content"]/div/div[1]/div/article[1]/div/div[2]/a')[0], encoding='unicode')), tags=[], strip=True)

    bot.say(STRINGS['PLUGIN_MESSAGE'] % fml.lstrip())

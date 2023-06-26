# -*- coding: utf-8 -*-

import logging
from completor import Completor, vim

logger = logging.getLogger('completor')


_cache = {}

class Vsnip(Completor):
    filetype = 'vsnip'
    sync = True

    @staticmethod
    def _snippets():
        bufnr = vim.Function('bufnr')()
        vsnip_snippets = vim.Function('vsnip#get_complete_items')(bufnr)
        logger.info(repr(vsnip_snippets))
        snippets = []
        for item in vsnip_snippets:
            snippets.append({
                'word': item[b'word'],
                'dup': 1,
                'menu': item[b'menu']
            })
        snippets.sort(key=lambda x: x['word'])
        return snippets

    def parse(self, base):
        if not self.ft or not base or base.endswith((' ', '\t')):
            return []

        if self.ft not in _cache:
            try:
                _cache[self.ft] = self._snippets()
            except Exception as e:
                logger.info('========== Exception ==========')
                logger.info(repr(e))
                _cache[self.ft] = []

        token = self.input_data.split()[-1]
        candidates = [dict(item) for item in _cache[self.ft]
                      if item['word'].startswith(token.encode('utf-8'))]
        logger.info(candidates)

        offset = len(self.input_data) - len(token)
        for c in candidates:
            c['abbr'] = c['word']
            c['offset'] = offset
        return candidates

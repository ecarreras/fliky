#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, url_for
from dulwich.repo import Repo

app = Flask(__name__)

#TODO outside from here, maybe fliky/backend/git.py
def get_or_init_repo(name='content'):
    if not os.path.exists(name):
        repo = Repo.init(name, mkdir=True)
    elif not os.path.exists(name + os.sep + '.git'):
        repo = Repo.init(name)
    else:
        repo = Repo(name)
    return repo

@app.route('/')
@app.route('/<path:wiki_page>')
def index(wiki_page=False):
    if not wiki_page:
        wiki_page = 'index.md'
    else:
        wiki_page += os.sep + 'index.md'
    repo = get_or_init_repo()
    store_page = 'content' + os.sep + wiki_page
    if not repo.get_named_file(wiki_page):
        return notfound(wiki_page)
    return 'Hello World! on %s (store_page:%s)' % (wiki_page, store_page)

def notfound(wiki_page):
    return 'Page %s not found. %s' % (wiki_page, url_for('edit', wiki_page=wiki_page))

@app.route('/edit/<path:wiki_page>')
def edit(wiki_page='index'):
    return 'Editing %s' % wiki_page

if __name__ == '__main__':
    app.run(debug=True)

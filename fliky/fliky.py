#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import os

from flask import Flask, url_for, render_template, request, redirect
from utils.git import *

app = Flask(__name__)

REPO = '/Users/eduard/Desktop/fliky'

exists = os.path.exists

@app.route('/')
@app.route('/<path:wiki_page>/')
def index(wiki_page='Main'):
    if not exists('%s/.git' % REPO):
        git_init(REPO)
    if not exists('%s/%s' % (REPO, wiki_page)):
        return notfound(wiki_page)
    content = open('%s/%s/index.rst' % (REPO, wiki_page)).read() 
    return render_template('view.html', content=content, wiki_page=wiki_page)

@app.errorhandler(404)
def notfound(wiki_page):
    return render_template('notfound.html', wiki_page=wiki_page, 
                           create_url=url_for('edit', wiki_page=wiki_page))

@app.route('/edit/<path:wiki_page>/', methods=['GET', 'POST'])
def edit(wiki_page='index'):
    if request.method == 'POST':
        try:
            if not exists('%s/%s' % (REPO, wiki_page)):
                os.makedirs('%s/%s' % (REPO, wiki_page))
            with open('%s/%s/index.rst' % (REPO, wiki_page), 'w') as wikip:
                wikip.write(request.form['text'])
            git_add('%s/index.rst' % wiki_page)
            git_commit(request.form['msg'], 'Eduard Carreras <ecarreras@gmail.com>')
            return redirect(url_for('index', wiki_page=wiki_page))
        except:
            return render_template('error.html')
    else:
        content = ''
        if exists('%s/%s' % (REPO, wiki_page)):
            content = open('%s/%s/index.rst' 
                % (REPO, wiki_page)).read()
    	return render_template('edit.html', wiki_page=wiki_page,
            content=content)


if __name__ == '__main__':
    app.run(debug=True)

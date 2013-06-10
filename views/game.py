# -*- coding: utf-8 -*-
"""
    game
    ~~~~~~

    「遊樂場」的部份

"""


from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# 資料庫相關
from model.GameObj import DbGame

game = Blueprint('game', __name__)

@game.route('/center')
def center():
    '''
    進到GameCenter
    '''
    try:
    	return render_template('game/center.html')
    except TemplateNotFound:
        abort(404)

@game.route('/<int:id>')
def enterGame(id):
    '''
    進入遊戲
    '''
    #檢查是否能玩此遊戲
    game_ = DbGame.query.filter_by(serial=id).first()
    if game_ is None:
        abort(404)
        return "sss"

    #啟動遊戲
    #game_ = {'id':id, 'name': u"找字測驗"}
    return render_template('game/game.html',game=game_)

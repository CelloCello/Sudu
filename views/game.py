# -*- coding: utf-8 -*-
"""
    game
    ~~~~~~

    「遊樂場」的部份

"""


from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask import g
from jinja2 import TemplateNotFound

# 資料庫相關
from model.extensions import db
from model.GameObj import DbGame

game = Blueprint('game', __name__)

@game.route('/center')
def center():
    '''
    進到GameCenter
    '''
    try:
        gameList_ = DbGame.query.all()
    	return render_template('game/center.html',games=gameList_)
    except TemplateNotFound:
        abort(404)

@game.route('/<int:id>')
def enterGame(id):
    '''
    進入遊戲
    '''
    #檢查有無登入
    if g.user == None:
        #沒登入就回到登入頁面
        flash(u"Please login!")
        return redirect(url_for('index'))

    #檢查是否能玩此遊戲
    game_ = DbGame.query.filter_by(serial=id).first()
    if game_ is None:
        abort(404)
        return "NG"

    if g.user.scoin < game_.cost:
        g.user.scoin = g.user.scoin + 1
        db.session.commit()
        flash(u"You don't have enough money")
        return redirect(url_for('game.center'))

    # 扣錢
    g.user.scoin = g.user.scoin - game_.cost
    db.session.commit()    

    #啟動遊戲
    #game_ = {'id':id, 'name': u"找字測驗"}
    return render_template('game/game.html',game=game_)

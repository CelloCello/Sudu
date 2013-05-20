#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import urllib

def https_send(ip, url_path, params, method='GET'):

    ec_params = urllib.urlencode(params)

    conn = httplib.HTTPSConnection(ip)

    method = method.upper()

    if method == 'GET':
        url = '%s?%s' % (url_path, ec_params)
        conn.request(method, url)
    else:
        conn.request(method, url_path, ec_params)

    rsp = conn.getresponse()

    if rsp.status != 200:
        raise ValueError, 'status:%d' % rsp.status
    data = rsp.read()

    return data

def get_image_type(pd, is_path=True):
    '''
    获取图片的类型，支持传入路径和文件内容
    '''
    if is_path:
        f = file(pd, 'rb')
        data = f.read(10).encode('hex')
    else:
        data = pd.encode('hex')

    ftype = None

    if data.startswith('ffd8'):
        ftype = 'jpeg'
    if data.startswith('424d'):
        ftype = 'bmp'
    if data.startswith('474946'):
        ftype = 'gif'
    elif data.startswith('89504e470d0a1a0a'):
        ftype = 'png'

    return ftype

def check2mkdir(dir_path):
    import os

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

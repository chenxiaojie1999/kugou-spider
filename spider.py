# -- coding: utf-8 --**
# @Author     : Bonnie
# @Time       : 2022/8/30 16:07
# @FileName   : spider.py
# @Description:
import json
import pprint

import parsel  # 数据解析模块
import requests
import re


def get_response(html_url):
    """

    :param html_url:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    response = requests.get(url=html_url, headers=headers)
    return response


def get_list_url(html_url):
    """
    获取榜单url
    :param html_url:
    :return:
    """
    response = get_response(html_url)
    selector = parsel.Selector(response.text)
    list_name_list = selector.css('.pc_rank_sidebar li a::attr(title)').getall()
    href = selector.css('.pc_rank_sidebar li a::attr(href)').getall()
    list_info = zip(list_name_list, href)
    # list_url = re.findall('<a title="(.*?)"  hidefocus="true" href="(.*?)"', response.text)  # 正则表达式
    # print(list_url)
    # print(len(list_url))
    return list_info


def get_music_id(html_url):
    """
    获取音频的hash、id参数
    :param html_url:
    :return:
    """
    response = get_response(html_url)
    Hash_List = re.findall('"Hash":"(.*?)"', response.text)
    album_id_list = re.findall('"album_id":(\d+)', response.text)
    # print(Hash_List)
    # print(album_id_list)
    music_id_list = zip(Hash_List, album_id_list)
    return music_id_list


def get_music_info(Hash, music_id):
    """
    获取音乐url 以及 音乐的标题
    :param html_url:
    :return:
    """
    link_url = f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={Hash}&dfid=4XSW703rDwgc1UmDsV27WjuP&appid=1014&mid=87b024e80e2cf1ff5054da28f370706c&platid=4&album_id={music_id}&_=1661933520109'

    response = get_response(html_url=link_url)
    # print(response.text)
    # pprint.pprint(response.json())
    title = response.json()['data']['audio_name']
    play_url = response.json()['data']['play_url']
    music_info = [title, play_url]
    return music_info


def save(title, play_url):
    """
    保存数据
    :param title:
    :param play_url:
    :return:
    """
    music_content = get_response(html_url=play_url).content  # 获取音乐的二进制内容
    with open('music\\' + title + '.mp3', mode='wb') as f:
        f.write(music_content)
        print(title, '保存成功')


def main(html_url):
    list_url = get_list_url(html_url=html_url)
    for list_name, link in list_url:
        print(f'---------正在爬取{list_name}--------')
        music_id_list = get_music_id(html_url=link)
        for Hash, music_id in music_id_list:
            music_info = get_music_info(Hash, music_id)
            save(music_info[0], music_info[1])
            # print(list_name, link)


if __name__ == '__main__':
    url = 'https://www.kugou.com/yy/html/rank.html'
    main(url)

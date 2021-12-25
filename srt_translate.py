import codecs
import re
import urllib.request
import sys
import os
import copy
import shutil
from google.cloud import translate
# from googletrans import Translator
from py_translator import Translator


def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def vpn_free_translate_text(text, dest='zh-CN'):
    '''
    需要科学上网，但是可以白嫖，是否被封全看运气
    :param text:
    :param dest:
    :return:
    '''
    result = Translator().translate(text=text, dest=dest).text
    return result


def vpn_GCP_translate_text(text, target_language="cn"):
    # [START translate_translate_text]
    """
    翻墙申请Google cloud platform后使用提供的api，可以免费使用一年
    Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target_language)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    return result
    # [END translate_translate_text]


def translate(content):
    '''
    不用科学上网，免费翻译，但是超过google设置的限制后就会被封
    :param content:
    :return:
    '''
    content = urllib.request.quote(content)
    url = "http://translate.google.cn/translate_a/single?client=gtx" \
          "&sl=en&tl=zh-CN&hl=EN&dt=t&q=%s" % content
    result = open_url(url)
    result = result.split(r'","')
    result.pop()
    texts = ''
    for ite in result:
        lst = ite.rfind(r'"')
        texts += ite[lst + 1::]
    return texts


def writefile(tran, tranlist):
    file = codecs.open(r"%s" % tran, 'w+', encoding='utf-8')
    for item in tranlist:
        item.replace(u'\xa0', u' ')
        file.write(item)
        file.write('\n')
    file.close()
    # input('文件保存完毕: %s\n按回车键退出' % tranfile)
    # exit()


def append_ori_text(origin, _index, _ori_text="", _time_zone=""):
    if bool(re.search("^([0-9]{2}:[0-9]{2}:[0-9]{2}).*?([0-9])$", origin[_index])):  # 当前行是时间戳
        _time_zone = origin[_index]
        _index += 1
        _ori_text = origin[_index]
        # 假设文字不止一行，但不超过三行
        detect_line_feeds_words = copy.deepcopy(origin[_index+1:_index+3])
        for next_line in detect_line_feeds_words:
            if bool(re.search(("\S"), next_line)): # 证明英文不止一行,所以将之前的一起拼接上
                _ori_text += " " + next_line
                _index += 1
                continue
            break
    # elif bool(re.search("^[1-9]\d*$"), origin[_index]):  # 当前行是数字标识符
    #     _ori_text = origin[_index]
    #     _index += 1
    else:
        _index += 1
    return _index, _ori_text, _time_zone


def translate_single_file_and_override_file(srtfile):
    origin = []
    tranlist = []
    try:
        testf = open(r"%s" % srtfile, 'r')
        testf.close()
    except FileNotFoundError:
        input('There in no such file in such directory\n文件路径或文件不存在!'
              '\nEnter to exit\n回车键退出')
        exit()
    with codecs.open(r"%s" % srtfile, 'r', encoding='utf-8') as f:
        try:
            for line in f:
                origin.append(line[0:-1].replace('\r', ''))
            origin.append("")
        except UnicodeDecodeError:
            input('编码错误 非utf-8,尚未支持,请用Notepad++或其他软件转换')
            exit()
        print('文件加载完毕...')

        print("翻译开始")
        if len(origin) <= 20:
            percent = len(origin)
            per = 100
        else:
            percent = len(origin) // 20 + 1
            per = 5

        symbol = "==>  "
        index = 0
        tranlist.append(origin[0])
        while index < len(origin) - 1:
            if index >= percent:
                symbol = "==" + symbol
                print(symbol + str(per) + '%')
                percent += len(origin) // 20 + 1
                per += 5

            index, ori_text, time_zone = append_ori_text(origin, index)
            if ori_text == '' and time_zone == '':
                tranlist.append(origin[index])
                continue

            long_sentences_size = 0
            ori_texts = []
            time_zones = []
            has_loop_once = False
            ori_long_text = ""
            while bool(re.search("(\,|-|[a-z])$", ori_text)):  # 是长句，需要拼接
                if not has_loop_once:
                    tranlist.pop()
                    ori_texts.append(ori_text)
                    time_zones.append(time_zone)
                    ori_long_text += ori_text

                index, ori_text, time_zone = append_ori_text(origin, index, _ori_text=ori_text)
                has_loop_once = True
                if time_zone == '':  # 空行
                    continue
                ori_texts.append(ori_text)
                time_zones.append(time_zone)
                long_sentences_size += 1
                ori_long_text += ori_text

            if long_sentences_size == 0:
                ori_long_text = ori_text

            try:
                # translate_text = translate(ori_long_text)
                translate_text = vpn_free_translate_text(ori_long_text)
            except urllib.error.URLError:
                input('翻译未成功(可能已经遭Google封禁) 按回车退出')
                exit()

            if long_sentences_size == 0:
                tranlist.append(ori_text)
                tranlist.append(translate_text)
            else:  # 英文长句切分
                translate_texts = translate_text.split(sep="，", maxsplit=long_sentences_size)
                if len(translate_texts) == len(time_zones):
                    values = zip(time_zones, ori_texts, translate_texts)
                    for value in values:
                        tranlist.append(value[0])
                        tranlist.append(value[1])
                        tranlist.append(value[2] + ",")
                        tranlist.append('')
                    tranlist[-2] = tranlist[-2][:-1]  # 去掉最后一句话中文逗号
                elif len(translate_texts) < len(time_zones):  # 翻译出来的中文语句少于是时间轴数目
                    trans_index = 0
                    while trans_index < len(time_zones):
                        tranlist.append(time_zones[trans_index])
                        tranlist.append(ori_texts[trans_index])
                        if trans_index <= len(translate_texts)-1:
                            tranlist.append(translate_texts[trans_index])
                        tranlist.append('')
                        trans_index += 1


        symbol = "==" + symbol
        print(symbol + '100%  当前文件翻译完毕...')

        print('即将写入文件: %s' % srtfile)
        try:
            testf = open(r"%s" % srtfile, 'r')
            testf.close()
            writefile(srtfile, tranlist)
        except FileNotFoundError:
            writefile(srtfile, tranlist)


if __name__ == "__main__":
    ver = 'beta'
    print('Srt/Vtt Translation Tool with google translation\nsrt字幕谷歌翻译软件\nver. %s' % ver)
    srtfile = input('\n请输入srt/ vtt 字幕文件的完整路径,e.g. D:\BaiduNetdiskDownload\V1-W2R32yXgwcg.en.srt \n')
    # srtfile = "D:\BaiduNetdiskDownload\AI量化投资\AI for Trading v1.0.0\Part 01-Module 01-Lesson 01_Welcome to the Nanodegree Program\\03. M1L1 Introducing The Instructors 1 V4-l5gG7r-BWYc.en.vtt"

    translate_files = []
    if os.path.isdir(srtfile):
        for root, dirs, files in os.walk(srtfile, topdown=False):
            for name in files:
                if bool(re.search("(.vtt)$", name)) or bool(re.search("(.srt)$", name)):
                    if bool(re.search("backup", root)):
                        continue
                    ori_file = os.path.join(root, name)
                    translate_files.append(ori_file)
                    # 备份
                    backup_dir = os.path.join(root, "backup")
                    if not os.path.exists(backup_dir):
                        os.mkdir(backup_dir)
                    if not os.path.exists(os.path.join(backup_dir, name)):
                        print("已将文件%s备份到目录%s下" % (name, backup_dir))
                        shutil.copy(ori_file, os.path.join(backup_dir, name))
    elif os.path.isfile(srtfile):
        if not bool(re.search("(.vtt)$", srtfile)) and not bool(re.search("(.srt)$", srtfile)):
            print("当前文件格式不支持")
            exit()
        file_spilt = srtfile.split(sep=".")
        backup_file = file_spilt[0] + "_backup." + file_spilt[1]
        if not os.path.isfile(backup_file):
            print("当前文件已备份为：%s"%backup_file)
            shutil.copy(srtfile, backup_file)
        translate_files.append(srtfile)

    for single_need_tranlsate_file in translate_files:
        print("当前正在翻译：%s"%single_need_tranlsate_file)
        translate_single_file_and_override_file(single_need_tranlsate_file)
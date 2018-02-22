import codecs
import re
import urllib.request
import sys


def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def translate(content):
    content = urllib.request.quote(content)
    url = "http://translate.google.cn/translate_a/single?client=gtx" \
          "&sl=en&tl=zh-CN&hl=EN&dt=t&q=%s" % content
    result = open_url(url)
    end = result.find("\",")
    if end > 4:
        texts = result[4:end]
    return texts


def writefile(tran):
    file = codecs.open(r"%s" % tran, 'w+', encoding='utf-8')
    for item in tranlist:
        item.replace(u'\xa0', u' ')
        file.write(item)
        file.write('\n')
    file.close()
    input('文件保存完毕: %s\n按回车键退出' % tranfile)
    exit()


if __name__ == "__main__":
    ver = 'alpha'
    origin = []
    tranlist = []
    print('Srt Translation Tool with google translation\nsrt字幕谷歌翻译软件\nver. %s' % ver)
    srtfile = input('\n请输入srt字幕文件的完整路径'
                    '\ne.g.\tC:\\Users\\Administrator\\Desktop\\test.srt\n')
    try:
        testf = open(r"%s" % srtfile, 'r')
        testf.close()
    except FileNotFoundError:
        input('Their in no such file in such directory\n文件路径或文件不存在!'
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
            percent = len(origin) // 20
            per = 5
        for x in origin:
            if origin.index(x) >= percent:
                print(str(per) + '%')
                percent += len(origin) // 20
                per += 5
            if bool(re.search("\d\d:\d\d:\d\d,\d\d\d", x)):
                current = origin.index(x) + 1
                start = current - 2
                cnt = 0
                text = ''
                while origin[current] != "":
                    if cnt != 0:
                        if origin[current][0] != " " and text[-1] != " ":
                            text += " "
                    text += origin[current]
                    cnt = 1
                    current += 1
                results = ''
                try:
                    results = translate(text)
                except urllib.error.URLError:
                    input('翻译未成功 请检查网络连接 按回车退出')
                    exit()
                tranlist.extend(origin[start:start + 2])
                tranlist.append(text)
                tranlist.append(results)
                tranlist.append("")
        print('翻译完毕...')

        tranfile = srtfile[0:-4] + "_translation.srt"
        print('即将写入文件: %s' % tranfile)
        try:
            testf = open(r"%s" % tranfile, 'r')
            testf.close()
            exist = 1
        except FileNotFoundError:
            writefile(tranfile)
        if exist == 1:
            print('此处已经有目标文件:%s' % tranfile)
            input_choice = input('\n覆盖原有文件吗?\n[y/n]:')
            if input_choice == 'y':
                writefile(tranfile)
            else:
                input('请将此文件拷贝至其他目录后回车')
                print('即将写入文件: %s' % tranfile)
                input('如原有文件未备份导致数据损失概不负责 确认请按回车')
                writefile(tranfile)

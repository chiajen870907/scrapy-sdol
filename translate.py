#conding:utf8


import requests



class Translate(object):
    def __init__(self):
        self.ok = 'ok'


    def en2ch(self, q):
        import urllib.request
        from HandleJs import Py4Js
        # 利用 谷歌翻译 爬虫 进行翻译
        #  http://blog.csdn.net/yingshukun/article/details/53470424
        content =  q
        js = Py4Js()
        tk = js.getTk(content)
        if len(content) > 4891:
            print("翻译的长度超过限制！！！")
            return

        param = {'tk': tk, 'q': content}

        result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en
                &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
                &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)

        # 返回的结果为Json，解析为一个嵌套列表
        rst = ''
        for ii in range(0, len(result.json()[0]) - 1):
            rst = rst + result.json()[0][ii][0]

        return rst


# 主程序
if __name__ == "__main__":
    # 实例化爬虫
    trans = Translate()

    # 翻译
    q = "The mechanism investigation of ultrasonic roller dressing vitrified bonded CBN grinding wheel"
    print(trans.en2ch(q))
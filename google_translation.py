import time
import urllib.request
import urllib.parse
import json
import re
import requests
import difflib


LANGUAGE = {
    'af': 'af', 'sq': 'sq', 'am': 'am', 'ar': 'ar', 'hy': 'hy', 'az': 'az', 'eu': 'eu', 'be': 'be', 'bn': 'bn',
    'bs': 'bs', 'bg': 'bg', 'ca': 'ca', 'ceb': 'ceb', 'ny': 'ny', 'zh_ch': 'zh-CH', 'zh_cn': 'zh-CH',
    'zh_tw': 'zh_tw', 'co': 'co', 'hr': 'hr', 'cs': 'cs', 'da': 'da', 'nl': 'nl', 'en': 'en', 'eo': 'eo',
    'et': 'et', 'tl': 'tl', 'fi': 'fi', 'fr': 'fr', 'fy': 'fy', 'gl': 'gl', 'ka': 'ka', 'de': 'de', 'el': 'el',
    'qu': 'gu', 'ht': 'ht', 'ha': 'ha', 'haw': 'haw', 'iw': 'iw', 'hi': 'hi', 'hmn': 'hmn', 'hu': 'hu',
    'is': 'is', 'ig': 'ig', 'id': 'id', 'ga': 'ga', 'it': 'it', 'ja': 'ja', 'jw': 'jw', 'kn': 'kn',
    'kk': 'kk', 'km': 'km', 'ko': 'ko', 'ku': 'ku', 'ky': 'ky', 'lo': 'lo', 'la': 'la', 'lv': 'lv', 'lt': 'lt',
    'lb': 'lb', 'mk': 'mk', 'mg': 'mg', 'ms': 'ms', 'ml': 'ml', 'mt': 'mt', 'mi': 'mi', 'mr': 'mr', 'mn': 'mn',
    'my': 'my', 'ne': 'ne', 'no': 'no', 'ps': 'ps', 'fa': 'fa', 'pl': 'pl', 'pt': 'pt', 'ma': 'ma', 'ro': 'ro',
    'ru': 'ru', 'sm': 'sm', 'gd': 'gd', 'sr': 'sr', 'st': 'st', 'sn': 'sn', 'sd': 'sd', 'si': 'si', 'sk': 'sk',
    'sl': 'sl', 'so': 'so', 'es': 'es', 'su': 'su', 'sw': 'sw', 'sv': 'sv', 'tg': 'tg', 'ta': 'ta', 'te': 'te',
    'th': 'th', 'tr': 'tr', 'uk': 'uk', 'ur': 'ur', 'uz': 'uz', 'vi': 'vi', 'cy': 'cy', 'xh': 'xh', 'yi': 'yi',
    'yo': 'yo', 'zu': 'zu', 'auto': 'auto'
}


class GoogleTrans:
    def __init__(self):
        self.url = 'https://translate.google.com.hk/translate_a/single'
        self.TKK = "434674.96463358"  # 这个值可能需要定期更新

        # HTTP请求头
        self.header = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "NID=188=M1p_rBfweeI_Z02d1MOSQ5abYsPfZogDrFjKwIUbmAr584bc9GBZkfDwKQ80cQCQC34zwD4ZYHFMUf4F59aDQLSc79_LcmsAihnW0Rsb1MjlzLNElWihv-8KByeDBblR2V1kjTSC8KnVMe32PNSJBQbvBKvgl4CTfzvaIEgkqss",
            "referer": "https://translate.google.com.hk/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "x-client-data": "CJK2yQEIpLbJAQjEtskBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQ==",
        }

        # 翻译请求的参数
        self.data = {
            "client": "webapp",  # 基于网页访问服务器
            "sl": "auto",  # 源语言, auto 表示由谷歌自动识别
            "tl": "zh-CN",  # 翻译的目标语言
            "hl": "zh-CN",  # 界面语言选中文
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],  # dt表示要求服务器返回的数据类型
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "kc": "1",
            "tk": "",  # 谷歌服务器会核对的token
            "q": ""  # 待翻译的字符串
        }

    def update_TKK(self):
        """更新TKK值的方法"""
        url = "https://translate.google.com.hk/"
        req = urllib.request.Request(url=url, headers=self.header)
        page_source = urllib.request.urlopen(req).read().decode("utf-8")
        self.TKK = re.findall(r"tkk:'([0-9]+\.[0-9]+)'", page_source)[0]

    def construct_url(self):
        """构建请求URL的方法"""
        base = self.url + '?'
        for key in self.data:
            if isinstance(self.data[key], list):
                base = base + "dt=" + "&dt=".join(self.data[key]) + "&"
            else:
                base = base + key + '=' + self.data[key] + '&'
        base = base[:-1]
        return base

    def generate_token(self, text, tkk):
        """计算谷歌翻译的tk参数"""
        def uo(a, b):
            for c in range(0, len(b) - 2, 3):
                d = b[c + 2]
                d = ord(d) - 87 if 'a' <= d else int(d)
                d = a >> d if b[c + 1] == '+' else a << d
                a = (a + d & 4294967295) if b[c] == '+' else a ^ d
            return a

        d = tkk.split('.')
        b = int(d[0])
        e = []
        for g in range(len(text)):
            l = ord(text[g])
            if l < 128:
                e.append(l)
            elif l < 2048:
                e.append(l >> 6 | 192)
                e.append(l & 63 | 128)
            elif 55296 == (l & 64512) and g + 1 < len(text) and 56320 == (ord(text[g + 1]) & 64512):
                l = 65536 + ((l & 1023) << 10) + (ord(text[g + 1]) & 1023)
                e.append(l >> 18 | 240)
                e.append(l >> 12 & 63 | 128)
                e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
                g += 1
            else:
                e.append(l >> 12 | 224)
                e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)

        a = b
        for f in range(len(e)):
            a += e[f]
            a = uo(a, "+-a^+6")
        a = uo(a, "+-3^+b+-f")
        a ^= int(d[1])
        if a < 0:
            a = (a & 2147483647) + 2147483648
        a %= 1E6
        return "{}.{}".format(int(a), int(a) ^ b)

    def query(self, q, lang_to=''):
        """发送翻译请求的方法"""
        # 清理输入字符串
        q = re.sub(r'''[^\u2E80-\u9FFF \n\t\w_.!'"“”`+-=——,$%^，。？、~@#￥%……|[\]&\\*《》<>「」{}【】()/]''', '', q)
        retry = 2
        while retry > 0:
            try:
                print(q)
                self.data['q'] = urllib.parse.quote(q)
                self.data['tk'] = self.generate_token(q, self.TKK)
                if lang_to:
                    self.data['tl'] = lang_to
                url = self.construct_url()
                # print(url, self.header)
                re_obj = requests.post(url, headers=self.header)
                response = json.loads(re_obj.text)
                target_text = ''
                for item in response[0]:
                    if item[0]:
                        target_text += item[0]
                # originalText = response[0][0][1]
                # originalLanguageCode = response[2]
                # originalText, originalLanguageCode
                # print(response[8])
                return target_text, response[2], re_obj.status_code
            except Exception as e:
                print(e)
                retry -= 1
                time.sleep(1)
        return "", False, False


def health():
    start_time = time.time()
    gs = GoogleTrans()
    tgt_string, _l, _c = gs.query('test test')
    end_time = time.time()
    if tgt_string and _c == 200:
        return end_time - start_time
    else:
        return -1


def translate(_data):

    msg_id = _data.get('msgId')
    src_content = _data.get('srcContent')
    language_from = _data.get('languageFrom')
    language_to = _data.get('languageTo')
    src_decrypted_content = _data.get('srcDecryptedContent')
    server_msg_id = _data.get('serverMsgId')
    task_id = _data.get('taskId')
    name_list = _data.get('nameList')

    gs = GoogleTrans()
    language_from = language_from.lower() if language_from else None
    language_to = language_to.lower() if language_to else None

    if language_to is None:
        _language_to = LANGUAGE['zh_cn']
    elif language_to not in LANGUAGE:
        return {'code': 200, 'msg': '语言不支持', 'data': {'msgId': msg_id, 'status': -1}}
    else:
        _language_to = LANGUAGE[language_to]

    gs.data['tl'] = _language_to

    if src_decrypted_content:
        src_decrypted_content = src_decrypted_content.strip()

    if not src_decrypted_content:
        return {'code': 200, 'msg': '内容不能为空', 'data': {'msgId': msg_id, 'status': -1}}

    if language_from and language_from in LANGUAGE:
        gs.data['sl'] = LANGUAGE[language_from]

    is_chinese = string_chinese(src_decrypted_content)

    if is_chinese:
        src_decrypted_content = (src_decrypted_content.
                                 replace("Chainless", "\n\"Chainless\"\n").replace("SimiTalk", "\n\"SimiTalk\"\n"))

    url_dict = extract_urls(src_decrypted_content)

    tgt_string, auto_from, _code = gs.query(src_decrypted_content)

    if is_chinese:
        # print('******\n', tgt_string, '******\n')
        tgt_string = re.sub("chainless", "Chainless", tgt_string, flags=re.IGNORECASE)
        tgt_string = re.sub("simitalk", "SimiTalk", tgt_string, flags=re.IGNORECASE)
        tgt_string = (tgt_string.replace("\n\"Chainless\"\n", " Chainless ").replace("\n\"SimiTalk\"\n", " SimiTalk ").
                      replace("\"Chainless\"\n", " Chainless ").replace("\"SimiTalk\"\n", " SimiTalk ").
                      replace("\n\"Chainless\"", " Chainless ").replace("\n\"SimiTalk\"", " SimiTalk "))

    if url_dict:
        over_url_dict = extract_urls(tgt_string)
        for _u in over_url_dict.keys():
            closest_match = difflib.get_close_matches(_u, url_dict.keys(), n=1)
            tgt_string = tgt_string.replace(_u, url_dict[closest_match[0]])

    if auto_from:
        language_from = auto_from

    if tgt_string and _code == 200:
        re_data = {
            "msgId": msg_id, "srcContent": src_content, "serverMsgId": server_msg_id,
            "srcDecryptedContent": src_decrypted_content,
            "languageFrom": language_from, "languageTo": language_to,
            "dstContent": tgt_string, "dstLength": len(str(tgt_string)),
            "status": 0, "taskId": task_id, "nameList": name_list,
            "recode": _code,
        }

        return {'code': 200, 'msg': 'success', 'data': re_data}
    else:
        return {'code': 500, 'msg': '翻译失败', 'data': {'msgId': msg_id, 'status': -1}}


def is_can_translate(_data):
    pattern = r'^[a-zA-Z0-9\u4e00-\u9fff\u3000-\u303f\u2000-\u206f\u0020-\u007e\uff00-\uffef]+$'
    return bool(re.match(pattern, _data))


def is_can_translate_d(_data):
    if _data != '。':
        return True
    return False


def concurrent_test(text):
    _text = ""
    replace_dict = {}
    num = 0
    for _ in text:
        if _ and is_can_translate(_) and _ != " ":
            _text += _
        else:
            symbol = f"[& {num} &]"
            num += 1
            _text += symbol
            replace_dict[symbol] = _
    return _text, replace_dict


def replace_str(_text, s_dict):
    for _k, _v in s_dict.items():
        _text = _text.replace(_k, _v)
    return _text


def run_test():
    st = time.time()
    test_model = "gpt-4o-mini"  # 模型名称，你的自定义模型
    test_message = test_text.ko_500
    ask_data = {
        'msgId': "",
        'srcContent': "",
        'languageFrom': "auto",
        'languageTo': "en",
        'srcDecryptedContent': test_message,
        'serverMsgId': "",
        'num': 100
    }
    results = translate(ask_data)
    print("cost time:", time.time() - st, "\nword num:", len(test_message))
    print(results)


def is_all_chinese_and_symbols(s):
    pattern = r'^[\u4e00-\u9fa5\u3000-\u303F\uFF00-\uFFEF]+$'
    return bool(re.match(pattern, s))


def string_chinese(in_put):
    in_put = in_put.replace("Chainless", "").replace("SimiTalk", "")
    _len = len(in_put)
    _cn = 0
    for _i, _s in enumerate(in_put):
        if is_all_chinese_and_symbols(_s):
            if _i == 0:
                _cn += _len / 4
            _cn += 1
    if _cn >= _len / 2:
        return True
    return False


def extract_urls(text):
    # 定义正则表达式模式，匹配 http、https 和 www 开头的 URL
    url_pattern = r'https?://[^\s]+|www\.[^\s]+'
    re_dict = {}
    # 使用 re.findall() 提取所有匹配的 URL
    urls = re.findall(url_pattern, text)
    for url in urls:
        re_dict[url.lower()] = url
    return re_dict


if __name__ == "__main__":
    test = """
武当山驻少林寺办事处王喇嘛
"""
    t2 = "你在干什么"
    print(len(test))
    ask_data = {
        'msgId': "",
        'srcContent': "",
        'languageFrom': "",
        'languageTo': "en",
        'srcDecryptedContent': test,
        'serverMsgId': "",
        'num': 100
    }
    for _ in range(5):
        print(11111, translate(ask_data)['data'])


    def chat_completion(model="gpt-4o-mini", stream=True):

        url = 'http://127.0.0.1:8080/v1/chat/completions'  # 替换成你的 API 地址
        headers = {
            'Content-Type': 'application/json'
        }

        in_put = f"请帮我生成一段50到200字的英文文本 要求中间有1-10个换行"
        # 请求的数据
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": in_put}
            ],
            "stream": stream
        }

        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=False)
        response.encoding = 'utf-8'

        # 用于存储处理后的响应内容
        result = []

        if stream:
            # 如果是流式响应，逐行处理
            for chunk in response.iter_lines():
                if chunk:
                    # 去掉开头的空格和换行符
                    chunk_data = chunk.decode('utf-8').strip()

                    # 检查是否是结束信号
                    if chunk_data == "data: [DONE]":
                        break

                    # 确保是以 data: 开头的有效行
                    if chunk_data.startswith("data:"):
                        try:
                            # 移除 "data: " 前缀并解析 JSON 数据
                            chunk_json = json.loads(chunk_data[6:])
                            if 'choices' in chunk_json:
                                # 提取 content 部分并追加到结果列表
                                delta_content = chunk_json['choices'][0]['delta'].get('content', '')
                                result.append(delta_content)
                        except json.JSONDecodeError:
                            pass  # 忽略无法解析的行
        else:
            # 如果不是流式响应，直接处理完整的响应
            response_data = response.json()
            print(response_data)
            result.append(response_data['choices'][0]['message']['content'])

        # 返回完整的响应内容
        return ''.join(result)


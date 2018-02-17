# -*- coding: utf-8 -*-

"""

    baidu ocr

"""

from aip import AipOcr
import re


def get_text_from_image(image_data, app_id, app_key, app_secret, api_version=0, timeout=3):
    """
    Get image text use baidu ocr

    :param image_data:
    :param app_id:
    :param app_key:
    :param app_secret:
    :param api_version:
    :param timeout:
    :return:
    """
    client = AipOcr(appId=app_id, apiKey=app_key, secretKey=app_secret)
    client.setConnectionTimeoutInMillis(timeout * 1000)

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["recognize_granularity"] = "big"
    options["detect_language"] = "true"
    options["vertexes_location"] = "true"
    options["probability"] = "true"

    if api_version == 1:
        result = client.basicAccurate(image_data, options)
    else:
        result = client.general(image_data, options)

    if "error_code" in result:
        print("baidu api error: ", result["error_msg"])
        return ""

    return group_question_and_answer(result)

    # return [words["words"] for words in result["words_result"]]

def group_question_and_answer(result):
    answer_number = 3  # 每道题目三个答案
    content_list =  [words["words"] for words in result["words_result"]]
    txt_list = [words["words"] for words in result["words_result"]]
    location_list = [loc["location"] for loc in result["words_result"]]

    answer_list = []

    title = ''
    lines = len(content_list)
    if lines > (answer_number + 1):
        title = '\n'.join(content_list[:lines - answer_number])
    else:
        title = content_list[0]

    answer_list = content_list[-3:]

    # 去掉空白字符（空格、换行、制表符等）
    title = re.sub('\s', '', title)
    ask = title.endswith('?') or title.endswith('？')
    if not ask:
        title += '?'

    # 对识别后的文字进行处理
    # 去掉题目序号
    # title = re.sub("^\d+['.]*", '', title)
    answer_list.insert(0, title)
    return answer_list

def group_question_and_answer_v2(result):
    content_list = [words["words"] for words in result["words_result"]]
    location_list = [loc["location"] for loc in result["words_result"]]
    return content_list
import requests
from jsonpath import jsonpath
import stylecloud
from PIL import Image
import re
import jieba

def combine_list(path):
    list1= read_as_list("bp_clean_comment_list1.txt")
    list2= read_as_list("bp_clean_comment_list2.txt")
    list3= read_as_list("bp_clean_comment_list3.txt")
    list4= read_as_list("bp_clean_comment_list4.txt")
    list1.extend(list2)
    list1.extend(list3)
    list1.extend(list4)
    save_list(list1,  path)

def read_as_list(path):
    with open(path, 'r') as f:
        comment = f.read()
    return comment.split("\n")

def save_list(cmt_list, path):
    with open(path, 'w') as f:
        for cmt in cmt_list:
            f.write(cmt + "\n")
    return True

def parse_cy_img(comment_list):
    print("--------词云图生成中--------")
    data = "".join(comment_list)
    stylecloud.gen_stylecloud(data, font_path="/System/Library/Fonts/PingFang.ttc")
    img = Image.open("./stylecloud.png")
    img.show()
    print("词云图已生成")

def worm():
    it = 188
    comment_list = []
    while True:
        try:
            print(it)
            start_url = "https://api.bilibili.com/x/v2/reply/main?csrf=04fc84f031a0a75e0e28dcb5da57ad30&mode=3&next={}&oid=968828987&plat=1&seek_rpid=&type=1".format(it)
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "referer": r"https://www.bilibili.com/video/BV1ep4y1S76z?spm_id_from=333.337.search-card.all.click&vd_source=09f4875e8204354f43a5213249ce7e48"

            }
            response=requests.get(start_url, headers).json()
            print(response)
            replies = jsonpath(response, "$..replies")[0]
            message_list = jsonpath(replies, '$..message')
            comment_list.extend(message_list)
            it += 1
            if it == 10000:
                break
        except:
            print("Worm Ending")
            break
    print(comment_list)
    save_list(comment_list, "bp_comment_list4.txt")
    #parse_cy_img(comment_list)

def get_indexs(my_str, tar):
    str_indexs = []
    it = 0
    while it < len(my_str):
        try:
            nxt_ind = my_str.index(tar, it)
            it = nxt_ind + 1
        except:
            break
        str_indexs.append(nxt_ind)
    return str_indexs

def data_cleaning(file_path):
    comment_list = read_as_list(file_path)
    # 去除文字中的"回复"
    for i in range(len(comment_list)):
        if "回复" in comment_list[i] and ":" in comment_list[i]:
            try:
                std_it = comment_list[i].index("回复")
                end_it = comment_list[i].index(":")
                # print(std_it, end_it)
                # print(comment[:std_it] + comment[end_it+1:])
                comment_list[i] = comment_list[i][:std_it] + comment_list[i][end_it+1:]
            except:
                print(comment_list[i])

    # 去除emoji
    for i in range(len(comment_list)):
        if "[" in comment_list[i] and "]" in comment_list[i]:
            regex = re.compile("\[(.*?)\]")
            comment_list[i] = regex.sub("", comment_list[i])
        if "【" in comment_list[i] and "】" in comment_list[i]:
            regex = re.compile("【(.*?)】")
            comment_list[i] = regex.sub("", comment_list[i])
        if "http" in comment_list[i]:
            idx = comment_list[i].index("http")
            try:
                idx2 = comment_list[i].index(" ", idx) + 1
                comment_list[i] = comment_list[i][:idx] + comment_list[i][idx2:]
            except:
                comment_list[i] = comment_list[i][:idx]

        if "👉" in comment_list[i]:
            regex = re.compile("👉")
            comment_list[i] = regex.sub("", comment_list[i])

        if "👈" in comment_list[i]:
            regex = re.compile("👈")
            comment_list[i] = regex.sub("", comment_list[i])

    non_empty_cmt_list = []
    # 去除空值
    for comment in comment_list:
        if len(comment) > 0:
            non_empty_cmt_list.append(comment)

    return non_empty_cmt_list

def test(comment_list):
    for comment in comment_list:
        print(comment)


if __name__ == "__main__":
    worm()
    cmt_list = data_cleaning("bp_comment_list4.txt")
    save_list(cmt_list, "bp_clean_comment_list4.txt")

    # combine_list("./bp_combine_list.txt")




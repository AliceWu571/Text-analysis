import requests
import stylecloud
from PIL import Image
from icecream import ic
from jsonpath import jsonpath


def parse_cy_img(comment_list):
    print("--------词云图生成中--------")
    data = "".join(comment_list)
    stylecloud.gen_stylecloud(data, font_path="C:/Windows/Fonts/msyh.ttc")
    img = Image.open("./stylecloud.png")
    img.show()
    print("词云图已生成")


def main():
    it = 1
    comment_list = []
    while True:
        try:
            print(it)
            start_url = "https://api.bilibili.com/x/v2/reply/main?csrf=30e98bb9d609badba314213e102937e4&mode=3&next={}&" \
                        "oid=938278029&plat=1&type=1".format(it)
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                "referer": r"https://www.bilibili.com/video/BV1RT4y1h7BF?spm_id_from=333.337.search-card.all.click&vd_source=3cdeb3c8e37b611f446f44b7c1a21139"
            }

            response = requests.get(start_url, headers).json()

            replies = jsonpath(response, "$..replies")[0]
            message_list = jsonpath(replies, '$..message')
            comment_list.extend(message_list)
            it += 1
            if it == 100:
                break
        except:
            print("Worm Ending")
            break

    parse_cy_img(comment_list)
    # ic(message_list)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

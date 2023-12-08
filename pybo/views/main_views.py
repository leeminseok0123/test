# -*- coding: utf-8 -*-
#
import datetime

from flask import Blueprint, request, jsonify, send_file
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
from konlpy.tag import Okt
from matplotlib import pyplot as plt
from io import BytesIO



def getToDay():
    return datetime.datetime.today().strftime("%Y%m%d")


def getNowTime():
    return datetime.datetime.today().strftime("%Y.%m.%d %H시%M분")



bp = Blueprint('main', __name__, url_prefix='/')

def getNVisitor(naver_id):

    print(f"naver_id: {naver_id}")

    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get("https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId=" + naver_id, headers=headers, timeout=5)
    print("#########################################")
    print(res.text)
    print("#########################################")
    return ET.fromstring(res.text)


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo! 2'


@bp.route('/')
def index():
    return 'Pybo index 2'


@bp.route('/bloginfo', methods=['GET', 'POST'])
def process_bloginfo_request():
    # HTTP POST 요청에서 'aaa' 파라미터를 받아옵니다.
    keyword = request.form.get('keyword', '')
    num_of_post = request.form.get('num_of_post', '')

    print(f"keyword: {keyword}")
    print(f"num_of_post: {num_of_post}")

    #keyword = "개인회생"

    okt = Okt()
    INCLUDE = ["Noun", "URL", "Alpha", "Number"]

    headers = {'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36')}

    url = f"https://search.naver.com/search.naver?query={keyword}&nso=&where=blog&sm=tab_opt"
    r = requests.get(url, headers=headers)
    print(r.text)
    bs = BeautifulSoup(r.text, "lxml")
    lis = bs.select("ul.lst_view > li.bx")

    num_of_post = int(num_of_post)

    legend = []
    final_sorted_dict = []

    ret = ""
    ret_list = []
    for idx_x, i in enumerate(lis):

        total_frequency = 0

        if idx_x > (num_of_post - 1):
            break
        user_info = i.select_one("div.user_info > a").get_text().strip()
        print(f"user_info: {user_info}")

        post_day = i.select_one("div.user_info > span.sub").get_text().strip()
        print(f"post_day: {post_day}")

        link = i.select_one("a.dsc_link").get("href")
        print(f"link: {link}")

        thumb_link = i.select_one("a.thumb_link")
        if thumb_link is not None:
            thumb = thumb_link.get("href")
            print(f"thumb: {thumb}")
        thumb_link = ""

        temp = thumb.split("https://blog.naver.com/")[1]
        uid = temp.split("/")[0]
        logNo = temp.split("/")[1]
        print(f"uid:{uid} logNo:{logNo}")


        print("방문자수")
        num_of_day = 0
        total_visitor = 0
        avg_visitor = 0

        visitor_xtree = getNVisitor(uid)
        for node in visitor_xtree.findall('visitorcnt'):
            visitor_day = node.get('id')

            if getToDay() != visitor_day:
                visitor = node.get('cnt')
                print(f"visitor_day: {visitor_day}: visitor: {visitor}")
                total_visitor += int(visitor)
                num_of_day += 1

        print(f"num_of_day: {num_of_day}")
        print(f"total_visitor: {total_visitor}")
        avg_visitor = int(total_visitor/num_of_day)
        print(f"avg_visitor: {avg_visitor}")

        post_url = f"https://blog.naver.com/PostView.naver?blogId={uid}&logNo={logNo}"
        r = requests.get(post_url, headers=headers)
        print(r.text)

        bs = BeautifulSoup(r.text, "lxml")
        #title = bs.select_one("div.pcol1 > div > p > span").text
        title = bs.select_one("div.pcol1 > div").text
        pub_date = bs.select_one("div.blog2_container > span.se_publishDate").text

        main_container = bs.select_one("div.se-main-container")
        if main_container is None:
            contents = bs.select_one("div.se_component_wrap.sect_dsc.__se_component_area").text.replace("\n", "")
            images = bs.select("div.se_component.se_image")

        else:
            contents = main_container.text.replace("\n", "")
            images = main_container.select("img")

        #contents = bs.select_one("div.se-main-container").text.replace("\n", "")
        #images = bs.select_one("div.se-main-container").select("img")
        total_len = len(contents)
        img_len = len(images)

        keyword_nouns = okt.pos(keyword)
        print("keyword_nouns", keyword_nouns)

        nouns = okt.pos(contents)

        # 각 키워드가 contents 안에 몇 번 반복되었는지 확인하고 합산
        num_of_keyword = 0
        count_with_spaces = 0
        count_without_spaces = 0

        # 키워드가 띄어쓰기를 포함하는 경우 처리
        if " " in keyword:
            count_with_spaces = contents.count(keyword)
            num_of_keyword += count_with_spaces
            print(f"num_of_keyword {num_of_keyword}")
        # 띄어쓰기를 제외한 키워드 생성
        keyword_without_spaces = keyword.replace(" ", "")
        # 띄어쓰기를 제외한 키워드 처리
        count_without_spaces = contents.count(keyword_without_spaces)
        num_of_keyword += count_without_spaces
        print(f"count_without_spaces {count_without_spaces}")

        print(f'키워드 "{keyword}"가 본문 안에 합쳐서 {num_of_keyword}번 반복됐습니다.')

        word_list = ["했다", "겠다", "했었다", "였다", "하였다", "과거", "했습니다", "였습니다",
                     "경험", "기억", "추억", "했던", "였던", "지난", "시절", "었다", "갔다", "갔었다", "았다"
                                                                                  "이예요", "았어요", "했어요", "었어요", "어요",
                     "있어요", "되어요", "습니다", "웠어요", "보았어요"]

        # 결과를 저장할 딕셔너리를 초기화합니다.
        word_frequency = {word: 0 for word in word_list}

        # 문자열을 공백을 기준으로 단어로 분리합니다.
        content_words = contents.split()
        print(f"len(content_words): {len(content_words)}")
        # 단어 리스트에 있는 각 단어를 문자열에서 찾고 빈도수를 계산합니다.
        for idxx, content_word in enumerate(content_words):
            print(idxx, content_word)
            for word in word_list:
                if word in content_word:
                    word_frequency[word] += 1
                    total_frequency += 1  # 모든 단어의 빈도수를 누적합니다.
        # 결과 출력
        for word, frequency in word_frequency.items():
            print(f"{word}: {frequency}번")

        print(f"총 빈도수: {total_frequency}번")

        words = {}

        str_temp = f"{idx_x + 1}위 {uid} ({user_info}) / {post_day}"
        # legend.append(str_temp)
        # legend.append(uid)

        # INCLUDE = ["Noun", "URL", "Alpha", "Number"]
        for n in nouns:
            # 단어가 아니거나 2글자 이하인경우 제외
            if n[1] not in INCLUDE or len(n[0]) < 2:
                continue
            if words.get(n[0]) is None:
                words[n[0]] = 1
            else:
                words[n[0]] = words[n[0]] + 1
            print(f"words: {words}")

        print(f"words: {words}")

        sorted_dict = sorted(words.items(), key=lambda item: item[1], reverse=True)
        final_sorted_dict.extend(sorted_dict[:10])

        sum_of_top = sum([len(w) * c for w, c in sorted_dict[:10]])
        per = sum_of_top / total_len * 100

        print(f"전체 글자수: {total_len} 상위단어: {sorted_dict[:10]} 상위단어비중: {per:.3f} 이미지갯수: {img_len}")
        strtemp2 = f"글자수: {total_len} 이미지: {img_len} 키워드: {keyword}({num_of_keyword})=({count_with_spaces})+({count_without_spaces})"

        str_temp3 = ""
        str_temp4 = ""

        for word, count in sorted_dict[:10]:
            print(f"word: {word} count: {count}")
            str_temp4 += f'{word}({count}회) '

        # sorted_dict를 순회하면서 검색어와 일치하는 단어가 있는 경우 빈도수 출력
        for word, count in sorted_dict:
            print(f"word: {word} count: {count} keyword_nouns: {keyword_nouns}")

            if any(word1 == word for word1, _ in keyword_nouns):
                print(f'"{word}"는 keyword_nouns 안에 있습니다.')

                print(f'검색어에 해당하는 단어: {word}, 빈도수: {count}')
                str_temp3 += f'{word}({count}회) '

        total_frequency = "{:2d}".format(total_frequency)
        avg_visitor = "{:5d}".format(avg_visitor)
        legend.append("DIA:" + str(total_frequency) + " 일" + str(
            avg_visitor) + "명 / " + str_temp + " / " + strtemp2 + " " + str_temp3)

        add_info = f"글자수: {total_len}자 이상\n"
        add_info += f"키워드: {keyword} 본문에 {num_of_keyword}번 이상 포함되게 작성\n"
        add_info += f"글자수: {total_len}자 이상\n"
        add_info += f"글자수: {total_len}자 이상\n"

        xy = [c for w, c in sorted_dict[:10]]
        word = [w for w, c in sorted_dict[:10]]
        for e, (x, w) in enumerate(zip(xy, word)):
            if idx_x == 0:
                plt.text(e, x, w, size=10, color="red", weight="bold", verticalalignment='bottom')
            else:
                plt.text(e, x, w, size=9, color="black", weight="normal", verticalalignment='bottom')
            plt.plot(xy, "--o")

        ret_list.append([idx_x + 1, post_url, uid, logNo, total_len, img_len, title, pub_date, total_frequency, avg_visitor, str_temp, strtemp2, str_temp3, str_temp4])


    # 첫 번째 요소를 기준으로 반복 횟수를 더함
    count_dict = {}
    for item in final_sorted_dict:
        key, count = item
        if key in count_dict:
            count_dict[key] += count
        else:
            count_dict[key] = count

    # 반복 횟수를 기준으로 내림차순으로 정렬
    sorted_count = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    # 상위 10개 요소 출력
    top_10 = sorted_count[:10]
    print(top_10)

    for item in top_10:
        print(item)

    output_string = ', '.join([item[0] for item in top_10])

    # 생성된 문자열 출력
    print("참고 키워드", output_string)
    #
    # title_font = {
    #     'fontsize': 20,
    #     'color': "blue",
    #     'fontweight': "bold",
    #     'fontstyle': "italic"
    # }
    #
    # plt.title(f"검색어: {keyword}", fontdict=title_font)
    # plt.suptitle(output_string, fontsize=12)  # 부제목의 크기를 12로 설정
    #
    # plt.xlabel("키워드 종류")
    # plt.ylabel("키워드 수")
    # plt.legend(legend)
    #
    # img = BytesIO()
    # plt.savefig(img, format='png', dpi=200)
    # img.seek(0)
    #
    # return send_file(img, mimetype='image/png')

    #ret_list.append([idx_x+1, post_url, uid, logNo, total_len, img_len, title, pub_date, output_string])

    print(f"output_string: {output_string}")

    # JSON 형식으로 응답합니다.
    response_data = {'keyword': keyword, 'data': ret_list, 'output_string': output_string}
    return jsonify(response_data)




@bp.route('/test')
def index2():
    return '''
    <!-- #######  THIS IS A COMMENT - Visible only in the source editor #########-->
    <h2>Welcome To The Best Online HTML Web Editor!</h2>
    <p style="font-size: 1.5em;">You can <strong style="background-color: #317399; padding: 0 5px; color: #fff;">type your text</strong> directly in the editor or paste it from a Word Doc, PDF, Excel etc.</p>
    <p style="font-size: 1.5em;">The <strong>visual editor</strong> on the right and the <strong>source editor</strong> on the left are linked together and the changes are reflected in the other one as you type! <img src="https://html5-editor.net/images/smiley.png" alt="smiley" /></p>
    <table class="editorDemoTable">
    <tbody>
    <tr>
    <td><strong>Name</strong></td>
    <td><strong>City</strong></td>
    <td><strong>Age</strong></td>
    </tr>
    <tr>
    <td>John</td>
    <td>Chicago</td>
    <td>23</td>
    </tr>
    <tr>
    <td>Lucy</td>
    <td>Wisconsin</td>
    <td>19</td>
    </tr>
    <tr>
    <td>Amanda</td>
    <td>Madison</td>
    <td>22</td>
    </tr>
    </tbody>
    </table>
    <p>This is a table you can experiment with.</p>
'''
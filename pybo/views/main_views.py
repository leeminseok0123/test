import datetime

from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET

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
    print(f"keyword: {keyword}")

    headers = {'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36')}

    url = f"https://search.naver.com/search.naver?query={keyword}&nso=&where=blog&sm=tab_opt"
    r = requests.get(url, headers=headers)
    print(r.text)
    bs = BeautifulSoup(r.text, "lxml")
    lis = bs.select("ul.lst_view > li.bx")

    num_of_post = 10

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

        ret_list.append([idx_x+1, post_url, uid, logNo, total_len, img_len, title, pub_date])

    # JSON 형식으로 응답합니다.
    response_data = {'keyword': keyword, 'data': ret_list}
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
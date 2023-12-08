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
    if request.method == 'GET':
        # GET 요청 처리
        aaa_param = request.args.get('aaa', '')
    elif request.method == 'POST':
        # POST 요청 처리
        aaa_param = request.form.get('aaa', '')

    print(f"aaa_param: {aaa_param}")

    headers = {'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36')}

    keyword = aaa_param
    url = f"https://search.naver.com/search.naver?query={keyword}&nso=&where=blog&sm=tab_opt"
    r = requests.get(url, headers=headers)
    bs = BeautifulSoup(r.text, "lxml")
    lis = bs.select("ul.lst_view > li.bx")

    num_of_post = 10

    ret_list = []
    for idx_x, i in enumerate(lis):
        if idx_x > (num_of_post - 1):
            break
        user_info = i.select_one("div.user_info > a").get_text().strip()
        post_day = i.select_one("div.user_info > span.sub").get_text().strip()
        link = i.select_one("a.dsc_link").get("href")
        ret_list.append({'user_info': user_info, 'post_day': post_day, 'link': link})

    # JSON 형식으로 응답합니다.
    response_data = {'aaa_param': aaa_param, 'data': ret_list}
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
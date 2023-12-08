import datetime

from flask import Blueprint, request

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
    aaa_param = request.form.get('aaa', '')
    print(f"aaa_param: {aaa_param}")

    num_of_day = 0
    total_visitor = 0
    avg_visitor = 0

    visitor_xtree = getNVisitor(aaa_param)
    for node in visitor_xtree.findall('visitorcnt'):
        visitor_day = node.get('id')

        if getToDay() != visitor_day:
            visitor = node.get('cnt')
            print(f"visitor_day: {visitor_day}: visitor: {visitor}")
            total_visitor += int(visitor)
            num_of_day += 1

    print(f"num_of_day: {num_of_day}")
    print(f"total_visitor: {total_visitor}")
    avg_visitor = int(total_visitor / num_of_day)
    print(f"avg_visitor: {avg_visitor}")



    # 받아온 문자열에 "응답"을 붙여 응답으로 반환합니다.
    response_text = aaa_param + '응답-' + total_visitor + "/" + num_of_day + "/" + avg_visitor

    return response_text



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
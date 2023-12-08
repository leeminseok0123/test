from flask import Blueprint, request

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo! 2'


@bp.route('/')
def index():
    return 'Pybo index 2'


@bp.route('/bloginfo', methods=['GET', 'POST'])
def process_bloginfo_request():
    # HTTP GET 요청에서 'aaa' 파라미터를 받아옵니다.
    aaa_param = request.args.get('aaa', '')

    # 받아온 문자열에 "응답"을 붙여 응답으로 반환합니다.
    response_text = aaa_param + '응답'

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
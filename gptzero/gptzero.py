import requests
from voluptuous import MultipleInvalid
from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Scope, String, Any, Dict
from xblock.fragment import Fragment

from gptzero.schema import CONFIG_SCHEMA
from gptzero.utils import resource_string, render_template
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


class GptZeroXBlock(XBlock):
    has_author_view = True
    display_name = String(help="This name appears in horizontal navigation at the top of the page.",
                          default="GPT Zero", scope=Scope.settings)

    prediction_results = Dict(
        default={},
        scope=Scope.user_state,
        help='Prediction results for each student submission'
    )

    config = Any(scope=Scope.settings, default={
        'gptzero_display_name': 'GPT Zero',
    })

    GPTZ_TEXT_LIMIT = 5000

    # GPTzero API configs
    base_url = 'https://api.gptzero.me/v2/predict'

    def author_view(self, context):  # pylint: disable=unused-argument
        frag = Fragment()
        frag.add_content(render_template('static/html/author_view.html', {'self': self}))
        return frag

    def studio_view(self, context):  # pylint: disable=unused-argument
        frag = Fragment()
        frag.add_content(render_template('static/html/studio_view.html', {'self': self}))
        frag.add_javascript(resource_string('static/js/studio_view.js'))
        frag.initialize_js('GPTZeroXBlockStudio')
        return frag

    def student_view(self, context):
        html = resource_string('static/html/student_view.html')
        frag = Fragment(html)
        frag.add_javascript(resource_string('static/js/student_view.js'))
        frag.initialize_js('GptZeroXBlock')
        return frag

    def text_predict(self, document, api_key):
        url = '{}/text'.format(self.base_url)
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if api_key:
            headers['X-Api-Key'] = api_key

        data = {
            'document': document
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @XBlock.json_handler
    def save_api_key(self, config, suffix=''):  # pylint: disable=unused-argument
        # Handle the form submission in the author view
        self.config = CONFIG_SCHEMA(config)
        return {'result': 'success'}

    @XBlock.json_handler
    def update_settings(self, config, suffix=''):  # pylint: disable=unused-argument
        try:
            self.config = CONFIG_SCHEMA(config)
            self.display_name = config['gptzero_display_name']
        except MultipleInvalid as e:
            raise JsonHandlerError(500, str(e)) from e

        return config

    @XBlock.json_handler
    def submit_text(self, data, suffix=''):  # pylint: disable=unused-argument
        text = data.get('text', '')
        api_key = configuration_helpers.get_value('GPTZ_API_KEY', None)
        if not api_key and len(text) > self.GPTZ_TEXT_LIMIT:
            return {
                'result': 'failure',
                'message': 'GPTZ_API_KEY Missing from Site Configuration, make sure to add that'
            }

        if self.prediction_results.get(self.runtime.user_id):
            return {
                'result': 'failure',
                'message': 'you arleady submitted you text'
            }

        prediction = self.text_predict(text, api_key)
        if prediction.get('error'):
            return {
                'result': 'failure',
                'message': prediction.get('error'),
            }

        self.prediction_results[self.runtime.user_id] = prediction.get('documents', [{}])[0]
        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        return [
            ("GptZeroXBlock", "<gptzeroxblock/>"),
        ]

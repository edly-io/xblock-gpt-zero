from pkg_resources import resource_string as pkg_resource_string

from django.template import Context, Template


def resource_string(path):
    data = pkg_resource_string(__name__, path)
    return data.decode("utf8")


def render_template(template_path, context):
    """
    Render resource using django template engine and the give content object to it.
    :param template_path: (str) path of the resource to load
    :param context: {} dic object to pass to django template

    :return: template.render
    """
    template_str = resource_string(template_path)
    template = Template(template_str)
    return template.render(Context(context))

from jinja2 import Template


def zonal_assignments_report():
    template = Template('Hello {{ name }}!')
    report = template.render(name='John Doe')
    return report

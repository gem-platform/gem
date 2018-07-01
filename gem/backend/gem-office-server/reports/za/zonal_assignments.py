from itertools import groupby

from jinja2 import Template
from gem.db.models import Official, Assignment


def zonal_assignments_report():
    report = []
    for official in Official.objects.all():
        assignments = Assignment.objects(officials__contains=official)
        if not assignments:
            continue

        report_record = {"name": official.semi_formal_name(), "groups": []}

        assignments = sorted(assignments, key=lambda x: (len(x.zone.assignees), x.zone.assignees))
        groups = groupby(assignments, key=lambda x: x.zone.assignees)

        for assignees, assignments in groups:
            assignees_without_self = list(filter(lambda x: x != official, assignees))
            cozonal = True if assignees_without_self else False
            cozonal_names = list(map(lambda a: a.semi_formal_name(), assignees_without_self))

            report_record_group = {"with": cozonal_names, "zones": []}

            rz = []
            for assignment in assignments:
                for child_zone in assignment.zone.children:
                    rz.append(child_zone)

            rz = sorted(rz)
            for r in rz:
                report_record_group["zones"].append(r.name)

            report_record["groups"].append(report_record_group.copy())
        report.append(report_record)

    # return generated html
    template_file = open("./za.html", "r").read()
    template = Template(template_file)
    report_html = template.render(data=report)
    return report_html

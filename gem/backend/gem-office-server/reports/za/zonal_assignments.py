from itertools import groupby

from jinja2 import Template
from gem.db.models import Official, Zone


def zonal_assignments_report():
    report = []

    # Go through all officials
    for official in Official.objects.all():
        # Get zones there this person is present
        zones = Zone.objects(officials__contains=official)
        if not zones:
            continue

        report_record = {"name": official.formal_name(), "groups": []}

        # sort and group records by co-zonals
        groups = sorted(zones,
                        key=lambda x: (len(x.officials), sorted(x.officials)))
        groups = groupby(groups, key=lambda x: x.officials)

        for assignees, zones in groups:
            without_self = list(filter(lambda x: x != official, assignees))
            co_zonals = list(map(lambda a: a.formal_name(), without_self))

            report_record_group = {"with": co_zonals, "zones": []}

            rz = []
            for zone in list(zones):
                for ch in zone.children:
                    rz.append(ch.name)

            report_record_group["zones"] = list(sorted(rz))
            report_record["groups"].append(report_record_group.copy())
        report.append(report_record)

    # return generated html
    template_file = open("./za.html", "r").read()
    template = Template(template_file)
    report_html = template.render(data=report)
    return report_html

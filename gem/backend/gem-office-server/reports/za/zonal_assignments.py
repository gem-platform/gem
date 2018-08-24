from itertools import groupby
from jinja2 import Template
from gem.db.models import Official, Zone


def __by_cozonals(zone):
    officials = zone.cachedOfficials
    return (len(officials), sorted(officials))


def __get_leaves(zone, result):
    if not zone.children:
        result.append(zone)
        return result
    for child in zone.children:
        __get_leaves(child, result)


def zonal_assignments_report(hierarchy=False, leaves_only=True):
    report = []

    # Go through all officials
    for official in Official.objects.all():
        # Get zones there this person is present
        # if no such zone found, skip that official
        zones = Zone.objects(cachedOfficials__contains=official)
        if not zones:
            continue

        report_record = {"name": official.formal_name(), "groups": []}

        # sort and group records by co-zonals
        groups = sorted(zones, key=__by_cozonals)
        groups = groupby(groups, key=lambda x: x.cachedOfficials)

        for assignees, zones in groups:
            without_self = list(filter(lambda x: x != official, assignees))
            co_zonals = list(map(lambda a: a.formal_name(), without_self))

            report_record_group = {"with": co_zonals, "zones": []}

            rz = zones
            if leaves_only:
                rz = list(filter(lambda x: not x.children, rz))

            if hierarchy:
                rz = list(map(lambda x: " / ".join(x.path + [x.name]), rz))
            else:
                rz = list(map(lambda x: x.name, rz))

            report_record_group["zones"] = list(sorted(rz))
            report_record["groups"].append(report_record_group.copy())
        report.append(report_record)

    # return generated html
    template_file = open("./za.html", "r").read()
    template = Template(template_file)
    report_html = template.render(data=report)
    return report_html

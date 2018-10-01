def finalize_ballot(sender, document, **kwargs):
    # remove any reference to user for secret ballot
    if document.secret:
        for vote in document.votes:
            vote.user = None

    # save as not finished if there is no any vote
    if document.votes:
        document.finished = True


def update_cached_fields(sender, document, **kwargs):
    def __get_parents_path(zone, result):
        if zone.parent:
            result.append(zone.parent.name)
            __get_parents_path(zone.parent, result)
        return list(reversed(result))

    officials = document.officials
    children = document.children
    cached = document.cachedOfficials

    # update own cached fields
    document.path = __get_parents_path(document, [])
    for official in officials:
        if official not in cached:
            cached.append(official)

    # update children cached fields
    for child in children:
        child_cached = child.cachedOfficials

        for official in officials:
            if official not in child_cached:
                child_cached.append(official)

    for child in children:
        child.save()

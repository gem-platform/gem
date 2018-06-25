def finalize_ballot(sender, document, **kwargs):
    if document.secret:
        for v in document.votes:
            v.user = None
    document.finished = True

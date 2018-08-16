from jinja2 import Template, Environment, FileSystemLoader
from gem.db.models import Comment, Proposal

def mark(value):
    if value is "+":
        return "plus"
    if value is "-":
        return "minus"
    if value is "i":
        return ""
    return value

def proposal_comments_report(proposal_id):
    # get all the comments for specified proposal
    proposal = Proposal.objects.get(id=proposal_id)
    comments = Comment.objects(proposal=proposal_id)

    # configure jijna
    env = Environment(
        loader=FileSystemLoader("templates")
    )
    env.filters["mark"] = mark

    # return generated html
    template = env.get_template("proposal_comments.html")
    report_html = template.render(proposal=proposal, comments=comments)
    return report_html

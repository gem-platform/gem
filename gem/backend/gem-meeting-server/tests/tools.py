from gem.db import User, Role, Proposal, Comment

def drop_db():
    User.drop_collection()
    Role.drop_collection()
    Proposal.drop_collection()
    Comment.drop_collection()

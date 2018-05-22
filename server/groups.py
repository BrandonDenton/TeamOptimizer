from flask import jsonify, Blueprint, g, current_app, abort
from flask.ext.login import login_required
import flask.ext.login as flask_login

groups_blueprint = Blueprint('groups', __name__)

class Group:
    def __init__(self, id, createdBy, groupName, numMembers, dateCreated, members):
        self.id = id
        self.createdBy = createdBy
        self.groupName = groupName
        self.numMembers = numMembers
        self.dateCreated = dateCreated
        self.members = members

    def serialize(self):
        return {
            'id': self.id,
            'createdBy': self.createdBy,
            'groupName': self.groupName,
            'numMembers': self.numMembers,
            'dateCreated': self.dateCreated.isoformat(),
            'members': self.members,
            # required by Ember
            'type': 'group'
        }

# get a group by its group id
def get_group_by_group_id(id, cursor):
    cursor.execute('SELECT createdBy, groupName, numMembers, dateCreated FROM groups WHERE id=%s', id)
    result = cursor.fetchone()
    if result == None:
        return None
    else:
        members = get_members_by_group_id(id, cursor)
        group = Group(id, result[0], result[1], result[2], result[3], members)
        return group

# get an array of members in a group by its group id
def get_members_by_group_id(id, cursor):
    members = []
    cursor.execute('SELECT id FROM users WHERE id IN (SELECT userId FROM pairs WHERE groupId=%s)', id)
    results = cursor.fetchall()
    for result in results:
        members.append(result[0])
    return members

# get an array of groups that a user is a member of by their user id
def get_groups_by_user_id(id, cursor):
    groups = []
    cursor.execute('SELECT id FROM groups WHERE id IN (SELECT groupId FROM pairs WHERE userId=%s)', id)
    results = cursor.fetchall()
    for result in results:
        group = get_group_by_group_id(result[0], cursor)
        groups.append(group)
    return groups

@groups_blueprint.route('/groups/<int:id>')
@login_required
def get_group_by_group_id_route(id):
    group = get_group_by_group_id(id, g.db.cursor())
    if group == None:
        abort(400)
    else:
        return jsonify(group=group.serialize())

@groups_blueprint.route('/groups')
@login_required
# get all of the groups that the currently logged in user is a member of
def get_groups_by_user_id_route():
    user_id = flask_login.current_user.id
    groups = get_groups_by_user_id(user_id, g.db.cursor())
    serialized_groups = []
    for group in groups:
        serialized_groups.append(group.serialize())
    return jsonify(groups=serialized_groups)

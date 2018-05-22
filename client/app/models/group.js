import DS from 'ember-data';

/* the group model that should be returned by the server. for example, when
   we call this.store.fetchAll('group'), our adapter (adapters/application.js)
   will make an AJAX call to the server route /groups, which should return a
   JSON object that matches the specs shown here. */
export default DS.Model.extend({
  createdBy: DS.belongsTo('user'),
  groupName: DS.attr('string'),
  numMembers: DS.attr('number'),
  dateCreated: DS.attr('date'),
  members: DS.hasMany('user')
});

import DS from 'ember-data';

/* this user model should match what the server returns from /users */
export default DS.Model.extend({
  name: DS.attr('string'),
  email: DS.attr('string'),
  mbti: DS.attr('string')
});

import Base from 'ember-simple-auth/authenticators/base';
import Ember from 'ember';

// http://ember-simple-auth.com/api/classes/BaseAuthenticator.html
export default Base.extend({
  prefix: '/api',
  restore(data) {
    // see restore() in server/auth.py
    let prefix = this.get('prefix');
    return Ember.$.get(`${prefix}/restore`);
  },
  authenticate(email, password) {
    let prefix = this.get('prefix');
    return Ember.$.post(`${prefix}/login`, {
      'email': email,
      'password': password
    });
  },
  invalidate(data) {
    let prefix = this.get('prefix');
    return Ember.$.post(`${prefix}/logout`);
  }
});

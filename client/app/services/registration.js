import Ember from 'ember';

export default Ember.Service.extend({
  prefix: '/api',
  createUser(fullName, email, password, mbti) {
    let prefix = this.get('prefix');
    return Ember.$.post(`${prefix}/register`, {
      'fullName': fullName,
      'email': email,
      'password': password,
      'mbti': mbti
    });
  }
});

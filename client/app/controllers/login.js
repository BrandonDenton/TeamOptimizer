import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service(),
  actions: {
    authenticate() {
      let { email, password } = this.getProperties('email', 'password');
      this.get('session').authenticate('authenticator:application', email, password).catch((err) => {
        switch(err.status) {
          case 401:
            this.set('errorMessage', 'Incorrect email or password.');
            break;
          case 404:
            this.set('errorMessage', 'Unable to contact the server. Contact us if the problem persists.');
            break;
          default:
            this.set('errorMessage', `The server returned error code ${err.status}. Contact us if the problem persists.`);
        }
      });
    }
  }
});

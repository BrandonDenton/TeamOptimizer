import Ember from 'ember';

export default Ember.Controller.extend({
  mbtiTypes: [],
  selectedType: '',
  init() {
    // generate MBTI types because I'm too lazy to type them all out plus this is super LEET
    // I'm sorry
    // ayy lmao
    for (let firstLetter of ['E', 'I']) {
      for (let secondLetter of ['S', 'N']) {
        for (let thirdLetter of ['T', 'F']) {
          for (let lastLetter of ['J', 'P']) {
            this.get('mbtiTypes').push(`${firstLetter}${secondLetter}${thirdLetter}${lastLetter}`);
          }
        }
      }
    }
    this.set('selectedType', this.get('mbtiTypes')[0]);
  },
  registration: Ember.inject.service(),
  session: Ember.inject.service(),
  actions: {
    signUp() {
      let { fullName, email, password } = this.getProperties('fullName', 'email', 'password');
      // make sure none of the fields are empty
      for (let str of [fullName, email, password]) {
        if (!str) {
          this.set('errorMessage', 'Validation failed. Make sure you\'ve filled out every field before continuing.');
          return;
        } else {
          this.set('errorMessage', null);
        }
      }
      let mbti = this.get('selectedType');
      this.get('registration').createUser(fullName, email, password, mbti).then(() => {
        // if successful
        this.get('session').authenticate('authenticator:application', email, password)
      }, (err) => {
        // if failed
        switch(err.status) {
          case 400:
            this.set('errorMessage', `The email address ${email} is already assigned
              to a registered user. Either log in with your existing password
              or create a new account with a different email address.`);
            break;
          case 404:
            this.set('errorMessage', 'Unable to contact the server. Contact us if the problem persists.');
            break;
          default:
            this.set('errorMessage', `The server returned error code ${err.status}. Contact us if the problem persists.`);
        }
      });
    },
    selectMBTI(value) {
      this.set('selectedType', value);
    }
  }
})

import Ember from 'ember';

export default Ember.Route.extend( {
  model() {
    // return survey questions
    return this.store.findAll('grabsurvey');
  }
});
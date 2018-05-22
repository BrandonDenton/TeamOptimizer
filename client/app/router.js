import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('about');
  this.route('contact');
  this.route('register');
  this.route('groups', function() {
    this.route('group', { path: ':group_id'});
    this.route('new');
  });
});

export default Router;

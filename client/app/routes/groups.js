import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

/* the AuthenticatedRouteMixin mixin forces this route to only be available when
 * the user is logged in. a user that is not logged in will be redirected to
 * the /login route. */
export default Ember.Route.extend(AuthenticatedRouteMixin, {
  model() {
    // override the model() hook, returning an array of groups
    return this.store.findAll('group');
  }
});

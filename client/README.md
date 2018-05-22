# Client

This is the client for Team Optimizer. It's a single-page web app made with [Ember.js](http://emberjs.com/).

## Prerequisites

You will need the following things properly installed on your computer.

* [Git](http://git-scm.com/)
* [Node.js](http://nodejs.org/) (with NPM)
* [Bower](http://bower.io/) (install with `npm install -g bower`)
* [Ember CLI](http://www.ember-cli.com/) (install with `npm install -g ember-cli`)
* [PhantomJS](http://phantomjs.org/) (optional)

## Setup

* `git clone git@gitlab.com:utk_cosc340_sp16/team09.git`
* `cd ./team09/client/`
* `npm install`
* `bower install`

## Running / Development

* `ember server --proxy http://localhost:5000` (this will proxy all AJAX requests to go to port 5000, which is the port the server runs on)
* Visit the app at [http://localhost:4200](http://localhost:4200).

### Code Generators

Make use of the many generators for code, try `ember help generate` for more details.

### Running Tests

* `ember test`
* `ember test --server`

### Building

* `ember build` (development)
* `ember build --environment production` (production)

### Deploying

After building, copy the `dist/` folder to the root of your webserver.

## Further Reading / Useful Links

* [ember.js](http://emberjs.com/)
* [ember-cli](http://www.ember-cli.com/)
* Development Browser Extensions
  * [ember inspector for chrome](https://chrome.google.com/webstore/detail/ember-inspector/bmdblncegkenkacieihfhpjfppoconhi)
  * [ember inspector for firefox](https://addons.mozilla.org/en-US/firefox/addon/ember-inspector/)

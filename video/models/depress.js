var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// create a schema
var peopleSchema = new Schema({
  location: String
}, { collection : 'depress' });

var User = mongoose.model('Depress', peopleSchema);

// make this available to our users in our Node applications
module.exports = User;
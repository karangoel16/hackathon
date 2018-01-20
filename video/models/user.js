var mongoose = require('mongoose');
var Schema = mongoose.Schema;

// create a schema
var peopleSchema = new Schema({
  location: String,
  age: Number,
  gender: String
}, { collection : 'people' });

var User = mongoose.model('People', peopleSchema);

// make this available to our users in our Node applications
module.exports = User;
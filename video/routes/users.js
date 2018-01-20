var express = require('express');
var router = express.Router();
var User = require('../models/depress');
/* GET users listing. */
router.get('/', function(req, res) {
  User.find({}, function(err, users) {
    if (err) throw err;
    console.log(users)
    res.render('index', { title: 'Depression Detection' ,users: users});
  });
});

module.exports = router;

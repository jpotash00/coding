//  webaddress = localhost:3000/

var express = require('express');
var bodyParser = require('body-parser');
// var cookieParser = require('cookie-parser');
// var flash = require('flash');
var app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname + "/public")); //use what evers in directory named public
// app.use(cookieParser('secretString'));
// app.use(flash());
var mysql = require('mysql2');
const { request } = require('express');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',  // your root username
    password : 'Newuser02.A',  //your password 
    database : 'join_us'   // the name of your db
});
// app.get("/home", function(req, res){//trigger when user asks for a home page [req = request, res = response]
//     res.render("home");
// }); 
app.get("/", function(req, res){//trigger when user asks for a home page [req = request, res = response]
    var q = 'SELECT COUNT(*) AS num_of_users from users';
    connection.query(q, function(error, results){
        if (error) throw error;
        var counter = results[0].num_of_users;
        res.render('home', {data: counter});
    });
});
// app.get("/home", function(req, res){//trigger when user asks for a home page [req = request, res = response]
//     var w = 'SELECT * from users';
//     connection.query(w, function(error, results){
//         if (error) throw error;
//         var c = results;
//         res.send('home', {all: c});
//     });
// });


// app.get("/logout", function(req, res){//trigger when user asks for a home page [req = request, res = response]
//     res.send("Your are logged out!");
// });
app.post("/register", function(req,res){
    var person = {
        email : req.body.email
    };
    connection.query('INSERT INTO users SET ?', person, function(err, result) {
        if (err) throw err;
        console.log(result);
    //console.log("post request sent to /register email is " + req.body.email);
    });
    // req.flash('signupMessage', anyValue);
    res.redirect("/");
});

// app.get("/random_num", function(req, res){//trigger when user asks for a home page [req = request, res = response]
//     var y = Math.floor(Math.random()*1000) + 1;
//     res.send("your lucky number is: " + y);
// });

app.listen(3000, function(){
 console.log('App listening on port 3000!');
});

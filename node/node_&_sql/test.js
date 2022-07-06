
const { faker } = require('@faker-js/faker');
const mysql = require('mysql2');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',  // your root username
  password : 'Newuser02.A',  //your password 
  database : 'join_us'   // the name of your db
});
//for(var i = 0; i < 500; i++){
   // console.log("Node.js, works");
//}
// function generateAddress(){
//     console.log(faker.address.streetAddress());
//     console.log(faker.address.city());
//     console.log(faker.address.state());
// }
//for (i = 0; i < 3; i++){
    //generateAddress();
    //console.log("\n")
//}

function queryA(){
    var q = 'select * from users ORDER BY created_at DESC LIMIT 1';
    connection.query(q, function(error, results, fields){
        if (error) throw error;
        console.log(results);
    });
}

// var person = {
//     email: faker.internet.email(),
//     created_at: faker.date.past()  
// }
// var end_result = connection.query('INSERT INTO users SET ?', person, function(err, result) {
//     if (err) throw err;
//     console.log(result);
//   });


// var data = [];
// for(var i = 0; i < 500; i++){
//     data.push([
//         faker.internet.email(),
//         faker.date.past()
//     ]);
// }
// var q = 'INSERT INTO users (email, created_at) VALUES ?'
 
// connection.query(q, [data], function(err, result) {
//   console.log(err);
//   console.log(result);
// });
queryA();
connection.end();
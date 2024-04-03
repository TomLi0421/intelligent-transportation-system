const express = require('express');
const cors = require('cors');
// const mysql = require('mysql');

const app = express();
app.use(express.json());
app.use(cors());

// const db = mysql.createConnection({
//     host        : 'localhost',
//     user        : 'root',
//     password    : '',
//     database    : 'codeboard'
// })

// db.connect((err)=> {
//     if(err) throw err;
//     console.log('connention done')
// })

app.post('/getdata', (req, res) => {
    console.log("HiHIHI");
    return res.json("No Record");
})

app.listen(8080, ()=> {
    console.log("listening");
})
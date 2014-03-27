var express = require('express');
var app = express();
var MongoClient = require('mongodb').MongoClient;
var format = require('util').format;
var swig = require('swig');


global.util = {
  flow: require('flow')
}
MongoClient.connect('mongodb://127.0.0.1:27017/kaiju', function(err, db){
  if(err){
    throw err;
  }
  global.db = db;
})

var kaiju = require('./routes/kaiju');

app.configure(function(){
  swig.init({ root: __dirname + '/views', allowErrors: true });
  app.engine('.html', require('consolidate').swig);
  app.set('view engine', 'html');
  app.use(express.bodyParser());
  app.use(express.logger());
  app.use("/public", express.static(__dirname + '/public'));
})

app.all('/', kaiju.main);
app.all('/saveWord', kaiju.saveWord);
app.all('/saveResult', kaiju.saveResult);
app.all('/showResult', kaiju.showResult);

util.flow.exec(
  function(){
    app.listen(3000);
    this();
  },
  
  function(){
    console.dir("Start listen 3000 port");
  }
)


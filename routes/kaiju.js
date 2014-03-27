module.exports.main = function(req, res, next){
  res.render('test');
  //~ res.send('Hello, Kaijus');
}

module.exports.saveWord = function(req, res, next){
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.send(200);
  var data = req.body.data;
  util.flow.exec(
    function(){
      db.collection("everyWord_info", this);
    },
    
    function(err, coll){
      coll.insert(data , function(){});
    }
  )
}


module.exports.saveResult = function(req, res, next){
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.send(200);
  var ObjectID = require('mongodb').ObjectID
  var result = req.body.result;
  util.flow.exec(
    function(){
      db.collection("result_info", this);
    },
    
    function(err, coll){
      coll.insert(result,function(){});
    }
  )
}

//~ module.exports.showResult = function(req, res, next){
  //~ var Users = []; // 玩家的玩家的objid
  //~ var info = [];
  //~ util.flow.exec(
    //~ function(){
      //~ db.collection("users", this);
    //~ },
    //~ 
    //~ function(err, coll){
      //~ coll.find({}).toArray(this);
    //~ },
    //~ 
    //~ function(err, docs){
      //~ if(err){
        //~ console.dir("err =" + err);
      //~ }
      //~ for(var i in docs){
        //~ var doc = docs[i];
        //~ var d = {};
        //~ d['uid'] = doc['_id'];
        //~ d["name"] = doc['name'];
        //~ Users.push(d);
      //~ }
      //~ this();
    //~ },
    //~ 
    //~ function(){
      //~ for(var j in Users){
        //~ var obj = {};
        //~ var uid = Users[j]['uid'];
        //~ obj.uid = uid;
        //~ obj.uname = Users[j]['name'];
        //~ console.dir(obj);
        //~ getUserGameInfo(uid, info, obj, this.MULTI());
      //~ }
    //~ },
    //~ 
    //~ function(){
      //~ res.render('result', {info:info})
    //~ }
  //~ )
//~ }


module.exports.showResult = function(req, res, next){
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  util.flow.exec(
    function(){
      db.collection("result_info", this);
    },
    
    function(err, coll){
      coll.find({}).toArray(this);
    },
    
    function(err, docs){
      //~ res.render('result', {info:info})
      res.jsonp(docs);
    }
  )
}

var getUserGameInfo = function(uid, info, obj, next){
  //~ console.dir(obj);
  util.flow.exec(
    function(){
      db.collection("result_info", this);
    },
    
    //~ function(err, coll){
      //~ coll.find({"user":{ $elemMatch: { "userid": uid }}}).toArray(this);
    //~ },
    function(err, coll){
      coll.find({"user":uid}).toArray(this);
    },
    
    function(err, docs){
      if(err){
        console.dir("err = " + err);
        next();
      }
      if(docs.length == 0){
        console.dir("docs.length == 0");
        next();
      }
      obj.games = docs;
      obj.games = [{"a":1}, {"b":2}];
      info.push(obj);
      next();
    }
  )
}

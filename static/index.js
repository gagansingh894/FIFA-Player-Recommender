// import {PythonShell} from 'python-shell';
// const {PythonShell} = require('python-shell');
// PythonShell.runString('x=1+1;print(x)', null, function (err) {
//     if (err) throw err;
//     console.log('finished');
//   });


function getValue(){
     var checkElem = document.getElementsByClassName("a0")[0].value
     console.log(checkElem)
     var name = document.getElementsByClassName("search_player_txt")[0].value;
     document.getElementById("myForm").submit();
};
function show(){
     var checkElem = document.getElementsByClassName("a0")[0].value
     console.log(checkElem)
     
     var element = document.getElementById("rs");
     element.style.visibility = "visible";
      };

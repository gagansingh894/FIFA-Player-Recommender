function getValue(){
    var name = document.getElementsByClassName("search_player_txt")[0].value;
    document.getElementById("myForm").submit();
    // var x = document.getElementById("p6").getElementsByTagName("h2");
    // console.log(x);

    
    // for (i=0; i<6; i++){
    //   var div = document.createElement('div');
    //   idx = "p" + i.toString()
    //   div.setAttribute('class', 'note');
    //   div.setAttribute('id', idx);
    //   if (i == 0) {
    //     document.getElementById(idx).innerHTML = "";
    //     document.body.appendChild(div);
    //   } else {
    //     document.getElementById(idx).innerHTML = "{{ recommendedNames[" + idx + "][0] }}";
    //     document.body.appendChild(div);
    //     var element = document.createElement('select');
    //     element.style.width = "100px";
    //   }
    // }    
    // return name;
  }


// function setValue(){
//   var s = getValue()
// }
  
// function showValue(){
//     var x = document.getElementById('rc');
//         if (x.style.visibility === 'hidden') {
//           x.style.visibility = 'visible';
//         } else {
//           x.style.visibility = 'visible';
//         }

//         for (i=0; i<5; i++){
//             var idx = i+1;
//             var elem = "p" + idx.toString();
//             document.getElementById(elem).innerHTML = "{{ recommendedNames[" + i.toString() + "][0] }}";
//         }
//         showValue()
//     // document.getElementsById("rc").style.visibility = "visible"; 
// }


//     for (i=0; i<5; i++){
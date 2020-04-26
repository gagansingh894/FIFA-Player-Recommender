function getValue(){
    var name = document.getElementsByClassName("search_player_txt")[0].value;
    document.getElementById("myForm").submit();

}

function showValue(){
    var x = document.getElementById('rc');
        if (x.style.visibility === 'hidden') {
          x.style.visibility = 'visible';
        } else {
          x.style.visibility = 'visible';
        }

        for (i=0; i<5; i++){
            var idx = i+1;
            var elem = "p" + idx.toString();
            document.getElementById(elem).innerHTML = "{{ recommendedNames[" + i.toString() + "][0] }}";
        }
        showValue()
    // document.getElementsById("rc").style.visibility = "visible"; 
}
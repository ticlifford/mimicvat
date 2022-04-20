filterSelection("all")
function filterSelection(c) {
  var x, i, j, b, d, split_words;
  x = document.getElementsByClassName("filterDiv");
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    b = 0;
    d = 0;
    split_words = x[i].className.split(" ")
    for (j=0; j < split_words.length; j++){
        if (split_words[j]==c){b++; console.log('increasing b:',b);}
        if (split_words[j]=="show"){d++; console.log('increasing d:',d);}

    }

    if (c == "all") b = 1;
    if (b>0 && d == 0) w3AddClass(x[i], "show");

  }
}

function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
  }
}

function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// Add active class to the current button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
    
    console.log('btn clicked i:',btns[i]);
    btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("activefilter");
    console.log('current:',current)
    current[0].className = current[0].className.replace(" activefilter", "");
    this.className += " activefilter";
  });
}
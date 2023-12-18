/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/ClientSide/javascript.js to edit this template
 */
function deleteProduct()
{
      document.getElementById("statusrow").style.display = 'none';
      document.getElementById("info").style.display = 'none';
      document.getElementById('productdeleteconfirm').style.display='block';
  }


function statusshow()
{
  if(document.getElementById("statusrow").style.display === 'block')
  {
      document.getElementById("statusrow").style.display = 'none';
  }
  else
  {
      document.getElementById("statusrow").style.display = 'block';
      document.getElementById("info").style.display = 'none';
  }
  }

function info() {
  if(document.getElementById("info").style.display === 'block')
{
document.getElementById("info").style.display = 'none';
}
else
{
document.getElementById('info').style.display = 'block';
document.getElementById('statusrow').style.display = 'none';
}
}
function openleftNav(y) {
  var w = window.innerWidth;

  if( w >= 1025 ){ 
      document.getElementById(y).style.width = "30%";
      }
      else {
          if(w > 700 && w < 1025)
            {document.getElementById(y).style.width = "40%";}
            else
            {document.getElementById(y).style.width = "60%";}
    }
      }
     
    function closeleftNav(y) {
      document.getElementById(y).style.width = "0%";
  
  }
  function openrightNav(z) {
    var w = window.innerWidth;
    
    if( w >= 1025 ){ 
        document.getElementById(z).style.width = "35%";
        }
        else {
            if(w > 700 && w < 1025)
              {document.getElementById(z).style.width = "60%";}
              else
              {document.getElementById(z).style.width = "90%";}
      }
        }
  
  function closerightNav(z) {
    if(z == 'changepasswordNav'){  
      document.getElementById(z).style.width = "0%";
      document.querySelector('.c-psw').value = '';
      document.querySelector('.n-psw').value = '';
      document.querySelector('.r-psw').value = '';
      document.querySelector('.psw-msg').textContent = ''
    } else {
      document.getElementById(z).style.width = "0%";
    }
    }
// function openNav(y) {
  
// if(document.getElementById(y).style.width === "50%")
// {
// document.getElementById(y).style.width = "0%";
// }
// else
// {
// document.getElementById(y).style.width = "50%";
// }
// }

// function closeNav(y) {
// document.getElementById(y).style.width = "0%";

// }

window.addEventListener("resize", resizetoggleMaxHeight);

function resizetoggleMaxHeight() {
  var w = window.innerWidth;
  const elements = document.querySelectorAll('.accordion-content');
  for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    const actualHeight = element.offsetHeight;
    if (actualHeight !== '0px') {
      element.style.maxHeight = actualHeight;
    }
  }
}
// function toggleMaxHeight(){

//   var div = document.getElementById("elementId");
//   var divHeight = div.scrollHeight + 10; // get the scroll height and add 10
//   div.style.height = divHeight + "px"; // set the height of the div element
// }


function toggleMaxHeight(elementId, newMaxHeight, newMaxHeight1) {
  var element = document.getElementById(elementId);
  var w = window.innerWidth;
 
  if (element) {
    if (element.style.maxHeight === '0px') {
      if( w >= 1025 ){ 
        element.style.maxHeight = newMaxHeight;
     }
          else {
              if(w > 700 && w < 1025)
                {element.style.maxHeight = newMaxHeight;}
                else
                {element.style.maxHeight = newMaxHeight1;} }
        
          if(document.getElementById(elementId+"Cancel")){
          document.getElementById(elementId+"Cancel").style.display = "block";
          document.getElementById(elementId+"Save").style.display = "block";
          }
      } 

    else {
      element.style.maxHeight = '0';
      if(document.getElementById(elementId+"Cancel")){
        document.getElementById(elementId+"Cancel").style.display = "none";
        document.getElementById(elementId+"Save").style.display = "none";  
      }
     }
  } else {
    console.log("Element with ID '" + elementId + "' not found.");
  }
}

function showdiv(x) {

if(document.getElementById(x).style.display === "block")
{
document.getElementById(x).style.display = "none";


}
else
{
document.getElementById(x).style.display = "block";


}
}

function arrowdirection(x){
var element = document.getElementById(x);
if (element.classList.contains("fa-arrow-circle-down")) {
  element.classList.remove("fa-arrow-circle-down");
  element.classList.add("fa-arrow-circle-up");
} else {
  element.classList.remove("fa-arrow-circle-up");
  element.classList.add("fa-arrow-circle-down");
}
}

function ChangePswMsgStatus(psw) {
// Check password and put the results (true or false in a variable
var result1 = psw.match(/[A-Z]/) ? "true" : "false";
var result2 = psw.match(/[a-z]/) ? "true" : "false";
var result3 = psw.match(/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/) ? "true" : "false";
var result4 = psw.match(/[0-9]/) ? "true" : "false";
var result5 = psw.length >= 8 ? "true" : "false";
var result6 = document.getElementById("psw").value;
var result7 = document.getElementById("psw-repeat").value;
// -----------------------------
// 1- check the password match :
// ---------------------------
if (result6 === "") {
  var element = document.getElementById("lab6");
  element.style.color = "red";
  element.innerHTML = element.innerHTML.replace(/✔/g, "✖");
} else if (result6 === result7) {
  var element = document.getElementById("lab6");
  element.style.color = "green";
  element.innerHTML = element.innerHTML.replace(/✖/g, "✔");
} else {
  var element = document.getElementById("lab6");
  element.style.color = "red";
  element.innerHTML = element.innerHTML.replace(/✔/g, "✖");
}
// ----------------------------------
// 2- Check the password conditions :
// ---------------------------------
// create array for password check results variables
results = [result1, result2, result3, result4, result5];
// create array for password message parts
labels = ["lab1", "lab2", "lab3", "lab4", "lab5"];
// create for loop and using the previous 2 arrays in it to repalce 
// the invalied message to valid for every part of the message
for (i = 0; i < 5; i++) {
  if (results[i] === "true")
  {
      var element = document.getElementById(labels[i]);
      element.innerHTML = element.innerHTML.replace(/✖/g, "✔");
      element.style.color = "green";
  } else
  {
      var element = document.getElementById(labels[i]);
      element.innerHTML = element.innerHTML.replace(/✔/g, "✖");
      element.style.color = "red";
  }
}
;
}
// END  of Check the password conditions ---------------------------
// 
//--------------------------------
// show password condition message 
//--------------------------------
function hidePswMsg() {
document.getElementById("pswMessage").style.display = "none";
}
;
function showPswMsg() {
document.getElementById("pswMessage").style.display = "block";
}
;
// End show password condition message ---------------------------------------
// 
//--------------------------------
// show password Match condition message 
//--------------------------------
function hidePswMatchMsg() {
document.getElementById("pswMatchMsg").style.display = "none";
}
;
function showPswMatchMsg() {
document.getElementById("pswMatchMsg").style.display = "block";
}
;


// End show password condition message ---------------------------------------




/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/ClientSide/javascript.js to edit this template
 */


function myFunction() {
  var x = document.getElementById("mynavbar");
  if (x.className === "navbar") {
    x.className += " responsive";
  } else {
    x.className = "navbar";
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
        element.style.backgroundColor = "white";
        element.style.color = "red";
        element.innerHTML = element.innerHTML.replace(/✔/g, "✖");
    } else if (result6 === result7) {
        var element = document.getElementById("lab6");
        element.style.backgroundColor = "white";
        element.style.color = "green";
        element.innerHTML = element.innerHTML.replace(/✖/g, "✔");
    } else {
        var element = document.getElementById("lab6");
        element.style.backgroundColor = "white";
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
            element.style.backgroundColor = "white";
            element.style.color = "green";
        } else
        {
            var element = document.getElementById(labels[i]);
            element.innerHTML = element.innerHTML.replace(/✔/g, "✖");
            element.style.backgroundColor = "white";
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

//A Function to Set a Cookie
//we create a function that stores the name of the user and the password in a cookie variable:
/*function createCookie()
 {
 if (document.getElementById("loginRemember").is(':checked'))
 {
 let cname = document.getElementById("usr1");
 let cpwd = document.getElementById("loginpsw");
 
 
 today = new Date();
 var expire = new Date();
 expire.setTime(today.getTime() + 3600000 * 24 * 15);
 
 
 document.cookie = "user" + cname.value + ";path=/" + ";expires=" + expire.toUTCString();
 document.cookie = "password=" + encodeURI(cpwd.value) + ";path=/" + ";expires=" + expire.toUTCString();
 }
 
 //can only write one entity at a time (name, pass)
 }
 */

function getCookie(username) {
    var name = username + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie(username) {

    let user = getCookie(username);
    if (user !== "") {
        // alert("Welcome again " + user);
        document.getElementById('loginpsw').value = user;
    }else
    {
       document.getElementById('loginpsw').value = ""; 
    }
}


function AddRemoveCookie(cname, cvalue, exdays) {
    if (document.getElementById('loginRemember').checked) {
            //Add Cookie
        //alert(cname + " - " + cvalue + " - " + exdays);
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toGMTString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    } else
    {     //Remove Cookie
        const d = new Date();
        d.setTime(d.getTime() - (24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toGMTString();
        document.cookie = cname + "=" + ";" + expires + ";path=/";
    }
}

function clearForm()
{
    document.getElementById('loginpsw').value = "";
    document.getElementById('usr1').value = "";
   
}
function orginfo() {
    if(document.getElementById("OrgInfo").style.display === 'block')
  {
    document.getElementById("OrgInfo").style.display = 'none';
  }
  else
  {
    document.getElementById('OrgInfo').style.display = 'block';
  }
  }
function openNav() {
    if(document.getElementById("myNav").style.width === "0%")
    {
      document.getElementById("myNav").style.width = "50%";
    }
    else
    {
      document.getElementById("myNav").style.width = "0%";
    }
  }
function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}

  document.addEventListener('DOMContentLoaded', function() {
    var cancelButton = document.getElementById('cancel-btn');

    cancelButton.addEventListener('click', function() {
      location.reload();
    });
  });

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

function arrowdirection(x) {
    if (document.getElementById(x).className === "fa fa-arrow-circle-down") {
      document.getElementById(x).className = "fa fa-arrow-circle-up";
    } else {
      document.getElementById(x).className = "fa fa-arrow-circle-down";
    }
  }

 

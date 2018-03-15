$(document).ready(function(){
   var userTypeSelect = $("select");
   userTypeSelect.on("change", function(){
       var element=this.value;

       var profiles=document.getElementsByClassName("profile");
       for(var i=0;i<profiles.length;i++){
           if(profiles[i].getAttribute('id') == element)
               profiles[i].style.display='block';
           else
               profiles[i].style.display='none'
       }


   });
});
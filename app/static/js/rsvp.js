"use strict";function submitAvailability(t,i){var a="PLAYING"===document.getElementById("player_availability").value;try{postAvailabilityToApi(t,i,a)}catch(t){console.log(t)}}async function postAvailabilityToApi(t,i,a){i=await fetch("/rsvp/"+i,{method:"POST",mode:"cors",cache:"no-cache",headers:{"Content-Type":"application/json"},body:JSON.stringify({player:t,availability:a})});if(200!=i.status)throw new Error(i.status);Swal.fire({icon:"success",title:"Nice!",timer:4e3,showConfirmButton:!1}).then(()=>{window.location="/"})}
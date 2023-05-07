"use strict";

function submitAvailability(player, rsvp_token, csrf_token) {
  const response = document.getElementById("player_availability").value;

  const is_playing = response === "PLAYING";

  try {
    postAvailabilityToApi(player, rsvp_token, is_playing, csrf_token);
  } catch (error) {
    console.log(error);
  }
}

async function postAvailabilityToApi(user, token_endpoint, is_playing, csrf_token) {
  const response = await fetch("/rsvp/" + token_endpoint, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token
    },
    body: JSON.stringify({
      player: user,
      availability: is_playing,
    }),
  });

  if (response.status == 200) {
    Swal.fire({
      icon: "success",
      title: "Nice!",
      timer: 4000,
      showConfirmButton: false,
    }).then(() => {
      window.location = "/";
    });
  } else {
    throw new Error(response.status);
  }
}

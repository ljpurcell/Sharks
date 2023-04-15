"use strict";

function submitAvailability(player, token) {
  const response = [document.getElementById("playing").value];

  const is_playing = response == "PLAYING";

  try {
    postAvailabilityToApi(player, token, is_playing);
  } catch (error) {
    console.log(error);
  }
}

async function postAvailabilityToApi(user, token_endpoint, is_playing) {
  const response = await fetch("/rsvp/" + token_endpoint, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
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

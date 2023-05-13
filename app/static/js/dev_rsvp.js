"use strict";

function submitAvailability(player, date_string) {
  const response = document.getElementById("player_availability").value;

  const is_playing = response === "PLAYING";

  try {
    postAvailabilityToApi(player, date_string, is_playing);
  } catch (error) {
    console.log(error);
  }
}

async function postAvailabilityToApi(user, date_string, is_playing) {
  const csrf_token = document.getElementById('csrf_token').value;

  const response = await fetch("/my-availability", {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token
    },
    body: JSON.stringify({
      game_date: date_string,
      player: user,
      availability: is_playing,
    }),
  });

  if (response) {
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

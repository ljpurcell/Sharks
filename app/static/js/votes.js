"use strict";

function submitVotes() {
  const voteGetterOptions = [
    document.getElementById("playerMenu1").value,
    document.getElementById("playerMenu2").value,
    document.getElementById("playerMenu3").value,
  ];

  const voteOptions = [
    parseInt(document.getElementById("votesMenu1").value),
    parseInt(document.getElementById("votesMenu2").value),
    parseInt(document.getElementById("votesMenu3").value),
  ];

  const validatedVotes = votesAreValid(voteGetterOptions, voteOptions);

  const indicesOfPlayers = voteGetterOptions.map(function (player) {
    return Boolean(player) && player !== "Player";
  });

  console.log(indicesOfPlayers);

  if (validatedVotes.value) {
    const votesAssigned = playersWhoGotVotes.map((player, i) => ({
      player: player,
      votes: givenVotes[i],
    }));

    const voteAssignments = {
      roundID: "TEST",
      voteGiverID: "TEST",
      assignedVotes: votesAssigned,
    };
    try {
      postVotesToApi(voteAssignments);
    } catch (error) {
      console.log(error);
    }
  } else {
    invalidVotes(validatedVotes.message);
  }
}

function votesAreValid(players, votes) {
  const givenVotes = votes.filter(Boolean);

  const votesSum = givenVotes.reduce(function (accumulator, current) {
    return accumulator + current;
  }, 0);

  if (votesSum !== 3) {
    return {
      value: false,
      message: "Total votes '" + votesSum + "' not equal to 3",
    };
  } else if (playersWhoGotVotes.length !== givenVotes.length) {
    return {
      value: false,
      message: "Mismatch of players and assigned votes",
    };
  } else {
    return {
      value: true,
      message: "Your votes were recorded successfully",
    };
  }
}

async function postVotesToApi(votes) {
  const response = await fetch("/record-votes", {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(votes),
  });

  if (response.ok) {
    const message = await response.json();
    Swal.fire({
      icon: "success",
      title: "Nice!",
      text: message,
      timer: 4000,
      showConfirmButton: false,
    }).then(() => {
      window.location = "/";
    });
  } else {
    invalidVotes(response.message);
    throw new Error(response.status);
  }
}
function invalidVotes(message) {
  Swal.fire({
    icon: "error",
    title: "Woops!",
    text: message,
  });
}

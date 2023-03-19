"use strict";

function submitVotes() {
  let voteGetter1 = document.getElementById("playerMenu1").value;
  let voteGetter2 = document.getElementById("playerMenu2").value;
  let voteGetter3 = document.getElementById("playerMenu3").value;
  let voteGetterOptions = [voteGetter1, voteGetter2, voteGetter3];

  let votes1 = parseInt(document.getElementById("votesMenu1").value);
  let votes2 = parseInt(document.getElementById("votesMenu2").value);
  let votes3 = parseInt(document.getElementById("votesMenu3").value);
  let voteOptions = [votes1, votes2, votes3];

  validatedVotes = votesAreValid(voteGetterOptions, voteOptions);

  if (validatedVotes.value) {
    let votesAssigned = playersWhoGotVotes.map(function (player, i) {
      return { player: player, votes: givenVotes[i] };
    });
    let voteAssignments = {
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
  let playersWhoGotVotes = players.filter(function (player) {
    return Boolean(player) && player !== "Player";
  });

  let givenVotes = votes.filter(Boolean);

  let votesSum = votes.reduce(function (accumulator, current) {
    return accumulator + current;
  }, 0);

  let playerInRow = playersWhoGotVotes.map((player) => {
    return players.includes(player);
  });

  let votesInRow = givenVotes.map((vote) => {
    return votes.includes(vote);
  });

  console.log(playerInRow);
  console.log(votesInRow);

  if (votesSum !== 3) {
    return {
      value: false,
      message: "Total votes '" + votesSum + "' not equal to 3",
    };
  } else if (
    playersWhoGotVotes.length !== givenVotes.length ||
    playerInRow !== votesInRow
  ) {
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

function postVotesToApi(votes) {
  fetch("/record-votes", {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(votes),
  }).then(() => {
    Swal.fire({
      icon: "success",
      title: "Nice!",
      text: message,
      timer: 4000,
      showConfirmButton: false,
    }).then(() => {
      window.location = "/";
    });
  });
}
function invalidVotes(message) {
  Swal.fire({
    icon: "error",
    title: "Woops!",
    text: message,
  });
}

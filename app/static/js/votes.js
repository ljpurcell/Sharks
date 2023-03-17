"use strict";

function submitVotes() {
  let votes1 = parseInt(document.getElementById("votesMenu1").value);
  let votes2 = parseInt(document.getElementById("votesMenu2").value);
  let votes3 = parseInt(document.getElementById("votesMenu3").value);

  let voteOptions = [votes1, votes2, votes3];
  let givenVotes = voteOptions.filter(Boolean);

  let votesSum = givenVotes.reduce(function (accumulator, current) {
    return accumulator + current;
  }, 0);

  if (votesSum !== 3) {
    invalidVotes("Total votes '".concat(votesSum, "' not equal to 3"));
    return false;
  }

  let voteGetter1 = document.getElementById("playerMenu1").value;
  let voteGetter2 = document.getElementById("playerMenu2").value;
  let voteGetter3 = document.getElementById("playerMenu3").value;

  let voteGetterOptions = [voteGetter1, voteGetter2, voteGetter3];

  let playersWhoGotVotes = voteGetterOptions.filter(function (player) {
    return Boolean(player) && player !== "Player";
  });

  console.log(voteOptions);
  console.log(playersWhoGotVotes);

  let indicesOfPlayersWithVotes = playersWhoGotVotes.map((player) => {
    return voteGetterOptions.indexOf(player);
  });

  let indicesOfVotes = givenVotes.map((vote) => {
    return voteOptions.indexOf(vote);
  });

  console.log(indicesOfPlayersWithVotes);
  console.log(indicesOfVotes);

  if (
    playersWhoGotVotes.length !== givenVotes.length ||
    indicesOfPlayersWithVotes !== indicesOfVotes
  ) {
    invalidVotes("Mismatch of players and assigned votes");
  } else {
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
      text: "Your votes were recorded successfully",
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

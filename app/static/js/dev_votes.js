"use strict";

function submitVotes(seasonString, rndString, dateString, csrf_token) {
  const playerOptions = [
    document.getElementById("playerMenu1").value,
    document.getElementById("playerMenu2").value,
    document.getElementById("playerMenu3").value,
  ];

  const voteOptions = [
    parseInt(document.getElementById("votesMenu1").value),
    parseInt(document.getElementById("votesMenu2").value),
    parseInt(document.getElementById("votesMenu3").value),
  ];

  const validatedVotes = votesValidator(playerOptions, voteOptions);

  if (validatedVotes.value) {
    const voteAssignments = {
      season: seasonString,
      round: rndString,
      date: dateString,
      assignedVotes: validatedVotes.votes,
    };
    try {
      postVotesToApi(voteAssignments, csrf_token);
    } catch (error) {
      console.log(error);
    }
  } else {
    invalidVotes(validatedVotes.message);
  }
}

function votesValidator(players, votes) {
  const playersWhoGotVotes = players.filter(
    (player) => Boolean(player) && player !== "Player"
  );

  const givenVotes = votes.filter(Boolean);

  const votesSum = givenVotes.reduce(
    (accumulator, current) => accumulator + current
  );

  const indicesOfPlayers = players.map((player) =>
    playersWhoGotVotes.includes(player)
  );
  const indicesOfVotes = votes.map((vote) => givenVotes.includes(vote));

  const distinctPlayersWhoGotVotes = new Set(playersWhoGotVotes);

  /**
   * Vote validation:
   * 1. Three votes have been given (votesSum)
   * 2. The number of players selected is the same as votes have been awarded (playersWhoGotVotes == givenVotes)
   * 3. There are no rows with only a vote or player assigned (playerInRow == voteInRow)
   * 4. There are no players listed more than once (playersWhoGotVotes.length == distinctPlayersWhoGotVotes.size)
   */

  if (votesSum !== 3) {
    return {
      value: false,
      message: "Total votes '" + votesSum + "' not equal to 3",
    };
  } else if (
    playersWhoGotVotes.length !== givenVotes.length ||
    !arraysAreSame(indicesOfPlayers, indicesOfVotes)
  ) {
    return {
      value: false,
      message: "Mismatch of players and assigned votes",
    };
  } else if (playersWhoGotVotes.length !== distinctPlayersWhoGotVotes.size) {
    return {
      value: false,
      message: "You have listed a player more than once",
    };
  } else {
    const votesAssigned = playersWhoGotVotes.map((player, i) => ({
      player: player,
      votes: givenVotes[i],
    }));

    return {
      value: true,
      message: "Your votes were recorded successfully",
      votes: votesAssigned,
    };
  }
}

async function postVotesToApi(votes, csrf_token) {
  const response = await fetch("/record-votes", {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token
    },
    body: JSON.stringify(votes),
  });

  if (response) {
    const message = await response.json();
    Swal.fire({
      icon: "success",
      title: "Nice!",
      text: votes.message,
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

function arraysAreSame(arr1, arr2) {
  return JSON.stringify(arr1) === JSON.stringify(arr2);
}

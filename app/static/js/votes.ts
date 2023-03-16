function submitVotes(): Boolean {
  const votes1: number = parseInt(
    (<HTMLSelectElement>document.getElementById("votesMenu1")).value
  );

  const votes2: number = parseInt(
    (<HTMLSelectElement>document.getElementById("votesMenu2")).value
  );

  const votes3: number = parseInt(
    (<HTMLSelectElement>document.getElementById("votesMenu3")).value
  );

  const givenVotes: Array<number> = [votes1, votes2, votes3].filter(Boolean);
  console.log(givenVotes);

  const votesSum: number = givenVotes.reduce((accumulator, current) => {
    return accumulator + current;
  }, 0);

  if (votesSum !== 3) {
    invalidVotes(`Total votes '${votesSum}' not equal to 3`);
    return false;
  }

  const voteGetter1: string = (<HTMLSelectElement>(
    document.getElementById("playerMenu1")
  )).value;

  const voteGetter2: string = (<HTMLSelectElement>(
    document.getElementById("playerMenu2")
  )).value;

  const voteGetter3: string = (<HTMLSelectElement>(
    document.getElementById("playerMenu3")
  )).value;

  let playersWhoGotVotes: Array<String> = [
    voteGetter1,
    voteGetter2,
    voteGetter3,
  ].filter((player) => Boolean(player) && player !== "Player");

  if (playersWhoGotVotes.length !== givenVotes.length) {
    invalidVotes("Mismatch of players and assigned votes");
    return false;
  }

  const votesAssigned: Object = playersWhoGotVotes.map((player, i) => {
    return { player: player, votes: givenVotes[i] };
  });

  const voteAssignments: Object = {
    roundID: "TEST",
    voteGiverID: "TEST",
    assignedVotes: votesAssigned,
  };

  try {
    postVotesToApi(voteAssignments);
  } catch (error) {
    console.log(error);
    return false;
  }

  return true;
}

function postVotesToApi(votes: Object): void {
  const votesEndPoint: string = "/votes";

  fetch(votesEndPoint, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(votes),
  });
}

function invalidVotes(message: String): void {
  const votesEndPoint: string = "/error-votes";

  fetch(votesEndPoint, {
    method: "GET",
    mode: "cors",
    cache: "no-cache",
    body: JSON.stringify(message),
  });
}

let message: string = "hello from TS";
console.log(message);

function submitVotes(): Boolean {
 
}

function getVoteAssignments(): Object | Error {
  const voteElement1: HTMLSelectElement = document.getElementById(
    "votesMenu1"
  ) as HTMLSelectElement;
  const votes1: number = parseInt(voteElement1.value) || 0;

  const voteElement2: HTMLSelectElement = document.getElementById(
    "votesMenu2"
  ) as HTMLSelectElement;
  const votes2: number = parseInt(voteElement2.value) || 0;

  const voteElement3: HTMLSelectElement = document.getElementById(
    "votesMenu3"
  ) as HTMLSelectElement;
  const votes3: number = parseInt(voteElement3.value) || 0;

  const totalVotes: number = votes1 + votes2 + votes3;
  
   if (totalVotes !== 3) {
     return Error;
   }

   const voteGetter1: string = (<HTMLSelectElement>document.getElementById(
    "playerMenu1"
   )).value || null;

   const voteGetter2: string = (<HTMLSelectElement>document.getElementById(
    "playerMenu2"
   )).value || null;

   const voteGetter3: string = (<HTMLSelectElement>document.getElementById(
    "playerMenu3"
   )).value || null;

   let playersWhoGotVotes: Array<String> = [voteGetter1, voteGetter2, voteGetter3].map(player => {
        if (player !== null) return player;
    });

    


    const votesAssigned: Object = playersWhoGotVotes.map((player, i) => {
        return {player, }
    })


    const votes: Object = {
        'roundID': '',
        'voteGiverID': '',
        'assignedVotes': votesAssigned
    


   try {
     
     };
     postVotesToApi(votes);
   } catch (error) {
     console.log(error);
     return false;
   }

  
  
  return { player: "", votes: 0 };
}


function postVotesToApi(votes: Object): void {
  const votesEndPoint: string = "/submit-votes";

  fetch(votesEndPoint, {
    method: "POST",
    body: JSON.stringify(votes),
  });
}

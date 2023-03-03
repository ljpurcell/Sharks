function submitVotes() {
    var votes1 = parseInt(document.getElementById("votesMenu1").value);
    var votes2 = parseInt(document.getElementById("votesMenu2").value);
    var votes3 = parseInt(document.getElementById("votesMenu3").value);
    var givenVotes = [votes1, votes2, votes3].filter(Boolean);
    console.log(givenVotes);
    var votesSum = givenVotes.reduce(function (accumulator, current) {
        return accumulator + current;
    }, 0);
    if (votesSum !== 3) {
        console.log("Total votes '".concat(votesSum, "' not equal to 3"));
        return false;
    }
    var voteGetter1 = (document.getElementById("playerMenu1")).value;
    var voteGetter2 = (document.getElementById("playerMenu2")).value;
    var voteGetter3 = (document.getElementById("playerMenu3")).value;
    var playersWhoGotVotes = [
        voteGetter1,
        voteGetter2,
        voteGetter3,
    ].filter(function (player) { return Boolean(player) && player !== "Player"; });
    console.log(playersWhoGotVotes);
    if (playersWhoGotVotes.length !== givenVotes.length) {
        console.log("Mismatch of players and assigned votes");
        return false;
    }
    var votesAssigned = playersWhoGotVotes.map(function (player, i) {
        return { player: player, votes: givenVotes[i] };
    });
    console.log(votesAssigned);
    var voteAssignments = {
        roundID: "TEST",
        voteGiverID: "TEST",
        assignedVotes: votesAssigned
    };
    try {
        postVotesToApi(voteAssignments);
    }
    catch (error) {
        console.log(error);
        return false;
    }
    return true;
}
function postVotesToApi(votes) {
    var votesEndPoint = "/votes";
    fetch(votesEndPoint, {
        method: "POST",
        body: JSON.stringify(votes)
    });
}

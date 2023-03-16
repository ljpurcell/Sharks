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
        invalidVotes("Total votes '".concat(votesSum, "' not equal to 3"));
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
    if (playersWhoGotVotes.length !== givenVotes.length) {
        invalidVotes("Mismatch of players and assigned votes");
        return false;
    }
    var votesAssigned = playersWhoGotVotes.map(function (player, i) {
        return { player: player, votes: givenVotes[i] };
    });
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
    var votesEndPoint = "/record-votes";
    fetch(votesEndPoint, {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(votes)
    }).then(function (response) {
        alert("Votes posted successfully");
        if (response.redirected) {
            window.location = response.url;
        }
    });
}
function invalidVotes(message) {
    return alert(message);
}

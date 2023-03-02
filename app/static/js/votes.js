var message = "hello from TS";
console.log(message);
function calculateVotesLeftToAssign() {
    var voteElement1 = document.getElementById("votesMenu1");
    var votes1 = parseInt(voteElement1.value) || 0;
    var voteElement2 = document.getElementById("votesMenu2");
    var votes2 = parseInt(voteElement2.value) || 0;
    var voteElement3 = document.getElementById("votesMenu3");
    var votes3 = parseInt(voteElement3.value) || 0;
    var totalVotes = votes1 + votes2 + votes3;
    console.log(totalVotes);
    return 3 - totalVotes;
}
function getVotesAssignment() {
    return { player: "", votes: 0 };
}
function postVotesToApi() {
    // post votes to api end point
}

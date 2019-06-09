function candidateselect(element){
	// Store the name and id of the selected candidate
	c_name = $(element).children(".candidate-header").html();
	c_id = $(element).children(".candidate-header").attr("candidate_id");
	house = $(element).children(".candidate-header").attr("house");
	poll_id = $(element).children(".candidate-header").attr("poll_id");

	//Confirmation for casting the vote
	confirmation = confirm("Select OK to confirm and cast your vote for " + c_name +" of House " + house);
	if(confirmation){
		document.location = "/cast/"+poll_id+"/"+c_id+"/";
	}else{
		alert("Select a candidate to vote for.");
	}
	
}





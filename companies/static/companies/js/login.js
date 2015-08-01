$('#loginForm').on('submit', function() {
	var email = $("input#loginEmail").val();
	if (email.endsWith('princeton.edu')) {
		window.alert('Please log in with NetID, using orange button to the left.');
		$('#loginForm').trigger("reset");
		return false;
	}
	else return true;
});
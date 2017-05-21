$(document).ready(function() {

	var maxBittLength = 140;

	$('#new-bitt-text').keyup(function() {
		var length = maxBittLength - $(this).val().length;
		$('#chars').text(length);
	});
	
});
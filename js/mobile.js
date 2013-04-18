$(function() {
	var data = {
		hall: 'whitman',
		day: '4/18/2013'
	}
	$.ajax({
		url: '/hall',
		data: data,
		success: function(r) {
			$('#hall').html(r);
		},
		error: function(r) {
			console.log(r);
		}
	});
})
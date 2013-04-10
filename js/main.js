// Load meal
$(function() {
	$('#meal-selector-form input').on('click', function() {
		var meal = $(this).attr('id');
		console.log(meal);
		$.ajax({
			url: '/menus',
			data: {
				meal: meal
			},
			success: function(r) {
				$('#menus-container').html(r);
			}
		});
	});
	$('#meal-selector-form input[id=lunch]').trigger('click');
});

$("document").ready(function() {
	$("#filters-form").hide();
	$("#filters-button").click(function() {
		$("#filters-form").toggle("slow");
	});
});
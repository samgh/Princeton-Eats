// Load meal
$(function() {
	$('#meal-selector-form input').on('click', function() {
		var meal = $(this).attr('id');
		$.ajax({
			url: '/menus',
			data: {
				meal: meal
			},
			async: false,
			success: function(r) {
				$('#menus-container').html(r);
			}
		});
	});
	$('#meal-selector-form input[id=lunch]').trigger('click');
});

$("document").ready(function() {
	// showing and hiding filters
	$("#filters-form").hide();
	$("#filters-button").click(function() {
		$("#filters-form").toggle("slow");
	});

	// handling checking and unchecking of filters
	$("#filters-form :checkbox").each(function() {
		if (this.checked) {
			$("." + $(this).attr('value')).css("color", "red");
		}
	});
	$("#filters-form :checkbox").click(function() {
		var $this = $(this);
		if ($this.is(':checked')) {
			$("." + $(this).attr('value')).css("color", "red");
		}
		else {
			$("." + $(this).attr('value')).css("color", "black");
			$("#filters-form :checkbox").each(function() {
				if (this.checked) {
					$("." + $(this).attr('value')).css("color", "red");
				}
			});
		}
	});

	// uncheck all filters
	$("#clear-filters").click(function() {
		$("#filters-form :checkbox").each(function() {
			$(this).attr("checked", false);
			$("." + $(this).attr('value')).css("color", "black");
		});
	});
});
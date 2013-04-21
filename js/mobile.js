$(function() {
	$("#filters").hide();
	$("#search").hide();
	getHall();
	setFilters();
	setSearch();
});

function getHall() {
	var data = {
		hall: 'whitman',
		day: '4/21/2013'
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
}

function setSearch() {
	$("#search-button-container").unbind("click");
	$("#search-button-container").click(function() {
		$("#filters").hide();
		$("#search").toggle();
		$("#search :input[type='text']").focus();
	});
}

function setFilters() {
	// showing and hiding filters
	$("#filters-button").unbind("click");
	$("#filters-button").click(function() {
		$("#search").hide();
		$("#filters").toggle();
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
};
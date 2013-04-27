var hall, 
	day;

$(function() {
	$("#filters").hide();
	$("#search").hide();
	setFilters();
	setSearch();
	setInitialDate();
});

function getHall() {
	var data = {
		hall: hall,
		day: day
	}
	$('#hall').css("opacity", "0.5");
	$.ajax({
		url: '/hall',
		data: data,
		success: function(r) {
			$('#hall').html(r);
			setAccordion();
			$('#hall').css("opacity", "1")
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

function setHallSelector() {
	$(".dining-hall-selector").click(function() {
		var container = $(this).attr('id')
		if (container === 'butlerwilson-selector') {
			hall = 'butlerwilson';
		} else if (container === 'forbes-selector') {
			hall = 'forbes';
		} else if (container === 'rockymathey-selector') {
			hall = 'rockymathey';
		} else if (container === 'whitman-selector') {
			hall = 'whitman';
		}
		getHall();
	});
	$('#butlerwilson-selector').trigger('click');
}

function setInitialDate() {
	var d0 = new Date(), d1 = new Date(), d2 = new Date(), d3 = new Date(), 
		d4 = new Date(), d5 = new Date();
	d0.setDate(d0.getDate() - 1);
	d1.setDate(d1.getDate());
	d2.setDate(d2.getDate() + 1);
	d3.setDate(d3.getDate() + 2);
	d4.setDate(d4.getDate() + 3);
	d5.setDate(d5.getDate() + 4);
	var dates = {
		0 : $.datepicker.formatDate('D, M d', d0),
		1 : $.datepicker.formatDate('D, M d', d1),
		2 : $.datepicker.formatDate('D, M d', d2),
		3 : $.datepicker.formatDate('D, M d', d3),
		4 : $.datepicker.formatDate('D, M d', d4),
		5 : $.datepicker.formatDate('D, M d', d5)
	};
	var $dateSelector = $("#date-selector-container select");
	$.each(dates, function(key, value) {
		$dateSelector.append($("<option></option>").attr("value", key).text(value));
	});
	$dateSelector.val(1);
	$dateSelector.change(function() {
		$("#date-selector-container select option:selected").each(function() {
			var dayVal = $(this).val();
			switch (dayVal) {
				case '0': day = dateString(d0);
					break;
				case '1': day = dateString(d1);
					break;
				case '2': day = dateString(d2);
					break;
				case '3': day = dateString(d3);
					break;
				case '4': day = dateString(d4);
					break;
				case '5': day = dateString(d5);
					break;
				default: day = dateString(d1);	
			}
			getHall();
		});
	});
	day = dateString(d1);
	setHallSelector();
}

function dateString(d) {
	return $.datepicker.formatDate('m/dd/yy', d);
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

function setAccordion() {
	$('#breakfast').hide();
	$('#dinner').hide();
	$('#breakfast-header').click(function() {
		$('#breakfast').show();
		$('#lunch').hide();
		$('#dinner').hide();
	});
	$('#lunch-header').click(function() {
		$('#breakfast').hide();
		$('#lunch').show();
		$('#dinner').hide();
	});
	$('#dinner-header').click(function() {
		$('#breakfast').hide();
		$('#lunch').hide();
		$('#dinner').show();
	});
}
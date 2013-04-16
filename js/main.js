var meal, 
	day;

$(function() {
	// Init
	initMealSelection();
	initDaySelection();
	
	// Trigger a meal selection
	$('#meal-selector-form input[id=' + meal + ']').trigger('click');
});

//Init meal selections
function initMealSelection() {
	$('#meal-selector-form input').on('click', function() {
		meal = $(this).attr('id');
		refreshMeals();
	});
	meal = 'lunch'; // Default, needs logic
}

// Init day selection
function initDaySelection() {
	var datepicker = $("#datepicker");
	datepicker.datepicker({
		dateFormat: 'DD, MM d',
		minDate: "-1D", 
		maxDate: "+5D",
		onSelect: function() {
			setDay(datepicker.datepicker('getDate'));
			refreshMeals();
		}
	}).datepicker('setDate', '+0');
	setDay(datepicker.datepicker('getDate'));
}

// Refresh meals
function refreshMeals() {
	var data = { 
		meal: meal, 
		day: day
	};
	$("#ajax-loader").show();
	$("#overlay").show();
	$.ajax({
		url: '/menus',
		data: data,
		success: function(r) {
			//setTimeout(function() {
			$('#menus-container').html(r);
			$('#ajax-loader').hide();
			$('#overlay').hide();//}, 500);
			setMenuListeners();
		},
		error: function(r) {
			console.log(r);
		}
	});
}

// Format javascript date
function setDay(d) {
	var date = d.getDate();
	var month = d.getMonth() + 1;
	var year = d.getFullYear();
	day = month + '/' + date + '/' + year;
}

// Set entree events
function setMenuListeners() {
	$('.item').on('click', function() {
		var el = $(this);
		var id = $(this).data('entreeid');
		$.get('/entree?id=' + id, function(r) {
			showEntree(el, r);
		});
	});
}

// Show entree
function showEntree(entreeEl, entreeHtml) {
	entreeEl.qtip({
	    content: {
	    	text: entreeHtml,
	    },
	    position: {
	    	my: 'top center',
	    	at: 'bottom center',
	    	target: entreeEl
	    },
	    hide: {
	    	event: 'unfocus'
	    },
	    show: {
	    	event: 'click',
	    	ready: true
	    },
	    events: {
	    	render: function() {
				//Global.set_notification_listeners();				    	
	    	}
	    },
	    style: 'qtip-shadow qtip-rounded qtip-light'
	});
}

$(function() {
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
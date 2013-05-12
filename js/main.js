var meal, 
	day;

$(function() {
	// Hide filters
	$("#filters-form").hide();
	if (window.location.pathname == '/') {
		var tempDay = getQueryVariable("day");
		var tempMeal = getQueryVariable("meal");
		if (tempDay != -1 && tempMeal != -1 && validate(tempMeal, tempDay)) {
			day = getQueryVariable("day");
			meal = getQueryVariable("meal");
			initMealSelection(true);
			initDaySelection(true);
		}
		else {
			// Init
			initMealSelection(false);
			initDaySelection(false);
		}
		// Trigger a meal selection
		$('#meal-selector-form input[id=' + meal + ']').trigger('click');
	}
	else {
		setFilters();
	}

	// Set entree listeners
	setEntreeListeners();
});

function getQueryVariable(variable)
{ 
	var query = window.location.search.substring(1); 
  	var vars = query.split("&"); 
  	for (var i=0;i<vars.length;i++) { 
	    var pair = vars[i].split("="); 
    	if (pair[0] == variable) { 
		    return pair[1]; 
    	} 
  	}
  	return -1; //not found 
}

function validate(tempMeal, tempDay) {
	return (validateMeal(tempMeal) && validateDay(tempDay));
}

function validateMeal(mealGet) {
	return (mealGet == "breakfast" || mealGet == "lunch" || mealGet == "dinner");
}

function validateDay(dayGet) {
	var d1 = new Date();
	d1.setHours(0,0,0,0);
	d1.setDate(d1.getDate() - 1);
	var d2 = new Date(dayGet);
	return ((d2 - d1) < 86400000 * 7);
}

//Init meal selections
function initMealSelection(hasMeal) {
	$('#meal-selector-form input').on('click', function() {
		meal = $(this).attr('id');
		$('#meal-selector-form :radio').each(function() {
			$('label[for=' + this.id + ']').css("background", "#ccc");
		});
		$('label[for=' + meal + ']').css("background", "#888");
		refreshMeals();
	});
	selectMeal(hasMeal);
}

// Auto meal selection
function selectMeal(hasMeal) {
	if (hasMeal == false) {
		var d = new Date();
		if (d.getHours() < 14) {
			meal = 'lunch';
		} else if (d.getHours() < 20) {
			meal = 'dinner';
		} else {
			meal = 'breakfast';
		}
		if (d.getUTCDay() != 0 && d.getUTCDay() != 7) {
			if (d.getHours() < 11) {
				meal = 'breakfast';
			}
		}
	}
	$('#meal-selector-form :radio').each(function() {
		$('label[for=' + this.id + ']').css("background", "#ccc");
	});
	$('label[for=' + meal + ']').css("background", "#888");
}

// Init day selection
function initDaySelection(hasDay) {
	var datepicker = $("#datepicker");
	datepicker.datepicker({
		dateFormat: 'DD, MM d',
		minDate: "-1d", 
		maxDate: "+5d",
		onSelect: function() {
			setDay(datepicker.datepicker('getDate'));
			refreshMeals();
		}
	}).datepicker('setDate', '+0');

	var d = new Date();
	if (d.getHours() >= 20) {
		datepicker.datepicker('setDate', '+1');
	}

	if (hasDay) {
		datepicker.datepicker('setDate', new Date(day));
	}
	setDay(datepicker.datepicker('getDate'));

	// Set previous and next controls
	$('.date-control').on('click', function() {
		var action = $(this).data('action');
		var op = action == 'prev' ? -1 : 1;
		var date = datepicker.datepicker('getDate');
		date = new Date(date.getTime() + op * 24 * 60 * 60 * 1000);
		datepicker.datepicker('setDate', date);
		setDay(date);
		refreshMeals();
		return false;
	});
}

// Refresh meals
function refreshMeals() {
	var data = { 
		meal: meal, 
		day: day
	};
	$("#ajax-loader").show();
	$('#menus-table #meal').css("opacity", "0.5");
	var selectedDay = new Date(day);
	if (selectedDay.getDay() == 0 || selectedDay.getDay() == 6) {
		$("#meal-selector-form label[for='lunch']").html("Brunch");
		$("#meal-selector-form label[for='lunch']").css("border-left", "1px solid gray");
		$("#meal-selector-form label[for='lunch']").css("border-radius", "3px 0 0 3px");
		$("label[for='breakfast']").hide();
		if (meal == "breakfast") {
			$('#meal-selector-form input[id=lunch]').trigger('click');
			return;
		}
	}
	else {
		$("label[for='breakfast']").show();
		$("#meal-selector-form label[for='lunch']").html("Lunch");
		$("#meal-selector-form label[for='lunch']").css("border-left", "");
		$("#meal-selector-form label[for='lunch']").css("border-radius", "");
	}
	$.ajax({
		url: '/menus',
		data: data,
		success: function(r) {
			$('#menus-container').html(r);
			$('#ajax-loader').hide();
			$('#menus-table #meal').css("opacity", "1")
			setMenuListeners();
			setFilters();
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
	    		setEntreeListeners();
	    	}
	    },
	    style: 'qtip-shadow qtip-rounded qtip-light'
	});
}

// Set entree listeners
function setEntreeListeners() {
	var ratings = $('.rating');
	ratings.off('click');
	ratings.on('click', function() {
		var el = $(this);
		var vote = $(this).parent().data('vote');
		var entreeID = $(this).parent().data('id');
		var action = $(this).data('action');
		// Validate
		if (vote == 1 && action == 'up' || vote == -1 && action == 'down') {
			return;
		}

		$.ajax({
			url: '/entree',
			data: {
				id: entreeID,
				vote: action == 'up' ? 1 : -1
			},
			type: 'POST',
			success: function(r) {				
				// Set styling
				el.addClass('selected');
				el.siblings().removeClass('selected');

				// Set number
				if (vote != 0) {
					var numEl = el.siblings().find('.num');
					var num = numEl.html();
					numEl.html(parseInt(num) - 1);
				}
				var numEl = el.find('.num');
				var num = numEl.html();
				numEl.html(parseInt(num) + 1);

				// Set vote
				el.parent().data('vote', action == 'up' ? '1' : '-1');
			},
			error: function(r) {
				console.log(r);
			}
		});
	});
}

function setFilters() {
	// showing and hiding filters
	$("#filters-button").unbind("click");
	$("#filters-button").click(function() {
		$("#filters-form").slideToggle("slow");
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
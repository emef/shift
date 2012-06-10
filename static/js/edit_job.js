var g;
function get_title(shift) {
    return $(shift).find(".shift-title");
}

function get_attrs(shift) {
    return $(shift).find(".shift-designer");
}

function get_role(shift) {
    return $(shift).find("select[name=role]").find("option:selected").text()
}

function set_role_form(shift, role) {
    attrs = get_attrs(shift);
    attrs.find(".role-form").hide().removeClass('set');
    attrs.find(".role-" + role).show().addClass('set');
}

function update_title(shift, text) {
    var title_box = $(shift).find("#id_title");
    get_title(shift).find("> span").text('Shift: ' + text);
    title_box.val(text);
    title_box.bind('change', function() {
	update_title(shift, $(this).val());
    });
}

function update_attrs(src, dest) {
    $(src).find("input").each(function() {
	var name = $(this).attr("name");
	dest.find("input[name=" + name + "]").val($(this).val());
    });
}

function init_shift(shift) {
    shift = $(shift);
    shift.addClass("job-shift");
    var del = shift.find(".deletelink");
    var modal = shift.find(".modallink");
    del.css("visibility", "visible");
    shift.unbind('click');
    del.click(function() {
	shift.remove();
    });
    shift.find("select[name=role]").change(function () {
	var role = $(this).find("option:selected").text();
	set_role_form(shift, role);
    }).change();
    shift.find("input[name=start], input[name=end]").each(function() {
	var input = $(this);
	var newinput = $("<input type='text' />");
	newinput.attr('name', input.attr('name'));
	newinput.val(input.val());
	newinput.insertBefore(input);
	newinput.datetimepicker({
	     dateFormat:"yy-mm-dd",
	     timeFormat:"h:m:s",
	     ampm: true
	});
	input.remove();
    });
    
    shift.find("input.range").each(function() {
	var hidden = $(this);
	var name = $(this).attr("name");
	var min = $("<input type='text' name='"+"min-"+name+"' />");
	var max = $("<input type='text' name='"+"max-"+name+"' />");
	var label = $("<label>" + name + "</label>");
	var li = $("<li />").append(label);
	
	if (hidden.val().length != 0) {
	    var vals = hidden.val().split(',');
	    min.val(vals[0]);
	    max.val(vals[1]);
	}
	
	if (hidden.hasClass("male")) li.addClass("male");
	if (hidden.hasClass("female")) li.addClass("female");
	
	var update = function() {
	    hidden.val(min.val() + "," + max.val());
	}
	min.change(update);
	max.change(update);
	
	li.append(min);
	li.append(max);
	$(this).parent().append(li);
    });
    shift.find("select.male, select.female").each(function() {
	var genderclass;
	if ($(this).hasClass("male"))
	    genderclass = "male";
	else
	    genderclass = "female";
	$(this).parent("li").addClass(genderclass);
    });
    var attrs = get_attrs(shift);
    attrs.find("select[name=Gender]").change(function () {
	var val = $(this).find("option:selected").text();
	if (val == "Male") {
	    attrs.find("li.male").show();
	    attrs.find("li.female").hide();
	} else if (val == "Female") {
	    attrs.find("li.male").hide();
	    attrs.find("li.female").show();
	} else {
	    attrs.find("li.male, li.female").show();
	}
    });
    g = modal;
    modal.click(function () {
	get_attrs(shift).modal({
	    persist: true,
	    onClose: function() {
		$.modal.close();
	    }
	});
    });
}

function valid_key(key) {
    return ! /(min-)|(max-)/.test(key)
}

function shift_to_obj() {
    var shift = $(this);
    var info = $(shift.find("form")[0]).toObject();
    var attrs = {};
    get_attrs(shift).find("form.set").each(function() {
	var obj = $(this).toObject();
	for (var key in obj) {
	    if (valid_key(key) && obj[key] != "-1" && obj[key] != undefined ) 
		attrs[key] = obj[key];
	}
    });
    return {info: info, attrs: attrs}
}

function save() {
    var data = {}
    data.basic = $("#basic-form").toObject();
    data.shifts = $.makeArray($(".job-shift").map(shift_to_obj));
    $('html').animate({scrollTop:0}, 'fast');
    $('body').animate({scrollTop:0}, 'fast');
    $('#errors').text('loading... please wait');
    $.ajax({
	url: window.location.path,
	type: 'POST',
	dataType: 'json',
	data: {json: JSON.stringify(data)},
	success: function(r) {
	    console.log(data);
	    $('#errors').html('');
	    $('#errors').children().remove();
	    if (r.status == 'ok') {
		$('#errors').html('<h3>Successfuly saved job info</h3>');
		$('#errors').fadeOut(2000, function() {
		    $('#errors').html('').show();
		});
	    } else {
		for (var title in r.errors) {
		    var div = $("<div />");
		    var h4 = $("<h4 />");
		    var ul = $("<ul />");
		    h4.text(title);
		    div.append(h4);
		    div.append(ul);
		    $('#errors').append(div);
		    for (var i=0; i<r.errors[title].length; i++) {
			var li = $("<li />");
			li.text(r.errors[title][i]);
			ul.append(li);
		    }
		}
	    }
	}
    });
}

$(document).ready(function () {
    var new_shift = $(".new-shift").clone();
    var mk_new_shift = function () {
	var next_new_shift = new_shift.clone();
	
	/* setup as new shift */
	init_shift(this);
	update_title(this, 'New Shift');
	
	/* setup the next 'add' button */
	mk_toggleable(next_new_shift, false);
	next_new_shift.click(mk_new_shift);
	$(this).parent().append(next_new_shift);
    }
    $(".job-shift").each(function() { init_shift(this) });
    $(".new-shift").click(mk_new_shift);
    $("#save-job").click(save);
});

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
    });
    shift.find("input[name=start], input[name=end]").datetimepicker({
	dateFormat:"yy-mm-dd",
	timeFormat:"h:m:s",
	ampm: true
    });
    g = modal;
    modal.click(function () {
	console.log('hi');
	get_attrs(shift).modal({
	    persist: true,
	    onClose: function() {
		$.modal.close();
	    }
	});
    });
}

function shift_to_obj() {
    var shift = $(this);
    var info = $(shift.find("form")[0]).toObject();
    var attrs = {};
    get_attrs(shift).find("form.set").each(function() {
	var obj = $(this).toObject();
	for (var key in obj) {
	    console.log(key, attrs[key]);
	    if (obj[key] != "-1") 
		attrs[key] = obj[key];
	}
    });
    return {info: info, attrs: attrs}
}

function save() {
    var data = {}
    data.basic = $("#basic-form").toObject();
    data.shifts = $.makeArray($(".job-shift").map(shift_to_obj));
    $.ajax({
	url: window.location.path,
	type: 'POST',
	dataType: 'json',
	data: {json: JSON.stringify(data)},
	success: function(r) { 
	    //window.location = '/client-manager/'
	    console.log(data, r);
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

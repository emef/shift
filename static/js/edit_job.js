var g;
function get_title(shift) {
    return $(shift).find(".shift-title");
}

function get_attrs(shift) {
    return $(shift).find(".shift-designer");
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
	console.log(name);
	console.log(dest);
	dest.find("input[name=" + name + "]").val($(this).val());
    });
}

function init_shift(shift) {
    shift = $(shift);
    var del = shift.find(".deletelink");
    var modal = shift.find(".modallink");
    del.css("visibility", "visible");
    shift.unbind('click');
    del.click(function() {
	shift.remove();
    });
    modal.click(function () {
	get_attrs(shift).modal({
	    persist: true,
	    onClose: function() {
		g = shift;
		$.modal.close();
	    }
	});
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
});

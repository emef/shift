var nav_ids = {}

function register_page(section, page) {
    if (!page) {
        nav_ids[section] = {
            id: "#" + section + "-nav",
            pages: {}
        };
    } else {
        nav_ids[section].pages[page] = "#" + page + "-nav";
    }
}

function nav_set(section, page) {
    $(document).ready(function() {
        var section_id = nav_ids[section].id;
        var page_id = nav_ids[section].pages[page];
        $(section_id + "," + page_id).addClass("active");
    });
}

register_page('shiftleader');
register_page('shiftleader', 'openjobs_list');
register_page('shiftleader', 'openjobs_calendar');
register_page('shiftleader', 'openjobs_gantt');
register_page('shiftleader', 'contractors_search');
register_page('shiftleader', 'unassigned_jobs');
register_page('shiftleader', 'completed_jobs');

register_page('talentmanager');

register_page('clientmanager');
register_page('clientmanager', 'job_new');
register_page('clientmanager', 'job_open');
register_page('clientmanager', 'job_edit');
register_page('clientmanager', 'job_status');

function mk_toggleable(parent, open) {
    var title = $(parent).find("> div:first-child");
    var data = title.next();
    var toggle_on, toggle_off;
	
    toggle_on = function() {
	data.show();
	title.bind('click', toggle_off);
    }

    toggle_off = function() {
	data.hide();
	title.click('click', toggle_on);
    }

    if (open)
	toggle_on();
    else
	toggle_off();
}

$(document).ready(function() {
    $(".toggle-able").each(function() {
	mk_toggleable(this)
    });
});

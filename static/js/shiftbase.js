var console = console || {log: function(msg) {}};
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
	//data.insertAfter(title);
	title.bind('click', toggle_off);
    }

    toggle_off = function() {
	data.hide();
	//data.remove();
	title.click('click', toggle_on);
    }

    
    if (open)
	toggle_on();
    else
	toggle_off();
	
}

$(document).ready(function() {
    setTimeout(function() {
	$(".toggle-able").each(function() {
	    mk_toggleable(this)
	});
    }, 250);
});


jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

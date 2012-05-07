var globals = [];
$(document).ready(function() {
    $($('div.inline-stacked')[1]).find('.items > div').removeClass('collapse-closed').addClass('collapse-open');
    var photos = $($('div.inline-group')[0]);
    var parent = photos.parent();
    photos.remove();
    parent.prepend(photos);
    photos.find('input[type=file]').change(function() {
	
    });
});

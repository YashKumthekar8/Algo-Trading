$(function() {

	$('.js-multiple-select').select2({
		tags: true,
		tokenSeparators: [',', ' '],
		placeholder: 'Select a state'
	});

});
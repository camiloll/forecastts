var $loaderSpin = $('#loaderSpin');
var $submitBtn = $('.ui.submit');

$(function(){
	$('.ui.form')
	.form({
	  fields: {
		"data"     : 'empty',
		"H" 	   : 'empty'
	  },
	  onSuccess: function(e, fields) {
		e.preventDefault();
		$submitBtn.prop('disabled',true);
		$loaderSpin.show();
		var formData = new FormData(document.getElementById('dataInput'));

		$.ajax({
			url: '/data/upload',
			type: 'POST',
			enctype: 'multipart/form-data',
			data: formData,
			contentType: false,
			processData: false,
			cache: false,
			success: function(r){
				$submitBtn.prop('disabled',false);
				$loaderSpin.hide();
				
				var data = JSON.parse(r);
				plot(data['t'], data['ts']);
			},
			error: function(e){
				console.error(e);
				$submitBtn.prop('disabled',false);
				$loaderSpin.hide();
			}
		});
	  }
	});
	
});

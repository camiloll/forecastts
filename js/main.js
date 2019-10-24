var $loaderSpin = $('#loaderSpin');
var $submitBtn = $('.ui.submit');
var $summary = $('#summary');
var data;

$(function () {
	$('.ui.form')
		.form({
			fields: {
				"file": 'empty',
				"H": 'empty',
				"C": 'empty',
				"Y": 'empty'
			},
			onSuccess: function (e, fields) {
				e.preventDefault();
				$submitBtn.prop('disabled', true);
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
					success: function (r) {
						$submitBtn.prop('disabled', false);
						$loaderSpin.hide();

						data = JSON.parse(r);
						print(data);
						plot(data);
					},
					error: function (e) {
						console.error(e);
						$submitBtn.prop('disabled', false);
						$loaderSpin.hide();
					}
				});
			}
		});

});
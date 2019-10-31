var $loaderSpin = $('#loaderSpin');
var $btnToggleInfo = $('#btnToggleInfo');
var $autoarimaForm = $('#autoarimaForm');
var $submitBtn = $('.ui.submit');
var $summary = $('#summary');
var $output = $('#output');
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
				formData.append('log', $('#btnLog').checkbox('is checked'));
				if ($autoarimaForm.is(':visible')) {
					formData.append('autoarima', 'off');
					formData.append('P', $('#autoarimaInput * input[name="P"]').val());
					formData.append('D', $('#autoarimaInput * input[name="D"]').val());
					formData.append('Q', $('#autoarimaInput * input[name="Q"]').val());
				};
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

						try {
							data = JSON.parse(r);
							print(data);
							plot(data);
						} catch (error) {
							printError(r);
						}
					},
					error: function (e) {
						console.error(e);
						$submitBtn.prop('disabled', false);
						$loaderSpin.hide();
					}
				});
			}
		});

	$('#btnAutoARIMA').checkbox({
		fireOnInit: true,
		onChecked: function () {
			$autoarimaForm.hide();

		},
		onUnchecked: function () {
			$autoarimaForm.show();
		},
		onChange: function () {
			$summary.hide();
			$output.hide();
		}
	});

	$('#btnLog').checkbox();

});
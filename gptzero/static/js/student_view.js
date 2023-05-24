function GptZeroXBlock(runtime, element) {
  // Submit the form and send the text for prediction
  $(element).find('#text-form').on('submit', function(e) {
      e.preventDefault();
      var data = JSON.stringify({
          text: $(this).find('#text-input').val()
      });
      runtime.notify('submit', {state: 'start'});
      $.post(runtime.handlerUrl(element, 'submit_text'), data).done(function() {
        runtime.notify('submit', {state: 'end'});
      });
  });
}

function GPTZeroXBlockStudio(runtime, element) {
    var _GPTZeroXBlockStudio = this;

    _GPTZeroXBlockStudio.element = element;
    _GPTZeroXBlockStudio.runtime = runtime
    _GPTZeroXBlockStudio.notify = typeof (runtime.notify) !== 'undefined';

    _GPTZeroXBlockStudio.URL = {
        UPDATE_SETTINGS: runtime.handlerUrl(element, 'update_settings')
    }

    _GPTZeroXBlockStudio.Selector = {
        SUBMIT_BUTTON: 'button.save-button[type="submit"]',
        STUDIO_FORM: '#gptzero-configs',
    }

    _GPTZeroXBlockStudio.View = {
        SUBMIT_BUTTON: $(_GPTZeroXBlockStudio.Selector.SUBMIT_BUTTON, element),
        STUDIO_FORM: $(_GPTZeroXBlockStudio.Selector.STUDIO_FORM, element),
    }

    $(function ($) {
        _GPTZeroXBlockStudio.init($);
    });
}

GPTZeroXBlockStudio.prototype.init = function($) {
    var _GPTZeroXBlockStudio = this;

    $(_GPTZeroXBlockStudio.View.STUDIO_FORM).submit(function (e) {
        e.preventDefault();
        var formData = _GPTZeroXBlockStudio.toJson(this);
        var config = {
            success: function (res) {
                if (_GPTZeroXBlockStudio.notify) {
                    _GPTZeroXBlockStudio.runtime.notify('save', {state: 'end'});
                }
            }
        };
        if (_GPTZeroXBlockStudio.notify) {
            _GPTZeroXBlockStudio.runtime.notify('save', {state: 'start', message: 'Saving'});
        }
        _GPTZeroXBlockStudio.submit(_GPTZeroXBlockStudio.URL.UPDATE_SETTINGS, formData, config);
        return false;
    });
}

GPTZeroXBlockStudio.prototype.toJson = function (form) {
    var serializedArray = $(form).serializeArray(), data = {};
    $.each(serializedArray, function (index, item) {
        data[item.name] = item.value;
    });

    return data;
}

GPTZeroXBlockStudio.prototype.submit = function (url, formData, config = undefined) {
    var _config = {
        url: url,
        type: "POST",
        contentType: false,
        cache: false,
        processData: false,
        data: JSON.stringify(formData)
    };
    _config = $.extend({}, _config, config);
    $.ajax(_config);
}

GPTZeroXBlockStudio.prototype.save = function () {
    var _GPTZeroXBlockStudio = this;

    $(_GPTZeroXBlockStudio.View.STUDIO_FORM).submit();
}

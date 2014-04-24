/* Before loading the Select2 library, ensure that window.jQuery is available.
 * If it's not, set it to django.jQuery which is loaded by the admin.
 */

var _jq = (jQuery || django.jQuery)

// We need this because Select2 needs window.jQuery
// to initialize. In fact it removes jQuery.noConflict(true) if
// django.jQuery is used.
if (window.jQuery == undefined) {
    window.jQuery = _jq;
}
if (window.$ == undefined) {
    window.$ = _jq;
}

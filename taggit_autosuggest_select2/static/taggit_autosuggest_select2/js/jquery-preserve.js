/* After loading the Select2 library, put jQuery into our own namespace.  If window.jQuery
 * wasn't defined when we ran jquery-prepare.js, we will have aliased it to django.jQuery -- in
 * that case, use jQuery.noConflict to free up window.jQuery again.
 */
var taggit_autosuggest = taggit_autosuggest || {};
if (django && jQuery === django.jQuery) {
  taggit_autosuggest.jQuery = jQuery.noConflict(true);
} else {
  taggit_autosuggest.jQuery = jQuery;
}

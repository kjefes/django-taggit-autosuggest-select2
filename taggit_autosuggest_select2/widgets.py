import copy
import json

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from taggit_autosuggest_select2.utils import edit_string_for_tags
json_encode = json.JSONEncoder().encode


MAX_SUGGESTIONS = getattr(settings, 'TAGGIT_AUTOSUGGEST_SELECT2_MAX_SUGGESTIONS', 20)
EXTRA_SETTINGS = getattr(settings, 'TAGGIT_AUTOSUGGEST_SELECT2_EXTRA_SETTINGS',{})
LOAD_SELECT2 = getattr(settings, 'TAGGIT_AUTOSUGGEST_SELECT2_LOAD_SELECT2', True)
WIDTH = getattr(settings, 'TAGGIT_AUTOSUGGEST_SELECT2_WIDTH', '60em')

class TagAutoSuggest(forms.TextInput):
    input_type = 'text'
    extra_settings = {}
    url = reverse_lazy('taggit_autosuggest_select2-list')

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            tags = [o.tag for o in value.select_related("tag")]
            value = edit_string_for_tags(tags)

        result_attrs = copy.copy(attrs)
        result_attrs['type'] = 'hidden'
        result_html = super(TagAutoSuggest, self).render(name,
                                                         value,
                                                         result_attrs)
        widget_attrs = copy.copy(attrs)
        widget_attrs['id'] += '__tagautosuggest'
        widget_html = super(TagAutoSuggest, self).render(name,
                                                         value,
                                                         widget_attrs)

        start_text = self.attrs.get('start_text') or _("Enter Tag Here")
        empty_text = self.attrs.get('empty_text') or _("No Results")
        prompt_text = self.attrs.get('prompt_text') or _("Enter a tag")
        limit_text = self.attrs.get('limit_text') or _('No More Selections Are Allowed')
        # In case there is no field_width, use the global setting TAGGIT_AUTOSUGGEST_SELECT2_WIDTH
        field_width = self.attrs.get('field_width') or WIDTH


        self.extra_settings.update(EXTRA_SETTINGS)

        context = {
            'result_id': result_attrs['id'],
            'widget_id': widget_attrs['id'],
            'url': self.url,
            'start_text': start_text,
            'prompt_text': prompt_text,
            'empty_text': empty_text,
            'limit_text': limit_text,
            'field_width': field_width,
            'retrieve_limit': MAX_SUGGESTIONS,
            'extra_settings': json_encode(self.extra_settings),
        }
        js = render_to_string('taggable_input.html', context)

        return result_html + widget_html + mark_safe(js)

    class Media:
        if LOAD_SELECT2:
            js_base_url = getattr(settings, 'TAGGIT_AUTOSUGGEST_SELECT2_STATIC_BASE_URL', 
            '%staggit_autosuggest_select2/' % settings.STATIC_URL)
            select2_css_url = getattr(settings,'TAGGIT_AUTOSUGGEST_SELECT2_CSS_URL',
                '%sselect2/select2.css' % js_base_url)
            select2_js_url = getattr(settings,'TAGGIT_AUTOSUGGEST_SELECT2_JS_URL',
                '%sselect2/select2.min.js' % js_base_url)
            css = {'all': (select2_css_url,)}
            js = [
                "%sjs/jquery-prepare.js" % js_base_url,
                select2_js_url, 
                "%sjs/jquery-preserve.js" % js_base_url
            ]

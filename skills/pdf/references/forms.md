# Interactive forms

Inspect `PdfReader.get_fields()` before editing. Field names may be hierarchical
and repeated across pages. Check each page's `/Widget` annotations and their
`/Parent` relationships when field discovery and visible controls disagree.
XFA forms and signature fields require specialized handling beyond this recipe.

For ordinary AcroForms, copy the whole document and fill the requested fields:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
requested = {"contact_name": "Taylor"}  # use actual field names and user values
fields = reader.get_fields() or {}
if not requested.keys() <= fields.keys():
    raise ValueError("Requested fields are absent; inspect the form before editing")
writer = PdfWriter()
writer.append(reader)
writer.update_page_form_field_values(None, requested, auto_regenerate=False)
writer.write("completed.pdf")
saved = PdfReader("completed.pdf").get_fields() or {}
for name, value in requested.items():
    if saved[name].get("/V") != value:
        raise ValueError(f"Saved value differs for {name}")
```

This example is for text fields. Check boxes, radio groups, and choices use
their defined export values, not arbitrary strings. Inspect each control's
available states before writing it. Keep fields editable unless the user
requests a static result.

After saving, compare logical field values with the associated page controls,
then render the updated pages. A correct stored value can still have an outdated
appearance; a correct preview can hide missing logical field data.

If the field tree is damaged, do not automatically rebuild it without examining
the widgets. A repair may introduce duplicate names or lose hierarchy. Preserve
the original and stop if the intended field cannot be identified unambiguously.

For requested flattening, consult the installed pypdf API first. In supported
versions, `flatten=True` paints field appearances into page content; removing
widget annotations completes the static conversion. Include existing values in
fields the user did not change so they remain visible. Reopen and render the
result, confirm no interactive widgets remain, and remove obsolete form-tree
entries only after checking there are no fields that should stay interactive.

Reference: [pypdf form documentation](https://pypdf.readthedocs.io/en/stable/user/forms.html).

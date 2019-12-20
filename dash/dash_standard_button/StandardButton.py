# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class StandardButton(Component):
    """A StandardButton component.
StandardButton

A button able to trigger a JavaScript function using a string "onclick",
like you would do in pure HTML

Compatible with Dash callbacks using n_click prop

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- onClick (string; optional): On click callback (must be a string, as Dash components user defined props must be serializable)
- id (string; optional): The ID used to identify this component in Dash callbacks.
- className (string; optional)
- n_clicks (number; default 0): An integer that represents the number of times
that this element has been clicked on.
- n_clicks_timestamp (number; default -1): An integer that represents the time (in ms since 1970)
at which n_clicks changed. This can be used to tell
which button was changed most recently.
- key (string; optional): A unique identifier for the component, used to improve
performance by React.js while rendering components
See https://reactjs.org/docs/lists-and-keys.html for more info
- role (string; optional): The ARIA role attribute
- data-* (string; optional): A wildcard data attribute
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, onClick=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'onClick', 'id', 'className', 'n_clicks', 'n_clicks_timestamp', 'key', 'role', 'data-*', 'loading_state']
        self._type = 'StandardButton'
        self._namespace = 'dash_standard_button'
        self._valid_wildcard_attributes =            ['data-']
        self.available_properties = ['children', 'onClick', 'id', 'className', 'n_clicks', 'n_clicks_timestamp', 'key', 'role', 'data-*', 'loading_state']
        self.available_wildcard_properties =            ['data-']

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(StandardButton, self).__init__(children=children, **args)

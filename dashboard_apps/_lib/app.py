from typing import Callable, Any, List, Mapping, TypeVar
import streamlit as st

TNav = TypeVar('TNav', bound='Nav')


class Nav():
    def __init__(
        self,
        title: str,
        app: Callable[[], Any] = lambda *arg, **kwargs: None,
        children: List[TNav] = []
    ):
        self.title = title
        self.app = app
        self.children = children
    
    def to_map(self, child_only: bool = False) -> Mapping[str, Callable[[], Any]]:
        result: Mapping[str, Callable[[], Any]] = {} if child_only else {self.title: self.app}
        for index, child in enumerate(self.children):
            child_map = child.to_map()
            for key, val in child_map.items():
                result[f'{index+1}.{key}'] = val
        return result


class App():
    def __init__(self, nav: Nav):
        self.nav = nav
    
    def run(self):
        app_map = self.nav.to_map(child_only=True)
        caption = st.sidebar.radio("Go to", list(app_map.keys()))
        app_map[caption]()


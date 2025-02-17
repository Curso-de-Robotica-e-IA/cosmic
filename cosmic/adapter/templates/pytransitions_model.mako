<%!
from mako.template import Template
%>\


class ${agent_name}Model:
    # Auto generated code. Please, adjust!

    % for dec_func in declared_functions:
    def ${dec_func}(self):
        raise NotImplementedError('Implement This Model Behavior.')

    % endfor
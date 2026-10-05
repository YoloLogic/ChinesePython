# -*- coding: utf-8 -*-
"""注解库 —— 汉语库（由 tools/汉化库.py 从 Lib/annotationlib.py 机械生成，**不要手改**）。

英文库 Lib/annotationlib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 注解库
"""


"""Helpers for introspecting and wrapping annotations."""
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import ast
import builtins
import enum
import keyword
import sys
import types
__all__ = ['Format', 'ForwardRef', 'call_annotate_function', 'call_evaluate_function', 'get_annotate_from_class_namespace', 'get_annotations', 'annotations_to_string', 'type_repr']

class 格式(enum.IntEnum):
    VALUE = 1
    VALUE_WITH_FAKE_GLOBALS = 2
    FORWARDREF = 3
    STRING = 4
_sentinel = object()
_NAME_ERROR_MSG = "name '{name:.200}' is not defined"
_SLOTS = ('__forward_is_argument__', '__forward_is_class__', '__forward_module__', '__weakref__', '__arg__', '__globals__', '__extra_names__', '__code__', '__ast_node__', '__cell__', '__owner__', '__stringifier_dict__', '__resolved_str_cache__')

class 前向引用:
    """Wrapper that holds a forward reference.

    Constructor arguments:
    * arg: a string representing the code to be evaluated.
    * module: the module where the forward reference was created.
      Must be a string, not a module object.
    * owner: The owning object (module, class, or function).
    * is_argument: Does nothing, retained for compatibility.
    * is_class: True if the forward reference was created in class scope.

    """
    __slots__ = _SLOTS

    def __init__(self, arg, *, module=None, owner=None, is_argument=True, is_class=False):
        if not isinstance(arg, str):
            raise TypeError(f'Forward reference must be a string -- got {arg!r}')
        self.__arg__ = arg
        self.__forward_is_argument__ = is_argument
        self.__forward_is_class__ = is_class
        self.__forward_module__ = module
        self.__owner__ = owner
        self.__globals__ = None
        self.__cell__ = None
        self.__extra_names__ = None
        self.__code__ = None
        self.__ast_node__ = None
        self.__resolved_str_cache__ = None

    def __init_subclass__(cls, /, *args, **kwds):
        raise TypeError('Cannot subclass ForwardRef')

    def 求值(self, *, globals=None, locals=None, type_params=None, owner=None, format=格式.VALUE):
        """Evaluate the forward reference and return the value.

        If the forward reference cannot be evaluated, raise an exception.
        """
        match format:
            case 格式.STRING:
                return self.__resolved_str__
            case 格式.VALUE:
                is_forwardref_format = False
            case 格式.FORWARDREF:
                is_forwardref_format = True
            case _:
                raise NotImplementedError(format)
        if isinstance(self.__cell__, types.CellType):
            try:
                return self.__cell__.cell_contents
            except ValueError:
                pass
        if owner is None:
            owner = self.__owner__
        if globals is None and self.__forward_module__ is not None:
            globals = getattr(sys.modules.get(self.__forward_module__, None), '__dict__', None)
        if globals is None:
            globals = self.__globals__
        if globals is None:
            if isinstance(owner, type):
                module_name = getattr(owner, '__module__', None)
                if module_name:
                    module = sys.modules.get(module_name, None)
                    if module:
                        globals = getattr(module, '__dict__', None)
            elif isinstance(owner, types.ModuleType):
                globals = getattr(owner, '__dict__', None)
            elif callable(owner):
                globals = getattr(owner, '__globals__', None)
        if globals is None:
            globals = {}
        if type_params is None and owner is not None:
            type_params = getattr(owner, '__type_params__', None)
        if locals is None:
            locals = {}
            if isinstance(owner, type):
                locals.update(vars(owner))
        elif type_params is not None or isinstance(self.__cell__, dict) or self.__extra_names__:
            locals = dict(locals)
        if type_params is not None:
            for param in type_params:
                locals.setdefault(param.__name__, param)
        if isinstance(self.__cell__, dict):
            for cell_name, cell in self.__cell__.items():
                try:
                    cell_value = cell.cell_contents
                except ValueError:
                    pass
                else:
                    locals.setdefault(cell_name, cell_value)
        if self.__extra_names__:
            locals.update(self.__extra_names__)
        arg = self.__forward_arg__
        if arg.isidentifier() and (not keyword.iskeyword(arg)):
            if arg in locals:
                return locals[arg]
            elif arg in globals:
                return globals[arg]
            elif hasattr(builtins, arg):
                return getattr(builtins, arg)
            elif is_forwardref_format:
                return self
            else:
                raise NameError(_NAME_ERROR_MSG.format(name=arg), name=arg)
        else:
            code = self.__forward_code__
            try:
                return eval(code, globals=globals, locals=locals)
            except Exception:
                if not is_forwardref_format:
                    raise
            new_locals = _StringifierDict({**builtins.__dict__, **globals, **locals}, globals=globals, owner=owner, is_class=self.__forward_is_class__, format=format)
            try:
                result = eval(code, globals=globals, locals=new_locals)
            except Exception:
                return self
            else:
                new_locals.transmogrify(self.__cell__)
                return result

    def _evaluate(self, globalns, localns, type_params=_sentinel, *, recursive_guard):
        import typing
        import warnings
        if type_params is _sentinel:
            typing._deprecation_warning_for_no_type_params_passed('typing.ForwardRef._evaluate')
            type_params = ()
        warnings._deprecated('ForwardRef._evaluate', '{name} is a private API and is retained for compatibility, but will be removed in Python 3.16. Use ForwardRef.evaluate() or typing.evaluate_forward_ref() instead.', remove=(3, 16))
        return typing.evaluate_forward_ref(self, globals=globalns, locals=localns, type_params=type_params, _recursive_guard=recursive_guard)

    @property
    def __forward_arg__(self):
        if self.__arg__ is not None:
            return self.__arg__
        if self.__ast_node__ is not None:
            self.__arg__ = ast.unparse(self.__ast_node__)
            return self.__arg__
        raise AssertionError("Attempted to access '__forward_arg__' on an uninitialized ForwardRef")

    @property
    def __resolved_str__(self):
        if self.__resolved_str_cache__ is None:
            resolved_str = self.__forward_arg__
            names = self.__extra_names__
            if names:
                visitor = _ExtraNameFixer(names)
                ast_expr = ast.parse(resolved_str, mode='eval').body
                node = visitor.visit(ast_expr)
                resolved_str = ast.unparse(node)
            self.__resolved_str_cache__ = resolved_str
        return self.__resolved_str_cache__

    @property
    def __forward_code__(self):
        if self.__code__ is not None:
            return self.__code__
        arg = self.__forward_arg__
        try:
            self.__code__ = compile(_rewrite_star_unpack(arg), '<string>', 'eval')
        except SyntaxError:
            raise SyntaxError(f'Forward reference must be an expression -- got {arg!r}')
        return self.__code__

    def __eq__(self, other):
        if not isinstance(other, 前向引用):
            return NotImplemented
        return self.__forward_arg__ == other.__forward_arg__ and self.__forward_module__ == other.__forward_module__ and (self.__globals__ is other.__globals__) and (self.__forward_is_class__ == other.__forward_is_class__) and ({name: id(cell) for name, cell in self.__cell__.items()} == {name: id(cell) for name, cell in other.__cell__.items()} if isinstance(self.__cell__, dict) and isinstance(other.__cell__, dict) else self.__cell__ is other.__cell__) and (self.__owner__ == other.__owner__) and ((tuple(sorted(self.__extra_names__.items())) if self.__extra_names__ else None) == (tuple(sorted(other.__extra_names__.items())) if other.__extra_names__ else None))

    def __hash__(self):
        return hash((self.__forward_arg__, self.__forward_module__, id(self.__globals__), self.__forward_is_class__, (tuple(sorted([(name, id(cell)) for name, cell in self.__cell__.items()])) if isinstance(self.__cell__, dict) else id(self.__cell__),), self.__owner__, tuple(sorted(self.__extra_names__.items())) if self.__extra_names__ else None))

    def __or__(self, other):
        return types.UnionType[self, other]

    def __ror__(self, other):
        return types.UnionType[other, self]

    def __repr__(self):
        extra = []
        if self.__forward_module__ is not None:
            extra.append(f', module={self.__forward_module__!r}')
        if self.__forward_is_class__:
            extra.append(', is_class=True')
        if self.__owner__ is not None:
            extra.append(f', owner={self.__owner__!r}')
        return f"ForwardRef({self.__resolved_str__!r}{''.join(extra)})"
_装类转发(前向引用, {'evaluate': '求值'}, {'evaluate': '求值'})
import annotationlib as _英文身份源
前向引用 = _英文身份源.ForwardRef
_Template = type(t'')

class _Stringifier:
    __slots__ = _SLOTS

    def __init__(self, node, globals=None, owner=None, is_class=False, cell=None, *, stringifier_dict, extra_names=None):
        assert isinstance(node, (ast.AST, str))
        self.__arg__ = None
        self.__forward_is_argument__ = False
        self.__forward_is_class__ = is_class
        self.__forward_module__ = None
        self.__code__ = None
        self.__ast_node__ = node
        self.__globals__ = globals
        self.__extra_names__ = extra_names
        self.__cell__ = cell
        self.__owner__ = owner
        self.__stringifier_dict__ = stringifier_dict
        self.__resolved_str_cache__ = None

    def __convert_to_ast(self, other):
        if isinstance(other, _Stringifier):
            if isinstance(other.__ast_node__, str):
                return (ast.Name(id=other.__ast_node__), other.__extra_names__)
            return (other.__ast_node__, other.__extra_names__)
        elif type(other) is _Template:
            return (_template_to_ast(other), None)
        elif self.__stringifier_dict__.format == 格式.STRING or other is None or type(other) in (str, int, float, bool, complex):
            return (ast.Constant(value=other), None)
        elif type(other) is dict:
            extra_names = {}
            keys = []
            values = []
            for key, value in other.items():
                new_key, new_extra_names = self.__convert_to_ast(key)
                if new_extra_names is not None:
                    extra_names.update(new_extra_names)
                keys.append(new_key)
                new_value, new_extra_names = self.__convert_to_ast(value)
                if new_extra_names is not None:
                    extra_names.update(new_extra_names)
                values.append(new_value)
            return (ast.Dict(keys, values), extra_names)
        elif type(other) in (list, tuple, set):
            extra_names = {}
            elts = []
            for elt in other:
                new_elt, new_extra_names = self.__convert_to_ast(elt)
                if new_extra_names is not None:
                    extra_names.update(new_extra_names)
                elts.append(new_elt)
            ast_class = {list: ast.List, tuple: ast.Tuple, set: ast.Set}[type(other)]
            return (ast_class(elts), extra_names)
        else:
            name = self.__stringifier_dict__.create_unique_name()
            return (ast.Name(id=name), {name: other})

    def __convert_to_ast_getitem(self, other):
        if isinstance(other, slice):
            extra_names = {}

            def conv(obj):
                if obj is None:
                    return None
                new_obj, new_extra_names = self.__convert_to_ast(obj)
                if new_extra_names is not None:
                    extra_names.update(new_extra_names)
                return new_obj
            return (ast.Slice(lower=conv(other.start), upper=conv(other.stop), step=conv(other.step)), extra_names)
        else:
            return self.__convert_to_ast(other)

    def __get_ast(self):
        node = self.__ast_node__
        if isinstance(node, str):
            return ast.Name(id=node)
        return node

    def __make_new(self, node, extra_names=None):
        new_extra_names = {}
        if self.__extra_names__ is not None:
            new_extra_names.update(self.__extra_names__)
        if extra_names is not None:
            new_extra_names.update(extra_names)
        stringifier = _Stringifier(node, self.__globals__, self.__owner__, self.__forward_is_class__, stringifier_dict=self.__stringifier_dict__, extra_names=new_extra_names or None)
        self.__stringifier_dict__.stringifiers.append(stringifier)
        return stringifier

    def __hash__(self):
        return id(self)

    def __getitem__(self, other):
        if self.__ast_node__ == '__classdict__':
            raise KeyError
        if isinstance(other, tuple):
            extra_names = {}
            elts = []
            for elt in other:
                new_elt, new_extra_names = self.__convert_to_ast_getitem(elt)
                if new_extra_names is not None:
                    extra_names.update(new_extra_names)
                elts.append(new_elt)
            other = ast.Tuple(elts)
        else:
            other, extra_names = self.__convert_to_ast_getitem(other)
        assert isinstance(other, ast.AST), repr(other)
        return self.__make_new(ast.Subscript(self.__get_ast(), other), extra_names)

    def __getattr__(self, attr):
        return self.__make_new(ast.Attribute(self.__get_ast(), attr))

    def __call__(self, *args, **kwargs):
        extra_names = {}
        ast_args = []
        for arg in args:
            new_arg, new_extra_names = self.__convert_to_ast(arg)
            if new_extra_names is not None:
                extra_names.update(new_extra_names)
            ast_args.append(new_arg)
        ast_kwargs = []
        for key, value in kwargs.items():
            new_value, new_extra_names = self.__convert_to_ast(value)
            if new_extra_names is not None:
                extra_names.update(new_extra_names)
            ast_kwargs.append(ast.keyword(key, new_value))
        return self.__make_new(ast.Call(self.__get_ast(), ast_args, ast_kwargs), extra_names)

    def __iter__(self):
        yield self.__make_new(ast.Starred(self.__get_ast()))

    def __repr__(self):
        if isinstance(self.__ast_node__, str):
            return self.__ast_node__
        return ast.unparse(self.__ast_node__)

    def __format__(self, format_spec):
        raise TypeError('Cannot stringify annotation containing string formatting')

    def _make_binop(op: ast.AST):

        def binop(self, other):
            rhs, extra_names = self.__convert_to_ast(other)
            return self.__make_new(ast.BinOp(self.__get_ast(), op, rhs), extra_names)
        return binop
    __add__ = _make_binop(ast.Add())
    __sub__ = _make_binop(ast.Sub())
    __mul__ = _make_binop(ast.Mult())
    __matmul__ = _make_binop(ast.MatMult())
    __truediv__ = _make_binop(ast.Div())
    __mod__ = _make_binop(ast.Mod())
    __lshift__ = _make_binop(ast.LShift())
    __rshift__ = _make_binop(ast.RShift())
    __or__ = _make_binop(ast.BitOr())
    __xor__ = _make_binop(ast.BitXor())
    __and__ = _make_binop(ast.BitAnd())
    __floordiv__ = _make_binop(ast.FloorDiv())
    __pow__ = _make_binop(ast.Pow())
    del _make_binop

    def _make_rbinop(op: ast.AST):

        def rbinop(self, other):
            new_other, extra_names = self.__convert_to_ast(other)
            return self.__make_new(ast.BinOp(new_other, op, self.__get_ast()), extra_names)
        return rbinop
    __radd__ = _make_rbinop(ast.Add())
    __rsub__ = _make_rbinop(ast.Sub())
    __rmul__ = _make_rbinop(ast.Mult())
    __rmatmul__ = _make_rbinop(ast.MatMult())
    __rtruediv__ = _make_rbinop(ast.Div())
    __rmod__ = _make_rbinop(ast.Mod())
    __rlshift__ = _make_rbinop(ast.LShift())
    __rrshift__ = _make_rbinop(ast.RShift())
    __ror__ = _make_rbinop(ast.BitOr())
    __rxor__ = _make_rbinop(ast.BitXor())
    __rand__ = _make_rbinop(ast.BitAnd())
    __rfloordiv__ = _make_rbinop(ast.FloorDiv())
    __rpow__ = _make_rbinop(ast.Pow())
    del _make_rbinop

    def _make_compare(op):

        def compare(self, other):
            rhs, extra_names = self.__convert_to_ast(other)
            return self.__make_new(ast.Compare(left=self.__get_ast(), ops=[op], comparators=[rhs]), extra_names)
        return compare
    __lt__ = _make_compare(ast.Lt())
    __le__ = _make_compare(ast.LtE())
    __eq__ = _make_compare(ast.Eq())
    __ne__ = _make_compare(ast.NotEq())
    __gt__ = _make_compare(ast.Gt())
    __ge__ = _make_compare(ast.GtE())
    del _make_compare

    def _make_unary_op(op):

        def unary_op(self):
            return self.__make_new(ast.UnaryOp(op, self.__get_ast()))
        return unary_op
    __invert__ = _make_unary_op(ast.Invert())
    __pos__ = _make_unary_op(ast.UAdd())
    __neg__ = _make_unary_op(ast.USub())
    del _make_unary_op

def _template_to_ast_constructor(template):
    """Convert a `template` instance to a non-literal AST."""
    args = []
    for part in template:
        match part:
            case str():
                args.append(ast.Constant(value=part))
            case _:
                interp = ast.Call(func=ast.Name(id='Interpolation'), args=[ast.Constant(value=part.value), ast.Constant(value=part.expression), ast.Constant(value=part.conversion), ast.Constant(value=part.format_spec)])
                args.append(interp)
    return ast.Call(func=ast.Name(id='Template'), args=args, keywords=[])

def _template_to_ast_literal(template, parsed):
    """Convert a `template` instance to a t-string literal AST."""
    values = []
    interp_count = 0
    for part in template:
        match part:
            case str():
                values.append(ast.Constant(value=part))
            case _:
                interp = ast.Interpolation(str=part.expression, value=parsed[interp_count], conversion=ord(part.conversion) if part.conversion else -1, format_spec=ast.Constant(value=part.format_spec) if part.format_spec else None)
                values.append(interp)
                interp_count += 1
    return ast.TemplateStr(values=values)

def _template_to_ast(template):
    """Make a best-effort conversion of a `template` instance to an AST."""
    if any((part.expression.strip() == '' for part in template.interpolations)):
        return _template_to_ast_constructor(template)
    try:
        parsed = tuple((ast.parse(f'({part.expression})', mode='eval').body for part in template.interpolations))
    except SyntaxError:
        return _template_to_ast_constructor(template)
    return _template_to_ast_literal(template, parsed)

class _StringifierDict(dict):

    def __init__(self, namespace, *, globals=None, owner=None, is_class=False, format):
        super().__init__(namespace)
        self.namespace = namespace
        self.globals = globals
        self.owner = owner
        self.is_class = is_class
        self.stringifiers = []
        self.next_id = 1
        self.format = format

    def __missing__(self, key):
        fwdref = _Stringifier(key, globals=self.globals, owner=self.owner, is_class=self.is_class, stringifier_dict=self)
        self.stringifiers.append(fwdref)
        return fwdref

    def transmogrify(self, cell_dict):
        for obj in self.stringifiers:
            obj.__class__ = 前向引用
            obj.__stringifier_dict__ = None
            if isinstance(obj.__ast_node__, str):
                obj.__arg__ = obj.__ast_node__
                obj.__ast_node__ = None
            if cell_dict is not None and obj.__cell__ is None:
                obj.__cell__ = cell_dict

    def create_unique_name(self):
        name = f'__annotationlib_name_{self.next_id}__'
        self.next_id += 1
        return name

def 调用求值函数(evaluate, format, *, owner=None):
    """Call an evaluate function. Evaluate functions are normally generated for
    the value of type aliases and the bounds, constraints, and defaults of
    type parameter objects.
    """
    return 调用注解函数(evaluate, format, owner=owner, _is_evaluate=True)

def 调用注解函数(annotate, format, *, owner=None, _is_evaluate=False):
    """Call an __annotate__ function. __annotate__ functions are normally
    generated by the compiler to defer the evaluation of annotations. They
    can be called with any of the format arguments in the Format enum, but
    compiler-generated __annotate__ functions only support the VALUE format.
    This function provides additional functionality to call __annotate__
    functions with the FORWARDREF and STRING formats.

    *annotate* must be an __annotate__ function, which takes a single argument
    and returns a dict of annotations.

    *format* must be a member of the Format enum or one of the corresponding
    integer values.

    *owner* can be the object that owns the annotations (i.e., the module,
    class, or function that the __annotate__ function derives from). With the
    FORWARDREF format, it is used to provide better evaluation capabilities
    on the generated ForwardRef objects.

    """
    if format == 格式.VALUE_WITH_FAKE_GLOBALS:
        raise ValueError('The VALUE_WITH_FAKE_GLOBALS format is for internal use only')
    try:
        return annotate(format)
    except NotImplementedError:
        pass
    if format == 格式.STRING:
        try:
            annotate(格式.VALUE_WITH_FAKE_GLOBALS)
        except NotImplementedError:
            return 注解转字符串(annotate(格式.VALUE))
        except Exception:
            pass
        globals = _StringifierDict({}, format=format)
        is_class = isinstance(owner, type)
        closure, _ = _build_closure(annotate, owner, is_class, globals, allow_evaluation=False)
        func = types.FunctionType(annotate.__code__, globals, closure=closure, argdefs=annotate.__defaults__, kwdefaults=annotate.__kwdefaults__)
        annos = func(格式.VALUE_WITH_FAKE_GLOBALS)
        if _is_evaluate:
            return _stringify_single(annos)
        return {key: _stringify_single(val) for key, val in annos.items()}
    elif format == 格式.FORWARDREF:
        namespace = {**annotate.__builtins__, **annotate.__globals__}
        is_class = isinstance(owner, type)
        globals = _StringifierDict(namespace, globals=annotate.__globals__, owner=owner, is_class=is_class, format=format)
        closure, cell_dict = _build_closure(annotate, owner, is_class, globals, allow_evaluation=True)
        func = types.FunctionType(annotate.__code__, globals, closure=closure, argdefs=annotate.__defaults__, kwdefaults=annotate.__kwdefaults__)
        try:
            result = func(格式.VALUE_WITH_FAKE_GLOBALS)
        except NotImplementedError:
            return annotate(格式.VALUE)
        except Exception:
            pass
        else:
            globals.transmogrify(cell_dict)
            return result
        globals = _StringifierDict({}, globals=annotate.__globals__, owner=owner, is_class=is_class, format=format)
        closure, cell_dict = _build_closure(annotate, owner, is_class, globals, allow_evaluation=False)
        func = types.FunctionType(annotate.__code__, globals, closure=closure, argdefs=annotate.__defaults__, kwdefaults=annotate.__kwdefaults__)
        result = func(格式.VALUE_WITH_FAKE_GLOBALS)
        globals.transmogrify(cell_dict)
        if _is_evaluate:
            if isinstance(result, 前向引用):
                return result.evaluate(format=格式.FORWARDREF)
            else:
                return result
        else:
            return {key: val.evaluate(format=格式.FORWARDREF) if isinstance(val, 前向引用) else val for key, val in result.items()}
    elif format == 格式.VALUE:
        raise RuntimeError('annotate function does not support VALUE format')
    else:
        raise ValueError(f'Invalid format: {format!r}')

def _build_closure(annotate, owner, is_class, stringifier_dict, *, allow_evaluation):
    if not annotate.__closure__:
        return (None, None)
    new_closure = []
    cell_dict = {}
    for name, cell in zip(annotate.__code__.co_freevars, annotate.__closure__, strict=True):
        cell_dict[name] = cell
        new_cell = None
        if allow_evaluation:
            try:
                cell.cell_contents
            except ValueError:
                pass
            else:
                new_cell = cell
        if new_cell is None:
            fwdref = _Stringifier(name, cell=cell, owner=owner, globals=annotate.__globals__, is_class=is_class, stringifier_dict=stringifier_dict)
            stringifier_dict.stringifiers.append(fwdref)
            new_cell = types.CellType(fwdref)
        new_closure.append(new_cell)
    return (tuple(new_closure), cell_dict)

def _stringify_single(anno):
    if anno is ...:
        return '...'
    elif isinstance(anno, str):
        return anno
    elif isinstance(anno, _Template):
        return ast.unparse(_template_to_ast(anno))
    else:
        return repr(anno)

def 从类命名空间取注解函数(obj):
    """Retrieve the annotate function from a class namespace dictionary.

    Return None if the namespace does not contain an annotate function.
    This is useful in metaclass ``__new__`` methods to retrieve the annotate function.
    """
    try:
        return obj['__annotate__']
    except KeyError:
        return obj.get('__annotate_func__', None)

def 取注解(obj, *, globals=None, locals=None, eval_str=False, format=格式.VALUE):
    """Compute the annotations dict for an object.

    obj may be a callable, class, module, or other object with
    __annotate__ or __annotations__ attributes.
    Passing any other object raises TypeError.

    The *format* parameter controls the format in which annotations are returned,
    and must be a member of the Format enum or its integer equivalent.
    For the VALUE format, the __annotations__ is tried first; if it
    does not exist, the __annotate__ function is called. The
    FORWARDREF format uses __annotations__ if it exists and can be
    evaluated, and otherwise falls back to calling the __annotate__ function.
    The STRING format tries __annotate__ first, and falls back to
    using __annotations__, stringified using annotations_to_string().

    This function handles several details for you:

      * If eval_str is true, values of type str will
        be un-stringized using eval().  This is intended
        for use with stringized annotations
        ("from __future__ import annotations").
      * If obj doesn't have an annotations dict, returns an
        empty dict.  (Functions and methods always have an
        annotations dict; classes, modules, and other types of
        callables may not.)
      * Ignores inherited annotations on classes.  If a class
        doesn't have its own annotations dict, returns an empty dict.
      * All accesses to object members and dict values are done
        using getattr() and dict.get() for safety.
      * Always, always, always returns a freshly-created dict.

    eval_str controls whether or not values of type str are replaced
    with the result of calling eval() on those values:

      * If eval_str is true, eval() is called on values of type str.
      * If eval_str is false (the default), values of type str are unchanged.

    globals and locals are passed in to eval(); see the documentation
    for eval() for more information.  If either globals or locals is
    None, this function may replace that value with a context-specific
    default, contingent on type(obj):

      * If obj is a module, globals defaults to obj.__dict__.
      * If obj is a class, globals defaults to
        sys.modules[obj.__module__].__dict__ and locals
        defaults to the obj class namespace.
      * If obj is a callable, globals defaults to obj.__globals__,
        although if obj is a wrapped function (using
        functools.update_wrapper()) it is first unwrapped.
    """
    if eval_str and format != 格式.VALUE:
        raise ValueError('eval_str=True is only supported with format=Format.VALUE')
    match format:
        case 格式.VALUE:
            ann = _get_dunder_annotations(obj)
            if ann is None:
                ann = _get_and_call_annotate(obj, format)
        case 格式.FORWARDREF:
            try:
                ann = _get_dunder_annotations(obj)
            except Exception:
                pass
            else:
                if ann is not None:
                    return dict(ann)
            ann = _get_and_call_annotate(obj, format)
            if ann is None:
                ann = _get_dunder_annotations(obj)
        case 格式.STRING:
            ann = _get_and_call_annotate(obj, format)
            if ann is not None:
                return dict(ann)
            ann = _get_dunder_annotations(obj)
            if ann is not None:
                return 注解转字符串(ann)
        case 格式.VALUE_WITH_FAKE_GLOBALS:
            raise ValueError('The VALUE_WITH_FAKE_GLOBALS format is for internal use only')
        case _:
            raise ValueError(f'Unsupported format {format!r}')
    if ann is None:
        if isinstance(obj, type) or callable(obj):
            return {}
        raise TypeError(f'{obj!r} does not have annotations')
    if not ann:
        return {}
    if not eval_str:
        return dict(ann)
    if globals is None or locals is None:
        if isinstance(obj, type):
            obj_globals = None
            module_name = getattr(obj, '__module__', None)
            if module_name:
                module = sys.modules.get(module_name, None)
                if module:
                    obj_globals = getattr(module, '__dict__', None)
            obj_locals = dict(vars(obj))
            unwrap = obj
        elif isinstance(obj, types.ModuleType):
            obj_globals = getattr(obj, '__dict__')
            obj_locals = None
            unwrap = None
        elif callable(obj):
            obj_globals = getattr(obj, '__globals__', None)
            obj_locals = None
            unwrap = obj
        else:
            obj_globals = obj_locals = unwrap = None
        if unwrap is not None:
            _seen_ids = {id(unwrap)}
            while True:
                if hasattr(unwrap, '__wrapped__'):
                    candidate = unwrap.__wrapped__
                    if id(candidate) in _seen_ids:
                        break
                    _seen_ids.add(id(candidate))
                    unwrap = candidate
                    continue
                if (functools := sys.modules.get('functools')):
                    if isinstance(unwrap, functools.partial):
                        candidate = unwrap.func
                        if id(candidate) in _seen_ids:
                            break
                        _seen_ids.add(id(candidate))
                        unwrap = candidate
                        continue
                break
            if hasattr(unwrap, '__globals__'):
                obj_globals = unwrap.__globals__
        if globals is None:
            globals = obj_globals
        if locals is None:
            locals = obj_locals
    if (type_params := getattr(obj, '__type_params__', ())):
        if locals is None:
            locals = {}
        locals = {param.__name__: param for param in type_params} | locals
    return_value = {key: value if not isinstance(value, str) else eval(_rewrite_star_unpack(value), globals, locals) for key, value in ann.items()}
    return return_value

def 类型表示(value):
    """Convert a Python value to a format suitable for use with the STRING format.

    This is intended as a helper for tools that support the STRING format but do
    not have access to the code that originally produced the annotations. It uses
    repr() for most objects.

    """
    if isinstance(value, (type, types.FunctionType, types.BuiltinFunctionType)):
        if value.__module__ == 'builtins':
            return value.__qualname__
        return f'{value.__module__}.{value.__qualname__}'
    elif isinstance(value, _Template):
        tree = _template_to_ast(value)
        return ast.unparse(tree)
    if value is ...:
        return '...'
    return repr(value)

def 注解转字符串(annotations):
    """Convert an annotation dict containing values to approximately the STRING format.

    Always returns a fresh a dictionary.
    """
    return {n: t if isinstance(t, str) else 类型表示(t) for n, t in annotations.items()}

def _rewrite_star_unpack(arg):
    """If the given argument annotation expression is a star unpack e.g. `'*Ts'`
       rewrite it to a valid expression.
       """
    if arg.lstrip().startswith('*'):
        return f'({arg},)[0]'
    else:
        return arg

def _get_and_call_annotate(obj, format):
    """Get the __annotate__ function and call it.

    May not return a fresh dictionary.
    """
    annotate = getattr(obj, '__annotate__', None)
    if annotate is not None:
        ann = 调用注解函数(annotate, format, owner=obj)
        if not isinstance(ann, dict):
            raise ValueError(f'{obj!r}.__annotate__ returned a non-dict')
        return ann
    return None
_BASE_GET_ANNOTATIONS = type.__dict__['__annotations__'].__get__

def _get_dunder_annotations(obj):
    """Return the annotations for an object, checking that it is a dictionary.

    Does not return a fresh dictionary.
    """
    if isinstance(obj, type):
        try:
            ann = _BASE_GET_ANNOTATIONS(obj)
        except AttributeError:
            return None
    else:
        ann = getattr(obj, '__annotations__', None)
        if ann is None:
            return None
    if not isinstance(ann, dict):
        raise ValueError(f'{obj!r}.__annotations__ is neither a dict nor None')
    return ann

class _ExtraNameFixer(ast.NodeTransformer):
    """Fixer for __extra_names__ items in ForwardRef __repr__ and string evaluation"""

    def __init__(self, extra_names):
        self.extra_names = extra_names

    def visit_Name(self, node: ast.Name):
        if (new_name := self.extra_names.get(node.id, _sentinel)) is not _sentinel:
            node = ast.Name(id=类型表示(new_name))
        return node


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import annotationlib as _英文库
前向引用 = _英文库.ForwardRef
_模块别名 = {
    'Format': '格式',
    'ForwardRef': '前向引用',
    'annotations_to_string': '注解转字符串',
    'call_annotate_function': '调用注解函数',
    'call_evaluate_function': '调用求值函数',
    'get_annotate_from_class_namespace': '从类命名空间取注解函数',
    'get_annotations': '取注解',
    'type_repr': '类型表示',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '前向引用': {
        'evaluate': '求值',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '前向引用': {
        'evaluate': '求值',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '从类命名空间取注解函数',
    '前向引用',
    '取注解',
    '格式',
    '注解转字符串',
    '类型表示',
    '调用求值函数',
    '调用注解函数',
])

# ---- 转发层结束 ----

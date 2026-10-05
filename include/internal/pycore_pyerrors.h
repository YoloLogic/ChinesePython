#ifndef Py_INTERNAL_PYERRORS_H
#define Py_INTERNAL_PYERRORS_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif


/* Error handling definitions */

extern _PyErr_StackItem* _PyErr_GetTopmostException(PyThreadState *tstate);
extern PyObject* _PyErr_GetHandledException(PyThreadState *);
extern void _PyErr_SetHandledException(PyThreadState *, PyObject *);
extern void _PyErr_GetExcInfo(PyThreadState *, PyObject **, PyObject **, PyObject **);

// Export for '_testinternalcapi' shared extension
PyAPI_FUNC(void) _PyErr_SetKeyError(PyObject *);


// Like PyErr_Format(), but saves current exception as __context__ and
// __cause__.
// Export for '_sqlite3' shared extension.
PyAPI_FUNC(PyObject*) _PyErr_FormatFromCause(
    PyObject *exception,
    const char *format,   /* ASCII-encoded string  */
    ...
    );

extern int _PyException_AddNote(
     PyObject *exc,
     PyObject *note);

extern int _PyErr_CheckSignals(void);

/* Support for adding program text to SyntaxErrors */

// Export for test_peg_generator
PyAPI_FUNC(PyObject*) _PyErr_ProgramDecodedTextObject(
    PyObject *filename,
    int lineno,
    const char* encoding);

extern PyObject* _PyUnicodeTranslateError_Create(
    PyObject *object,
    Py_ssize_t start,
    Py_ssize_t end,
    const char *reason          /* UTF-8 encoded string */
    );

extern void _Py_NO_RETURN _Py_FatalErrorFormat(
    const char *func,
    const char *format,
    ...);

extern PyObject* _PyErr_SetImportErrorWithNameFrom(
        PyObject *,
        PyObject *,
        PyObject *,
        PyObject *);
extern int _PyErr_SetModuleNotFoundError(PyObject *name);


/* runtime lifecycle */

extern PyStatus _PyErr_InitTypes(PyInterpreterState *);
extern void _PyErr_FiniTypes(PyInterpreterState *);


/* other API */

static inline PyObject* _PyErr_Occurred(PyThreadState *tstate)
{
    assert(tstate != NULL);
    if (tstate->current_exception == NULL) {
        return NULL;
    }
    return (PyObject *)Py_TYPE(tstate->current_exception);
}

static inline void _PyErr_ClearExcState(_PyErr_StackItem *exc_state)
{
    Py_CLEAR(exc_state->exc_value);
}

extern PyObject* _PyErr_StackItemToExcInfoTuple(
    _PyErr_StackItem *err_info);

extern void _PyErr_Fetch(
    PyThreadState *tstate,
    PyObject **type,
    PyObject **value,
    PyObject **traceback);

PyAPI_FUNC(PyObject*) _PyErr_GetRaisedException(PyThreadState *tstate);

PyAPI_FUNC(int) _PyErr_ExceptionMatches(
    PyThreadState *tstate,
    PyObject *exc);

PyAPI_FUNC(void) _PyErr_SetRaisedException(PyThreadState *tstate, PyObject *exc);

extern void _PyErr_Restore(
    PyThreadState *tstate,
    PyObject *type,
    PyObject *value,
    PyObject *traceback);

extern void _PyErr_SetObject(
    PyThreadState *tstate,
    PyObject *type,
    PyObject *value);

extern void _PyErr_ChainStackItem(void);
extern void _PyErr_ChainExceptions1Tstate(PyThreadState *, PyObject *);

PyAPI_FUNC(void) _PyErr_Clear(PyThreadState *tstate);

extern void _PyErr_SetNone(PyThreadState *tstate, PyObject *exception);

extern PyObject* _PyErr_NoMemory(PyThreadState *tstate);

extern int _PyErr_EmitSyntaxWarning(PyObject *msg, PyObject *filename, int lineno, int col_offset,
                                    int end_lineno, int end_col_offset);
extern void _PyErr_RaiseSyntaxError(PyObject *msg, PyObject *filename, int lineno, int col_offset,
                                    int end_lineno, int end_col_offset);

PyAPI_FUNC(void) _PyErr_SetString(
    PyThreadState *tstate,
    PyObject *exception,
    const char *string);

/*
 * Set an exception with the error message decoded from the current locale
 * encoding (LC_CTYPE).
 *
 * Exceptions occurring in decoding take priority over the desired exception.
 *
 * Exported for '_ctypes' shared extensions.
 */
PyAPI_FUNC(void) _PyErr_SetLocaleString(
    PyObject *exception,
    const char *string);

PyAPI_FUNC(PyObject*) _PyErr_Format(
    PyThreadState *tstate,
    PyObject *exception,
    const char *format,
    ...);

PyAPI_FUNC(PyObject*) _PyErr_FormatV(
    PyThreadState *tstate,
    PyObject *exception,
    const char *format,
    va_list vargs);

extern void _PyErr_NormalizeException(
    PyThreadState *tstate,
    PyObject **exc,
    PyObject **val,
    PyObject **tb);

extern PyObject* _PyErr_FormatFromCauseTstate(
    PyThreadState *tstate,
    PyObject *exception,
    const char *format,
    ...);

extern PyObject* _PyExc_CreateExceptionGroup(
    const char *msg,
    PyObject *excs);

extern PyObject* _PyExc_PrepReraiseStar(
    PyObject *orig,
    PyObject *excs);

extern int _PyErr_CheckSignalsTstate(PyThreadState *tstate);

extern void _Py_DumpExtensionModules(int fd, PyInterpreterState *interp);
extern PyObject* _Py_CalculateSuggestions(PyObject *dir, PyObject *name);
extern PyObject* _Py_Offer_Suggestions(PyObject* exception);

// Export for '_testinternalcapi' shared extension
PyAPI_FUNC(Py_ssize_t) _Py_UTF8_Edit_Cost(PyObject *str_a, PyObject *str_b,
                                          Py_ssize_t max_cost);

// Export for '_json' shared extension
PyAPI_FUNC(void) _PyErr_FormatNote(const char *format, ...);

/* Context manipulation (PEP 3134) */

Py_DEPRECATED(3.12) extern void _PyErr_ChainExceptions(PyObject *, PyObject *, PyObject *);

// implementation detail for the codeop module.
// Exported for test.test_peg_generator.test_c_parser
PyAPI_DATA(PyTypeObject) _PyExc_IncompleteInputError;
#define PyExc_IncompleteInputError ((PyObject *)(&_PyExc_IncompleteInputError))

extern int _PyUnicodeError_GetParams(
    PyObject *self,
    PyObject **obj,
    Py_ssize_t *objlen,
    Py_ssize_t *start,
    Py_ssize_t *end,
    Py_ssize_t *slen,
    int as_bytes);

/* --- ChinesePython：C 那台打印机也要说中文 -------------------------------

   Python 侧的报错显示走 Lib/traceback.py，那边查表换词就够了。
   但有一条路**完全在 C 里**：unraisable（`__del__` 之类的异常被忽略时），
   它用 write_unraisable_exc_file() + PyTraceBack_Print()，不经过 Python 的
   traceback 模块。所以这几个字只能在 C 里换。

   开关跟 Python 侧共用同一个环境变量 CHINESEPYTHON_ERRORS：en 就退回纯英文，
   其它值（含没设）都用中文，跟 Python 侧的规矩一致。

   ⚠ 两条硬约束：
     1. PyUnicode_FromFormat() / PyErr_Format() 的**格式串必须是纯 ASCII**
        （运行时会检查，非 ASCII 直接报 "expects an ASCII-encoded format
        string"）。所以中文只能走 %s 参数，或者单独用 PyFile_WriteString /
        PyUnicode_FromString 写出去 —— 那两个收 UTF-8，中文没问题。
        （源码里直接写中文字面量是可以的：PCbuild\pyproject.props 带 /utf-8。）
     2. 异常类的 __name__ 一个字都不许动（改了断 pickle 和 inspect）。
        这里返回的中文名只用来**显示**。 */

extern int _PyErr_UseChinese(void);

/* C 侧**兜底显示**专用（照 D-027）：比上面多一条 —— 身上已经挂着未处理的错误时
   一律退回英文。`Python/traceback.c` 与本文件 unraisable 那条路是最后一道兜底，
   在那里再制造分配失败会递归到爆栈（test_atexit 踩过）。 */
extern int _PyErr_UseChineseC(void);

/* 诊断用分级（照 D-027）：0=全关、1=只开 errors.c 的 unraisable 那组、
   2=再开 Python/traceback.c 那组（默认）。用来二分「崩溃在 C 的哪一组」。 */
extern int _PyErr_ChineseLevel(void);
/* Python/traceback.c 那三个显示点专用（级别 >= 2）。 */
extern int _PyErr_UseChineseTB(void);

/* 内置异常的显示用中文主名；不是内置异常、或查不到，返回 NULL。
   **借用引用**（别 DECREF），而且是预建好的 interned 串 ——
   这条查找跑在报错最里层，**一次分配都不做**（照 D-030）。 */
extern PyObject *_PyExc_ChineseName(PyObject *exc_type);

#ifdef __cplusplus
}
#endif
#endif /* !Py_INTERNAL_PYERRORS_H */

#ifndef Py_INTERNAL_ZH_METHODS_H
#define Py_INTERNAL_ZH_METHODS_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

/* ChinesePython：内置类型方法名的中文别名（`list.追加` 之类）。
 *
 * 属性查找**失败之后**才会被调到，返回中文名对应的英文名（新引用）；
 * 查不到、或者 `CHINESEPYTHON_ERRORS=en`，返回 NULL。
 * 由 tools/生成方法名别名.py 生成，不要手改。 */
extern PyObject *_PyZhMethods_EnglishName(PyTypeObject *tp, PyObject *name);

#ifdef __cplusplus
}
#endif
#endif /* !Py_INTERNAL_ZH_METHODS_H */

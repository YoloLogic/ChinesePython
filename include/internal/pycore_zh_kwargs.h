#ifndef Py_INTERNAL_ZH_KWARGS_H
#define Py_INTERNAL_ZH_KWARGS_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

/* ChinesePython：内置函数形参名的中文别名，英文名 -> 中文名。
 *
 * 没登记、`en` 模式、或者传 NULL，一律返回 NULL（调用方就当成没有中文名）。
 * 由 tools/生成形参名表.py 生成，不要手改。 */
extern const char *_PyArg_ChineseKeyword(const char *en);

#ifdef __cplusplus
}
#endif
#endif /* !Py_INTERNAL_ZH_KWARGS_H */

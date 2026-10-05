/* ChinesePython: 全局中文别名（内置名 / 异常名 / 模块孪生属性）。
 *
 * 这三张表原来是**往字典里塞条目**实现的，代价是 `dir(模块)` / `vars(模块)` /
 * `globals()` 里凭空多出中文名 —— 而 CPython 自带测试把这几样当硬不变量
 * （D-021 栽在 test_descr/test_builtin，D-026 栽在 test_pickle/test_interpreters）。
 *
 * 现在统一走**查找层**：
 *   * 裸名字（`长度([1,2])`、`捕获 值错误`）—— Python/codegen.c 编译期改写成英文名；
 *   * 属性（`builtins.长度`、`内置模块.值错误`）—— Objects/moduleobject.c 的 getattro 转发。
 * 两条路都查这里的 `_PyZh_GlobalAliasEnglish()`。
 *
 * 字典保持干净，一个中文别名都不进去。 */
#ifndef Py_INTERNAL_ZH_GLOBALS_H
#define Py_INTERNAL_ZH_GLOBALS_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

/* 模块的 5 个中文孪生属性（Objects/moduleobject.c） */
extern const char *_PyModule_ChineseTwinEnglish(const char *utf8);
/* 内置名的中文别名，主表 + 晚装的那两个（Python/bltinmodule.c、Python/pylifecycle.c） */
extern const char *_PyBlTin_ChineseAliasEnglish(const char *zh);
extern const char *_PyBlTin_LateChineseAliasEnglish(const char *zh);
/* 异常类的中文别名（Objects/exceptions.c） */
extern const char *_PyExc_ChineseAliasEnglish(const char *zh);

/* 四张表合起来查：中文名 -> 英文名；查不到返回 NULL。返回值是静态字符串。 */
extern const char *_PyZh_GlobalAliasEnglish(const char *utf8);

#ifdef __cplusplus
}
#endif
#endif /* !Py_INTERNAL_ZH_GLOBALS_H */

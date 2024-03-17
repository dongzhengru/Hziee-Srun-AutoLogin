# 概述

适用于杭电信工校园网的自动登录Python脚本，基于深澜校园网登录认证流程。

由于信工校园网的登录过程其中的三项加密参数的加密方式有别于其他学校的深澜校园网（具体区别可以参考这一条Issue[Still prompts the problem of Password Error after using md5 encryption · Issue #47](https://github.com/BITNP/bitsrun/issues/47)），所以本脚本可能只适用于本校，如有能力可以自行适配修改。

# 使用说明

在`/data`路径下新建一个文件`accounts.txt`，输入账号密码以及`ac_id`，以空格分隔，格式如下：

```
账号 密码 ac_id
```

其中`ac_id`以连接的网络类型决定，目前发现`I-XG`无线网的`ac_id`是`5`，有线网的`ac_id`是`10`

# 参考

1. [深澜校园网登录的分析与python实现-北京理工大学版 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/122556315)
2. [深澜认证协议分析,python模拟登录_模拟登录和协议登录-CSDN博客](https://blog.csdn.net/qq_41797946/article/details/89417722)
3. [coffeehat/BIT-srun-login-script](https://github.com/coffeehat/BIT-srun-login-script)
4. [BITNP/bitsrun](https://github.com/BITNP/bitsrun)
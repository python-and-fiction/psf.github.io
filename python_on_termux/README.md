# Python的Termux之旅

## 0 前言

机缘巧合之下，看到有人在手机上使用Termux，就像运行Linux发行版一样。再结合自己日常使用Python较多，就想尝试在Termux中安装Python的包。没想到，折腾数日之后，发现在Termux中安装Python的包问题颇多。虽然可以使用proot之类的容器工具，运行正常的发行版，实现和在正常发行版一样的使用体验，但本着活着就是折腾的原则，尝试了在纯Termux无二阶容器的前提下，安装了几个Python的包。由此，本教程诞生。同时，也是为了后续重复操作更加方便，本教程会不定期更新，增加新的踩坑记录。

## 1 准备

虽然Python是一门跨平台的编程语言，但使用的包还是有很多针对特定平台编译的二进制文件。此外，Termux也不是一个单独的系统，是运行在安卓之上的Linux环境程序，有一定的差异，并不能当成普通的Linux发行版。因此，在Termux上安装Python的包并没有想象中容易。

Python的包有以下几类：

-   源代码，直接包含此包的源代码，可以使用setup.py安装，需要执行导入（通常是复制）或者编译操作。
-   whl二进制包，但适用于任何版本（主要是Python3或者Python2），不依赖于特定小版本号或者系统，比如pip的pip-24.3.1-py3-none-any.whl，任何平台的Python3都可以安装。
-   whl二进制包，但有明确的版本号和系统，比如kivy的Kivy-2.3.0-cp312-cp312-win32.whl，cp312表示此包适用于CPython3.12版本（即Python 3.12.\*），win32表示此包适用于Windows的32位系统。

对于Termux来说，安装Python包最简单的是第二种，直接安装没问题。其次是支持Termux的第三种，即要求的Python版本正好是Termux可以安装的Python版本，且支持的系统是Linux，系统架构为aarch64（其他诸如amd64的话则对应Termux的x86_64，模拟器通常是这个）。当然，第三种没有对应的支持的话，第一种也不是不行。只不过，编译安装最容易出现问题，也正是本教程诞生的原因。相比于第二第三种Python包，源码包安装、编译耗时且不一定成功，更考验开发者的综合实力，需要了解Python之外的编译知识，还要善于搜索资料。

好在Termux官方有专门的[wiki页面](https://wiki.termux.com/wiki/Python)，囊括了大部分常用Python包的安装方法和常见问题，如果遇到Python包使用pip安装失败，可以先看看官方wiki，尝试一下官方的方法。不过，官方wiki也不是万能的，有些新的Python包或者不太流行的Python包也不是不能安装，但是安装过程中也会遇到问题，而这些问题官方wiki也没有说，就可以参考一下本教程，学习一下方法或者思路，尝试自己解决。

在正式尝试具体包之前，需要先了解一下解决在Termux安装Python包问题的基本思路：

Python包通常不是单独的包，会基于现有的包扩展、实现新的功能。而目前大部分新的包是纯Python代码实现，包的类别属于第二种。只有那些依赖非纯Python代码包的包和实现基础功能的包才容易出现Python包安装失败的问题，因此，最终的问题原因，就变成了依赖的包无法安装或者源码包编译失败。

分析包的依赖，先安装依赖，解决遇到的编译问题，就是解决问题的基本思路。

### 1.1 环境准备

第一次安装完Termux之后，默认的仓库镜像使用的是镜像组，为了加快后续的安装过程，可以使用`termux-change-repo`命令切换[Termux镜像](https://github.com/termux/termux-packages/wiki/Mirrors)。不修改也可以，下载速度不受影响，只是会浪费一点时间在搜索最快镜像上。

为了确保后续编译正常，可以先使用`pkg upgrade`更新一下环境，避免出现版本差异较大。

然后，就是安装必要的工具。

```shell
pkg install binutils build-essential openssl rust python-pip patchelf ninja
```

安装完Python和pip之后，需要设置pip的镜像，参考[清华镜像设置](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)或者其他镜像设置教程，这里使用的是清华镜像，命令行如下：

```shell
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

部分Python包使用rust编译，还要参考中科大的[Crates加速设置](https://mirrors.ustc.edu.cn/help/crates.io-index.html)、清华的[Crates加速设置](https://mirrors.tuna.tsinghua.edu.cn/help/crates.io-index/)或者其他加速设置方法，来加速rust编译过程，这里以中科大的为例，命令行如下：

```shell
mkdir -vp ${CARGO_HOME:-$HOME/.cargo}

cat << EOF | tee -a ${CARGO_HOME:-$HOME/.cargo}/config.toml
[source.crates-io]
replace-with = 'ustc'

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
EOF
```

清华的命令行如下：

```shell
mkdir -vp ${CARGO_HOME:-$HOME/.cargo}

cat << EOF | tee -a ${CARGO_HOME:-$HOME/.cargo}/config
[source.crates-io]
replace-with = 'mirror'

[source.mirror]
registry = "sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/"
EOF
```

termux的tur-repo（Termux用户仓库）提供了部分Python包的预编译包，补充了官方仓库中的缺失（即官方wiki中提到解决方法但仍然需要使用pip安装的包）。

使用方法有两种（均需要良好的Github访问速度，但可以下载成品包之后安装）：

1，pip安装法：

https://termux-user-repository.github.io/pypi/ 是tur的pypi仓库，可以像上面的清华镜像加速pip安装一样，提供额外的Python包，使用方法如下：

```
python -m pip install some_packages --extra-index-url https://termux-user-repository.github.io/pypi/
```

tui目前提供如下Python包的Termux编译成品：[cmake](https://termux-user-repository.github.io/pypi/cmake) [cryptography](https://termux-user-repository.github.io/pypi/cryptography) [grpcio](https://termux-user-repository.github.io/pypi/grpcio) [lxml](https://termux-user-repository.github.io/pypi/lxml) [mitmproxy-wireguard](https://termux-user-repository.github.io/pypi/mitmproxy-wireguard) [ninja](https://termux-user-repository.github.io/pypi/ninja) [numpy](https://termux-user-repository.github.io/pypi/numpy) [onnxruntime](https://termux-user-repository.github.io/pypi/onnxruntime) [pandas](https://termux-user-repository.github.io/pypi/pandas) [pillow](https://termux-user-repository.github.io/pypi/pillow) [playwright](https://termux-user-repository.github.io/pypi/playwright) [polars](https://termux-user-repository.github.io/pypi/polars) [pycairo](https://termux-user-repository.github.io/pypi/pycairo) [pycryptodomex](https://termux-user-repository.github.io/pypi/pycryptodomex) [pydantic-core](https://termux-user-repository.github.io/pypi/pydantic-core) [scikit-learn](https://termux-user-repository.github.io/pypi/scikit-learn) [scipy](https://termux-user-repository.github.io/pypi/scipy) [tflite-runtime](https://termux-user-repository.github.io/pypi/tflite-runtime) [tiktoken](https://termux-user-repository.github.io/pypi/tiktoken) [tokenizers](https://termux-user-repository.github.io/pypi/tokenizers)

2，pkg安装法：

此方法需要启用tur-repo，使用`pkg install tur-repo`启用。

使用`pkg install {Python包名}`的方法查询有没有`python-{Python包名}`格式的包，然后使用`pkg install python-{Python包名}`的方法安装。

比如，使用`pkg install pandas`可以得到如下输出：

```shell
python-pandas/tur-packages 2.2.3-1 x86_64
  Powerful Python data analysis toolkit
```

可以使用`pkg install python-pandas`安装pandas，就不用等待漫长的编译过程。

注意，虽然tur提供不少Python包的Termux编译成品，但其下载都是从Github的发布页下载，相比于漫长的编译，不稳定的网络连接同样耽误时间。后续如果没有启用tur-repo的必要性的话，仅介绍使用官方仓库的方法，尽量避免从Github下载的情况。网络稳定的读者可以将对应包的编译替换为从tur下载成品，之后便不再赘述。

### 1.2 Termux的wiki原文

Python is an interpreted, high-level, general-purpose programming language. Created by Guido van Rossum and first released in 1991, Python's design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.

In Termux Python v3.x can be installed by executing

```
pkg install python
```

Legacy, deprecated version 2.7.x can be installed by

```
pkg install python2
```

**Warning**: upgrading major/minor version of Python package, for example from Python 3.8 to 3.9, will make all your currently installed modules unusable. You will need to reinstall them. However upgrading patch versions, for example from 3.8.1 to 3.8.2, is safe.

**Due to our infrastructure limits, we do not provide older versions of packages. If you accidentally upgraded to unsuitable Python version and do not have backups to rollback, do not complain! We recommend doing backups of $PREFIX for developers and other people who rely on specific software versions.**

#### Package management

After installing Python, `pip` (`pip2` if using python2) package manager will be available. Here is a quick tutorial about its usage.

Installing a new Python module:

```
pip install {module name}
```

Uninstalling Python module:

```
pip uninstall {module name}
```

Listing installed modules:

```
pip list
```

When installing Python modules, it is highly recommended to have a package `build-essential` to be installed - some modules compile native extensions during their installation.

A few python packages are available from termux's package manager (for python3 only), and should be installed from there to avoid compilation errors. This is the case for:

-   numpy, `pkg install python-numpy`
-   electrum, `pkg install electrum`
-   opencv, `pkg install opencv-python`
-   asciinema, `pkg install asciinema`
-   matplotlib, `pkg install matplotlib`
-   cryptography, `pkg install python-cryptography`

#### Python module installation tips and tricks

It is assumed that you have `build-essential` or at least `clang`, `make` and `pkg-config` installed.

It also assumed that `termux-exec` is not broken and works on your device. Environment variable `LD_PRELOAD` is not tampered or unset. Otherwise you will need to patch modules' source code to fix all shebangs!

*Tip: help us to collect more information about installing Python modules in Termux. You can also help to keep this information up-to-date, because current instructions may eventually become obsolete.*

| Package |                         Description                          |     Dependencies      |                     Special Instructions                     |
| :------ | :----------------------------------------------------------: | :-------------------: | :----------------------------------------------------------: |
| gmpy2   | C-coded Python modules for fast multiple-precision arithmetic. https://github.com/aleaxit/gmpy | libgmp libmpc libmpfr |                                                              |
| lxml    |      Bindings to libxml2 and libxslt. https://lxml.de/       |    libxml2 libxslt    |                                                              |
| pandas  | Flexible and powerful data analysis / manipulation library for Python. https://pandas.pydata.org/ |                       | `export CFLAGS="-Wno-deprecated-declarations -Wno-unreachable-code"` `pip install pandas` |
| pynacl  | Bindings to the Networking and Cryptography library. https://pypi.python.org/pypi/PyNaCl |       libsodium       |                                                              |
| pillow  | Python Imaging Library. https://pillow.readthedocs.io/en/stable/ | libjpeg-turbo libpng  | 64-bit devices require running `export LDFLAGS="-L/system/lib64"` before pip command. |
| pyzmq   | Bindings to libzmq. https://pyzmq.readthedocs.io/en/latest/  |        libzmq         | On some devices the libzmq library can't be found by setup.py.If `pip install pyzmq` does not work, try: `pip install pyzmq --install-option="--libzmq=/data/data/com.termux/files/usr/lib/libzmq.so"` |

##### Advanced installation instructions

Some Python modules may not be easy to install. Here are collected information on how to get them available in your Termux.

###### Tkinter

Tkinter is splitted of from the `python` package and can be installed by

```
pkg install python-tkinter
```

We do not provide Tkinter for Python v2.7.x.

Since Tkinter is a graphical library, it will work only if X Windows System environment is installed and running. How to do this, see page [Graphical Environment](https://wiki.termux.com/wiki/Graphical_Environment).

##### Installing Python modules from source

Some modules may not be installable without patching. They should be installed from source code. Here is a quick how-to about installing Python modules from source code.

1.   Obtain the source code. You can clone a git repository of your package:

```
git clone https://your-package-repo-url
cd ./your-package-repo
```

or download source bundle with `pip`:

```
pip download {module name}
unzip {module name}.zip
cd {module name}
```

2.   Optionally, apply the desired changes to source code. There no universal guides on that, perform this step on your own.
3.   Optionally, fix the all shebangs. This is not needed if `termux-exec` is installed and works correctly.

```
find . -type f -not -path '*/\.*' -exec termux-fix-shebang "{}" \;
```

4.   Finally install the package:

```
python setup.py install
```

#### Troubleshooting

##### pip doesn't read config in `~/.config/pip/pip.conf`

A.k.a.

-   virtualenv doesn't read config in `~/.config/virtualenv/virtualenv.ini` / stores its data in `/data/data/com.termux/files/virtualenv` .

-   pip / virtualenv doesn't follow freedesktop `$XDG_CONFIG_HOME` / `$XDG_DATA_HOME` / `$XDG_CACHE_HOME` .

-   pylint / black doesn't store its cache in `~/.cache` but stores its cache in `/data/data/com.termux/cache` .

All of above are because of [platformdirs](https://github.com/platformdirs/platformdirs). Platformdirs aims to replace [appdirs](https://github.com/ActiveState/appdirs), since [pip v21.3.0](https://github.com/pypa/pip/pull/10202) and [virtualenv v20.5.0](https://github.com/pypa/virtualenv/pull/2142), they started to use platformdirs instead of appdirs. Appdirs doesn't do anything else on Android, it just follows freedesktop standards. But platformdirs is different, it takes termux as a simple Android app but not a unix evironment.

See details: [platformdirs issue 70](https://github.com/platformdirs/platformdirs/issues/70).

It it predictable that all packages using platformdirs can't behave well on termux, see: [[1\]](https://libraries.io/pypi/platformdirs/dependents). Before [PR 72](https://github.com/platformdirs/platformdirs/pull/72) is merged, the only way to fix it is to patch it manually.

There are two copies of platformdirs we need to patch:

1.  Pip vendors its own copy in `$PREFIX/lib/pythonX.Y/site-packages/pip/_vendor`.
2.  Platformdirs is installed as a dependency in `$PREFIX/lib/pythonX.Y/site-packages`. (If it was installed by `pip install --user`, the path is `~/.local/lib/pythonX.Y/site-packages`.)

Every time after we upgrade pip or platformdirs, we need to patch it again.

Patch for platformdirs before v2.5.0:

```
--- __init__.py.bak	2022-03-09 02:21:09.888903935 +0800
+++ __init__.py	2022-04-02 02:37:05.802427311 +0800
@@ -18,7 +18,7 @@
 
 
 def _set_platform_dir_class() -> type[PlatformDirsABC]:
-    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
+    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system" and os.getenv("SHELL") is None:
         module, name = "pip._vendor.platformdirs.android", "Android"
     elif sys.platform == "win32":
         module, name = "pip._vendor.platformdirs.windows", "Windows"
```

Patch for platformdirs v2.5.0 or later:

```
--- __init__.py.bak	2022-03-09 02:29:15.338903750 +0800
+++ __init__.py	2022-04-02 02:44:38.992427138 +0800
@@ -25,6 +25,10 @@
         from platformdirs.unix import Unix as Result
 
     if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
+
+        if os.getenv("SHELL") is not None:
+            return Result
+
         from platformdirs.android import _android_folder
 
         if _android_folder() is not None:
```

We can simply patch it by:

```shell
patch ~/../usr/lib/python3.10/site-packages/pip/_vendor/platformdirs/__init__.py -i platformdirs.patch
```

Notice that the two copies may be different versions, so they need different patches. For example, pip v21.3 and v22.0 use platformdirs v2.4, and the lastest version (on 2022-04-02) is v2.5.1.

## 2 从头再来的每一次安装

为了确保每个Python库的安装过程具有参考性，未明确准备步骤的变动的话，下面每一小节都是基于上一节的准备基础进行。因为手机的性能孱弱，演示采用模拟器操作（x86_64），如果是使用手机（aarch64）操作，请注意架构差异。

### 2.1 nicegui

NiceGui是一款基于Quasar框架、Tailwindcss框架、VUE框架、Fastapi框架，搭建GUI、WebUI的Python框架。具有语法简单、组件丰富、高性能等特点，适合有快速搭建图形界面需求的开发者。

更多详情可以访问官方网站：https://nicegui.io/

pip安装命令：

```shell
pip install nicegui nicegui[plotly] nicegui[matplotlib] nicegui[highcharts] nicegui[sass]
```

nicegui是包的主体，后面几个是可选功能支持，以上是能在Termux上成功安装的包。NiceGUI还支持桌面模式，因为本教程不涉及Termux的图形界面支持，这里便不提供安装方法。

依赖分析：

nicegui主体依赖以下库：aiofiles, aiohttp, certifi, docutils, fastapi, httpx, ifaddr, itsdangerous, jinja2, markdown2, orjson, Pygments, python-multipart, python-socketio, requests, typing-extensions, urllib3, uvicorn, vbuild, watchfiles

nicegui[plotly]依赖plotly。

nicegui[matplotlib]依赖matplotlib。

nicegui[highcharts]依赖nicegui-highcharts。

nicegui[sass]依赖libsass。

在正式安装之前，需要先测试安装一下依赖库（使用`pip install {包名}`测试，表格结果为模拟器测试），如果有官方解决方法，需要先依照官方解决方法安装。

依赖测试结果如下：

| 依赖库             | 安装结果 | 备注                                                         |
| ------------------ | -------- | ------------------------------------------------------------ |
| aiofiles           | 成功     | 二进制包                                                     |
| aiohttp            | 成功     | 源代码包                                                     |
| certifi            | 成功     | 二进制包                                                     |
| docutils           | 成功     | 二进制包                                                     |
| fastapi            | 成功     | 二进制包<br>依赖pydantic_core（源代码包）                    |
| httpx              | 成功     | 二进制包                                                     |
| ifaddr             | 成功     | 二进制包                                                     |
| itsdangerous       | 成功     | 二进制包                                                     |
| jinja2             | 成功     | 二进制包<br>依赖MarkupSafe（源代码包）                       |
| markdown2          | 成功     | 二进制包                                                     |
| orjson             | 成功     | 源代码包                                                     |
| Pygments           | 成功     | 二进制包                                                     |
| python-multipart   | 成功     | 二进制包                                                     |
| python-socketio    | 成功     | 二进制包                                                     |
| requests           | 成功     | 二进制包                                                     |
| typing-extensions  | 成功     | 二进制包                                                     |
| urllib3            | 成功     | 二进制包                                                     |
| uvicorn            | 成功     | 二进制包                                                     |
| uvloop             | 成功     | 源代码包<br/>uvicorn[standrad]的依赖<br>安装nicegui时触发    |
| vbuild             | 成功     | 二进制包                                                     |
| watchfiles         | 成功     | 源代码包                                                     |
| plotly             | 成功     | 二进制包                                                     |
| matplotlib         | 成功     | 参考wiki教程<br>使用`pkg install matplotlib`安装<br>此命令会同时安装好numpy和pillow |
| nicegui-highcharts | 成功     | 二进制包<br>依赖nicegui（二进制包）                          |
| libsass            | 成功     | `pkg install python-libsass`                                 |

之后安装nicegui没有任何问题。

注意，nicegui-highcharts的安装需要等nicegui安装成功后才能测试。

nicegui的安装难点主要在几个包的编译和需要使用pkg安装的包，编译需要较长时间，尽量提前安装，确保成功之后再安装nicegui。如果是直接安装nicegui，会因为每次安装失败都要重复编译过程，而浪费不少时间。另外，编译需要设备的内存较大，如果程序闪退，可以适当调整交换空间大小。rust写的包的编译还需要较好Github连接性，如果编译报rust相关的错误（比如看到cargo字样），可以多尝试几次。

### 2.2 streamlit

Streamlit是一个基于tornado框架的快速搭建Web应用的Python库，封装了大量常用组件方法，支持大量数据表、图表等对象的渲染，支持网格化、响应式布局。简单来说，可以让不了解前端的人搭建网页。

更多详情参考官网：https://streamlit.io/

pip安装命令：

```shell
pip install streamlit
```

依赖分析：

streamlit主要依赖以下库：altair, blinker, cachetools, click, gitpython, numpy, packaging, pandas, pillow, protobuf, pyarrow, pydeck, requests, rich, tenacity, toml, tornado, typing-extensions, watchdog

从依赖关系看，numpy、pandas、pillow都是官方wiki里提到的，pyarrow是官方没有提到但是官方也有包可以直接安装的，唯一需要注意的就是，pillow不需要提前安装，streamlit依赖特定pillow版本，安装时会指定版本。

依赖测试结果如下：

| 依赖库            | 安装结果 | 备注                                                         |
| ----------------- | -------- | ------------------------------------------------------------ |
| altair            | 成功     | 二进制包                                                     |
| blinker           | 成功     | 二进制包                                                     |
| cachetools        | 成功     | 二进制包                                                     |
| click             | 成功     | 二进制包                                                     |
| gitpython         | 成功     | 二进制包                                                     |
| numpy             | 成功     | 源代码包<br/>使用`pkg install python-numpy`安装              |
| packaging         | 成功     | 二进制包                                                     |
| pandas            | 成功     | 源代码包<br/>安装放到其他源代码包最后<br>先执行`export CFLAGS="-Wno-deprecated-declarations -Wno-unreachable-code"`<br>再执行`pip install pandas` |
| pillow            | 成功     | 源代码包<br/>先运行`pkg install libjpeg-turbo libpng`<br/>如果是64位设备，需要先运行`export LDFLAGS="-L/system/lib64"`<br/>再运行`pip install pillow`（实际上不用提前安装） |
| protobuf          | 成功     | 二进制包                                                     |
| pyarrow           | 成功     | 源代码包<br>使用`pkg install python-pyarrow`安装             |
| pydeck            | 成功     | 二进制包<br>依赖numpy                                        |
| requests          | 成功     | 二进制包                                                     |
| rich              | 成功     | 二进制包                                                     |
| tenacity          | 成功     | 二进制包                                                     |
| toml              | 成功     | 二进制包                                                     |
| tornado           | 成功     | 源代码包                                                     |
| typing-extensions | 成功     | 二进制包                                                     |
| watchdog          | 成功     | 源代码包                                                     |
| rpds-py           | 成功     | 源代码包<br/>jsonschema的依赖                                |
| markupsafe        | 成功     | 源代码包<br/>jinja2的依赖                                    |

streamlit的安装难点主要在几个包的编译和需要使用pkg安装的包，编译需要较长时间，尽量提前安装，确保成功之后再安装streamlit。如果是直接安装streamlit，会因为每次安装失败都要重复编译过程，而浪费不少时间。另外，编译需要设备的内存较大，如果程序闪退，可以适当调整交换空间大小。rust写的包的编译还需要较好Github连接性，如果编译报rust相关的错误（比如看到cargo字样），可以多尝试几次。

### 2.3 solara

Solara是一个开源的Python库，旨在简化交云端数据处理和交互式Web应用的开发过程。

它基于流行的数据科学库如Pandas和Plotly，提供了一种高效、直观的方式来创建数据驱动的Web应用。

更多详情参见官网：https://solara.dev/

pip安装命令：

```shell
pip install solara solara[assets]
```

依赖分析：

solara依赖solara-server和solara-ui。

solara[assets]（solara-assets）依赖solara。

solara-server依赖以下库：click, filelock, ipykernel, jinja2, jupyter-client, nbformat, rich-click, solara-ui

solara-ui依赖以下库：humanize, ipyvue, ipyvuetify, ipywidgets, reacton, requests

依赖测试结果如下：

| 依赖库         | 安装结果 | 备注                                                         |
| -------------- | -------- | ------------------------------------------------------------ |
| watchdog       | 成功     | 源代码包<br>solara-server[dev,starlette]的依赖               |
| watchfiles     | 成功     | 源代码包<br/>solara-server[dev,starlette]的依赖              |
| psutil         | 成功     | 源代码包<br/>solara-server[dev,starlette]的依赖              |
| markupsafe     | 成功     | 源代码包<br/>solara-server[dev,starlette]的依赖              |
| tornado        | 成功     | 源代码包<br/>solara-server[dev,starlette]的依赖              |
| pyzmq          | 成功     | 源代码包<br/>solara-server[dev,starlette]的依赖<br>运行`pkg install libzmq`之后，再运行`pip install pyzmq` |
| numpy          | 成功     | solara-ui[all]的依赖<br>使用`pkg install python-numpy`安装   |
| pillow         | 成功     | 源代码包<br/>solara-ui[all]的依赖<br/>先运行`pkg install libjpeg-turbo libpng`<br>如果是64位设备，需要先运行`export LDFLAGS="-L/system/lib64"`<br>再运行`pip install pillow`（实际上不用提前安装） |
| rpds-py        | 成功     | 源代码包<br/>solara-server[dev,starlette]的依赖              |
| pyyaml         | 成功     | 源代码包<br>solara-ui[all]的依赖                             |
| click          | 成功     | 二进制包                                                     |
| filelock       | 成功     | 二进制包                                                     |
| ipykernel      | 成功     | 二进制包                                                     |
| jinja2         | 成功     | 二进制包                                                     |
| jupyter-client | 成功     | 二进制包                                                     |
| nbformat       | 成功     | 二进制包                                                     |
| rich-click     | 成功     | 二进制包                                                     |
| humanize       | 成功     | 二进制包                                                     |
| ipyvue         | 成功     | 二进制包                                                     |
| ipyvuetify     | 成功     | 二进制包                                                     |
| ipywidgets     | 成功     | 二进制包                                                     |
| reacton        | 成功     | 二进制包                                                     |
| requests       | 成功     | 二进制包                                                     |

solara的安装难点主要在几个包的编译和需要使用pkg安装的包，编译需要较长时间，尽量提前安装，确保成功之后再安装solara。如果是直接安装solara，会因为每次安装失败都要重复编译过程，而浪费不少时间。另外，编译需要设备的内存较大，如果程序闪退，可以适当调整交换空间大小。rust写的包的编译还需要较好Github连接性，如果编译报rust相关的错误（比如看到cargo字样），可以多尝试几次。

### 2.4 gradio

Gradio是一个开源Python包，可以为机器学习模型、API或任何Python函数快速构建演示或web应用程序，然后可以使用Gradio的内置共享功能在几秒钟内通过公共链接共享演示。

Gradio 的主要特点包括：

-   **简单易用**：只需几行代码即可生成完整的Web应用。
-   **兼容性**：支持多种输入输出类型，如文本、图像、音频等。
-   **集成方便**：可以轻松地与Jupyter Notebook或本地 Python 脚本集成。
-   **自定义选项**：提供丰富的样式和布局选项以满足不同的需求。

更多详情参见官网：https://www.gradio.app/

pip安装命令：

```shell
pip install gradio
```

依赖分析：

gradio依赖以下库：aiofiles, anyio, fastapi, ffmpy, gradio-client, httpx, huggingface-hub, jinja2, markupsafe, numpy, orjson, packaging, pandas, pillow, pydantic, pydub, python-multipart, pyyaml, ruff, safehttpx, semantic-version, starlette, tomlkit, typer, typing-extensions, uvicorn

大部分依赖库在上面几节中都提到过，安装没有难度，唯一需要注意的是ruff需要编译安装。虽然termux提供了ruff包可以直接安装，但提供的不是Python的包，gradio还是需要安装一次ruff。此外，ruff的编译需要比较复杂的步骤，具体步骤将在下面的依赖测试中详细说明。

依赖测试结果如下：

| 依赖库            | 安装结果 | 备注                                                         |
| ----------------- | -------- | ------------------------------------------------------------ |
| ruff              | 失败     | 源代码包<br>`pkg install ruff`可以安装<br>但gradio不能识别   |
| pandas            | 成功     | 源代码包<br/>安装放到其他源代码包最后<br>先执行`export CFLAGS="-Wno-deprecated-declarations -Wno-unreachable-code"`<br>再执行`pip install pandas` |
| pillow            | 成功     | 源代码包<br/>先运行`pkg install libjpeg-turbo libpng`<br/>如果是64位设备，需要先运行`export LDFLAGS="-L/system/lib64"`<br/>再运行`pip install pillow`（实际上不用提前安装） |
| numpy             | 成功     | 源代码包<br/>使用`pkg install python-numpy`安装              |
| orjson            | 成功     | 源代码包                                                     |
| fastapi           | 成功     | 二进制包<br>依赖pydantic_core（源代码包）                    |
| pydantic          | 成功     | 二进制包<br/>依赖pydantic_core（源代码包）                   |
| markupsafe        | 成功     | 源代码包                                                     |
| uvicorn           | 成功     | 二进制包                                                     |
| uvloop            | 成功     | 源代码包<br/>uvicorn[standrad]的依赖<br>安装gradio时触发     |
| aiofiles          | 成功     | 二进制包                                                     |
| anyio             | 成功     | 二进制包                                                     |
| ffmpy             | 成功     | 二进制包                                                     |
| pyyaml            | 成功     | 源代码包                                                     |
| httpx             | 成功     | 二进制包                                                     |
| huggingface-hub   | 成功     | 二进制包                                                     |
| gradio-client     | 成功     | 二进制包                                                     |
| jinja2            | 成功     | 二进制包<br>依赖MarkupSafe（源代码包）                       |
| packaging         | 成功     | 二进制包                                                     |
| pydub             | 成功     | 二进制包                                                     |
| python-multipart  | 成功     | 二进制包                                                     |
| safehttpx         | 成功     | 二进制包                                                     |
| semantic-version  | 成功     | 二进制包                                                     |
| starlette         | 成功     | 二进制包                                                     |
| tomlkit           | 成功     | 二进制包                                                     |
| typer             | 成功     | 二进制包                                                     |
| typing-extensions | 成功     | 二进制包                                                     |

从依赖测试的情况看，除了ruff，都是可以成功安装的。

为了确保ruff被gradio识别，需要执行下面的步骤来确保ruff编译成功：

-   启用tur-repo，命令行为`pkg install tur-repo`。

-   安装gcc编译器，命令行为`pkg install gcc-14`。
-   编译ruff，命令行为`pip install ruff`。

在安装完gcc编译器之后，使用`gcc -v`应该可以看到检测到gcc编译器的提示，而不是之前只有clang的版本信息。

```shell
~ $ gcc -v
clang version 19.1.3
Target: x86_64-unknown-linux-android24
Thread model: posix
InstalledDir: /data/data/com.termux/files/usr/bin
Found candidate GCC installation: /data/data/com.termux/files/usr/lib/gcc/x86_64-linux-android/14.1.0
Selected GCC installation: /data/data/com.termux/files/usr/lib/gcc/x86_64-linux-android/14.1.0
Candidate multilib: .;@m64
Selected multilib: .;@m64
```

另外，此步骤不得不使用tur-repo的包，安装过程需要良好的Github连接性，网络不好的话可以多试几次。由于模拟器（网易mumu）兼容性有问题，完成上述操作之后也不能编译成功，不过手机（红米note9，aarch64）上实测可以编译成功，并且后续安装gradio也能成功。

gradio最大的安装难点是ruff的编译，虽然termux提供了ruff，但不是pip包，gradio没法识别，必须自己安装一次。而ruff的编译需要链接gcc库，默认的gcc是clang，而不是真的gcc，需要通过启用tur-repo来安装gcc，进而让编译时可以成功链接。

gradio的其他安装难点则和前面一样，在几个包的编译和需要使用pkg安装的包，编译需要较长时间，尽量提前安装，确保成功之后再安装gradio。如果是直接安装gradio，会因为每次安装失败都要重复编译过程，而浪费不少时间。另外，编译需要设备的内存较大，如果程序闪退，可以适当调整交换空间大小。rust写的包的编译还需要较好Github连接性，如果编译报rust相关的错误（比如看到cargo字样），可以多尝试几次。

### 2.5 flet

Flet是一个基于Flutter框架构建、专为Python提供构建跨平台图形界面的快速开发框架。

官网：https://flet.dev/

安装命令：

```shell
pip install flet[all]
```

依赖分析：

其实flet的依赖都可以正常安装，安装命令没法在Termux正常使用的原因很低级：官方的all和desktop可选项会让linux平台安装flet-desktop-light，而不是flet-desktop。哪怕flet程序只是设置为web端而不是桌面端，运行命令`flet run -w`还是需要flet-desktop的二进制文件。因此，安装要分步骤，需要先解决flet-desktop的安装问题，而不能直接安装flet[all]。

解决步骤：

先安装flet-desktop，再安装flet、flet-cli、flet-web（或者 flet[cli]、flet[web]），这样才能成功安装。其实只要单独安装即可，不使用 flet[all]、flet[desktop]就行，最后确保flet、flet-cli、flet-desktop、flet-web都安装成功，版本都是0.25.0以上且版本号一样即可。

即便如此，也只能运行web视图，不建议使用桌面视图。

## 3 还有一件事

上面检查依赖的方法是`pip show {Python包名}`，只能检查一级依赖，如果依赖产生的依赖需要特殊处理，则只能手动测试发现。其实，如果想要一次性、完整检查出可能需要解决的依赖问题，可以在普通的系统平台上，运行`pip download {Python包名}`，当前目录就会下载该包和该包所有的依赖（包括依赖的依赖）。

注意，上面的方法会因为系统不同而依赖不同，比如在win下运行，就不会下载uvloop依赖，那个是Linux下特有的依赖；另外，win下还会产生win特有的依赖，比如pywin32。因此，最好是在Linux系统中下载，实在不能满足的，可以具体自己测试之后根据实际情况修改操作教程，避免因为系统差异而导致依赖缺失。
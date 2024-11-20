# textual的中文入门教程

[TOC]

## 0 前言

Textual是一个用于 Python 的 TUI（文本用户界面）库，是 Rich 的姐妹项目，也依赖于 Rich。它支持 Rich 的 Renderable 类，同时有自己的互动性组件 Widget 类。通过使用简单的 Python API 构建复杂的用户界面，在shell工具或浏览器上运行。

什么是TUI？

之前的《nicegui的中文入门教程》中介绍的nicegui是一个GUI框架、WebUI框架，基于它实现的界面可以运行在桌面和浏览器中，对应的，可以称之为GUI程序、WebUI程序。TUI程序则是运行在用户终端（或者叫命令行）中，以终端支持的显示方式提供的图形化程序，因此TUI可以解释为终端用户界面（Terminal User Interface），而终端能提供的显示方式一般是可打印字符，可以通过特定字符的组合使用，实现GUI中组件的类似效果，因此，TUI也可以被解释为基于文本的用户界面（Text-based User Interface）。

相比于nicegui的框架用法简单，组件用法繁多，textual的框架用法硬核不少，需要了解一些Python之外的Web知识（样式、布局），再加上textual官网不提供中文教程，本教程由此诞生。本教程将基于textual的官网教程，整合官网教程内容，系统性地提供中文版学习教程，方便中文开发者入门使用。

## 1 环境准备

《nicegui的中文入门教程》已经详细介绍了基本环境的准备过程，这里不再赘述，直接说使用的工具和命令。

开发工具选用的是vscode，安装python开发使用的插件。

环境管理工具选用pdm，python版本选用3.12。注意，3.13版本也可以，但为了保证框架稳定运行，推荐使用上一个大版本的python。

为了确保vscode的终端可以正常运行textual程序，使用浏览器访问下面地址，将vscode的该项设置启用，确保终端不会冻结：

```shell
vscode://settings/terminal.integrated.experimental.windowsUseConptyDll
```

基础环境的初始化同样参考《nicegui的中文入门教程》，在初始化完成之后，添加textual、textual-serve、textual-dev三个包，命令如下：

```shell
pdm add textual textual-serve textual-dev
```

其中，textual是框架的主体包，textual-serve是一个让textual程序在网页中运行的扩展包，textual-dev是一个调试textual程序的开发调试工具。扩展包和开发调试工具的用法将在后面介绍，这里只是提前准备好。

如果不使用pdm管理虚拟环境，而是使用全局pip安装，直接调用全局python解释器来开发textual程序，可以使用下面的pip命令安装：

```shell
pip install textual textual-serve textual-dev
```

打开vscode的终端，分别运行`textual`和`python -m textual`，输出以下内容和textual的演示程序，则表示环境没有问题：

```shell
Usage: textual [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  borders   Explore the border styles available in Textual.
  colors    Explore the design system.
  console   Run the Textual Devtools console.
  diagnose  Print information about the Textual environment.
  easing    Explore the animation easing functions available in Textual.
  keys      Show key events.
  run       Run a Textual app.
  serve     Run a local web server to serve the application.
```

![textual_demo](textual.assets/textual_demo.svg)

因为textual还在活跃开发中，版本发布比较频繁，可以使用`pdm update textual textual-serve textual-dev`（pdm）或者`pip install -U textual textual-serve textual-dev`（pip）来更新包，确保问题及时修复，可以使用最新的功能。

## 2 入门基础

### 2.1 认识textual

[Textual](https://textual.textualize.io/)，一款颇具Web风格的TUI框架。这是在系统性看完textual这个框架的教程之后，留下的第一印象。

在正式开始textual的学习之前，有必要讲一讲textual的设计哲学。在《nicegui的中文入门教程》中，介绍了图形界面的三个基本概念——控件、布局和交互。但这些对于简陋的TUI来说，想要实现同等的效果，需要付出更多的代码成本。C语言的ncurses太过底层，需要自己完全实现组件、交互。可以使用脚本调用的whiptail，虽然提供了不少组件，但是纯向导式交互，也不支持直接点击操作，用途有限。尽管dialog在whiptail基础上支持点击，但也是‌因循守旧‌，并没有青出于蓝的表现。

因此，textual借助python的易学性，结合了Web中CSS样式的灵活美观，创新性地设计出基于CSS样式设计TUI程序的方式。当然，GUI中的组件和交互也没有落下。只不过受限于终端的表现形式，动画、色彩、布局等表现只能算差强人意，并不能做到媲美。

### 2.2 基础知识

本节主要内容源于官网的[guide页](https://textual.textualize.io/guide/)。

#### 2.2.1 Hello World

正如编程语言的学习始于输出“Hello World!”，先看一下textual程序的“Hello World!”代码是什么样子：

```python3
from textual.app import App
from textual.widgets import Static

class MyApp(App):
    def compose(self):
        yield Static("Hello World!")

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

将代码保存为`myapp.py`或者任意`.py`后缀的文件，点击运行或者在终端中使用`python myapp.py`命令运行，可以看到终端显示下面的内容：

![hello_world](textual.assets/hello_world.png)

上面的代码可以在终端输出一句话，只不过，这句话不同于直接在终端回显的文字，这句话是显示在textual程序中的静态文本。

如果需要退出的话，按下`ctrl`+`c`，即可退出。

需要注意的是，因为pdm初始化项目会产生`src\{项目名}`目录，标准操作是将源代码放到该目录下，而vscode的打开终端只是到项目根目录，通过命令行运行的话，需要cd到`src\{项目名}`目录，即源代码文件的同级目录，后续的命令行操作之前皆需要执行此操作，就不再赘述，读者实操之前请不要忘了这一步。

相比于nicegui最短三行的“Hello World!”，textual的代码显得臃肿不少，结构上也复杂得多。不过不用担心，这里只是简单看一下textual程序的代码和运行效果，不需要细究每一行代码的作用，在学习textual代码的作用之前，还需要学习一些代码之外的知识。

#### 2.2.2 开发者工具

前面环境准备中安装了textual-dev之后，可以在终端执行`textual`得到一系列输出，此工具就是本节要介绍的开发者工具，完整介绍可以参考[官网文档](https://textual.textualize.io/guide/devtools/)。

##### 2.2.2.1 run命令

运行textual程序有千百种姿势，前面介绍了textual程序的“Hello World!”代码，采用的运行方式是直接运行，本质上就是`python main.py`这种直接运行python源代码文件的常规方法。但是，textual的开发者工具`textual`的run命令也可以运行textual程序。

最常规的方法：

```shell
textual run myapp.py
```

此方法等同于`python myapp.py`，后面直接跟可运行的python源代码文件。

run命令还支持运行模块中的textual类或者实例。想要测试这种运行方法的话，需要对前面的textual程序的“Hello World!”代码做一点小小的改动。

改动后的代码如下：

```python3
from textual.app import App
from textual.widgets import Static

class MyApp(App):
    def compose(self):
        yield Static("Hello World!")

app = MyApp()
```

改动后的代码将`app = MyApp()`移动到最左端的缩进，同时去掉了对`__name__ == "__main__"`的判断和`app.run()`，这就意味着，该python源代码文件在当作模块导入（`from . import myapp`）时，不会运行`app.run()`，同时可以导入`app`和`MyApp`这两个模块的成员。

接下来，新建文件夹test，将myapp.py放到test文件夹，并在文件夹中创建空白的\_\_init\_\_.py文件，用于表明test是个包。那么，将得到以下文件结构：

```shell
test
├─__init__.py
└─myapp.py
```

执行以下命令，将看到熟悉的输出：

```shell
textual run test.myapp
```

![hello_world](textual.assets/hello_world.png)

聪明的读者肯定想到，前面的myapp.py既可以直接运行，也可以当做模块导入。这里很复杂的操作只为构建一个包，如果不做包，直接执行模块文件，行不行？

当然可以，假如当前目录下的myapp.py是前面改动后的代码，下面的命令可以运行单文件模块：

```shell
textual run myapp
```

不过很可惜，上面的命令并不能成功，它只得到以下输出：

```shell
Unable to import 'app' from module 'myapp'
```

因为当前目录下的myapp.py是最开始的textual程序的“Hello World!”代码，当做模块导入的话，没有`app`这个成员，只有`MyApp`这个成员，因此默认不能执行。想要成功执行的话，要么像上面的改动一样，添加`app = MyApp()`到最左端的缩进，要么就用下面的命令指定App的继承类来执行：

```shell
textual run myapp:MyApp
```

然后，就能看到熟悉的输出：

![hello_world](textual.assets/hello_world.png)

当然，上面费劲构建出来的包也支持指定继承类来执行：

```shell
textual run test.myapp:MyApp
```

run命令还支持一些额外的选项，进而解锁textual程序的其他能力。

run命令加上`--dev`选项，可以开启调试模式，能让textual程序的样式修改可以实时生效，也能将textual程序的终端输出和日志消息输出到console（提前在另一个终端中运行`textual console`可以开启console界面）中。关于样式和console，后面会介绍到，这里只需记住`--dev`选项是一个方便的调试选项即可。示例如下：

```shell
textual run --dev myapp.py
```

run命令还支持`-c`选项，与python的`-c`选项可以执行python代码字符串类似，此选项后可以跟任意可通过“运行”执行的命令，比如notepad。字符串或者直接裸命令都可以。示例如下：

```shell
textual run -c notepad
textual run -c 'notepad'
```

当然，使用`-c`选项也可以执行运行textual程序的命令，不过，嵌套在run命令下执行原本可以运行textual程序的命令，就有点多此一举。示例如下：

```shell
textual run -c python myapp.py
```

注意，某些命令（如“dir”、“ls”）不是可以通过“运行”执行的可执行文件，而是终端或者shell提供的内建命令，则无法使用`-c`选项执行。

此外，部分命令（如“python”、“textual”）也支持`-c`选项的话，不能重复添加`-c`选项到裸命令后来让被执行的命令接收，只能使用字符串的形式间接让被执行的命令接收。比如：

```shell
textual run -c python -c "print('abc')"
# 上面的命令会报错，被执行命令的-c选项会被textual接收，进而把print('abc')传递给终端
# 可以把被执行命令的-c选项连同被执行命令，一起放到字符串内，如下面所示
textual run -c 'python -c "print(''abc'')" '
```

至此，在终端运行textual程序的所有方法都解锁完毕，最后用一个表格总结一下run命令的用法：

| 命令行示例                                                   | 运行目标                                                     | 命令说明                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `textual run myapp.py`                                       | python源代码                                                 | 和`python myapp.py`一样                                      |
| `textual run myapp`<br>`textual run test.myapp`              | 包的模块文件或者单模块文件的app成员                          | app必须是App（来自textual.app）的子类的实例<br>并且在可以从模块中导出 |
| `textual run myapp:MyApp`<br/>`textual run test.myapp:MyApp` | 包的模块文件或者单模块文件的指定类                           | 指定的类必须是App（来自textual.app）的子类<br/>并且在可以从模块中导出 |
| `textual run --dev myapp.py`<br>`textual run --dev myapp`    | python源代码<br>包的模块文件或者单模块文件的app成员<br>包的模块文件或者单模块文件的指定类 | 开启调试模式<br>样式修改可以实时生效<br>终端输出和日志消息会输出到console |
| `textual run -c notepad`<br/>`textual run -c 'notepad'`<br>`textual run -c python myapp.py`<br>`textual run -c 'python -c "print(''abc'')" '` | 可在终端运行的可执行程序名<br>基于上一目标添加的、不包括-c/--dev的选项和参数<br>使用字符串表示的上面两种目标 | 如果想给被运行的命令传入-c/--dev选项<br>必须用字符串表示运行目标 |

run命令支持的参数和用法还有很多，不过在前期基础学习阶段用不上，这里就不引入了。等到后面需要使用时再扩展这部分内容。

##### 2.2.2.2 serve命令

前言中介绍过，textual程序可以在浏览器中运行，这话并不是说textual是一个WebUI框架。起码从它在浏览器中运行的表现来看，textual不同于常规的WebUI框架。textual程序在浏览器中运行，更像是在浏览器中模拟出一个终端，让程序在正常终端中的输出，全部在浏览器中原样呈现。

环境准备中提到，textual-serve是一个让textual程序在网页中运行的扩展包，后续可以基于此扩展包，编写出将普通textual程序转化为网页的python脚本。在正式学习textual-serve之前，读者可以使用textual的serve命令，快捷运行textual程序，让其呈现在浏览器中。

以下面的命令为例：

```shell
textual serve myapp.py
```

执行命令之后，可以看到终端有如下输出：

```shelll
___ ____ _  _ ___ _  _ ____ _       ____ ____ ____ _  _ ____ 
 |  |___  \/   |  |  | |__| |    __ [__  |___ |__/ |  | |___ 
 |  |___ _/\_  |  |__| |  | |___    ___] |___ |  \  \/  |___ v1.1.1

Serving 'python myapp.py' on http://localhost:8000

Press Ctrl+C to quit
```

在浏览器中访问`http://localhost:8000`，即可看到网页运行的效果：

![hello_world_web](textual.assets/hello_world_web.png)

serve命令不仅支持所有run命令的格式，还比run命令支持更多功能。

首先，serve命令默认支持等同于`-c`选项的参数。尽管serve命令可以通过添加`-c`选项实现和run命令一样的效果，但serve命令依旧可以不使用该选项的情况下，直接支持`-c`选项的参数。比如，上面的示例就可以变成下面这种格式：

```shell
textual serve python myapp.py
```

需要特别注意的是，serve命令本质上是将textual程序在终端的输出传递给textual-serve扩展包，让其在浏览器中显示。因此，serve命令运行`-c`选项的参数必须输出的是textual程序，这一点与run命令不同：

```shell
textual serve 'python myapp.py'
```

serve命令支持的参数和用法还有很多，不过在前期基础学习阶段用不上，这里就不引入了。等到后面需要使用时再扩展这部分内容。

#### 2.2.3 textual程序的基本概念

前面讲了一堆textual程序之外的命令，这一节重点讲一下textual程序本身。

##### 2.2.3.1 App类

以下面的代码为例，了解一下textual程序的基本结构：

```python3
from textual.app import App
from textual.widgets import Static

class MyApp(App):
    def compose(self):
        yield Static("Hello World!")

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

textual.app中的App类，是一个预先定义好的模板类，开发者可以通过继承此类，快速实现一个可以实例化的标准textual程序中的App子类。一般来说，textual程序，就是调用App类或者其子类的实例的run方法，来让消息循环占据终端的输入输出，显示出预先设计的界面。因此，代码中必须要有类的实例化和调用run方法的过程。当然，如果是采用其他方法运行，比如`textual run myapp`或者`textual run myapp:MyApp`，textual命令会自动寻找模块中名为`app`的实例来调用其run方法，或者基于提供的子类类名，自动完成实例化和调用run方法的过程。

代码中的`__name__ == "__main__"`条件判断，是针对该文件不是当做模块调用，而是直接运行时的选择，因为`app.run()`在导入时被运行的话，会导致程序进入textual的消息循环，无法正常导入其成员。当然，导入一般是导入类或者方法，`app = MyApp()`这句是实例化一个对象，一般不会当做导入的成员，自然需要放到判断分支内。

关于App类，还有两点需要补充，以下面的代码为例：

```python3
from textual.app import App
from textual.widgets import Static

class MyApp(App):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ansi_color = False
    def compose(self):
        yield Static("Hello World!")

if __name__ == "__main__":
    app = MyApp()
    app.run(inline=False)
```

代码中，在初始化方法中设置了一个属性`ansi_color`的值为`False`（默认值），在run方法中设置了一个参数`inline`的值为`False`（默认值）。

其中，ansi_color表示textual程序是否启用终端的ansi颜色的转义序列。表示的是，如果终端支持颜色主题切换，textual程序的默认颜色就会随终端主题走，而不是替换为textual自己设定的默认颜色。此颜色仅指没有经过样式、主题指定的显示颜色，如果颜色被指定，则不受影响。

`ansi_color`的值为`False`时终端的显示效果：

![ansi_color](textual.assets/ansi_color.png)

`ansi_color`的值为`True`时终端的显示效果：

![ansi_color_2](textual.assets/ansi_color_2.png)

可以看到，当启用ansi颜色，原本与终端背景颜色略有区别的黑色，变成了与终端背景一样的黑色。

inline参数表示是否启用textual程序的行内模式。一般的，此参数不设置为`True`的话，textual程序会以应用模式运行，textual程序的界面会占据终端全部的显示区域。如果此参数设置为`True`，则textual程序会以行内模式运行，程序界面显示为固定大小，甚至能看到程序上面显示着之前输入的命令。

注意，行内模式目前不支持在Windows的终端，下面的演示截图来自Linux的终端。

还是上面提供的代码，在只修改inline参数为`True`的情况下，效果如图：

![inline](textual.assets/inline.png)

##### 2.2.3.2 事件

textual有一套自己的事件响应系统（[官网文档](https://textual.textualize.io/events/)），它可以响应键盘按键、鼠标按键、组件状态变化等事件。事件的响应方法是一系列以`on_`为前缀的方法，比如下面代码中的`on_mount`和`on_key`，就是响应程序加载和键盘按键的方法。

```python3
from textual.app import App
from textual import events

class EventApp(App):
    COLORS = [
        "white",
        "maroon",
        "red",
        "purple",
        "fuchsia",
        "olive",
        "yellow",
        "navy",
        "teal",
        "aqua",
    ]
    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"
    def on_key(self, event: events.Key) -> None:
        if event.key.isdecimal():
            self.screen.styles.background = self.COLORS[int(event.key)]

if __name__ == "__main__":
    app = EventApp()
    app.run()
```

运行上面代码，可以看到终端显示如下：

![event_1](textual.assets/event_1.png)

这是因为响应程序加载的`on_mount`方法中，将`self.screen.styles.background`（主屏幕背景色）设置为"darkblue"，表示程序加载完成时的背景色。如果按下数字键0-9中的任意数字，可以看到背景色会随着按键的按下而变化。这是因为响应键盘按键的`on_key`方法中，会基于事件中按键的值，到`COLORS`这个预先定义了一系列颜色名字的列表中取值，赋给`self.screen.styles.background`（主屏幕背景色），让背景颜色随之变化。

当然，读者并不需要细究到底有多少事件响应方法，也不需要细究背景色支持哪些名字，只需要记住`on_`为前缀的方法是textual的事件响应方法。至于具体用法，将会在后面用到时细讲，同时也可以查阅官网文档手册，这里只是介绍一下事件系统。

##### 2.2.3.3 组件



退出



挂起



CSS



标题与副标题



#### 2.2.4 样式



#### 2.2.5 textual的CSS



DOM查询



布局



事件与消息



输入



行动



组件



动画



屏幕





### 2.3 组件详解





## 3 高阶技巧

https://textual.textualize.io/reference/

https://textual.textualize.io/api/

### 3.1 高阶知识

开发者工具的console和log相关部分

​	run和serve的端口参数`--port`，同名不同义，修改serve命令调试端口的技巧

主题

反应

worker

调色盘
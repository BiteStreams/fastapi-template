# Fastapi 项目模板


使用 Make、Docker Compose 和 Github Actions 的 FastAPI 项目模板，
其中包括 **SQLAlchemy**、**Alembic** 和集成测试设置。

[![代码集成](https://github.com/bitestreams/fastapi-template/actions/workflows/code-integration.yml/badge.svg)](https://github.com/bitestreams/fastapi-template /actions/workflows/code-integration.yml)

＃＃  安装

开发的唯一要求是 **Docker** 和 **Make**。
Docker 使入门变得容易，并使项目、操作系统和机器之间的切换更加容易。

要在本地启动项目，首先要克隆项目，然后在克隆的目录中运行以下命令：
```嘘
$ git 克隆 https://github.com/BiteStreams/fastapi-template.git
$ cd fastapi-模板
$化妆
```
然后在另一个 shell 中使用 alembic 更新模式：
```嘘
$ 进行迁移
```
**就是这样**。该应用程序已设置并且应该在 [localhost:5000/docs](localhost:5000/docs) 上运行。
使用已安装的 docker 卷自动检测代码更改。


### 生成文件

---
Makefile 是此结构中工具的“入口点”，
这样您就可以轻松地运行不同的命令而无需记住确切的参数。
运行“make help”以获得可用命令的概述：
```嘘
$ 帮忙
向上：
 运行应用程序
完成：棉绒测试
 准备提交
测试：utest itest
 运行单元和集成测试
查看：
 检查代码库
皮棉：
 检查代码库，并修复它
清洁测试：
 清理测试容器
迁移：
 使用 alembic 生成迁移
迁移：
 使用 alembic 运行迁移升级
降级：
 使用 alembic 运行降级迁移
帮助：
 显示此帮助消息
```

Make 允许您收集项目的常用脚本和命令。
其他使用不同编程语言和框架的项目通过使用 Make 获得相同的开发界面。

---

### 不用Docker安装
要安装 python 环境的本地副本（例如获取代码完成），
你必须安装 **Poetry**。
通过在项目的根目录下运行 `poetry install` 来创建诗歌环境。
要在 poetry 环境中启动服务器并与 ./test.db 中的测试 sqlite 数据库对话，请运行
```狂欢
$ export DB_STRING=sqlite:///test.db/
$ poetry run alembic 升级 head && poetry run uvicorn api.main:app --port 5000 --reload
```
同样，应用程序应该在 [localhost:5000/docs](localhost:5000/docs) 上全部设置并运行。

### 测试

---

测试是容器化的，Docker 设置可以在 .ci/ 文件夹中找到。
它们是使用 Pytest 编写的。
您可以使用以下方式运行测试：
```狂欢
$ 进行测试
```
这将运行集成和单元测试。如果您想单独运行它们，请使用“make itest”运行集成测试，使用“make utest”运行单元测试。


## 延伸阅读

要了解使用此模板的好处，
查看 [我们的博文](https://bitestreams.com/blog/fastapi_template/)。
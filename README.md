# project-1

## 1. 文件说明

- static：存放 js 和 css
- templates： 各种 jinja 模板
  - errors：自定义 404 和 500 错误页面
- app.py：应用入口
- commands.py：定义了初始化数据库和导入数据的 flask 命令
- errors.py：HTTP错误处理器
- forms.py：各种表单类
- models.py：数据库实体类
- settings.py：配置文件
- views.py：Flask 视图文件
- books.csv：图书原始数据

## 2. 数据库

1. 初始化数据库

   ```bash
   flask initdb --drop
   ```

   ![1559057719412](imgs/README/1559057719412.png)

2. 数据表

   ![1559057759291](imgs/README/1559057759291.png)

3. 各表的结构

   ![1559057809165](imgs/README/1559057809165.png)

   ![1559057836516](imgs/README/1559057836516.png)

   ![1559057855180](imgs/README/1559057855180.png)

   

## 界面展示

### 首页

![1559057955165](imgs/README/1559057955165.png)

### 注册、登录

![1559058033608](imgs/README/1559058033608.png)

![1559058048496](imgs/README/1559058048496.png)

### 搜索

![1559057989608](imgs/README/1559057989608.png)

![1559058002569](imgs/README/1559058002569.png)

### 图书详情页

![1559058130385](imgs/README/1559058130385.png)

![1559058144188](imgs/README/1559058144188.png)

### api

![1559058203004](imgs/README/1559058203004.png)






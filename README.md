## 应用介绍
一个常见的观点是 Serverless 工作流只适用于编排多个函数计算（FC）functions。实际上任何一贯的需要状态观测（可查询），执行时间长，结果重要不允许消息丢失的场景，即使整个逻辑只有一个 FC 函数，也可以通过 Serverless 工作流调用该函数可以达到如下效果
1. **FC HTTP 函数异步支持：** 目前 FC HTTP 触发器仅支持同步调用。使用 HTTP FC 发起工作流（StartExecution）, 使用另一个 HTTP 函数可以查询（DescribeExecution）异步任务结果
2. **异步任务可靠保证：** 自定义重试机制，让异步任务更可靠地执行

本应用将使用 Serverless 工作流实现一个可查询，可靠执行的异步任务

## 工作原理
如下图所示，HTTP 触发器目前不支持异步调用，对于需要使用 HTTP 触发一个异步任务（job）并且可以查询该任务状态的场景，可以通过一个 HTTP FC 函数接受开始任务和查询任务的

![intro](https://img.alicdn.com/tfs/TB1VQsrCEY1gK0jSZFCXXcwqXXa-1261-441.png)

## 开发、部署、调用
应用源代码：https://github.com/awesome-fnf/async-http-jobs

1. 安装 fun 工具，用于部署 FnF 流程, FC 函数，以及配置权限 https://github.com/alibaba/funcraft/blob/master/docs/usage/installation-zh.md
2. 执行 `fun config` 配置主账号 ID，子账号 AKID, AKSecret
3. 在 async-http-jobs 下执行下面命令，创建工作流和 HTTP trigger 函数
  ```
  fun package; fun deploy --use-ros --stack-name fnf-demo-http-async
  ```
4. 开始执行 HTTP 异步任务
  ```bash
  ## 开始异步流程执行，该命令会数出 executionName 字段，代表可查询的任务
  curl -X POST --data '{"key":"value"}' '<replace_fc_http_trigger_url>start?flowName=<replace_flow_name>'
  ```
5. 发起 HTTP 查询任务状态
  ```bash
  curl -X GET '<replace_fc_http_trigger_url>describe?flowName=replace_flow_name>&executionName=<replace_execution_name>'
  ```
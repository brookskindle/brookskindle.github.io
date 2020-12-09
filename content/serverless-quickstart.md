Title: Build a highly scalable REST API in 100 lines
Date: 2020-12-02
Category: programming
Tags: serverless, javascript

Today I'll be walking through how to build a REST API endpoint with the
following features:

* Automatic TLS/SSL encryption
* Accessible by both front and back-end applications
* Horizontally scalable
* API key validation and limiting
* Persistent storage
* Automated deployments

All in about 100 lines of code. It can be a bit more if you wish to include
verbose comments, or it can be a bit less if you discount the starting
boilerplate code. **The line count itself is not important**, but serves as a
proxy to illustrate the little amount of effort it takes to start a modern REST
API if you choose the right tools to do so.

## The tools?
[AWS Lambda](https://aws.amazon.com/lambda/), the [Serverless
Framework](https://www.serverless.com), and [node.js](https://nodejs.org/en/).

Lambda bills itself as a pay-for-usage way of running code without setting up a
server to run it. Even so, you'll still need to configure the environment
through what's known as a [CloudFormation
template](https://docs.aws.amazon.com/cloudformation/) - a configuration file
written in either JSON or YAML. CloudFormation templates *will* get verbose and
tedius to write for anything beyond a sample application. That's where the next
framework comes in.

Serverless is a provisioning framework meant to make deploying lambdas a more
pleasant experience. It works with a number of cloud providers, defaulting to
AWS. You will still end up needing to write parts of Cloudformation here and
there (read: make sure to have the docs handy), but the `serverless.yaml`
configuration file is miles easier to understand and work with than vanilla
CloudFormation.

node.js, but this can be interchangeable as both Serverless and AWS allow
lambdas to be written in a great many languages.

## The API?
We will build an API with one endpoint, `/hello`. It will require an API key to
access, and when invoked correctly will return a JSON payload greeting the
person (customizeable through the `name` url parameter). The endpoint will also
keep track of the number of people who have called the endpoint with a given
name, and will tell them how many other people of the same name have come
before.

## The code?
I'm glad you're excited, but rather than showing you all the code up front, I
think it will be helpful to walk through the changes step by step as if reading
a series of git commits.

### `7731ca0` Initial commit
The boilerplate code we're left with after going through the serverless
[getting started
guide](https://www.serverless.com/framework/docs/getting-started/). Some
unnecessary lines have been removed for the sake of brevity.

**handler.js**
```js
module.exports.hello = async event => {
  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        message: 'Go Serverless v1.0! Your function executed successfully!',
        input: event,
      },
      null,
      2
    ),
  };
};
```

A single exported async function; the entrypoint for our lambda. Maybe it's
obvious to say this, but every time the lambda is invoked, this function is
called. The function itself accepts one parameter, `event`, and returns a JSON response with a
success message.

Up to 3 parameters can be passed to the function, depending on signature, but
in this case we only need the first. AWS has more documentation on the [node.js
handler](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html) for
the curious.

**serverless.yml**
```yaml
# For full config options, check the docs:
#    docs.serverless.com

service: SERVICE_NAME_HERE
# app and org for use with dashboard.serverless.com
app: APP_NAME_HERE
org: SERVERLESS_ACCOUNT_HERE

# You can pin your service to only deploy with a specific Serverless version
# Check out our docs for more details
frameworkVersion: '2'

provider:
  name: aws
  runtime: nodejs12.x

functions:
  hello:
    handler: handler.hello
```

Most important right now is the `functions` section, which defines a `hello`
lambda whose entrypoint is the `hello` function of `handler.js`. At this point,
we can already deploy the code to AWS through `serverless deploy` and invoke
it with `serverless invoke -f hello`

> When deploying, serverless converts the above yaml file to a CloudFormation
> template and executes that. Neat, huh? If you're curious and want to take a
> peek behind the curtains, run `serverless package` and check out the
> CloudFormation files that are generated in the `.serverless` folder.

### `8ee5621` Make endpoint public

```diff
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -63,10 +63,10 @@ functions:
functions:
  hello:
    handler: handler.hello
+    events:
+      - http:
+          path: hello
+          method: get
```

These four lines allow us to call our lambda externally through an https
endpoint.

```console
$ curl 'https://sdlfkj3408jjlk.execute-api.us-east-1.amazonaws.com/dev/hello'
{
  "message": "Go Serverless v1.0! Your function executed successfully!",
  "input": {
    ...
  }
}
```

Serverless achieves this by automatically configuring an [API
Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
entry for the application.

### `d169028` Greet based on url param

```diff
--- a/blocks/lambda-webhook-callback/handler.js
+++ b/blocks/lambda-webhook-callback/handler.js
@@ -1,12 +1,16 @@
 'use strict';

 module.exports.hello = async event => {
+  let name = 'anonymous'
+  if (event.queryStringParameters && event.queryStringParameters.name) {
+    name = event.queryStringParameters.name
+  }
+
   return {
     statusCode: 200,
     body: JSON.stringify(
       {
-        message: 'Go Serverless v1.0! Your function executed successfully!',
-        input: event,
+        message: `Hello ${name}!`
       },
       null,
       2
```

Now that our lambda can be called by the API Gateway, we get all sorts of
interesting properties through the `event` parameter. In this case, we want to
know if the user passed in a `name` url parameter.

```console
$ curl 'https://sdflkj398987.execute-api.us-east-1.amazonaws.com/dev/hello'
{
  "message": "Hello anonymous!"
}
```

```console
$ curl 'https://sdflkj398987.execute-api.us-east-1.amazonaws.com/dev/hello?name=brooks'
{
  "message": "Hello brooks!"
}
```

[API Gateway docs with example `event`
payload](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)

### `f486d35` Require api keys

```diff
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -23,6 +23,16 @@ frameworkVersion: '2'
 provider:
   name: aws
   runtime: nodejs12.x
+  apiKeys:
+    - testkey1
+    - testkey2

@@ -67,6 +77,7 @@ functions:
       - http:
           path: hello
           method: get
+          private: true
```

API keys are configured for the whole project, so if you end up having more
than one function/lambda they will all share the same set of API keys.
Setting our function to private will now only allow traffic through if they
have an `X-Api-Key` header with a valid API key. Serverless has great
documentation on [setting up
keys](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/#setting-api-keys-for-your-rest-api)
as well, there's many more ways to customize them than I've shown here.

```console
$ curl 'https://sdflkj398987.execute-api.us-east-1.amazonaws.com/dev/hello'
{"message":"Forbidden"}
```
```console
$ curl 'https://sdflkj398987.execute-api.us-east-1.amazonaws.com/dev/hello' \
    -H 'x-api-key: sdlfkjo4582730sdflskdfj034lskdfj'
{
  "message": "Hello anonymous!"
}
```

### `b2d9941` Set CORS for endpoint

```diff
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -78,6 +78,7 @@ functions:
           path: hello
           method: get
           private: true
+          cors: true
```

This is a small code change, but the impact is huge. With CORS enabled, our API
can now be queried from any front end application.

What is CORS? Cross-Origin-Resource-Sharing. In brief, it's a security check
that the browser makes when making "special" requests to endpoints on a
different domain than itself. Our API requires the special `x-api-key` header,
which the browser identifies as "special," so it fires off an `OPTIONS` http
request against the endpoint to check if this action is allowed or not. If
you're not familiar with what CORS is or how it works, the Mozilla web docs
have a [comprehensive
article](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) to
understanding CORS.

### `22d2412` Set usage plans for keys

```diff
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -26,13 +26,26 @@ provider:
   apiKeys:
-    - testkey1
-    - testkey2
+    - free:
+      - testkey1
+    - paid:
+      - testkey2
+  usagePlan:
+    - free:
+        quota:
+          limit: 5
+          period: DAY
+        throttle:
+          burstLimit: 5
+          rateLimit: 5
+    - paid:
+        quota:
+          limit: 5000
+          period: DAY
+        throttle:
+          burstLimit: 200
+          rateLimit: 100
```

I'll re-iterate the serverless documentation on [setting up API
keys](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/#setting-api-keys-for-your-rest-api).
With this change, we can now limit by API keys, the number of requests that
come in on a set time period (in this case `DAY`). Exceeding this limit will
result in a 429 Too Many Requests error.

```console
$ curl 'https://3lskdjfsdlf8.execute-api.us-east-1.amazonaws.com/dev/hello' \
    -H 'x-api-key: jsdlkfjslkj343434234lksjdflkj'
{"message":"Limit Exceeded"}
```

### `b8a7405` Integrate with DynamoDB

This is a big one. Also not included in this diff is `package.json` and
`package-lock.json`, needed because we introduced `aws-sdk` as a dependency.
The two files can be created, however, with `npm init --y && npm install
aws-sdk`.

To make things easier, let's walk through the changes per file.

```diff
diff --git a/blocks/lambda-webhook-callback/handler.js b/blocks/lambda-webhook-callback/handler.js
index b6e6b0d..956f2eb 100644
--- a/blocks/lambda-webhook-callback/handler.js
+++ b/blocks/lambda-webhook-callback/handler.js
@@ -1,11 +1,29 @@
+const AWS = require('aws-sdk')
+const dynamo = new AWS.DynamoDB.DocumentClient()
+
 module.exports.hello = async event => {
   let name = 'anonymous'
   if (event.queryStringParameters && event.queryStringParameters.name) {
     name = event.queryStringParameters.name
   }

+  const params = {
+    TableName: process.env.TABLE_NAME
+    Item: {
+      name: name
+    }
+  }
+  const result = await dynamo.put(params).promise()
+
   return {
     statusCode: 200,
     body: JSON.stringify(
```

We're using the aws-sdk to initialize a DynamoDB connection. DynamoDB is
Amazon's own NoSQL offering and we'll be using it as a way to persist data
between calls. At present, all we are saving to the table is the name of the
user we're greeting.

Also note: for flexibility, we expect the table name to be available via the
`TABLE_NAME` environment variable rather than hardcoding a value for it. The
reason why will become apparent when we look at the next file.

```diff
diff --git a/blocks/lambda-webhook-callback/serverless.yml b/blocks/lambda-webhook-callback/serverless.yml
index d889190..7e6fc28 100644
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -46,6 +46,18 @@ provider:
         throttle:
           burstLimit: 200
           rateLimit: 100
+  iamRoleStatements:
+    - Effect: Allow
+      Action:
+        - dynamodb:PutItem
+      Resource: !Sub 'arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/${helloTable}'
+
+  environment:
+    TABLE_NAME: !Ref helloTable
@@ -58,3 +70,20 @@ functions:
           method: get
           private: true
           cors: true
+
+resources:
+  Resources:
+    helloTable:
+      Type: AWS::DynamoDB::Table
+      Properties:
+        BillingMode: PAY_PER_REQUEST
+        AttributeDefinitions:
+          - AttributeName: name
+            AttributeType: S
+        KeySchema:
+          - AttributeName: name
+            KeyType: HASH
```

Let's look at the **resources** first. This section defines a DynamoDB table,
which we're referencing as `helloTable`. The syntax for this section is
CloudFormation, as the [serverless docs on
resources](https://www.serverless.com/framework/docs/providers/aws/guide/resources/)
suggest. As Dynamo is a NoSQL database, no schema is needed, but it does need
to know the table's primary key, which is `name` in this case.

Up next, **environment**. The lambda will have access to these values through
the use of environment variables (eg: `process.env.VARIABLE_NAME`). The `!Ref`
part is a bit confusing for someone not familiar with CloudFormation, so here
goes. In the previous section, `helloTable` is the reference name for our
table, but it does not actually represent the name of the table when it gets
created. In the absense of a defined table name, CloudFormation will choose one
for us on stack create/update, so the only way to reference the name of our
table is through a [Ref
value](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)

If we created the database and our code knows the name of the database to
connect to, what else is left? **iamRoleStatements**, or access/authentication,
which is handled within AWS by IAM. IAM is based on the
[RBAC](https://en.wikipedia.org/wiki/Role-based_access_control) access paradigm
. An IAM role can be configured to allow access to all sorts of `resources`
within AWS, but in this case the only action we need to do right now is a
`PutItem` action on a DynamoDB. See [IAM
docs](https://www.serverless.com/framework/docs/providers/aws/guide/iam/).

The last potentially confusing part of the IAM section is the `!Sub` resource
value. Functionally, this acts no differently than the `!Ref` section of the
environments, with one difference. `!Ref` only returns the name of the
resource, and for `Resource` under IAM, we are required to provide the fully
qualified ARN value of the thing we're trying to access. It's a bit like
specifying the name of a file vs. specifying the full path to a file. More
documentation on the contents of the `!Sub` section:
[ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html),
[Pseudo-parameter
references](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html),
[!Sub](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html#w2ab1c33c28c59c11).

### `3f338a6` Count the number of visitors

```diff
diff --git a/blocks/lambda-webhook-callback/handler.js b/blocks/lambda-webhook-callback/handler.js
index e1b1496..6568753 100644
--- a/blocks/lambda-webhook-callback/handler.js
+++ b/blocks/lambda-webhook-callback/handler.js
@@ -14,20 +14,26 @@ module.exports.hello = async event => {

   const params = {
     TableName: process.env.TABLE_NAME,
-    Item: {
-      name: name,
-    }
+    Key: {
+      name,
+    },
+    UpdateExpression: 'ADD #count :num',
+    ExpressionAttributeNames: {
+      '#count': 'greeting_count',
+    },
+    ExpressionAttributeValues: {
+      ':num': 1,
+    },
+    ReturnValues: 'UPDATED_NEW',
   }
-  const result = await dynamo.put(params).promise()
+  const result = await dynamo.update(params).promise()

   return {
     statusCode: 200,
     body: JSON.stringify(
       {
-        message: `Hello ${name}!`
+        message: `Hello ${name} #${result.Attributes.greeting_count}!`
       },
       null,
       2
diff --git a/blocks/lambda-webhook-callback/serverless.yml b/blocks/lambda-webhook-callback/serverless.yml
index 0741a40..d726cf7 100644
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -53,7 +53,7 @@ provider:
   iamRoleStatements:
     - Effect: Allow
       Action:
-        - dynamodb:PutItem
+        - dynamodb:UpdateItem
       Resource: !Sub 'arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/${helloTable}'
```

With this commit, we change the response value of our endpoint to also include
the visitor count per name. Instead of putting an item, we are updating an item
(which can create new elements *or* update existing ones) and adding a
`greeting_count` field ([API docs on node.js DynamoDB
client](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB/DocumentClient.html)).
Calling our API now looks like this:

```console
$ curl 'https://34iisdflkj.execute-api.us-east-1.amazonaws.com/dev/hello' \
    -H 'x-api-key: lksjdfljl3j45lk2345jlkjsdflksjdfljklsdkjf'
{
  "message": "Hello anonymous #1!"
}
$ curl 'https://34iisdflkj.execute-api.us-east-1.amazonaws.com/dev/hello' \
    -H 'x-api-key: lksjdfljl3j45lk2345jlkjsdflksjdfljklsdkjf'
{
  "message": "Hello anonymous #2!"
}
$ curl 'https://34iisdflkj.execute-api.us-east-1.amazonaws.com/dev/hello?name=brooks' \
    -H 'x-api-key: lksjdfljl3j45lk2345jlkjsdflksjdfljklsdkjf'
{
  "message": "Hello brooks #1!"
}
```

### `6ddad1f` Dynamo: use SET, not ADD

```diff
diff --git a/blocks/lambda-webhook-callback/handler.js b/blocks/lambda-webhook-callback/handler.js
index 6568753..2e53aa4 100644
--- a/blocks/lambda-webhook-callback/handler.js
+++ b/blocks/lambda-webhook-callback/handler.js
@@ -17,11 +17,12 @@ module.exports.hello = async event => {
     Key: {
       name,
     },
-    UpdateExpression: 'ADD #count :num',
+    UpdateExpression: 'SET #count = if_not_exists(#count, :initial) + :num',
     ExpressionAttributeNames: {
       '#count': 'greeting_count',
     },
     ExpressionAttributeValues: {
+      ':initial': 0,
       ':num': 1,
     },
     ReturnValues: 'UPDATED_NEW',
```

This is a best practices change because functionally the two `UpdateExpression`
lines do the same thing. However, AWS recommends [using SET in most
cases](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.ADD) instead of ADD.
Initially I thought ADD would be a more obvious and simple solution, but the
more I think about it, SET makes it abundantly clear what the logic is if
`greeting_count` does not yet exist as an attribute. ADD hides this logic, and
therefore has the potential to cause hard-to-debug errors.

### `4562185` Add DeletionPolicy note

```diff
--- a/blocks/lambda-webhook-callback/serverless.yml
+++ b/blocks/lambda-webhook-callback/serverless.yml
@@ -82,6 +82,12 @@ resources:
   Resources:
     helloTable:
       Type: AWS::DynamoDB::Table
+      DeletionPolicy: Retain
       Properties:
         BillingMode: PAY_PER_REQUEST
         AttributeDefinitions:
```

This change is optional, but in a production setting you most likely want to
retain your database in the case of CloudFormation stack removal. The exception
to this would be if your database contained **only** information that is easy
to regenerate programmatically. For some resources, CloudFormation performs a
backup before deletion, but in the case of DynamoDB, [this does not
happen](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html#aws-attribute-deletionpolicy-options).

---

## Closing thoughts
And that's it.

This project only scratched the surface of what is possible with the right
toolset and a healthy dose of documentation. In a real life scenario, a REST
API server would be much more complicated not only in terms of supported
features, but also in terms of team size and software process bottlenecks. But
that's for you to figure out if you fit that scenario 🙃. Additional resources:

* [AWS: organizing large serverless
  applications](https://aws.amazon.com/blogs/compute/best-practices-for-organizing-larger-serverless-applications/)
* [Serverless: real world app
  structures](https://www.serverless.com/blog/structuring-a-real-world-serverless-app)
* [Build a full-stack app in Serverless](https://serverless-stack.com/)

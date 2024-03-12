# Artillery

## Before you start

This exercise assumes you have a recent version of Node/npm installed - [if not you can install that from here](https://nodejs.org/en/download).

## What is it?

Artillery is a load testing library; it is designed for triggering large numbers of requests to a service and monitoring how the service under test handles the load.

### An aside on load testing

Running load tests doesn't always* have to be hard, but _designing_ good load tests typically is.

*Particularly if you're testing at a low enough traffic level that a single machine can make sufficient requests.

Before setting up load tests, consider what you're actually hoping to achieve with them:
* Do you want to check the system is performing at its usual pace under normal load?
* Do you want to check that it can handle spikes in traffic beyond normal levels?
* Do you want to find out at what level of traffic the system struggles or gives up?
* Do you want to check that the system degrades gracefully under heavy load?

Each of these tests will demand a slightly different configuration, and a different analysis of the results.

We will discuss load testing more in future workshops.

## Alternatives?

Lots of alternative open-source load testing tools exist such as:
* [JMeter](https://jmeter.apache.org/)
* [Gatling](https://gatling.io/)
* [k6](https://k6.io/open-source/)

In addition, once we're reaching a stage where the requests need to be distributed across multiple machines, many more paid options exist to help you.

### Disclaimer

A load test only differs from a Distributed-Denial-of-Service (DDoS) attack in intent - you should be wary of just running load tests against arbitrary sites; this could potentially be a criminal offence!

Even testing your own applications can be subject to restrictions if you're hosting systems on a public cloud, e.g.AWS has clear policies on both [Network Stress Testing including load testing](https://aws.amazon.com/ec2/testing/) and [DDoS simulations](https://aws.amazon.com/security/ddos-simulation-testing/) - although note that both of these require significant traffic levels to be in violation.

Thankfully, Artillery offer a site that they host and allow us to use for the sake of testing.

## Try it out

First off, we should know our target! Check out Artillery's practice Dino: <http://asciiart.artillery.io:8080/dino>

### Our first load test

To start with, run a quick test against this single endpoint:
* Run `npm install` in this `artillery` directory to install the tool
* Try running `npx artillery quick http://asciiart.artillery.io:8080/dino` to fire off requests

> Artillery recommend installing the tool globally with `npm install -g artillery`, in which case we could run these tests without the npx prefix; we have chosen to isolate that instead, and to specify the version, by using a local `package.json`.

Artillery will produce reports for each 10 second period as it runs, and then a final summary report, which should look something like:

```
All VUs finished. Total time: 3 seconds

--------------------------------
Summary report @ 15:20:37(+0000)
--------------------------------

http.codes.200: ................................................................ 100
http.downloaded_bytes: ......................................................... 54500
http.request_rate: ............................................................. 84/sec
http.requests: ................................................................. 100
http.response_time:
  min: ......................................................................... 25
  max: ......................................................................... 46
  mean: ........................................................................ 29.6
  median: ...................................................................... 29.1
  p95: ......................................................................... 36.2
  p99: ......................................................................... 40.9
http.responses: ................................................................ 100
vusers.completed: .............................................................. 10
vusers.created: ................................................................ 10
vusers.created_by_name.0: ...................................................... 10
vusers.failed: ................................................................. 0
vusers.session_length:
  min: ......................................................................... 330.4
  max: ......................................................................... 426.2
  mean: ........................................................................ 356.6
  median: ...................................................................... 347.3
  p95: ......................................................................... 368.8
  p99: ......................................................................... 368.8
```

Take a moment to read over those stats, and understand those; note that all "time" results are measured in milliseconds.

`pXX` refers to the XXth percentile, e.g. `p95` refers to the 95th percentile, so in this case a `p95` value of 36.2 means that 95% of responses were handled in under 36.2 milliseconds. Why do you think that's a specific stat that Artillery outputs?

Take a moment to discuss this with your room, before you read on.

<details> <summary>Why use p95 or p99?</summary> 

In many scenarios, we care most about some form of _average_ result, but not always. In particular, it's easy for those to be skewed:
* If one request takes 1 second, but nine requests take 10 milliseconds, the _mean_ is going to be ~100ms; which doesn't give us a representative picture of the user experience.
* Likewise, the median can miss out a long tail; if 60% of results take 10ms, but 40% take 500ms, then a median of 10ms is equally misleading

By comparison, a p95 of 50ms tells us that 95% of requests took under 50ms; it doesn't necessarily tell us what the most common experience looked like, but it does assure us that most requests were met within a defined timeframe. 

Given that network response times are often quite variable - e.g. based on other traffic in the network, the route a packet takes, or even the physical location of the device testing - using this approach is a good way to reduce the noise but still focus on "did the majority of requests get satisified in a reasonable timeframe".

</details>

### Understanding our results

As our load-testing jobs get longer, we could easily lose info from the outputted stats. Run the test again, but this time [add the `-o` flag and specify a json file](https://www.artillery.io/docs/reference/cli/run#--output---create-a-json-report) to write the summary results to.

Check out those stats, how many requests were made total? What was the 75th percentile response time?

You can view those stats better by generating a HTML page through the `report` option:
* `npx artillery report <json_file>`

> If using VSCode, there are several "Open In Browser" extensions that will give you an easy option to view the HTML in your Browser without navigating File Explorer/Finder.

### Adding more structure

Next, we'll run through a similar example to [the Artillery tutorial](https://www.artillery.io/docs/get-started/first-test).

**Take a moment here to look at the `first-test.yml` file**, can you work out what's going to happen? When you have a hypothesis, then trigger your first test with `npx artillery run first-test.yml`

This will take a minute or two, so as it runs, read [the Artillery docs about how Virtual Users work](https://www.artillery.io/docs/get-started/core-concepts#virtual-users). Note that a given "user" maintains its own cookies, so they can handle some degree of statefulness.

Once the test has passed, review its results again.

### Plugins
Enable the plugins section in the yml file, including the `apdex` and `ensure` sections, and run the test again.

We will now see some additional behaviours:
- [ensure](https://www.artillery.io/docs/reference/extensions/ensure) provides us an option to specify pass/fail criteria for our load test.
  - For example, we have specified that 99% of responses need to be satisifed in under 100ms
- [metrics-by-endpoint](https://www.artillery.io/docs/reference/extensions/metrics-by-endpoint) does what it says on the tin - you should see a breakdown of the results according to which precise URL endpoint was hit.
- [apdex](https://www.artillery.io/docs/reference/extensions/apdex) comes from "Application Performance Index" and provides a method to convert our complex output of statistics into a simple summary score for our performance
  - This determines whether users were "satisfied", "tolerant" or "frustrated" based on a threshold.

### Making load more realistic with Playwright

One problem with designing load tests is in ensuring that the load pattern resembles real user usage. For example, suppose your load test demonstrates that your site can handle 2,000 requests per minute spread across a collection of 20 URLs.

* Are they the URLs that users actually hit?
* For a user following a typical route through your site, do different URLs get hit equally often?
* Have you got any traffic hitting assets that pages would load in turn, such as images or script files?

One way to make the approach here more realistic can be to have artillery follow more realistic user journeys. In particular, Artillery offers the option to use Playwright to run through scripts.

> If you haven't met Playwright before, it is recommended to complete [that exercise now](../playwright/Readme.md) and come back to this.

Right now, Artillery only supports JavaScript (or, experimentally, TypeScript) Playwright scripts, so we can't directly use the scripts we created earlier*, so we'll create some new tests for Artillery's site.

> *And we should also not assume that permission to use Playwright's site for testing means they are happy with us running high traffic tests!

In order to do this, first create a new artillery config script in `artillery-playwright.yml`:
```yml
config:
  target: https://www.artillery.io
  phases:
    - duration: 5
      arrivalRate: 1
      rampTo: 2
      name: Warm up phase
  # Load the Playwright engine:
  engines:
    playwright: {}
  # Path to JavaScript file that defines Playwright test functions
  processor: "./flows.js"
scenarios:
  - engine: playwright
```

Playwright comes bundled with Artillery so there's no extra installation required, and we can immediately use it to start generating our new test:

`npx playwright codegen artillery.io --target javascript`

Copy the contents of that test and add it to a new file called `flows.js` which should follow the structure below:
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    // Note this will be set "false" when generating the code
    headless: true
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://www.artillery.io/');
  await page.locator('#masthead').getByRole('button').click();
  // ....

  // ---------------------
  await context.close();
  await browser.close();
})();
```

> Note that the code generation will set headless to false; if you are running the test for more than a single user, then you will want to leave headless mode on!

Take a look at the `first-test.yml`, and decide if you want to add any more structure to your test.

When you're ready, start your tests with `npx artillery run artillery-playwright.yml`.

## Further Reading

You've now configured load tests that can run through a variety of scenarios. If you're interested:
- Read through [the Artillery best practices](https://www.artillery.io/docs/get-started/best-practices)
- Take a look at [an alternative tool](#alternatives)
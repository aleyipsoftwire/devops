# Google Lighthouse

## Before you start

Running this tool requires having Google Chrome installed on your machine.

## What is Lighthouse?

[Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) is an open-source tool designed by Google for improving websites, particularly with a focus on:
* Performance - fast page loads
* Accessibility - how easy is your site to navigate for users

Lighthouse can be run in a range of ways:
* Within Google Chrome, it can be run from the Lighthouse tab within the Chrome DevTools
  * Accessible through right clicking on a web page in Chrome and selecting Inspect
* Installed through node, which can be used:
  * Directly as a CLI
  * Or programmatically from JavaScript code
* Added as a [Chrome Extension](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk)

Today we'll look mostly at the CLI tool so that we can define our success and failure results consistently, so that we're best placed to integrate our tooling into a Continuous Integration pipeline later down the line.

## Try it out

Run `npm install` within this folder to install the lighthouse tool, and then run it using:
```
npx lighthouse https://developer.chrome.com/docs/lighthouse/overview --view
```

Once the test is complete, you'll see a report load up with various scores assigned to different aspects of the site's performance. Take a moment to read through this, what does the site score well on, and what not so well?

If you work on a project that creates or relies on a specific webpage, try running Lighthouse against that next. How does it score? Are you surprised?

> As an alternative to outputting the HTML directly, we can also generate a JSON output by passing the `--output json --output-path output.json` flags, which can be shared with others, and can be viewed on the [Google Lighthouse Viewer](https://googlechrome.github.io/lighthouse/viewer/).

## Defining Success

These reports can be great for providing us with actionable advice & ideas, but they're currently dependent on being opened and reviewed by someone periodically. If instead we can specify pass/fail criteria for our reports, then we can potentially take this further and ensure that once we have a score we are happy with, we are notified if that drops below our chosen thresholds.

In order to add assertions and requirements to our tool, we will need to use [the Lighthouse CI tool](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md).

First, create a config file named `.lighthouserc.json` and add the following contents:
```json
{
  "ci": {
    "collect": {
      "url": ["https://developer.chrome.com/docs/lighthouse/overview"],
      "numberOfRuns": 1
    }
  }
}
```

So far we've only defined the [collect stage](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md#collect-lighthouse-results) - where we run the test and store results locally in a `.lighthouseci` folder. Try running that now:
```sh
npx lhci collect
```

Take a quick look inside the `.lighthouseci` folder that was generated, but don't worry about the exact structure of those files.

Next, we can add an [assertions block](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md#add-assertions) under the collect block to specify the standards we want to hold our site to.
```json
{
  "ci": {
    "collect": { ... },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "unused-css-rules": ["warn", {"maxScore": 0}],
        "unminified-javascript": ["warn", {"maxScore": 0}]
      }
    }
  }
}
```

For example, the above specifies that:
- There should be no unused CSS rules
- There should be no unminified JavaScript
- We should also be held to the pre-defined `lighthouse:recommended` expectations.
  - You can see [what expectations those preset rules come with in the GitHub docs](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md#preset)
- If you want to view the full set of rules, you can find that [directly in the code](https://github.com/GoogleChrome/lighthouse/blob/v5.5.0/lighthouse-core/config/default-config.js#L375-L407)

Run your assertions with `npx lhci assert` now to generate a simple report of what passed.

Take a look at the results, what categories passed, and which failed?

> You'll likely see a number of failures - meeting best practices on every category is no mean feat. Even the Lighthouse docs advise that maintaining the `lighthouse:all` preset, which checks every audit is perfect, "is extremely difficult to do"!

What value would you assign to improving some of the low scores, are there any that you might prioritise?

## Further Reading

- We've focused primarily on the Performance and Accessibility aspects of Lighthouse, but it also provides best practice feedback on:
  - [Search Engine Optimisation (SEO)](https://developer.chrome.com/docs/lighthouse/seo/meta-description)
  - [Progressive Web App (PWAs)](https://developer.chrome.com/docs/lighthouse/pwa/load-fast-enough-for-pwa)
  - So take a look over those links as well